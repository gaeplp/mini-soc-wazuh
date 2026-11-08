# Scénario 04 — Modification d'un fichier surveillé

## Statut

Test réalisé le 6 novembre 2026. La création, la modification et la restauration du fichier de test ont été détectées par Wazuh sur `SOC-LINUX`.

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

Configurer la surveillance en temps réel d’un dossier de test dédié sur
`SOC-LINUX`, créer un fichier dans ce dossier, modifier son contenu, puis
restaurer son contenu initial.

Aucun fichier système critique n’est utilisé.

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

## Résultats — test contrôlé du 6 novembre 2026

Le dossier `/opt/soc-lab-fim` a été créé sur `SOC-LINUX`, puis ajouté à la
configuration de surveillance d’intégrité de l’agent Wazuh avec l’option
`realtime="yes"`. Le test de configuration a réussi et l’agent a été
redémarré. Son journal confirme le démarrage de la surveillance en temps
réel du dossier.

Le fichier `/opt/soc-lab-fim/test-soc.txt` a ensuite été créé avec le
contenu « Version initiale du fichier de test ». Wazuh a signalé sa
création : `syscheck.event = added`, règle `554`, niveau `5`, avec le
chemin correct et `syscheck.mode = realtime`.

Le contenu a été remplacé par « Version modifiée du fichier de test ».
Une alerte « Integrity checksum changed. », de niveau `7`, a été observée
pour `soc-linux`. Le détail de l’alerte a été vérifié pour confirmer
qu’elle concernait le fichier de test.

**Preuve :** [alerte Wazuh de la première modification du fichier](../screenshots/modification-fichier-soc-linux.png).
La capture montre le chemin du fichier, l’événement `modified`, le mode
`realtime` et le changement des empreintes avant et après.

Enfin, le contenu initial a été restauré et vérifié dans la VM. Wazuh a
également signalé cette restauration comme une modification :
`syscheck.event = modified`, `syscheck.mode = realtime`, avec le chemin
`/opt/soc-lab-fim/test-soc.txt`. Le détail montre un changement des
empreintes du fichier.

**Qualification :** la création et les modifications du fichier de test
ont été détectées dans le laboratoire. Les alertes examinées permettent
d’identifier le fichier concerné et la nature du changement.

**Limites :** aucun délai précis de détection n’a été mesuré. Ce test ne
démontre pas l’identification de l’utilisateur ayant modifié le fichier.
La surveillance du dossier de test reste active.