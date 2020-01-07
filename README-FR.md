# site de travail collaboratif avec Docker

Un script d'installation  pour un environnement Docker avec plusieurs applications (Wordpress, Nextcloud, RocketChat), un authentificateur automatique (via KeyCloak) pour
utiliser un ID / mot de passe pour tous les services, ainsi qu'un reverse proxy automatique, avec un SSL.

## Vous aurez besoin de :
- Docker installé (  + docker compose )
- 5 Noms de domaine et sous-domaine enregistrés et configurés
- Python3

## Compilé avec : 
- docker 
- Keycloack
- Nextcloud
- Wordpress 
- Rocket.chat
- Apache 
- Docker-letsencrypt-nginx-proxy-companion ( Un reverse proxy automatique avec un ssl valide)

## Que fait le script d'installation ?

Le script intallera un site de travail collaboratif qui pourra être utilisé pour partager des fichiers, poster des articles et discuter.
Un compte administrateur sera créé pendant l'installation. Ce site peut être utilie pour les écoles, ou vous pourriez vouloir offrir aux étudiants
un outil d'apprentissage complet, ou pour une institution souhaitant partager des fichiers et permettre à ses employés de discuter.


Plus techniquement, il s'agit seulement de quelques scripts qui créeront des conteneurs docker, les initialiseront et qui configureront OpenID
automatiquement pour un SSO (single sign on).

## Le resultat final (post installation) : 
Après l'installation, vous aurez plusieurs conteneurs docker qui géreront :
Une page d'accueil simple avec un lien vers les 4 autres services,
Un serveur d'authentification OpenID (KeyCloak)
Un blog grâce à Wordpress
Un service de partage de fichiers avec NextCloud (comme Google Drive)
Une application de messagerie instantannée grâce à RocketChat (comme Discord)

## Comment le script fonctionne-t-il ?
Le script vous posera une série de questions : des IDs, et une adresse mail, ce seront les ID administrateurs locaux pour chacun des applications.
Il vous demandera aussi 5 noms de domains (possiblement différents) devant pointer vers l'ip de votre serveur.
Il écrira certaines données dans des fichiers de configuration (fichier .env)
Il lancera le reverse proxy
Il lancera KeyCloak et attendra son installation complète
Il créera 3 clients dans KeyCloak ( WP, NXTC, RKTC)
Il récupérera les "secrets" des 3 clients pour les stocker dans le fichier .env
Il lancera WP, NXTC, RKTC et Apache
OpenID sera configuré dans RKTC via des variables d'environnement.
A ce moment là vous aurez WP et NXTC fonctionnels sans OpenID de configuré. Le script insérera les données de configuration dans les bases de données SQL de WP et NXTC

## Utilisation 

Quelques exemples:

Pour lancer en mode guidé qui vous posera des questions pour le mot de passe, nom de domaines...etc
 ``` python3 installation.py```

Avec parametres
```python3 installation.py -u adminusername -p mySecretpassword -m maihhl@mail.com -i homepage.mydomain.com -k keycloack-auth.mydomain.com -w wordpressBlogddsd.com -n nextcloud.mydomain.com -r rocketchat.mydomain.org -a false```

ou Encore en mode auto

 ```python3 installation.py -u adminusername -p mySecretpassword -m maihhl@mail.com -i homepage.mydomain.com -k keycloack-auth.mydomain.com -w wordpressBlogddsd.com -n nextcloud.mydomain.com -r rocketchat.mydomain.org -a true```

#### Remarques importantes:
Rocket.chat a un petit bug, il prends les paramètres de configuration de Keycloak en variables d'environnement mais il ne crée pas de client automatiquement. Il faut créer le client à la main et la configuration sera importé automatiquement selon les variables. (cf étapes 4 de l'installation guidé sous 'Usage' dans le readme anglais).
Les développeurs de rocket.chat sont au courant de ce bug, Il sera possiblement résolu dans une future version.
pour plus de détailles, merci de vous réferer au readme principale en anglais
