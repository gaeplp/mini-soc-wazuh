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
