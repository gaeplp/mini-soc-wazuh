# Déploiement de SOC-WIN11

## Objectif

Préparer un poste Windows 11 destiné à être supervisé par Wazuh dans le
laboratoire Mini-SOC.

## Configuration de la VM

| Élément | Configuration |
|---|---|
| Nom de la VM et de l’ordinateur | `SOC-WIN11` |
| Hyperviseur | Hyper-V, génération 2 |
| Système installé | Windows 11 Professionnel 26H2 |
| Processeurs virtuels | 2 |
| Mémoire | 4 Gio au démarrage, mémoire dynamique activée (configuration Hyper-V relevée lors du diagnostic) |
| Disque virtuel | VHDX dynamique, capacité maximale de 80 Gio (vérifiée sur l’hôte Hyper-V) |
| Sécurité | Démarrage sécurisé activé, modèle « Microsoft Windows », TPM virtuel activé |
| Commutateur du laboratoire | `SOC-LAB-INT` |
| Adresse IPv4 | `192.168.100.20/24` |

## Installation et préparation

Windows 11 Professionnel a été installé depuis l’ISO conservée dans
`C:\Hyper-V\ISO`. La configuration initiale et les mises à jour Windows
ont été effectuées pendant une connexion temporaire au `Default Switch`.

Après les mises à jour, la VM a été arrêtée puis reconnectée au commutateur
isolé `SOC-LAB-INT`. L’adresse IPv4 statique `192.168.100.20/24` a été
attribuée à son interface `Ethernet`, sans passerelle prévue sur le réseau
du laboratoire.

## Vérifications réseau

L’adresse `192.168.100.20/24` a été vérifiée à l’état `Preferred`.
La carte virtuelle est connectée à `SOC-LAB-INT`.

Le profil réseau Windows de la VM est `Public`. Une règle de pare-feu
entrante autorise uniquement les requêtes ICMPv4 provenant de l’hôte
`192.168.100.1`, à destination de `192.168.100.20`, sur l’interface
`Ethernet`. Le pare-feu reste actif.

Après l’ajout de cette règle, le ping depuis l’hôte vers la VM a réussi :
4 paquets reçus sur 4.

## État de la supervision

L’agent Wazuh Windows a été installé sur `SOC-WIN11`. Le service
`WazuhSvc` a été vérifié à l’état `Running`, avec un démarrage
`Automatic`.

Lors de cette vérification, `SOC-WAZUH` était arrêté : le journal de
l’agent indiquait une impossibilité de joindre le service d’enrôlement
à `192.168.100.10:1515`. L’installation et le fonctionnement local du
service sont donc confirmés, mais l’enrôlement et la remontée d’alertes
Windows ne sont pas encore démontrés.

La mémoire disponible sur l’hôte de 16 Go a empêché le démarrage
simultané des deux VM dans la configuration alors testée. L’enrôlement
reste à vérifier lors d’une session où les deux VM peuvent fonctionner
ensemble.

La suite des vérifications est décrite dans le
[plan de reprise de l’agent Windows](plan-reprise-agent-win11.md).

## Points à vérifier ou compléter

- Vérifier la situation de l’activation de Windows ; la licence de l’hôte
  ne vaut pas automatiquement pour la VM.
- Relever les comptes de test créés pour les scénarios, sans publier de
  mots de passe.
