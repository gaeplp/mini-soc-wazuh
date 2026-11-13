import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path


FENETRE_SSH = timedelta(seconds=60)


def creer_table(connexion):
    colonnes = {
        ligne[1] for ligne in connexion.execute("PRAGMA table_info(alertes)")
    }

    if colonnes and "cle_evenement" not in colonnes:
        raise ValueError(
            "Ancien format de base SQLite : utilise une nouvelle base avec --db. "
            "Conserve l'ancienne base pour le moment."
        )

    connexion.execute("""
        CREATE TABLE IF NOT EXISTS alertes (
            id INTEGER PRIMARY KEY,
            cle_evenement TEXT NOT NULL UNIQUE,
            timestamp TEXT NOT NULL,
            agent TEXT NOT NULL,
            rule_id INTEGER NOT NULL,
            level INTEGER NOT NULL,
            description TEXT NOT NULL,
            dstuser TEXT,
            srcip TEXT,
            srcport TEXT
        )
    """)

    # Ajoute les champs SSH aux bases créées par la version précédente.
    colonnes = {
        ligne[1] for ligne in connexion.execute("PRAGMA table_info(alertes)")
    }
    for nom in ("dstuser", "srcip", "srcport"):
        if nom not in colonnes:
            connexion.execute(f"ALTER TABLE alertes ADD COLUMN {nom} TEXT")


def extraire_alerte(alerte):
    if not isinstance(alerte, dict):
        raise ValueError("l'alerte doit être un objet JSON")

    if isinstance(alerte.get("agent"), dict):
        valeurs = (
            str(alerte["timestamp"]),
            str(alerte["agent"]["name"]),
            int(alerte["rule"]["id"]),
            int(alerte["rule"]["level"]),
            str(alerte["rule"]["description"]),
        )
        identifiant = alerte.get("id")
    else:
        valeurs = (
            str(alerte["timestamp"]),
            str(alerte["agent"]),
            int(alerte["rule_id"]),
            int(alerte["level"]),
            str(alerte["description"]),
        )
        identifiant = None

    if identifiant is not None and str(identifiant).strip():
        cle = "wazuh:" + str(identifiant)
    else:
        # Repli pour les données fictives et les extraits sans ID Wazuh.
        contenu = json.dumps(valeurs, ensure_ascii=False)
        cle = "champs:" + hashlib.sha256(contenu.encode("utf-8")).hexdigest()

    donnees = alerte.get("data")
    if not isinstance(donnees, dict):
        donnees = {}

    champs_ssh = tuple(
        str(donnees[nom]) if donnees.get(nom) not in (None, "") else None
        for nom in ("dstuser", "srcip", "srcport")
    )

    return (cle, *valeurs, *champs_ssh)


