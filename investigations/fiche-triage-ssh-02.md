# Fiche de triage — Échec SSH suivi d’une réussite

## Signal examiné

Le 6 novembre 2026, l’outil Python a rapproché sur `lab-linux` une
alerte d’échec SSH (`5760`) à 08:58:08.743 UTC et une alerte de
réussite (`5715`) à 08:58:14.746 UTC, soit 6,003 secondes d’écart.

Dans l’extrait minimisé utilisé par l’outil Python, `lab-linux` désigne
l’agent affiché sous le nom `soc-linux` dans Wazuh. Les horodatages
Python comportent des millisecondes ; le journal SSH cité ci-dessous
affiche les événements à la seconde.

Ce rapprochement temporel constitue une piste d’investigation, pas
une preuve que les deux alertes concernent la même connexion.

## Recoupement avec la source

Le journal SSH de `SOC-LINUX` indique un `Failed password`, puis un
`Accepted password` pour le compte de test `gaetan`. Les deux lignes
mentionnent l’adresse source `192.168.100.1` et le même port source
`50164`. Ce recoupement permet de rattacher les événements à la même
connexion SSH lors du test contrôlé.

Le déroulement est consigné dans le
[scénario 02](../scenarios/02-succes-apres-echecs.md) et
[l’investigation 02](02-succes-apres-echecs.md).

## Qualification et décision

**Qualification :** un échec suivi d’une réussite sur le compte de test,
dans une connexion autorisée du laboratoire. La réussite ne démontre
pas une compromission.

**Décision :** conserver les journaux et alertes comme preuves du test ;
aucune mesure de blocage n’est justifiée pour cette activité autorisée.

## Limites

Un seul échec a précédé la réussite. Wazuh a signalé les deux
événements séparément : aucune alerte de corrélation automatique
n’a été démontrée. La commande Python ne conserve pas les champs
nécessaires pour confirmer, à elle seule, le compte ou le port source.
