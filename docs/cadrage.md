# Cadrage du projet Mini-SOC

## 1. Identification du projet

**Nom :** Mini-SOC personnel — détection et investigation avec Wazuh, Python et SQLite  
**Auteur :** Gaëtan PHILIPPE  
**Système hôte :** Windows 11 Professionnel 25H2  
**Durée prévisionnelle :** 55 à 70 heures  
**Disponibilité hebdomadaire :** À déterminer  
**Statut :** Cadrage initial

---

## 2. Contexte

Ce projet personnel vise à développer et à démontrer des compétences pratiques
en supervision de sécurité, analyse de journaux, détection, investigation,
gestion des risques et documentation technique.

Le laboratoire reproduira un petit environnement informatique composé d'un
serveur Wazuh, d'un endpoint Windows et d'un endpoint Linux.

Les événements de sécurité seront centralisés et analysés afin d'identifier
plusieurs activités contrôlées : échecs d'authentification, réussite après
plusieurs échecs, modification des privilèges et modification d'un fichier
surveillé.

Le projet inclura également un outil Python et SQLite permettant d'importer,
normaliser, stocker et analyser un échantillon d'événements de sécurité.

Toutes les expérimentations seront réalisées sur des machines virtuelles
personnelles placées dans un réseau de laboratoire isolé.

---

## 3. Problématique

Comment construire un laboratoire de supervision permettant de :

1. collecter des événements Windows et Linux ;
2. détecter des activités potentiellement suspectes ;
3. qualifier les alertes produites ;
4. reconstituer une chronologie d'incident ;
5. identifier les risques associés ;
6. proposer des mesures de traitement ;
7. exploiter les événements avec Python et SQLite ;
8. produire des résultats mesurables et reproductibles ?

---

## 4. Objectif général

Construire et documenter un Mini-SOC capable de centraliser et d'analyser les
événements de sécurité d'un endpoint Windows et d'un endpoint Linux, puis de
produire des alertes, des chronologies, des investigations et des
recommandations de traitement des risques.

---

## 5. Objectifs mesurables

| Indicateur | Objectif minimal |
|---|---:|
| Endpoints connectés | 2 |
| Scénarios documentés | 4 |
| Scénarios exécutés | 4 |
| Scénarios détectés | Au moins 3 |
| Règles Wazuh personnalisées | Au moins 1 |
| Règles Python ou SQL | Au moins 3 |
| Investigations documentées | Au moins 2 |
| Chronologies générées | Au moins 2 |
| Jeux de données de test | Au moins 2 |
| Rapport final | 1 |

Lorsque cela sera possible, les mesures suivantes seront également relevées :

- délai entre l'action et la réception de l'événement ;
- délai entre l'action et la génération de l'alerte ;
- nombre d'événements produits par scénario ;
- nombre d'alertes produites ;
- faux positifs observés ;
- différences entre les résultats avant et après ajustement des règles.

---

## 6. Périmètre technique

Le projet comprend :

- un serveur Wazuh tout-en-un ;
- un endpoint Windows 11 ;
- un endpoint Ubuntu Linux ;
- un réseau virtuel isolé ;
- la collecte des journaux d'authentification ;
- la surveillance des comptes et des privilèges ;
- la surveillance d'un ensemble limité de fichiers ;
- quatre scénarios de sécurité ;
- au moins une règle Wazuh personnalisée ;
- au moins deux investigations documentées ;
- un outil d'analyse développé avec Python et SQLite ;
- une documentation technique publiée sur GitHub.

---

## 7. Éléments hors périmètre

Le projet exclut :

- les logiciels malveillants réels ;
- les simulations de ransomware ;
- les attaques contre des systèmes tiers ;
- les scans dirigés vers Internet ;
- les tests d'intrusion externes ;
- l'exploitation de vulnérabilités réelles ;
- les systèmes de production ;
- la haute disponibilité ;
- les modèles d'intelligence artificielle ;
- les réponses automatiques susceptibles de bloquer une machine ;
- la surveillance de l'intégralité des disques ;
- l'automatisation avancée avant la validation du projet principal.

---

## 8. Architecture prévue

