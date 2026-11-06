# Investigation 03 — Ajout d’un compte au groupe privilégié sudo

## Contexte et question d’investigation
Le 6 novembre 2026, un test contrôlé a été réalisé sur `SOC-LINUX`
(`192.168.100.30`), supervisée par l’agent Wazuh `soc-linux` sur le réseau
isolé du Mini-SOC.

Le compte standard `soc-test`, initialement absent du groupe `sudo`, y a été
ajouté temporairement depuis le compte administrateur `gaetan`.

**Question d’investigation :** les éléments collectés permettent-ils
d’établir quelle commande a été exécutée, par qui, et si l’appartenance
au groupe `sudo` a effectivement changé ?

## Sources et éléments de preuve
Les éléments examinés proviennent de trois sources :

1. **Journal local de `SOC-LINUX`** : les entrées `sudo` et `usermod`
   consultées avec `journalctl` montrent la commande exécutée et le
   changement de groupe.
2. **Alerte du tableau de bord Wazuh** : l’événement de l’agent
   `soc-linux` contient notamment `data.srcuser = gaetan`,
   `data.dstuser = root` et
   `data.command = /usr/sbin/usermod -aG sudo soc-test`.
3. **Vérification de l’état du groupe** : `id soc-test` et
   `getent group sudo` ont été exécutées avant l’ajout, après l’ajout,
   puis après le retrait du compte.

La [capture de l’alerte Wazuh](../screenshots/ajout-groupe-sudo-soc-linux.png)
montre l’exécution de la commande par `gaetan` avec les droits de `root`.
Elle ne prouve pas, à elle seule, que l’ajout au groupe a réussi ; ce point
est confirmé par le journal local et les vérifications décrites dans le
[scénario 03](../scenarios/03-ajout-groupe-privilegie.md).


## Chronologie
Les heures du journal de `SOC-LINUX` sont indiquées en UTC. Le tableau de
bord Wazuh peut afficher les mêmes événements en heure locale française
(UTC+1 le 6 novembre 2026).

| Moment | Observation |
|---|---|
| Avant 09:13:22 UTC | `id soc-test` ne liste pas `sudo` ; `getent group sudo` ne liste que `gaetan`. |
| 09:13:22 UTC | Le journal local indique que `gaetan` lance `sudo usermod -aG sudo soc-test`, puis que `usermod` ajoute le compte au groupe `sudo`. |
| Après l’ajout | `id soc-test` et `getent group sudo` confirment que `soc-test` appartient à `sudo`. |
| Après l’investigation | `sudo gpasswd -d soc-test sudo` retire le compte ; les vérifications confirment que seul `gaetan` reste membre du groupe. |

La minute exacte du retrait n’a pas été relevée ; elle n’est donc pas
reconstituée ici.

## Analyse des événements
L’alerte Wazuh issue de `journald` montre que le compte `gaetan`
(`data.srcuser`) a lancé, avec les droits de `root` (`data.dstuser`),
la commande `/usr/sbin/usermod -aG sudo soc-test` sur `soc-linux`.

Cette alerte établit **l’exécution de la commande privilégiée** et
identifie son initiateur. Elle ne suffit pas, à elle seule, à prouver
que l’ajout au groupe a réussi : une commande exécutée peut échouer.

Le journal local contient également une entrée `usermod` indiquant
l’ajout au groupe. Les vérifications effectuées ensuite avec
`id soc-test` et `getent group sudo` confirment que `soc-test` est
effectivement devenu membre de `sudo`.

Aucune alerte Wazuh **spécifique au changement de groupe** n’a été
démontrée. La conclusion repose donc sur le recoupement entre l’alerte
de commande, le journal local et l’état du groupe.

## Conclusion et limites
**Conclusion :** dans ce test contrôlé, `gaetan` a ajouté `soc-test`
au groupe privilégié `sudo` sur `SOC-LINUX`. L’exécution de la commande
est visible dans Wazuh ; le journal local et la vérification des groupes
confirment que l’ajout a réussi.

**Limites :** aucune alerte Wazuh dédiée au changement de groupe n’a été
démontrée. Le délai de réception de l’alerte n’a pas été mesuré. Ce test
n’établit pas que `soc-test` a utilisé ses privilèges ni qu’une action
malveillante a eu lieu : la modification était autorisée dans le
laboratoire.

## Actions et retour à l’état initial
Le compte de test a été retiré du groupe `sudo` avec
`sudo gpasswd -d soc-test sudo`. Les commandes `id soc-test` et
`getent group sudo` ont confirmé que `soc-test` n’en est plus membre
et que `gaetan` reste le seul membre affiché.

Le compte `soc-test` existe toujours sur la VM, sans appartenance au
groupe `sudo`.

**Améliorations à étudier :** mettre en place une détection dédiée
aux changements de groupes privilégiés, définir une procédure de
qualification et conserver des preuves horodatées lors des prochains
tests. Ces améliorations ne sont pas présentées comme déjà réalisées.