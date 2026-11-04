# Déploiement de SOC-LINUX

## Objectif

Préparer un endpoint Ubuntu Linux pour le superviser avec Wazuh dans le Mini-SOC.

## Configuration de la VM

| Élément | Valeur |
|---|---|
| Nom Hyper-V | `SOC-LINUX` |
| Nom d’hôte Ubuntu | `soc-linux` |
| Système | Ubuntu Server 24.04.5 LTS, 64 bits, sans interface graphique |
| Processeurs virtuels | 2 |
| Mémoire | 2 Go fixes |
| Disque virtuel | VHDX dynamique, capacité maximale de 40 Go |
| Commutateur de laboratoire | `SOC-LAB-INT` |
| Adresse IPv4 prévue | `192.168.100.30/24` |
| Serveur SSH | Installé |

## Installation et préparation

Ubuntu Server a été installé depuis l’ISO officielle AMD64. La VM a utilisé
temporairement le `Default Switch` pour l’installation et les mises à jour.
Elle a ensuite été reconnectée à `SOC-LAB-INT`, et son adresse statique
`192.168.100.30/24` a été configurée avec Netplan.

## Vérifications effectuées

- Le nom d’hôte `soc-linux` a été vérifié.
- Les mises à jour Ubuntu ont été installées.
- `eth0` possède l’adresse `192.168.100.30/24`.
- Aucune route par défaut n’est configurée sur le réseau de laboratoire.
- Le ping depuis l’hôte Windows a réussi : 4 paquets reçus sur 4.

## Agent Wazuh : installation et enrôlement

L’agent Wazuh `4.14.9-1` a été installé sur `SOC-LINUX`. Pour télécharger le
paquet, la VM a été connectée temporairement au `Default Switch`, puis
reconnectée au réseau isolé `SOC-LAB-INT`.

Le dépôt Wazuh a été désactivé après l’installation ; son fichier de
configuration est conservé sous le nom `wazuh.list.disabled`.

Au premier démarrage, l’agent a échoué car le fichier
`/var/ossec/etc/ossec.conf` contenait encore la valeur d’exemple
`MANAGER_IP`. L’adresse du serveur a été corrigée dans la section
`<client><server>` :

```xml
<address>192.168.100.10</address>
```

Après cette correction, le service `wazuh-agent` a démarré avec l’état
`active`. Le tableau de bord Wazuh confirme l’enrôlement de l’agent :

| Élément | Résultat observé |
|---|---|
| ID de l’agent | `001` |
| Nom | `soc-linux` |
| Adresse IP | `192.168.100.30` |
| Système | Ubuntu 24.04.5 LTS |
| Version affichée | `v4.14.9` |
| Statut | `active` |

Pour lancer simultanément `SOC-WAZUH` et `SOC-LINUX` sur l’hôte doté de
16 Go de RAM, la mémoire fixe de `SOC-WAZUH` a été réduite de 8 à **6 Gio
à titre expérimental**. Ses trois services étaient `active` et l’agent
Linux s’est enrôlé avec succès. La stabilité sous une charge de journaux
prolongée reste à évaluer.

## Informations

- Date d’installation : non relevée.
- Version exacte d’Ubuntu : `24.04.5 LTS (Noble Numbat)`.
- Version du noyau : `6.8.0-147-generic`.