| Machine | Système | Rôle | vCPU | RAM | Stockage |
|---|---|---|---:|---:|---:|
| SOC-WAZUH | Ubuntu Server | Serveur Wazuh tout-en-un | 4 | 8 Go | 60 Go |
| SOC-WIN11 | Windows 11 | Endpoint Windows | 2 | 4 Go | 60 Go |
| SOC-LINUX | Ubuntu Server | Endpoint Linux | 2 | 2 Go | 30 Go |
| Machine hôte | Windows 11 Pro 25H2 | Administration et développement | — | 16 Go | Environ 400 Go disponibles |

Les disques virtuels seront alloués dynamiquement.

Afin de préserver suffisamment de mémoire pour la machine hôte, les trois
machines virtuelles ne seront normalement pas exécutées simultanément.

Les combinaisons principales seront :

- `SOC-WAZUH` et `SOC-WIN11` ;
- `SOC-WAZUH` et `SOC-LINUX`.

Ces allocations sont provisoires et pourront être adaptées après mesure de la
consommation réelle.

> **Mise à jour du dimensionnement :** les ressources et capacités de disque
> retenues après vérification de l'hôte sont détaillées dans la section
> « Architecture et ressources prévues ». Ce premier tableau constitue
> l'estimation initiale du cadrage.

---

## 9. Environnement matériel

| Élément | Caractéristique |
|---|---|
| Système d'exploitation | Windows 11 Professionnel 25H2 |
| Build Windows | 26200 |
| Architecture | x64 |
| Processeur | Intel Core Ultra 5 135H |
| Cœurs physiques | 14 |
| Processeurs logiques | 18 |
| Mémoire installée | 16 Go DDR5 |
| Mémoire utilisable | Environ 15,4 Gio |
| Espace disque disponible | Environ 400 Go |
| Virtualisation | Disponible |
| Hyper-V | Disponible, mais désactivé |
| Hyperviseur définitif | À sélectionner |

La machine hôte dispose de ressources suffisantes pour réaliser le projet. La
principale contrainte concerne la mémoire vive.

---

## 10. Outils de travail

| Outil | Version ou configuration |
|---|---|
| Git | 2.55.0.5 |
| Branche Git par défaut | `main` |
| Identité Git | Nom réel et adresse GitHub `noreply` |
| Visual Studio Code | 1.140.0 x64 |
| Python | 3.14.7 x64 |
| pip | 26.2.1 |
| SQLite | 3.50.4 |
| Environnements virtuels | Module `venv` disponible |
| GitHub | Compte existant, dépôt public prévu |

---

## 11. Scénarios prioritaires

### Scénario 1 — Échecs d'authentification répétés

Plusieurs tentatives de connexion incorrectes seront effectuées sur un compte
de test.

**Résultat attendu :**

- identification du compte ciblé ;
- identification de la machine ;
- comptage des échecs ;
- conservation des horodatages ;
- génération ou identification d'une alerte.

### Scénario 2 — Connexion réussie après plusieurs échecs

Une connexion réussie sera effectuée après plusieurs tentatives incorrectes.

**Résultat attendu :**

- identification des échecs ;
- identification de la connexion réussie ;
- reconstruction de la séquence ;
- qualification du niveau de risque.

### Scénario 3 — Ajout à un groupe privilégié

Un compte de test sera temporairement ajouté à un groupe disposant de
privilèges administratifs.

**Résultat attendu :**

- identification du compte ajouté ;
- identification du groupe modifié ;
- identification du compte ayant effectué l'action ;
- génération ou identification d'une alerte ;
- retour du système à son état initial.

### Scénario 4 — Modification d'un fichier surveillé

Un fichier de test placé sous surveillance d'intégrité sera modifié, puis
restauré.

**Résultat attendu :**

- identification du fichier ;
- détection de la modification ;
- conservation de l'horodatage ;
- identification de l'hôte ;
- identification de l'utilisateur, si l'information est disponible.

---

## 12. Dimension GRC

Chaque scénario sera associé à :

