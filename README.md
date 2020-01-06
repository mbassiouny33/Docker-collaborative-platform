# Docker-collaborative-platform
A one-click installation script for a Dockerized environment with a couple of apps (wordpress, nextcloud,rocketchat), an automated openid login (via keycloak) in order to unify a single set of login credentials for all services and an automated reverse proxy with ssl.


## Requirements:
- docker and docker compose installed
- Registered domain name and subdomains( or mulitple domains) configured to point to the IP of the installation server.
- Python3 installed

## Built thanks thanks to:
- docker 
- Keycloack
- nextcloud
- wordpress 
- Rocket.chat
- Apache 
- docker-letsencrypt-nginx-proxy-companion ( an automated reverse proxy with valid ssl!)

## What the installation script does (goal):
In plain english: The script will install a colaborative platforme, which can be used for filesharing, posting articles,  and chatting. An admin account will be created during the installation
In technical terms: it's just a bunch of scripts to run a couple of docker containers, initialize them and configures openid settings automatically for a single sign-on.


## The outcome (/result)
At the end of an installation you will have a couple of docker containers running the following:
- A simple home page running  

## How it works( what the script does):

## Usage:
### Guided usage (default)
1. configure your 5 domains 
2. clone or download the zip of this repo.
3. Simlpy run the script without any arguments the script will prompt for the required data.
While installing the script will stop and ask you to visit your web sites to check if they work, once they're up press enter.
 ``` python3 installation.py```
3. After the installation is done you will notice Wordpress and nextcloud have login with keycloack buttons but not rocketchat. This is due to a bug that might be fixed in later versions of rocket chat. The currect solution is: go to your Rocket.chat website login with the admin credentials you provided to the script  click options (the 3 points on top left) > administration> oauth (scroll down under settings) > add custom oauth > call it "keycloak" (without quotes). Save and the settings will be filled for you.

### advanced usage with arguments

If you opt for usage with arguments you will have to give all arguements, they're all mandatory.

##### faster lauch (auto = false) 
just like the guided usage with a blocking wait but you only run the script faster or you can use shell variables.

Example: 

`python3 installation.py -u adminusername -p mySecretpassword -m maihhl@mail.com -i homepage.mydomain.com -k keycloack-auth.mydomain.com -w wordpressBlogddsd.com -n nextcloud.mydomain.com -r rocketchat.mydomain.org -a false`

You can also use long version

`python3 installation.py --user adminusername --password mySecretpassword --mail_address maihhl@mail.com --homepage_domain homepage.mydomain.com --auth_keycloak_domain keycloack-auth.mydomain.com --blog_domain wordpressBlogddsd.com --cloud_domain nextcloud.mydomain.com --chat_domain rocketchat.mydomain.org --auto false`

##### Fully automated (auto = true) [ experimental !]
Sometimes you might want to do a headless installation without interacting with the shell. There are various cases where you just wanna run 1 single command and that's it, for example if you run the command with WinSCP's non-interactive shell or inside a loop to install on multiple machines with an algorithm like 
such as

```
for (i in 0:50)
   DO on server[i] : run this python script with arguments {set_of_names}.listOFdomains[i].org
```

Example 
`
python3 installation.py -u adminusername -p mySecretpassword -m maihhl@mail.com -i homepage.mydomain.com -k keycloack-auth.mydomain.com -w wordpressBlogddsd.com -n nextcloud.mydomain.com -r rocketchat.mydomain.org -a True
`

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

#### Wordpress not installed
Sometimes the wordpress installation might start before the database container is ready causing the installation to fail and exit. The solution is easy.
- open your terminal
- cd to script directory
- Run `docker-compose run -d wordpress-cli` (might take 1-2 minutes to install)
