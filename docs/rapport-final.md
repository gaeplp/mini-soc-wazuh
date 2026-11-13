# Bilan du Mini-SOC Wazuh

## Objectif et périmètre

Ce projet personnel met en place un laboratoire de détection et
d’investigation sur un réseau virtuel isolé. Il comprend un serveur Wazuh,
un endpoint Ubuntu `SOC-LINUX` et une VM `SOC-WIN11`.

Les tests décrits ici sont contrôlés et réalisés uniquement dans le
laboratoire.

## Résultats validés

| Domaine | Résultat | Référence |
|---|---|---|
| Supervision Linux | L’agent `soc-linux` a été observé actif dans Wazuh. | [Déploiement Linux](deploiement-soc-linux.md) |
| Échec SSH | Un échec isolé a déclenché la règle `5760`. | [Scénario 01](../scenarios/01-echecs-authentification.md) |
| SSH : échec puis réussite | Les règles `5760` et `5715` ont permis de reconstituer une séquence d’un échec suivi d’une réussite. | [Scénario 02](../scenarios/02-succes-apres-echecs.md) |
| Groupe privilégié | L’exécution de la commande d’ajout à `sudo` a été visible dans Wazuh ; le changement de groupe a été confirmé localement. | [Scénario 03](../scenarios/03-ajout-groupe-privilegie.md) |
| Intégrité des fichiers | La création et les modifications d’un fichier de test surveillé ont été détectées. | [Scénario 04](../scenarios/04-modification-fichier.md) |
| Analyse locale | L’outil Python/SQLite importe, liste et résume des alertes JSONL. Sur un extrait minimisé de 12 alertes du laboratoire, sa commande `sequences-ssh` a repéré deux séquences candidates « échec puis réussite » sur le même agent, à 36,012 s et 6,003 s d’intervalle. Les 7 tests automatisés passent. | [Outil Python/SQLite](outil-alertes-sqlite.md) |

## Limites

- Le test SSH « échec puis réussite » comporte **un seul échec** avant
  la réussite ; aucune corrélation automatique de plusieurs échecs
  suivis d’une réussite n’a été démontrée.
- L’alerte liée à l’ajout au groupe `sudo` montre l’exécution de la
  commande, mais pas à elle seule la réussite de la modification.
- L’alerte d’intégrité examinée n’identifie pas l’auteur du changement.
- L’agent de `SOC-WIN11` a été installé et son service local observé en
  fonctionnement, mais **son enrôlement et la remontée d’alertes Windows
  ne sont pas validés**. La mémoire de l’hôte a limité les essais avec
  les deux VM nécessaires démarrées simultanément.
- L’outil SQLite conserve une sélection de champs, pas l’intégralité
  des alertes Wazuh. L’extrait réel minimisé ne contenait pas les
  identifiants d’événements Wazuh.
  - Le repérage des séquences SSH est réalisé par l’outil Python, **pas par
  une règle de corrélation Wazuh**. Les données importées ne permettent
  pas de confirmer que les événements rapprochés concernent le même
  compte ou la même connexion SSH.

## Suites prioritaires

1. Reprendre l’enrôlement de `SOC-WIN11` lorsque les ressources permettent
   de faire fonctionner la VM et le serveur Wazuh ensemble.
2. Tester plusieurs échecs SSH rapprochés et vérifier si une alerte
   corrélée est produite.
3. Étudier une détection dédiée aux changements de groupes privilégiés
   et une source permettant d’attribuer les modifications de fichiers.
4. Définir une procédure de qualification et de réponse aux alertes,
   sans présenter la détection seule comme une mesure de prévention.

## Conclusion

Le laboratoire a permis de collecter et d’analyser plusieurs types
d’événements Linux, de conserver des preuves d’investigation et de
relier les observations à un registre de risques. La supervision
Windows et certaines capacités de corrélation restent des travaux à
poursuivre, et non des résultats acquis.
