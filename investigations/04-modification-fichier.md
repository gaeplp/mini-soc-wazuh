# Investigation 04 — Modification d’un fichier surveillé

## Contexte et question d’investigation

Le 6 novembre 2026, un test contrôlé de surveillance d’intégrité a été réalisé
sur `SOC-LINUX` (`192.168.100.30`). L’agent Wazuh surveillait en temps réel
le dossier `/opt/soc-lab-fim`.

**Question d’investigation :** Wazuh permet-il d’établir qu’un fichier de ce
dossier a été modifié, et quelles informations fournit-il sur ce changement ?

## Sources et éléments de preuve

- **Fichier de test :** `/opt/soc-lab-fim/test-soc.txt`.
- **Alerte Wazuh :** événement de modification remonté par l’agent `soc-linux`,
  avec `syscheck.event = modified` et `syscheck.mode = realtime`.
- **Preuve visuelle :** [détail de l’alerte de modification](../screenshots/modification-fichier-soc-linux.png).
- **Déroulement du test :** décrit dans le [scénario 04](../scenarios/04-modification-fichier.md).

## Chronologie du test

| Étape | Observation |
|---|---|
| Préparation | Le dossier de test est configuré pour la surveillance d’intégrité en temps réel. |
| Création | Le fichier est créé avec le contenu « Version initiale du fichier de test ». Wazuh signale son ajout : règle `554`, niveau `5`. |
| Modification | Le contenu est remplacé par « Version modifiée du fichier de test ». Wazuh affiche une alerte « Integrity checksum changed. », de niveau `7`. |
| Restauration | Le contenu initial est rétabli et vérifié dans la VM. Wazuh signale également cette opération comme une modification. |

## Analyse

L’alerte de modification concerne le chemin
`/opt/soc-lab-fim/test-soc.txt`. Les champs `syscheck.event = modified` et
`syscheck.mode = realtime` indiquent la nature de l’événement et le mode de
surveillance. Les empreintes avant et après sont différentes, ce qui confirme
un changement du contenu du fichier surveillé.

L’alerte prouve qu’un changement a été détecté sur ce fichier. **Elle ne
permet pas, à elle seule, d’identifier l’utilisateur qui l’a effectué.**
Le test a été réalisé volontairement dans le laboratoire ; il ne démontre
pas une modification malveillante.

## Conclusion, limites et retour à l’état initial

**Conclusion :** Wazuh a détecté la création du fichier, sa modification,
puis la modification correspondant à la restauration de son contenu initial.

**Limites :** le délai précis de détection n’a pas été mesuré. L’identité
de l’auteur du changement n’a pas été établie par l’alerte FIM examinée.
La détection concerne le périmètre configuré ; elle ne prévient pas la
modification du fichier.

**Retour à l’état initial :** le contenu initial du fichier a été restauré
et vérifié. La surveillance du dossier de test reste active.

**Amélioration à étudier :** compléter l’investigation des modifications
par une source de journalisation permettant d’attribuer les actions à un
compte, sans présenter cette attribution comme déjà obtenue.