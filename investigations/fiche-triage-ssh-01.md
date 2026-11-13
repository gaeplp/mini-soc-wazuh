# Fiche de triage — Échec SSH isolé

## Alerte examinée

- **Machine :** `SOC-LINUX` ; agent Wazuh `soc-linux` (ID `001`).
- **Événement :** échec d’authentification SSH.
- **Règle Wazuh :** `5760`, niveau `5`.
- **Source du journal :** `journald`.

## Recoupement

Le journal SSH consulté lors du test indique un `Failed password` pour
le compte de test `gaetan`, depuis `192.168.100.1`, port source `49670`.
L’événement a été retrouvé dans Wazuh.

Voir le [scénario 01](../scenarios/01-echecs-authentification.md) et
[l’investigation 01](01-echec-authentification-ssh.md) pour le déroulement
et la preuve conservée.

## Qualification et décision

**Qualification :** détection correcte d’un échec SSH provoqué
volontairement dans le laboratoire.

**Décision :** conserver l’alerte comme preuve du test. Aucun blocage
de l’adresse source ni traitement d’incident n’est requis pour cette
activité autorisée.

## Limites

Cet échec isolé ne démontre ni une attaque par force brute ni une
compromission du compte. La présente fiche applique la
[procédure de qualification SSH](../docs/procedure-triage-ssh.md)
à un événement historique ; elle ne démontre pas qu’un traitement
automatique ou continu est en place.
