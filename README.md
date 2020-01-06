# Docker-collaborative-platform
A one-click installation script for a Dockerized environment with a couple of apps (wordpress, nextcloud,rocketchat, OpenlD(via keycloak))


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
- docker-letsencrypt-nginx-proxy-companion

## What this script does (goal):
The script will install a colaborative platforme, which can be used for filesharing, posting articles,  and chatting.

## The outcome (/result)
At the end of an installation you will have a couple of docker containers running the following:
- A simple home page running  

## How it works( what the script does):

## Usage:
### Guided usage (default)
1. configure your 5 domains 
2. clone or download the zip of this repo.
3. Simlpy run the script without any arguments the script will prompot for the required .
 ``` python3 installation.py```
3. After the installation is done you will notice Wordpress and nextcloud have login with keycloack buttons but not rocketchat. This is due to a bug that might be fixed in later versions of rocket chat. The currect solution is: go to your Rocket.chat website login with the admin credentials you provided to the script  click options (the 3 points on top left) > administration> oauth (scroll down under settings) > add custom oauth > call it "keycloak" (without quotes). Save and the settings will be filled for you.

### advanced usage with arguments
##### faster lauch (auto = false) 
##### Fully automated (auto = true) [ experimental !]
Sometimes you might want to do a headless installation without interacting with the shell. There are various cases where you just wanna run 1 single command and that's it, for example if you run the command with WinSCP's non-interactive shell or inside a loop to install on multiple machines with an algorithm like 
such as

```
for (i in 0:50)
   DO on server[i] : run this python script with {set_of_names}.listOFdomains[i].org
```

simple example 
`
`



## Goal



## Troubleshooting common issues:
#### Error 502
Usually this is due to certificates taking time to be signed. Be patient it might take a couple of minutes (up to 15!)

#### Wordpress not installed
Sometimes the wordpress installation might start before the database container is ready causing the installation to fail and exit. The solution is easy.
- open your terminal
- cd to script directory
- Run `docker-compose run -d wordpress-cli` (might take 1-2 minutes to install)