- un actif ;
- une menace ;
- une vulnérabilité ou faiblesse ;
- un événement redouté ;
- une vraisemblance ;
- un impact ;
- un niveau de risque initial ;
- un contrôle de sécurité ;
- une preuve de fonctionnement ;
- un niveau de risque résiduel ;
- des recommandations.

Une méthode simplifiée de cotation de 1 à 4 sera utilisée pour la
vraisemblance et l'impact.

```text
Score de risque = vraisemblance × impact
```

## Stockage de l'infrastructure virtuelle

La machine hôte dispose d'un volume `C:` au format NTFS, installé sur un SSD
SanDisk PC SN5100S SDFPMSM-512G-1101.

| Élément | Valeur |
|---|---|
| Capacité totale | Environ 475,9 Go |
| Espace libre observé | Environ 419,1 Go |
| Type de stockage | SSD |
| État de santé | Healthy |
| Emplacement des VM | `C:\Hyper-V` |

Les fichiers de l'infrastructure virtuelle seront organisés comme suit :

```
C:\Hyper-V\
├── Exports\
├── ISO\
├── Virtual Hard Disks\
└── Virtual Machines\
```

## Réseau du laboratoire

Le laboratoire utilisera un commutateur Hyper-V interne nommé `SOC-LAB-INT`.
Ce commutateur permet aux machines virtuelles de communiquer entre elles et
avec l'hôte Windows, sans les connecter directement au réseau physique.

Le réseau prévu est `192.168.100.0/24`. Aucune passerelle ni aucun serveur DNS
ne seront configurés sur ce réseau isolé.

| Machine | Adresse IPv4 prévue | Rôle |
|---|---:|---|
| Hôte Windows | `192.168.100.1/24` | Administration du laboratoire |
| `SOC-WAZUH` | `192.168.100.10/24` | Serveur Wazuh |
| `SOC-WIN11` | `192.168.100.20/24` | Endpoint Windows |
| `SOC-LINUX` | `192.168.100.30/24` | Endpoint Linux |

L'adresse `192.168.100.1/24` de l'interface virtuelle de l'hôte a été
configurée et vérifiée à l'état `Preferred`. Un ping local vers cette adresse
a réussi (4 paquets reçus sur 4).

Les adresses des machines virtuelles sont planifiées ; elles ne sont pas
encore configurées. L'accès Internet des VM n'est pas prévu sur ce commutateur.
Toute connexion temporaire nécessaire aux installations ou mises à jour sera
définie séparément et contrôlée.

## Architecture et ressources prévues

Les machines virtuelles seront hébergées sur Hyper-V, dans les dossiers
préparés sous `C:\Hyper-V`. Elles utiliseront le commutateur interne
`SOC-LAB-INT`. Celui-ci permet les communications entre les VM et l'hôte,
sans connexion directe au réseau physique. ([learn.microsoft.com](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/plan-hyper-v-networking-in-windows-server?utm_source=openai))

| Machine | Système prévu | Rôle | vCPU | Mémoire de démarrage | Disque virtuel maximal | Adresse prévue |
|---|---|---|---:|---:|---:|---|
| `SOC-WAZUH` | Ubuntu Server 24.04.5 LTS, sans interface graphique | Serveur Wazuh all-in-one | 4 | 8 Go, fixe | 80 Go, dynamique | `192.168.100.10/24` |
| `SOC-WIN11` | Windows 11 Professionnel 26H2 x64, installé depuis l’ISO multiédition française | Endpoint Windows supervisé | 2 | 4 Go, fixe | 80 Go, dynamique | `192.168.100.20/24` |
| `SOC-LINUX` | Ubuntu Server 24.04.5 LTS, sans interface graphique | Endpoint Linux supervisé | 2 | 2 Go, fixe | 40 Go, dynamique | `192.168.100.30/24` |

> **Dimensionnement testé :** la VM `SOC-WAZUH`, initialement prévue avec
> 8 Gio de mémoire fixe, a été réglée à 6 Gio à titre expérimental pour
> fonctionner en parallèle avec `SOC-LINUX` sur l’hôte de 16 Go. Les trois
> services Wazuh ont atteint l’état `active` et l’agent `soc-linux` a été
> enrôlé avec le statut `active`. Ce test ne valide pas encore la stabilité
> du serveur sous une charge de journaux prolongée. Le réglage sera
> réévalué pendant les scénarios de détection.


