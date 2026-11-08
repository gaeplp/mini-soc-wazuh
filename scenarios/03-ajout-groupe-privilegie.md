# Scénario 03 — Ajout d'un compte à un groupe privilégié

## Statut

Test réalisé le 6 novembre 2026 ; modification du groupe confirmée localement et exécution de la commande observée dans Wazuh.
**Investigation associée :** [investigation 03](../investigations/03-ajout-groupe-privilegie.md).

## Objectif

Détecter l'ajout temporaire d'un compte de test à un groupe disposant de
privilèges administratifs.

## Risque associé

**Référence :** R-03  
**Actif :** comptes et groupes privilégiés  
**Événement redouté :** élévation non autorisée de privilèges  

## Prérequis

- endpoint supervisé par Wazuh ;
- compte standard de test ;
- compte administrateur distinct ;
- journalisation des modifications de comptes et groupes ;
- laboratoire virtuel isolé.

## Action prévue

Créer ou utiliser un compte standard de test, puis l'ajouter temporairement à
un groupe privilégié. Retirer ensuite ce compte du groupe.

Les commandes exactes seront définies après le choix de l'endpoint utilisé.

## Traces attendues

- compte ajouté ;
- groupe modifié ;
- compte ayant initié l'action ;
- machine concernée ;
- date et heure ;
- identifiant d'événement ;
- règle Wazuh déclenchée.

## Résultat attendu

Wazuh doit fournir suffisamment d'informations pour identifier la modification
du groupe privilégié, le compte concerné et l'auteur de l'action.

## Mesures

- délai de réception ;
- nombre d'événements ;
- nombre d'alertes ;
- niveau de gravité ;
- informations disponibles sur l'initiateur ;
- faux positifs observés.

## Retour à l'état initial

Retirer le compte de test du groupe privilégié et vérifier que les privilèges
ont été supprimés.

Le compte pourra être supprimé à la fin des tests s'il n'est plus nécessaire.

## Limites de sécurité

Seuls les comptes et groupes du laboratoire seront utilisés. Aucun compte réel
ou système de production ne sera concerné.

## Résultats — test contrôlé du 6 novembre 2026

Le compte de test `soc-test` a été créé sur `SOC-LINUX` sans appartenance
au groupe privilégié `sudo`. Depuis le compte administrateur `gaetan`,
il a ensuite été ajouté temporairement à ce groupe avec
`sudo usermod -aG sudo soc-test`.

Le journal local de `SOC-LINUX` indique, à 09:13:22 UTC, que `gaetan` a
exécuté la commande `usermod` via `sudo`. Une ligne `usermod` indique
l’ajout de `soc-test` au groupe `sudo`. La commande `id soc-test` a
confirmé cette appartenance.

Dans le tableau de bord Wazuh, une alerte associée à l’exécution de
`sudo` sur l’agent `soc-linux` contient :

- `data.srcuser` : `gaetan` ;
- `data.dstuser` : `root` ;
- `data.command` : `/usr/sbin/usermod -aG sudo soc-test` ;
- `location` : `journald`.

**Qualification :** Wazuh a enregistré l’exécution de la commande
privilégiée et permet d’identifier son initiateur et sa cible.
L’ajout effectif au groupe est confirmé par le journal local et par
la vérification des groupes du compte. Ce test ne démontre pas
l’existence d’une alerte Wazuh dédiée à la modification d’un groupe.

**Retour à l’état initial :** `sudo gpasswd -d soc-test sudo` a retiré
le compte de test du groupe. Les commandes `id soc-test` et
`getent group sudo` ont confirmé que seul `gaetan` reste membre de `sudo`.

**Limites :** aucune mesure de délai de réception ni de détection
spécifique des changements de groupe n’a été réalisée. Le compte
`soc-test` existe toujours, sans appartenance au groupe `sudo`.