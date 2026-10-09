# Scénario 04 — Modification d'un fichier surveillé

## Statut

À préparer.

## Objectif

Vérifier que la modification d'un fichier de test placé sous surveillance
d'intégrité produit un événement exploitable dans Wazuh.

## Risque associé

**Référence :** R-04  
**Actif :** fichier de test représentant un fichier sensible  
**Événement redouté :** altération non autorisée d'un fichier  

## Prérequis

- endpoint supervisé par Wazuh ;
- surveillance d'intégrité configurée ;
- fichier de test dédié ;
- copie de sauvegarde du contenu initial ;
- laboratoire virtuel isolé.

## Action prévue

Créer un fichier de test, activer sa surveillance, modifier son contenu puis le
restaurer.

Aucun véritable fichier système critique ne sera utilisé lors du premier test.

## Traces attendues

- chemin du fichier ;
- nom de la machine ;
- date et heure de la modification ;
- nature de la modification ;
- informations sur l'utilisateur, si disponibles ;
- règle Wazuh déclenchée ;
- ancienne et nouvelle empreinte, si disponibles.

## Résultat attendu

Wazuh doit signaler la modification du fichier surveillé et fournir les
éléments nécessaires à sa qualification.

## Mesures

- délai de détection ;
- nombre d'événements ;
- nombre d'alertes ;
- niveau de gravité ;
- informations disponibles sur le changement ;
- faux positifs observés.

## Retour à l'état initial

Restaurer le contenu initial du fichier et vérifier son état.

La surveillance pourra être supprimée après le test si elle n'est plus utile.

## Limites de sécurité

Le premier test utilisera uniquement un fichier créé pour le laboratoire.
Aucun fichier critique de la machine hôte ou d'un système tiers ne sera
modifié.

## Résultats

À compléter après exécution.

