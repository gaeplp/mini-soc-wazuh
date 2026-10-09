# Scénario 01 — Échecs d'authentification répétés

## Statut

À préparer.

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

À compléter après exécution.
