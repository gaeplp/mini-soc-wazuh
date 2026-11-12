import argparse
import json
import sqlite3
from pathlib import Path


def creer_table(connexion):
    connexion.execute("""
        CREATE TABLE IF NOT EXISTS alertes (
            id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            agent TEXT NOT NULL,
            rule_id INTEGER NOT NULL,
            level INTEGER NOT NULL,
            description TEXT NOT NULL,
            UNIQUE(timestamp, agent, rule_id, description)
        )
    """)


def importer(connexion, fichier):
    ajoutees = 0
    for numero, ligne in enumerate(fichier.read_text(encoding="utf-8").splitlines(), 1):
        if not ligne.strip():
            continue
        try:
            alerte = json.loads(ligne)
            if isinstance(alerte.get("agent"), dict):
                # Format d'une alerte Wazuh
                valeurs = (
                    str(alerte["timestamp"]),
                    str(alerte["agent"]["name"]),
                    int(alerte["rule"]["id"]),
                    int(alerte["rule"]["level"]),
                    str(alerte["rule"]["description"]),
                )
            else:
                # Format simplifié des données de démonstration
                valeurs = (
                    str(alerte["timestamp"]),
                    str(alerte["agent"]),
                    int(alerte["rule_id"]),
                    int(alerte["level"]),
                    str(alerte["description"]),
                )
        except (ValueError, TypeError, KeyError) as erreur:
            raise ValueError(f"Ligne {numero} invalide : {erreur}") from erreur

        curseur = connexion.execute(
            """INSERT OR IGNORE INTO alertes
               (timestamp, agent, rule_id, level, description)
               VALUES (?, ?, ?, ?, ?)""",
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

def main():
    analyseur = argparse.ArgumentParser(
        description="Chronologie locale d'alertes de démonstration"
    )
    analyseur.add_argument(
        "--db", required=True, type=Path, help="Chemin de la base SQLite"
    )
    commandes = analyseur.add_subparsers(dest="commande", required=True)
    commandes.add_parser("importer").add_argument("fichier", type=Path)
    commandes.add_parser("lister").add_argument("--agent")
    commandes.add_parser("resumer").add_argument("--agent")


    arguments = analyseur.parse_args()
    with sqlite3.connect(arguments.db) as connexion:
        creer_table(connexion)
        if arguments.commande == "importer":
            importer(connexion, arguments.fichier)
        elif arguments.commande == "lister":
            lister(connexion, arguments.agent)
        else:
            resumer(connexion, arguments.agent)

if __name__ == "__main__":
    main()
