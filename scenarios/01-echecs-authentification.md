# Scénario 01 — Échecs d'authentification répétés

## Statut

Test réalisé le 5 novembre 2026 : un échec d’authentification SSH isolé a été détecté par Wazuh sur `SOC-LINUX` (règle `5760`, niveau `5`). L’investigation correspondante est documentée dans [l’investigation 01](../investigations/01-echec-authentification-ssh.md).

## Objectif

Vérifier que plusieurs échecs d'authentification effectués sur un compte de
test sont collectés, horodatés et détectables dans Wazuh.

## Risque associé

**Référence :** R-01  
**Actif :** compte utilisateur de test  
**Événement redouté :** tentative répétée d'accès non autorisé  

## Prérequis

- endpoint supervisé par Wazuh ;
- compte utilisateur de test ;
- journalisation des authentifications activée ;
- horloges synchronisées ;
- laboratoire virtuel isolé.

## Action prévue

Effectuer plusieurs tentatives de connexion incorrectes sur le même compte
pendant une courte période.

Le nombre exact de tentatives et la durée seront définis après l'étude des
journaux et des règles Wazuh.

## Traces attendues

- date et heure des tentatives ;
- nom de la machine ;
- nom du compte ciblé ;
- résultat d'authentification ;
- source de la tentative, si disponible ;
- identifiant d'événement ;
- règle Wazuh déclenchée, si applicable.

## Résultat attendu

Wazuh doit permettre d'identifier ou de regrouper plusieurs échecs concernant
un même compte dans une période courte.

## Mesures

- nombre de tentatives réalisées ;
- nombre d'événements reçus ;
- délai de réception ;
- nombre d'alertes ;
- niveau de gravité ;
- faux positifs observés.

## Retour à l'état initial

Aucune modification permanente n'est prévue. Le compte de test sera vérifié et
déverrouillé si nécessaire.

## Limites de sécurité

Le scénario sera réalisé uniquement avec un compte de test dans le laboratoire
personnel. Aucun compte externe ou appartenant à un tiers ne sera ciblé.

## Résultats

### Premier test — échec SSH isolé

**Environnement :** `SOC-LINUX` (`192.168.100.30`), supervisé par
`SOC-WAZUH` sur le réseau isolé `SOC-LAB-INT`.

**Action :** depuis l’hôte Windows (`192.168.100.1`), une connexion SSH
au compte de test `gaetan` a été tentée avec un mot de passe incorrect,
puis interrompue.

**Trace observée :** le 5 novembre 2026 à 14 h 11 min 52 s, le journal
SSH de `SOC-LINUX` contient `Failed password` pour `gaetan`, depuis
`192.168.100.1`, port source `49670`.

**Résultat Wazuh :** l’événement est visible dans le tableau de bord
pour l’agent `soc-linux` (ID `001`). Il a déclenché la règle `5760`,
« sshd: authentication failed. », de niveau `5`. La source indiquée
est `journald`.

**Qualification :** vrai positif pour la détection d’un échec
d’authentification. L’action était autorisée et réalisée dans le
laboratoire ; une seule tentative ne démontre pas une attaque par force
brute.

**Difficulté rencontrée :** l’alerte n’a pas été retrouvée lors des
premières recherches dans le tableau de bord. La vérification des
fichiers du manager, puis la recherche de l’événement précis dans
l’interface, ont confirmé qu’elle avait bien été générée. L’archivage
JSON exhaustif, activé temporairement pour le diagnostic, a ensuite
été désactivé ; `wazuh-manager` est resté actif.

**Preuve :** [détail de l’alerte Wazuh — règle 5760](../screenshots/ssh-echec-isole-soc-linux.png).

**Reste à tester :** plusieurs échecs rapprochés et leur éventuelle
corrélation. Aucun résultat de détection d’échecs répétés n’est
revendiqué à ce stade.