Les capacités de disque indiquées sont des plafonds pour des disques virtuels
à allocation dynamique : l'espace réellement occupé sur le SSD augmentera
avec les données écrites dans les VM.

La machine hôte dispose de 16 Go de RAM installée. Pour limiter la pression
mémoire, les trois VM ne seront pas démarrées simultanément au début. Les
essais commenceront avec SOC-WAZUH seul, puis avec SOC-WAZUH et un seul
endpoint. La stabilité de l'hôte sera vérifiée avant d'envisager d'autres
combinaisons.

Les systèmes indiqués sont les versions retenues pour le projet ; les ISO
n'ont pas encore été téléchargées et les VM n'ont pas encore été créées.

## Accès réseau temporaire pour l'installation

Le commutateur `SOC-LAB-INT` restera dédié au réseau du laboratoire. Pour les
téléchargements et mises à jour nécessaires à l'installation, une VM pourra
être connectée temporairement au `Default Switch` de Hyper-V, qui fournit
un accès réseau via l'hôte.

Cette connexion ne sera utilisée que pour les opérations nécessaires. Après
l'installation et les mises à jour, l'adaptateur réseau de la VM sera
reconnecté à `SOC-LAB-INT` et l'accès réseau temporaire sera retiré. Une VM
ne sera pas connectée simultanément aux deux commutateurs pendant les tests.

Le `Default Switch` n'est pas un réseau isolé. Les activités de simulation
seront réalisées uniquement sur `SOC-LAB-INT`, dans le périmètre du laboratoire.

## Sources et vérification des images ISO

Les images ISO seront obtenues depuis les sources officielles des éditeurs.
Elles seront enregistrées dans `C:\Hyper-V\ISO`. Avant leur utilisation,
leur empreinte SHA-256 sera calculée et comparée à la valeur officielle.

| Système | Fichier ou source prévue | SHA-256 officiel |
|---|---|---|
| Ubuntu Server 24.04.5 LTS AMD64 | `ubuntu-24.04.5-live-server-amd64.iso` — page officielle Ubuntu Releases, fichier `SHA256SUMS` | `97f3d7ffb032c3eb3b23d2c8be9cc76e60c2c1f2c0146ba5ba9fe01cafae0fd8` |
| Windows 11 26H2 x64, français | ISO multiédition — page officielle Microsoft de téléchargement | `AA515279F02FB2B425EFF341F0A1F158D61288C72CCA5F9D87B79B5A23F7F918` |

Pour Ubuntu, la valeur sera vérifiée dans le fichier officiel `SHA256SUMS`
correspondant à la version téléchargée. Pour Windows, la valeur sera
comparée à celle publiée par Microsoft pour l'ISO française x64.

La vérification dans PowerShell s'effectuera après téléchargement avec :

```powershell
Get-FileHash "C:\Hyper-V\ISO\nom-du-fichier.iso" -Algorithm SHA256
```

Une ISO ne sera utilisée que si son empreinte calculée correspond exactement
à la valeur officielle. L'ISO Windows est multiédition ; la disponibilité et
l'activation de l'édition Pro dépendront de la licence utilisée.

## Horodatage du laboratoire

`SOC-LINUX` et `SOC-WAZUH` utilisent le fuseau horaire UTC. Le PC hôte
Windows affiche l’heure locale française : le 6 novembre 2026, elle
était à UTC+1. Cela explique que les événements SSH datés de 08 h 18
dans le journal Linux apparaissent vers 09 h 18 dans le tableau de bord
Wazuh.

Lors d’une vérification, les trois machines affichaient la même heure
UTC, sans dérive notable constatée. Le service d’intégration Hyper-V
« Synchronisation date/heure » était activé pour les deux VM.

Sur les VM, `timedatectl` indiquait néanmoins
`System clock synchronized: no` : la synchronisation NTP n’est donc
pas confirmée sur ce réseau isolé. Les investigations préciseront
toujours le fuseau utilisé pour chaque horodatage.