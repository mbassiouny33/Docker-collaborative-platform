#!/bin/sh

docker stop $(docker ps -qf "name=sdtc") $(docker ps -qf "name=openid_keycloak") $(docker ps -qf "name=nginx") 
rm -r data
rm -r uploads
rm -r docker-compose-letsencrypt-nginx-proxy-companion/nginx-data
docker system prune -f
docker volume prune -f
