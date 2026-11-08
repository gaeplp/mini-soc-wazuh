# Investigation 01 — Échec d’authentification SSH isolé

## Contexte et question d’investigation

Le 5 novembre 2026, une tentative de connexion SSH avec un mot de passe
incorrect a été réalisée dans le laboratoire depuis l’hôte Windows
(`192.168.100.1`) vers `SOC-LINUX` (`192.168.100.30`).

**Question d’investigation :** l’échec est-il visible dans Wazuh et
permet-il d’identifier le compte, la machine et la source concernés ?

## Sources et éléments de preuve

- Le journal SSH de `SOC-LINUX` contient un événement `Failed password`
  pour le compte de test `gaetan`, depuis `192.168.100.1`.
- Le tableau de bord Wazuh présente une alerte sur l’agent `soc-linux`
  (ID `001`) : règle `5760`, « sshd: authentication failed. », niveau `5`.
- La source de l’événement dans Wazuh est `journald`.
- [Capture du détail de l’alerte](../screenshots/ssh-echec-isole-soc-linux.png).
- [Déroulement du scénario 01](../scenarios/01-echecs-authentification.md).

## Chronologie

| Moment | Observation |
|---|---|
| 5 novembre 2026, 14:11:52, heure du journal SSH | Événement `Failed password` pour `gaetan`, depuis `192.168.100.1`, port source `49670`. |
| Après la tentative | L’alerte correspondante est retrouvée dans le tableau de bord Wazuh sur l’agent `soc-linux`. |

Le délai exact entre l’événement et son affichage dans Wazuh n’a pas été
mesuré.

## Analyse et qualification

Le journal SSH établit qu’une authentification a échoué pour `gaetan`
depuis l’adresse de l’hôte du laboratoire. L’alerte Wazuh correspondante
confirme que cet échec a été collecté et signalé.

Il s’agit d’un **vrai positif pour la détection d’un échec
d’authentification**. La tentative était autorisée et contrôlée ; un
échec isolé ne permet pas de conclure à une attaque par force brute
ni à une compromission du compte.

## Conclusion et limites

**Conclusion :** Wazuh a détecté l’échec SSH isolé et fourni une alerte
exploitable pour commencer l’investigation.

**Limites :** ce test ne démontre ni la corrélation de plusieurs échecs,
ni une réponse automatique, ni le blocage de l’adresse source. Aucun
délai de détection précis n’a été établi.

**Retour à l’état initial :** aucune modification durable du compte ou
de la configuration SSH n’a été effectuée pour cette tentative.