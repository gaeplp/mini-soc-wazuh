import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path


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
            description TEXT NOT NULL
        )
    """)


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

    return (cle, *valeurs)


def importer(connexion, fichier):
    ajoutees = 0
    for numero, ligne in enumerate(fichier.read_text(encoding="utf-8").splitlines(), 1):
        if not ligne.strip():
            continue
        try:
            valeurs = extraire_alerte(json.loads(ligne))
        except (ValueError, TypeError, KeyError) as erreur:
            raise ValueError(f"Ligne {numero} invalide : {erreur}") from erreur

        curseur = connexion.execute(
            """INSERT OR IGNORE INTO alertes
               (cle_evenement, timestamp, agent, rule_id, level, description)
               VALUES (?, ?, ?, ?, ?, ?)""",
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
        print(f"{horodatage} | {nom} | règle {regle} | niveau {niveau} | {description}")


def resumer(connexion, agent=None):
    requete = "SELECT rule_id, COUNT(*) FROM alertes"
    parametres = ()

    if agent:
        requete += " WHERE agent = ?"
        parametres = (agent,)

    requete += " GROUP BY rule_id ORDER BY rule_id"

    for regle, nombre in connexion.execute(requete, parametres):
        print(f"Règle {regle} : {nombre} alerte(s)")

def sequences_ssh(connexion, agent=None):
    requete = """
        SELECT timestamp, agent, rule_id
        FROM alertes
        WHERE rule_id IN (5760, 5715)
    """
    parametres = ()
    if agent:
        requete += " AND agent = ?"
        parametres = (agent,)

    evenements = []
    for horodatage, nom_agent, regle in connexion.execute(requete, parametres):
        try:
            instant = datetime.fromisoformat(
                horodatage.replace("Z", "+00:00")
            )
        except ValueError as erreur:
            raise ValueError(
                f"Horodatage invalide : {horodatage}"
            ) from erreur

        if instant.tzinfo is None:
            raise ValueError(f"Fuseau horaire absent : {horodatage}")

        evenements.append(
            (instant.astimezone(timezone.utc), horodatage, nom_agent, regle)
        )

    evenements.sort(key=lambda evenement: evenement[0])
    dernier_echec = {}

    for instant, horodatage, nom_agent, regle in evenements:
        if regle == 5760:
            dernier_echec[nom_agent] = (instant, horodatage)
        elif nom_agent in dernier_echec:
            instant_echec, horodatage_echec = dernier_echec.pop(nom_agent)
            delai = instant - instant_echec

            if timedelta(0) <= delai <= timedelta(seconds=60):
                print(
                    f"{nom_agent} | échec {horodatage_echec} | "
                    f"réussite {horodatage} | délai {delai.total_seconds():.3f} s"
                )

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
