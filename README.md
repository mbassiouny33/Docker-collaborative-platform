# Docker-collaborative-platform
A one-click installation script for a Dockerized environment with a couple of apps (Wordpress, Nextcloud, Rocketchat), an automated openid login (via keycloak) in order to unify a single set of login credentials for all services and an automated reverse proxy with ssl.


## Requirements:
- docker and docker compose installed
- Registered domain name and subdomains(or multiple domains) configured to point to the IP of the installation server.
- Python3 installed

## Built thanks to:
- docker 
- Keycloack
- Nextcloud
- Wordpress 
- Rocket.chat
- Apache 
- Docker-letsencrypt-nginx-proxy-companion ( an automated reverse proxy with valid ssl!)

## What the installation script does (goal):
In plain English: The script will install a colaborative platforme, which can be used for filesharing, posting articles, and chat. An admin account will be created during the installation.
It is useful for schools for example, where you might want to offer complete e-learning tools for students or for a company wishing to offer such filesharing and chat features to their employees.
In technical terms: it's just a bunch of scripts to run a couple of docker containers, initialize them and configures OpenID settings automatically for a single sign-on.


## The outcome (/result)
At the end of an installation you will have a couple of docker containers running the following:
- A simple home page with links to the other 4 services
- A Keycloak openID authentication server
- A blog with wordpress
- a file sharing service with Nextcloud (like Gdrive and MS onedrive)
- discord-like instant messaging app with Rocket chat

## How it works(what the script does):
1- The script will ask you for an admin/password combination and email. They will be used as local admins for each of the apps.
2- The script will ask your for your 5 domains. Can be 5 different domains. or a domain for home and subdomain or whatever you want as long as they point to the server ip.
3- Write some data in config files. (in .env file)
3- The script will launch the reverse proxy (basically the set of containers from Docker-letsencrypt-nginx-proxy-companion)
4- The script will launch keycloak and wait till it's installed (you will have to manually press enter or use auto mode)
5- The script will create 3 clients in Keyclaok for WP, Nextcloud, and Rocketchat.
6. The script will retrieve the secrets for 3 created clients and store them in the .env file
7. The script will launch WP+NC+Rocketchant+Apache.
8. OpenID is configured in Rocket chat via environment variables.
9. At this point you have working WP+NC without OpenID configured. The script will then insert into WP and NC's sql databases the config data and activate openID for both of them.


## Usage:
### Guided usage (default)
1. configure your 5 domains to point to the server ip.
2. clone or download the zip of this repo and Enter it.
3. Simply run the script without any arguments the script will prompt for the required data.
While installing the script will stop and ask you to visit your web sites to check if they work, once they're up press enter.
 ``` python3 installation.py```
4. After the installation is done you will notice Wordpress and nextcloud have login with keycloack buttons but not rocketchat. This is due to a bug that might be fixed in later versions of rocket chat. The current solution is: go to your Rocket.chat website login with the admin credentials you provided to the script  click options (the 3 points on top left) > administration> oauth (scroll down under settings) > add custom Oauth > call it "keycloak" (without quotes). Save and the settings will be filled for you.

### advanced usage with arguments

If you opt for usage with arguments you will have to give all arguments, they're all mandatory.

####  just faster launch (auto = false) 
just like the guided usage with a blocking wait but you only run the script faster or you can use shell variables.

Example: 

```python3 installation.py -u adminusername -p mySecretpassword -m maihhl@mail.com -i homepage.mydomain.com -k keycloack-auth.mydomain.com -w wordpressBlogddsd.com -n nextcloud.mydomain.com -r rocketchat.mydomain.org -a false```

You can also use long version

```python3 installation.py --user adminusername --password mySecretpassword --mail_address maihhl@mail.com --homepage_domain homepage.mydomain.com --auth_keycloak_domain keycloack-auth.mydomain.com --blog_domain wordpressBlogddsd.com --cloud_domain nextcloud.mydomain.com --chat_domain rocketchat.mydomain.org --auto false```

#### Fully automated (auto = true) [ experimental!]
Sometimes you might want to do a headless installation without interacting with the shell. There are various cases where you just wanna run 1 single command and that's it, for example if you run the command with WinSCP's non-interactive shell or inside a loop to install on multiple machines with an algorithm like 
such as

```
for (i in 0:50)
   DO on server[i] : run this python script with arguments {set_of_names}.listOFdomains[i].org
```


WARNING: instead of waiting for your confirmation when SSl signature is done, the script will blindly wait for an amount of seconds and try to resume. Thus it might fail if the wait timer is over before letsencrypt signs your certificate.


Example 
```
python3 installation.py -u adminusername -p mySecretpassword -m maihhl@mail.com -i homepage.mydomain.com -k keycloack-auth.mydomain.com -w wordpressBlogddsd.com -n nextcloud.mydomain.com -r rocketchat.mydomain.org -a True
```

##### List of arguments:
The arguments with the above examples are pretty intuitive  but here's a list of arguments if you still need it:

```
-u, --user                 : admin username (this admin will be local to each website)
-p, --password             : admin password
-m, --mail_adress          : VALID email (will be provided to letsencrypt to sign ssl certificates:: FAIL if mail not valid)
-i, --homepage_domain      : Home page/ welcome page containing link to the other websites (we provide one in web/index.html)
-k, --auth_keycloak_domain : domain that will be used for the keycloack authentifaction
-w, --blog_domain          : blog domain to be used by wordpress
-n, --cloud_domain         : file sharing service domain for nextcloud 
-r, --chat_domain          : chat service domain for rocket chat 
-a, --auto                 : True/False for auto installation without any questions from the script. (set to false if input not boolean)
```

### remove containers and delete them

If for whatever reason you need take down all the containers and delete everything you can do so by running uninstall.sh
```chmod a+x uninstall.sh
./uninstall.sh
```

## Extending this script for production use:
While this script works good enough, it was not meant for production enviornment. So here are a couple of things to do check before you use it in production.
- Make sure volumes are all persistent volumes.
- If you already have a userbase on an LDAP/SAML server, keycloak can delegate the authentication to them. You just need to configure it from the administration panel. 



## Troubleshooting common issues:
#### Error 502
Usually this is due to certificates taking time to be signed. Be patient it might take a couple of minutes (up to 15!)

#### Rocket.chat does not have keycloack option
Please go to Usage section and check instructions for guided installation step 4.


#### Rocket.chat does nothing after I authenticate with Keycloak
Rocket.chat will refuse to login an OpenID user if a local user with the same name exists. For instance The admin account created by the script should be used to login locally. You should not login to rocket.chat administration panel using admin user via keycloak.

#### I logged in with admin but it looks like a normal account (Wordpress and Nextcloud)
The admin account is local to each website. Make sure you didn't log in using Keycloak. When you login with the admin through keycloak, WP/NC will just consider it as another user and will give another login id and let you login as a standard user.


#### Wordpress not installed
Sometimes the wordpress installation might start before the database container is ready causing the installation to fail and exit. The solution is easy.
- open your terminal
- cd to script directory
- Run `docker-compose run -d wordpress-cli` (might take 1-2 minutes to install)

#### Openid button does nothing in wordpress / Openid not present in nextcloud (with auto mode)
Probaly the automated insertion of openid setting failed because by the time the script tried to insert the databases were not ready
- open your terminal
- cd to script directory
- Run `chmod a+x push_oid2db.sh`
- Run `./push_oid2db.sh` (might take 1-2 minutes to install)
