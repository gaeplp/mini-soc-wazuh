# Investigation 02 — Connexion SSH réussie après un échec

## Contexte et question d’investigation

Le 6 novembre 2026, un test contrôlé a été réalisé depuis l’hôte Windows
(`192.168.100.1`) vers `SOC-LINUX` (`192.168.100.30`). Une tentative
d’authentification SSH incorrecte a été suivie d’une authentification
réussie, pour le compte de test `gaetan`, dans la même connexion.

**Question d’investigation :** les journaux et les alertes Wazuh
permettent-ils de reconstituer cette séquence et d’en apprécier la portée ?

## Sources et éléments de preuve

- Le journal SSH de `SOC-LINUX` contient un `Failed password` puis un
  `Accepted password` pour `gaetan`, depuis `192.168.100.1`.
- Les deux événements indiquent le même port source : `50164`.
- Le tableau de bord Wazuh présente deux alertes sur l’agent `soc-linux` :
  la règle `5760` pour l’échec et la règle `5715` pour la réussite.
- [Déroulement et résultats du scénario 02](../scenarios/02-succes-apres-echecs.md).

## Chronologie

Les heures ci-dessous proviennent du journal de `SOC-LINUX` (UTC).
Le 6 novembre 2026, le tableau de bord affichait les alertes en heure
locale française (UTC+1).

| Heure UTC | Trace sur `SOC-LINUX` | Alerte Wazuh |
|---|---|---|
| 08:58:08 | `Failed password` pour `gaetan` | Règle `5760`, niveau `5` : « sshd: authentication failed. » |
| 08:58:14 | `Accepted password` pour `gaetan` | Règle `5715`, niveau `3` : « sshd: authentication success. » |

Les deux traces proviennent de `192.168.100.1` et mentionnent le port
source `50164`. La réussite intervient **six secondes après l’échec**,
d’après les secondes affichées dans le journal SSH. Le délai de
réception des alertes par Wazuh n’a pas été mesuré.

## Analyse et qualification

Le rapprochement du compte, de l’adresse source, du port source et des
horodatages permet de reconstituer **un échec suivi d’une réussite dans
la même connexion SSH**. Wazuh a signalé séparément les deux événements.

Ce test a été effectué volontairement dans le laboratoire. La réussite
prouve que le compte de test s’est authentifié lors de cette connexion ;
elle ne démontre pas une compromission.

**Aucune alerte Wazuh distincte corrélant automatiquement l’échec et
la réussite n’a été observée.** La séquence a été reconstruite par
l’analyse des événements.

## Conclusion et limites

**Conclusion :** les journaux SSH et les alertes Wazuh permettent de
reconstituer la séquence contrôlée « un échec, puis une réussite ».

**Limites :** malgré son titre initial, ce scénario n’a testé qu’un
seul échec avant la réussite, et non plusieurs échecs rapprochés.
Aucun seuil de corrélation ou délai de réception n’a été validé.

**Retour à l’état initial :** la session SSH de test a été fermée ;
aucune modification durable du compte n’est revendiquée pour ce test.