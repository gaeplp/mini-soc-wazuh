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
python src/alertes_sqlite.py --db "$env:TEMP\mini-soc-demo.db" resumer
```
La commande `resumer` accepte aussi `--agent demo-linux` pour limiter
les comptages à cet agent ; sans ce filtre, elle compte tous les agents.

Une seconde importation du même fichier n’ajoute pas les alertes déjà
présentes selon la clé d’unicité de l’outil.

## Tests

```powershell
python -m unittest discover -s tests -v
```

Les trois tests vérifient l’absence de doublons lors d’un second import,
l’ordre chronologique et le filtre par agent, ainsi que l’import du
format Wazuh fictif.
Un quatrième test vérifie le comptage des alertes par règle.

## Limites et précautions

L’outil est un prototype de consultation locale : il ne collecte pas
directement les alertes du serveur Wazuh et ne remplace pas son tableau
de bord. Les tests réalisés utilisent uniquement des données fictives ;
ils ne valident pas encore l’import d’un export réel du laboratoire.

Avant d’utiliser un export réel, examiner et anonymiser ses données.
Ne publier dans le dépôt ni journaux bruts, ni identifiants sensibles,
ni base SQLite contenant des alertes réelles.

## Essai avec des alertes du laboratoire

Les archives Wazuh des 5 et 6 novembre 2026 ont été consultées sur
`SOC-WAZUH`. Pour l’agent `soc-linux`, 12 alertes correspondant aux
règles `5760`, `5715` et `554` ont été sélectionnées.

Un fichier JSONL minimal a été créé hors du dépôt. Il conserve uniquement
l’horodatage, un nom d’agent fictif (`lab-linux`), l’identifiant et le
niveau de la règle, ainsi qu’une description générique. Les comptes,
adresses IP et journaux bruts n’y figurent pas.

Ce fichier a été copié dans le dossier temporaire du PC hôte et importé
dans une base SQLite temporaire. Le filtre `--agent lab-linux` a retourné
12 lignes. Une seconde importation du même fichier a ajouté 0 alerte.

Ce test valide l’import et la consultation de **cet extrait minimisé**
d’événements du laboratoire. Il ne valide pas l’import exhaustif des
alertes Wazuh ni l’absence de collisions entre alertes distinctes.
Le fichier JSONL et la base SQLite n’ont pas été ajoutés au dépôt.

