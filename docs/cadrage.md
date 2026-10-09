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
