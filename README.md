# Mini-SOC Wazuh

## Présentation

Ce projet personnel est un laboratoire de supervision et d’investigation
de sécurité construit avec Hyper-V et Wazuh. Il associe des tests contrôlés
à une démarche simplifiée de gestion des risques.

Le projet est en cours : les scénarios documentés ont été réalisés sur
Linux. La supervision de Windows et l’exploitation des événements avec
Python et SQLite restent à valider ou à développer.

## Architecture du laboratoire

- **Hôte :** Windows 11 avec Hyper-V, 16 Go de RAM.
- **SOC-WAZUH :** serveur Wazuh tout-en-un sous Ubuntu Server.
- **SOC-LINUX :** endpoint Ubuntu Server avec agent Wazuh actif.
- **SOC-WIN11 :** endpoint Windows 11 avec agent installé ; son enrôlement
  et la remontée d’alertes ne sont pas encore confirmés.
- **Réseau :** commutateur virtuel isolé `SOC-LAB-INT`.

La mémoire de l’hôte limite les combinaisons de VM pouvant fonctionner
simultanément. Voir le [cadrage](docs/cadrage.md) et le
[plan de reprise de l’agent Windows](docs/plan-reprise-agent-win11.md).

## Scénarios réalisés sur SOC-LINUX

| Scénario | Résultat observé | Investigation |
|---|---|---|
| [01 — Échec SSH isolé](scenarios/01-echecs-authentification.md) | Échec détecté par Wazuh ; un événement isolé ne démontre pas une attaque par force brute. | [Investigation 01](investigations/01-echec-authentification-ssh.md) |
| [02 — Échec puis réussite SSH](scenarios/02-succes-apres-echecs.md) | Deux événements détectés séparément ; aucune alerte de corrélation automatique démontrée. | [Investigation 02](investigations/02-succes-apres-echecs.md) |
| [03 — Ajout au groupe sudo](scenarios/03-ajout-groupe-privilegie.md) | Commande privilégiée visible dans Wazuh ; changement de groupe confirmé par les vérifications locales. | [Investigation 03](investigations/03-ajout-groupe-privilegie.md) |
| [04 — Modification d’un fichier](scenarios/04-modification-fichier.md) | Création et modifications détectées par la surveillance d’intégrité ; auteur non établi par l’alerte examinée. | [Investigation 04](investigations/04-modification-fichier.md) |

Les risques associés et les limites des contrôles sont consignés dans le
[registre des risques](docs/registre-risques.md).

## État du projet

- [x] Architecture Hyper-V et réseau de laboratoire préparés
- [x] Serveur Wazuh installé et accessible
- [x] Agent Linux enrôlé et quatre scénarios documentés
- [x] Investigations associées aux quatre scénarios
- [x] Registre simplifié des risques
- [ ] Enrôlement et remontée d’alertes de l’agent Windows à confirmer
- [ ] Exploitation des événements avec Python et SQLite
- [ ] Rapport final

## Outil Python et SQLite

Un prototype permet d’importer des alertes fictives et de les consulter
dans une base SQLite, avec un filtre par agent.

La [documentation de l’outil Python/SQLite](docs/outil-alertes-sqlite.md)
présente son utilisation, ses tests et ses limites.

## Cadre éthique

Les tests sont réalisés uniquement dans un laboratoire personnel isolé,
sur des machines et des comptes autorisés. Les résultats documentent ce
qui a été effectivement observé, sans assimiler les tests à des incidents
réels. Aucun mot de passe ou autre secret ne doit être publié dans le dépôt.

## Bilan du projet

Le [bilan du Mini-SOC](docs/rapport-final.md) récapitule les résultats
validés, les limites des tests et les suites prioritaires. La supervision
Linux a été testée ; l’enrôlement et la remontée d’alertes de `SOC-WIN11`
restent à valider.
