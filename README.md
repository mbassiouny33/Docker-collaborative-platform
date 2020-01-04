# Docker-collaborative-platform
A one-click installation script for a Dockerized environment with a couple of apps (wordpress, nextcloud,rocketchat, OpenlD(via keycloak))

### Requirements:
- docker and docker compose installed
- Registered domainname and subdomains( or mulitple domains) configured to point to the installation server.
- Python3 installed

### Goal



### Troubleshooting common issues:
#### Error 502
Usually this is due to certificates taking time to be signed. Be patient it might take a couple of minutes (up to 15!)

#### Wordpress not installed
Sometimes the wordpress installation might start before the database container is ready causing the installation to fail and exit. The solution is easy.
- open your terminal
- cd to script directory
 Run `docker-compose run -d wordpress-cli` (might take 1-2 minutes to install)
