# Mini-SOC Wazuh, Python et SQLite

## Présentation

Ce projet personnel consiste à construire un laboratoire de supervision,
détection et investigation de sécurité reposant sur Wazuh, Windows, Linux,
Python et SQLite.

Le projet associe des compétences techniques de SOC à une démarche simplifiée
de gestion des risques. Chaque scénario de détection sera relié à un actif, une
menace, un impact potentiel, un contrôle de sécurité et des recommandations.

## Objectifs

- centraliser des événements Windows et Linux ;
- détecter des activités contrôlées dans un laboratoire isolé ;
- analyser et qualifier les alertes ;
- reconstituer des chronologies d'incident ;
- relier les détections à des risques de sécurité ;
- exploiter des événements avec Python et SQLite ;
- produire une documentation technique reproductible.

## Architecture prévue

Le laboratoire comprendra :

- un serveur Wazuh tout-en-un sous Ubuntu Server ;
- un endpoint Windows 11 ;
- un endpoint Ubuntu Linux ;
- un réseau virtuel isolé ;
- une machine hôte Windows 11 pour l'administration et le développement.

## Scénarios principaux

1. Échecs d'authentification répétés
2. Connexion réussie après plusieurs échecs
3. Ajout d'un compte à un groupe privilégié
4. Modification d'un fichier surveillé

## Technologies

- Wazuh
- Windows 11
- Ubuntu Server
- Python
- SQLite
- Git et GitHub
- Visual Studio Code
- Virtualisation

## État du projet

- [x] Évaluation des ressources matérielles
- [x] Installation des outils de travail
- [x] Initialisation du dépôt Git local
- [ ] Documentation initiale
- [ ] Choix et configuration de l'hyperviseur
- [ ] Architecture réseau
- [ ] Installation de Wazuh
- [ ] Déploiement des agents
- [ ] Configuration de la journalisation
- [ ] Exécution des scénarios
- [ ] Règles personnalisées
- [ ] Investigations
- [ ] Outil Python et SQLite
- [ ] Rapport final

## Cadre éthique

Toutes les expérimentations seront réalisées dans un laboratoire personnel
isolé. Aucun système tiers ne sera ciblé. Aucun logiciel malveillant réel,
identifiant réel ou donnée personnelle sensible ne sera utilisé.

Les données publiées seront fictives, synthétiques ou anonymisées.

## Statut

Projet en cours de cadrage.
