# Plan de reprise — Agent Wazuh de SOC-WIN11

## Situation actuelle

L’agent Wazuh est installé sur `SOC-WIN11` (`192.168.100.20`).
Le service `WazuhSvc` a été observé à l’état `Running`, avec un
démarrage `Automatic`.

L’enrôlement auprès de `SOC-WAZUH` (`192.168.100.10`) et la remontée
d’alertes Windows ne sont pas encore confirmés. Lors d’un contrôle,
le journal de l’agent indiquait que le service d’enrôlement à
`192.168.100.10:1515` était inaccessible alors que le serveur était arrêté.

## Contrainte matérielle

L’hôte dispose de 16 Go de RAM. `SOC-WAZUH` utilise actuellement
6 Gio de mémoire fixe ; `SOC-WIN11` est configurée avec 4 Gio au
démarrage et la mémoire dynamique activée.

Le démarrage simultané des deux VM a échoué dans une configuration
précédemment testée, faute de mémoire disponible. Ne pas considérer
la capacité à les faire fonctionner ensemble comme acquise.

## Conditions avant une nouvelle tentative

1. Confirmer que les autres VM du laboratoire sont arrêtées.
2. Mesurer la mémoire disponible sur l’hôte et vérifier qu’une marge
   suffisante reste disponible pour Windows et les services de l’hôte.
3. Démarrer les VM uniquement si Hyper-V peut leur attribuer leurs
   mémoires de démarrage sans mettre l’hôte sous pression.
4. Ne pas réduire à l’aveugle la mémoire de `SOC-WAZUH` : vérifier
   l’état de ses services après toute modification.

## Vérifications à réaliser si les deux VM démarrent

1. Confirmer que les deux cartes réseau sont reliées à `SOC-LAB-INT`.
2. Depuis `SOC-WIN11`, tester l’accès à `192.168.100.10` sur les ports
   nécessaires à l’enrôlement et à la communication de l’agent.
3. Vérifier les journaux de l’agent Windows et l’état de `WazuhSvc`.
4. Vérifier dans le tableau de bord Wazuh que l’agent Windows est
   enregistré et affiche un statut actif.
5. Produire un événement de test bénin dans la VM Windows, puis
   vérifier qu’il apparaît dans Wazuh avant de conclure que la
   supervision fonctionne.

## Critère de validation

L’enrôlement ne sera considéré comme confirmé que si `SOC-WIN11`
apparaît actif dans Wazuh. La remontée d’alertes Windows sera validée
séparément à partir d’un événement observé.

Si la contrainte mémoire empêche toujours le fonctionnement simultané,
documenter l’échec et étudier une solution matérielle ou une autre
organisation du laboratoire avant de poursuivre.
