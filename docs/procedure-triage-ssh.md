# Procédure de qualification — Alerte SSH

## Déclencheur

Une alerte d’échec d’authentification SSH (`5760`) ou de réussite
(`5715`) est observée sur l’agent `soc-linux`.

## Vérifications

1. Relever l’heure, l’agent, la règle et le niveau de l’alerte.
2. Examiner le journal SSH correspondant pour identifier, si disponibles,
   le compte, l’adresse source et le port source.
3. Rechercher les échecs et réussites proches dans le temps.
4. Comparer le compte et la source avant de conclure que les événements
   appartiennent à une même connexion.
5. Déterminer si l’activité correspond à un test autorisé du laboratoire.

## Qualification

- **Test autorisé** : conserver les preuves et classer l’alerte comme
  détection correcte d’une activité contrôlée.
- **Contexte insuffisant** : poursuivre l’investigation ; ne pas
  conclure à une compromission sur la seule proximité des alertes.
- **Activité non reconnue** : vérifier le compte et la source, puis
  envisager des mesures de protection adaptées au contexte.

## Preuves à conserver

Horodatages avec fuseau horaire, détails des alertes Wazuh, extraits
pertinents du journal SSH et conclusion motivée. Ne pas publier de
mots de passe ni de données sensibles.

## Limites du laboratoire

La commande Python `sequences-ssh` fournit des pistes fondées sur le
même agent et une fenêtre de 60 secondes. Elle ne vérifie pas le compte
ni la connexion SSH. Aucun blocage ou traitement automatique n’est
revendiqué.
