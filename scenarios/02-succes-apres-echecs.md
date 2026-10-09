# Scénario 02 — Connexion réussie après plusieurs échecs

## Statut

À préparer.

## Objectif

Vérifier qu'une connexion réussie après plusieurs échecs peut être identifiée
et reconstituée sous la forme d'une séquence chronologique.

## Risque associé

**Référence :** R-02  
**Actif :** compte utilisateur de test  
**Événement redouté :** accès réussi avec des identifiants potentiellement compromis  

## Prérequis

- endpoint supervisé par Wazuh ;
- compte utilisateur de test ;
- journalisation des échecs et réussites activée ;
- horloges synchronisées ;
- laboratoire virtuel isolé.

## Action prévue

Effectuer plusieurs tentatives de connexion incorrectes sur un compte de test,
puis réaliser une connexion correcte avec ce même compte.

Le nombre de tentatives et la fenêtre temporelle seront précisés après l'étude
des événements disponibles.

## Traces attendues

- événements d'échec ;
- événement de réussite ;
- nom du compte ;
- nom de la machine ;
- source de la connexion, si disponible ;
- horodatages ;
- identifiants d'événements ;
- règles Wazuh déclenchées.

## Résultat attendu

Les événements doivent permettre de reconstruire une séquence composée de
plusieurs échecs suivis d'une réussite sur le même compte.

## Mesures

- nombre d'échecs ;
- délai entre le dernier échec et la réussite ;
- délai de réception des événements ;
- nombre d'alertes ;
- niveau de gravité ;
- faux positifs observés.

## Retour à l'état initial

Fermer la session de test et vérifier l'état du compte.

## Limites de sécurité

Le scénario sera exécuté uniquement avec un compte créé pour le laboratoire.
Aucun identifiant réel ou appartenant à un tiers ne sera utilisé.

## Résultats

À compléter après exécution.
