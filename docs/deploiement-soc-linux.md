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

## État du déploiement Wazuh

L’agent Wazuh n’est pas encore installé ni enregistré auprès du manager.
Le déploiement et la vérification de l’agent feront l’objet d’une étape séparée.

## Informations à compléter

- Date d’installation : `28/10/2027`
- Version exacte d’Ubuntu : `24.04.5 LTS (Noble Numbat)`
- Version du noyau : `6.8.0-147-generic`

## Installation de l’agent Wazuh

L’agent Wazuh a été installé sur `SOC-LINUX` depuis le dépôt officiel Wazuh,
pendant une connexion temporaire de la VM au commutateur `Default Switch`.

| Élément | Valeur |
|---|---|
| Paquet installé | `wazuh-agent` |
| Version | `4.14.9-1` |
| Vérification de version | `dpkg-query` |
| Dépôt Wazuh après installation | Désactivé |
| Fichier du dépôt désactivé | `/etc/apt/sources.list.d/wazuh.list.disabled` |

Après l’installation, le dépôt Wazuh a été désactivé en renommant son fichier
de configuration en `wazuh.list.disabled`. Cette précaution évite qu’une mise
à jour générale des paquets installe une version différente de l’agent sans
vérification préalable.

La VM a ensuite été reconnectée au commutateur isolé `SOC-LAB-INT`. Sa
configuration réseau a été vérifiée : l’interface `eth0` possède l’adresse
`192.168.100.30/24` et aucune route par défaut n’est configurée.

L’agent n’a pas encore été démarré ni enrôlé auprès du manager `SOC-WAZUH`.
Cette étape est reportée jusqu’à ce que les deux VM puissent fonctionner
simultanément et communiquer sur le réseau du laboratoire.
