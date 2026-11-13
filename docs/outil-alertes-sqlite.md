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

Pour les alertes Wazuh possédant un champ `id`, l’outil utilise cet
identifiant pour éviter les doublons lors d’une réimportation, tout en
conservant deux événements distincts ayant les mêmes champs affichés.
Sans `id`, il utilise une clé calculée à partir des champs conservés :
deux événements distincts ayant exactement ces mêmes champs peuvent
encore être confondus.
Un quatrième test vérifie le comptage des alertes par règle.

## Limites et précautions

L’outil est un prototype de consultation locale : il ne collecte pas
directement les alertes du serveur Wazuh et ne remplace pas son tableau
de bord. Les tests réalisés utilisent uniquement des données fictives ;
ils ne valident pas encore l’import d’un export réel du laboratoire.

Avant d’utiliser un export réel, examiner et anonymiser ses données.
Ne publier dans le dépôt ni journaux bruts, ni identifiants sensibles,
ni base SQLite contenant des alertes réelles.

Le nouveau schéma SQLite n’est pas compatible avec les bases créées par
l’ancienne version de l’outil. Conserver ces bases et utiliser un nouveau
chemin `--db` pour les prochains imports ; aucune migration automatique
n’est réalisée.

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

### Vérification avec le nouveau schéma SQLite

L’extrait minimisé de 12 alertes a été réimporté dans une nouvelle base
SQLite, sans modifier la base créée avec l’ancien schéma. Le résumé filtré
sur `lab-linux` indique 1 alerte pour la règle `554`, 5 pour `5715` et
6 pour `5760`. Une seconde importation a ajouté 0 alerte.

Cet extrait ne contient pas les identifiants `id` d’origine de Wazuh :
ce test vérifie donc le repli sur les champs conservés, et non la
déduplication par identifiant réel.

## Repérage de séquences SSH

La commande suivante recherche, sur un même agent, un échec SSH
(règle `5760`) suivi d’une réussite SSH (règle `5715`) dans un délai
maximal de 60 secondes :

```powershell
python src/alertes_sqlite.py --db "$env:TEMP\mini-soc-alertes-v2-20261113-092859.db" sequences-ssh --agent lab-linux
```

Lorsque les alertes contiennent un compte (dstuser), une adresse source (srcip) et un port source (srcport), l’outil compare ces champs. Deux valeurs renseignées et différentes empêchent le rapprochement. Si un champ manque dans l’une des alertes, la séquence peut encore être affichée : elle reste alors une piste à vérifier dans les journaux d’origine.

Les bases SQLite créées par la version précédente reçoivent les nouvelles colonnes, mais les alertes déjà importées ne sont pas enrichies rétroactivement. Les 12 alertes minimisées du premier essai ne permettent donc pas, à elles seules, de valider cette comparaison. Les tests automatisés couvrent les cas de comptes différents et de sources identiques ou différentes.
