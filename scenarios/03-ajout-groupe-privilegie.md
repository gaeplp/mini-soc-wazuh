# Scénario 03 — Ajout d'un compte à un groupe privilégié

## Statut

À préparer.

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

## Résultats

À compléter après exécution.