def importer(connexion, fichier):
    ajoutees = 0

    for numero, ligne in enumerate(
        fichier.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not ligne.strip():
            continue

        try:
            valeurs = extraire_alerte(json.loads(ligne))
        except (ValueError, TypeError, KeyError) as erreur:
            raise ValueError(f"Ligne {numero} invalide : {erreur}") from erreur

        curseur = connexion.execute(
            """
            INSERT OR IGNORE INTO alertes
                (cle_evenement, timestamp, agent, rule_id, level,
                 description, dstuser, srcip, srcport)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            valeurs,
        )
        ajoutees += curseur.rowcount

    connexion.commit()
    print(f"{ajoutees} alerte(s) ajoutée(s).")


def lister(connexion, agent):
    requete = """
        SELECT timestamp, agent, rule_id, level, description
        FROM alertes
    """
    parametres = ()

    if agent:
        requete += " WHERE agent = ?"
        parametres = (agent,)

    requete += " ORDER BY timestamp, id"

    for horodatage, nom, regle, niveau, description in connexion.execute(
        requete, parametres
    ):
        print(
            f"{horodatage} | {nom} | règle {regle} | "
            f"niveau {niveau} | {description}"
        )


def resumer(connexion, agent=None):
    requete = "SELECT rule_id, COUNT(*) FROM alertes"
    parametres = ()

    if agent:
        requete += " WHERE agent = ?"
        parametres = (agent,)

    requete += " GROUP BY rule_id ORDER BY rule_id"

    for regle, nombre in connexion.execute(requete, parametres):
        print(f"Règle {regle} : {nombre} alerte(s)")


def convertir_horodatage(horodatage):
    try:
        instant = datetime.fromisoformat(horodatage.replace("Z", "+00:00"))
    except ValueError as erreur:
        raise ValueError(f"Horodatage invalide : {horodatage}") from erreur

    if instant.tzinfo is None:
        raise ValueError(f"Fuseau horaire absent : {horodatage}")

    return instant.astimezone(timezone.utc)


def champs_compatibles(echec, reussite):
    # Un champ connu dans les deux alertes ne doit pas se contredire.
    return all(
        valeur_echec is None
        or valeur_reussite is None
        or valeur_echec == valeur_reussite
        for valeur_echec, valeur_reussite in zip(echec, reussite)
    )


def sequences_ssh(connexion, agent=None):
    requete = """
        SELECT timestamp, agent, rule_id, dstuser, srcip, srcport
        FROM alertes
        WHERE rule_id IN (5760, 5715)
    """
    parametres = ()

    if agent:
        requete += " AND agent = ?"
        parametres = (agent,)

    evenements = []
    for horodatage, nom_agent, regle, compte, ip, port in connexion.execute(
        requete, parametres
    ):
        evenements.append(
            (
                convertir_horodatage(horodatage),
                horodatage,
                nom_agent,
                regle,
                (compte, ip, port),
            )
        )

    evenements.sort(key=lambda evenement: evenement[0])

    # Plusieurs échecs peuvent coexister sur un agent : on conserve
    # les candidats afin qu'une réussite pour Bob n'efface pas
    # un échec précédent concernant Alice.
    echecs_par_agent = {}

    for instant, horodatage, nom_agent, regle, champs in evenements:
        echecs = echecs_par_agent.setdefault(nom_agent, [])

        # Les événements sont parcourus dans l'ordre chronologique.
        echecs[:] = [
            echec
            for echec in echecs
            if instant - echec[0] <= FENETRE_SSH
        ]

        if regle == 5760:
            echecs.append((instant, horodatage, champs))
            continue

        # Cherche l'échec compatible le plus récent.
        for index in range(len(echecs) - 1, -1, -1):
            instant_echec, horodatage_echec, champs_echec = echecs[index]

            if not champs_compatibles(champs_echec, champs):
                continue

            delai = instant - instant_echec
            if not timedelta(0) <= delai <= FENETRE_SSH:
                continue

            # Un échec n'est associé qu'à une seule réussite.
            echecs.pop(index)
            print(
                f"{nom_agent} | échec {horodatage_echec} | "
                f"réussite {horodatage} | "
                f"délai {delai.total_seconds():.3f} s"
            )
            break


def main():
    analyseur = argparse.ArgumentParser(
        description="Chronologie locale d'alertes JSONL"
    )
    analyseur.add_argument(
        "--db", required=True, type=Path, help="Chemin de la base SQLite"
    )

    commandes = analyseur.add_subparsers(dest="commande", required=True)
    commandes.add_parser("importer").add_argument("fichier", type=Path)
    commandes.add_parser("lister").add_argument("--agent")
    commandes.add_parser("resumer").add_argument("--agent")
    commandes.add_parser("sequences-ssh").add_argument("--agent")

    arguments = analyseur.parse_args()

    with sqlite3.connect(arguments.db) as connexion:
        creer_table(connexion)

        if arguments.commande == "importer":
            importer(connexion, arguments.fichier)
        elif arguments.commande == "lister":
            lister(connexion, arguments.agent)
        elif arguments.commande == "resumer":
            resumer(connexion, arguments.agent)
        else:
            sequences_ssh(connexion, arguments.agent)

if __name__ == "__main__":
    main()
