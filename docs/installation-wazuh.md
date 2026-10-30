# Installation de Wazuh — SOC-WAZUH

## Objectif

Installer Wazuh en architecture all-in-one dans la VM `SOC-WAZUH`
pour centraliser et consulter les alertes du laboratoire.

## Environnement

| Élément | Valeur |
|---|---|
| Hyperviseur | Hyper-V |
| VM | `SOC-WAZUH` |
| Système invité | Ubuntu Server 24.04.5 LTS, 64 bits, sans interface graphique |
| Processeurs virtuels | 4 |
| Mémoire | 8 Go fixes ; mémoire dynamique désactivée |
| Disque virtuel | VHDX dynamique, capacité maximale de 80 Go |
| Disque racine après extension | Environ 76 Go |
| Réseau de laboratoire | `SOC-LAB-INT` |
| Adresse IPv4 finale | `192.168.100.10/24` |
| Passerelle par défaut sur le réseau de laboratoire | Aucune |

## Installation

Wazuh a été installé en architecture all-in-one à l'aide de l'assistant officiel
téléchargé depuis `packages.wazuh.com`. L'installation a été lancée avec
l'option `-a`.

La VM a eu un accès réseau temporaire via le `Default Switch` pour les mises
à jour Ubuntu et le téléchargement de l'assistant. Après l'installation, sa
carte réseau a été reconnectée à `SOC-LAB-INT` et la configuration Netplan
statique du laboratoire a été restaurée.

## Vérifications effectuées

- Les services `wazuh-manager`, `wazuh-indexer` et `wazuh-dashboard`
  sont actifs et activés au démarrage.
- Le port HTTPS 443 est joignable depuis l'hôte Windows à
  `192.168.100.10`.
- Le tableau de bord Wazuh s'affiche depuis l'hôte.
- La VM ne possède pas de route par défaut sur `SOC-LAB-INT`.

## Identifiants et secrets

Les identifiants générés par l'assistant d'installation sont conservés
hors du dépôt. Aucun mot de passe, jeton ou secret ne doit être publié.

## Informations à compléter

- Date de l'installation : 27/10/2026
- Version exacte de Wazuh : `4.14.9-1`
- Version du noyau Ubuntu : `6.8.0-147-generic`
