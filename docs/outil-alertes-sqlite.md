# Consultation locale d’alertes avec Python et SQLite

## Objectif

L’outil `src/alertes_sqlite.py` importe des alertes depuis un fichier JSONL
(une alerte JSON par ligne) dans une base SQLite, puis les affiche dans
l’ordre chronologique. Il fonctionne sans connexion au serveur Wazuh.

## Formats pris en charge

- Le format simplifié utilisé dans `sample-data/alertes-demo.jsonl`.
- Les champs principaux d’une alerte au format Wazuh, illustrés par
  `sample-data/alerte-wazuh-fictive.jsonl`.

Pour chaque alerte, l’outil conserve l’horodatage, le nom de l’agent,
l’identifiant et le niveau de la règle, ainsi que sa description. Il
n’importe pas l’intégralité de l’alerte Wazuh.

## Démonstration

Depuis la racine du dépôt, dans PowerShell :

```powershell
python src/alertes_sqlite.py --db "$env:TEMP\mini-soc-demo.db" importer sample-data/alertes-demo.jsonl
python src/alertes_sqlite.py --db "$env:TEMP\mini-soc-demo.db" lister --agent demo-linux
```

Pour essayer le format Wazuh fictif dans une base distincte :

```powershell
python src/alertes_sqlite.py --db "$env:TEMP\mini-soc-wazuh-format.db" importer sample-data/alerte-wazuh-fictive.jsonl
python src/alertes_sqlite.py --db "$env:TEMP\mini-soc-wazuh-format.db" lister --agent demo-linux
```

Une seconde importation du même fichier n’ajoute pas les alertes déjà
présentes selon la clé d’unicité de l’outil.

## Tests

```powershell
python -m unittest discover -s tests -v
```

Les trois tests vérifient l’absence de doublons lors d’un second import,
l’ordre chronologique et le filtre par agent, ainsi que l’import du
format Wazuh fictif.

## Limites et précautions

L’outil est un prototype de consultation locale : il ne collecte pas
directement les alertes du serveur Wazuh et ne remplace pas son tableau
de bord. Les tests réalisés utilisent uniquement des données fictives ;
ils ne valident pas encore l’import d’un export réel du laboratoire.

Avant d’utiliser un export réel, examiner et anonymiser ses données.
Ne publier dans le dépôt ni journaux bruts, ni identifiants sensibles,
ni base SQLite contenant des alertes réelles.
