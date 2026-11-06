# Scénario 02 — Connexion réussie après plusieurs échecs

## Statut

Test partiel réalisé : un échec suivi d’une réussite. Le scénario
complet avec plusieurs échecs reste à tester.

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

## Résultats — test contrôlé du 6 novembre 2026

Ce test valide la reconstitution d’une séquence minimale. Il ne valide
pas encore l’objectif de plusieurs échecs suivis d’une réussite.

Une connexion SSH a été effectuée depuis le PC hôte (`192.168.100.1`)
vers `SOC-LINUX` (`192.168.100.30`) avec un premier mot de passe incorrect,
suivi du mot de passe correct dans la même connexion.

| Heure du journal Linux (UTC) | Événement | Résultat Wazuh |
|---|---|---|
| 08 h 58 min 08 s | `Failed password` pour `gaetan` | Règle `5760` — `sshd: authentication failed.`, niveau `5` |
| 08 h 58 min 14 s | `Accepted password` pour `gaetan` | Règle `5715` — `sshd: authentication success.`, niveau `3` |

Les deux lignes du journal concernent l’adresse source `192.168.100.1`
et le même port source `50164`. Les alertes correspondantes apparaissent
vers 09 h 58 dans le tableau de bord, affiché en heure locale UTC+1.

**Qualification :** séquence « échec puis réussite » reconstituée à
partir de deux événements détectés individuellement. Le test a été
réalisé volontairement dans le laboratoire : il ne constitue pas une
compromission.

**Limite :** aucune alerte distincte corrélant l’échec et la réussite
n’a été observée. Ce test ne démontre donc pas une détection automatique
de cette séquence.