## Projet Interface-Admin - Groupe 5

### Description du projet :loudspeaker: :

Cette application a été développée pour s'entrainer à python, docker, Gitlab pipeline,server administration (ssh connexion, parsing logs...).<br />
L'utilisateur sélectionne une machine distante, et on affiche une dashboard contenant plusieurs statistiques sur cette machine (utilisation ram, utilisation cpu, nombre de connections par page,nombre d'erreurs...).

### Prérequis :white_check_mark: :

Avant de continuer, veuillez vous assurer d'avoir répondu aux exigences suivantes :

> Vous avez installé Python3 ou une version supérieure

Pour ce faire vous pouvez utiliser la commande suivante :
`apt-get install -y python3`

### Installation :wrench: :

Pour que l'application fonctionne correctement, vous devez avoir installé les modules python suivants :
- paramiko
- apachelogs
- dash 
- dash-html-components 
- dash-core-components 
- plotly

Commencez par installer pip pour pouvoir installer les différents modules par la suite.
Nous recommandons d'utiliser les commandes suivantes :

```
apt-get install -y python3-pip
python3 -m pip install paramiko
python3 -m pip install apachelogs
python3 -m pip install dash
python3 -m pip install dash-html-components
python3 -m pip install dash-core-components
python3 -m pip install plotly --upgrade
```
### Utilisation :bulb: :

Il vous suffit de lancer le fichier main.py <br />
S'il n'y a pas d'erreur, le projet doit être lancé à http://localhost:8050 et vous devez avoir ce résultat : <br />

![Alt text](./dashboard.png?raw=true "Dashboard")


### Contributeurs :raising_hand: :

ANTONINI Arnaud - KLEIJN Emile - GESSEAUME Martial - GUIRONNET Yannis - SAJED Soufiane

### Contact :mailbox: :

- arnaud.antonini@telecom-st-etienne.fr
- emile.kleijn@telecom-st-etienne.fr
- martial.gesseaume@telecom-st-etienne.fr
- yannis.guironnet@telecom-st-etienne.fr
- soufiane.sajed@telecom-st-etienne.fr

### Licence :scroll: :
Pour toute information concernant la licence d'utilisation du logiciel, veuillez vous adresser à Télécom Saint-Étienne.
