# Registre simplifié des risques

## 1. Objectif

Ce registre relie les scénarios techniques du Mini-SOC à des risques de
sécurité.

Il sera mis à jour au fur et à mesure des tests afin de comparer le niveau de
risque initial, les contrôles mis en place et le risque résiduel.

---

## 2. Méthode de cotation

La vraisemblance et l'impact sont évalués sur une échelle de 1 à 4.

### Vraisemblance

| Note | Niveau | Description |
|---:|---|---|
| 1 | Rare | Situation peu probable dans le contexte étudié |
| 2 | Possible | Situation pouvant se produire occasionnellement |
| 3 | Probable | Situation susceptible de se produire régulièrement |
| 4 | Très probable | Situation fréquemment attendue ou observée |

### Impact

| Note | Niveau | Description |
|---:|---|---|
| 1 | Faible | Effet limité et facilement réversible |
| 2 | Modéré | Perturbation nécessitant une intervention |
| 3 | Important | Compromission ou perturbation significative |
| 4 | Critique | Perte majeure de confidentialité, d'intégrité ou de disponibilité |

### Calcul

```text
Score de risque = vraisemblance × impact

```

Le score varie de 1 à 16. La cotation représente une appréciation dans le
contexte du laboratoire ; elle ne constitue pas une mesure statistique.

## 3. Registre des risques

| ID | Risque | Actif concerné | Vraisemblance initiale | Impact | Score initial | Contrôle et preuve | Vraisemblance résiduelle | Score résiduel | Limites et actions |
|---|---|---|---:|---:|---:|---|---:|---:|---|
| R-01 | Accès non autorisé à `SOC-LINUX` par authentification SSH | Compte utilisateur et VM `SOC-LINUX` | 2 — possible | 3 — important | 6 | Échecs SSH détectés individuellement par Wazuh : règle `5760`, niveau `5`. Voir [scénario 01](../scenarios/01-echecs-authentification.md). | 2 — possible | 6 | La détection ne bloque pas une connexion réussie. Corrélation d’échecs répétés et procédure de réponse à tester ; revoir la cotation après mise en place de contrôles préventifs. |
| R-02 | Accès SSH réussi après un échec d’authentification | Compte de test et VM `SOC-LINUX` | 2 — possible | 3 — important | 6 | Un échec puis une réussite ont été observés pour le même compte et la même connexion : règles `5760` et `5715`. Voir [scénario 02](../scenarios/02-succes-apres-echecs.md). | 2 — possible | 6 | Test limité à un échec suivi d’une réussite ; aucune alerte corrélée spécifique ni compromission démontrée. Tester plusieurs échecs et définir une procédure d’investigation. |
| R-03 | Ajout non autorisé d’un compte au groupe privilégié `sudo` | Comptes et privilèges de `SOC-LINUX` | 2 — possible | 3 — important | 6 | Wazuh a enregistré la commande `usermod -aG sudo soc-test` exécutée par `gaetan` via `sudo` ; l’ajout a été confirmé localement. Voir [scénario 03](../scenarios/03-ajout-groupe-privilegie.md). | 2 — possible | 6 | Aucune alerte dédiée au changement de groupe démontrée. Étudier une surveillance spécifique et limiter les droits d’administration. |
| R-04 | Altération non autorisée d’un fichier surveillé | Fichier de test sur `SOC-LINUX` | 2 — possible | 3 — important | 6 | Wazuh a détecté la création puis les modifications de `/opt/soc-lab-fim/test-soc.txt` en temps réel ; création : règle `554`, niveau `5` ; modification : alerte de niveau `7`. Voir [scénario 04](../scenarios/04-modification-fichier.md). | 2 — possible | 6 | Détection limitée au périmètre surveillé ; auteur de la modification non établi et aucune prévention automatique démontrée. Étudier l’attribution des changements et la procédure de réponse. |