
# -*- coding: utf-8 -*-

import optparse
import os
import sys
import json
import time
import requests

parser = optparse.OptionParser()



ArgumentsPasses = False
HelpInstructions = True

a = len(sys.argv[1:])

print ("Arguments passés :", a)

auto = False

if a == 18:
	ArgumentsPasses = True
elif a == 0:
	ArgumentsPasses = False
	HelpInstructions = False
else :
	print("Vous n'avez pas entré le bon nombre d'arguments.")
	print("Votre entrée doit être de la forme : ")
	print("'py script.py -u username -p password -ad mail_address -h nd_home -a nd_authetification -b nd_blog -cl nd_cloud -ch nd_chat -auto auto'.")
	print("Merci de réessayer.")


if(ArgumentsPasses==True) :
	parser.add_option('-u', '--user',
  	  action="store", dest="user", help="user string", default="spam")

	parser.add_option('-p', '--password',
  	  action="store", dest="password", help="password string", default="spam")

	parser.add_option('-m', '--mail_address',
 	   action="store", dest="mail_address", help="mail_address string", default="spam")

	parser.add_option('-i', '--homepage_domain',
 	   action="store", dest="homepage_domaine", help="homepage_domaine string", default="spam")

	parser.add_option('-k', '--auth_keycloak_domain',
 	   action="store", dest="auth_keycloak_domaine", help="auth_keycloak_domaine string", default="spam")

	parser.add_option('-w', '--blog_domain',
 	   action="store", dest="blog_domaine", help="blog_domaine string", default="spam")

	parser.add_option('-n', '--cloud_domain',
 	   action="store", dest="cloud_domaine", help="cloud_domaine string", default="spam")

	parser.add_option('-r', '--chat_domain',
 	   action="store", dest="chat_domaine", help="chat_domaine string", default="spam")

	parser.add_option('-a', '--auto',
 	   action="store", dest="auto", help="auto string", default="spam")



	options, args = parser.parse_args()



elif(ArgumentsPasses==False and HelpInstructions == False) :
	print("Vous n'avez entré aucun argument lors du lancement du script.")
	user = input("Veuillez entrer votre nom d'utilisateur: ")
	password = input("Veuillez entrer votre mot de passe : ")
	mail = input("Veuillez entrer votre adresse mail : ")
	homepage_domaine = input("Veuillez entrer votre nom de domaine de votre page d'accueil : ")
	auth_keycloak_domaine = input("Veuillez entrer votre nom de domaine de votre page d'authenification : ")
	blog_domaine = input("Veuillez entrer votre nom de domaine de votre blog : ")
	cloud_domaine = input("Veuillez entrer votre nom de domaine de votre cloud : ")
	chat_domaine = input("Veuillez entrer votre nom de domaine de votre chat : ")
	
	


if(ArgumentsPasses == True) :
	user = options.user
	password = options.password
	mail = options.mail_address
	homepage_domaine = options.homepage_domaine
	auth_keycloak_domaine = options.auth_keycloak_domaine
	blog_domaine = options.blog_domaine
	cloud_domaine = options.cloud_domaine
	chat_domaine = options.chat_domaine
	auto = options.auto

fichier = open(".env",'a+')

fichier.write("\n")
fichier.write("sd_global_admin=" + user + "\n")
fichier.write("sd_global_passwd=" + password+ "\n")
fichier.write("sdtc_admin_email=" + mail + "\n")
fichier.write("home_domain=" + homepage_domaine+ "\n")
fichier.write("wp_domain=" + blog_domaine+ "\n")
fichier.write("nc_domain=" + cloud_domaine+ "\n")
fichier.write("rc_domain=" + chat_domaine+ "\n")
fichier.write("keycloak_domain=" + auth_keycloak_domaine+ "\n")

fichier.close()

fichier_json = open("web/urls.js",'w')
fichier_json.write("var myJSONfile = `{ ")
fichier_json.write("\"wordpress\":\"https://"+blog_domaine+"\",")
fichier_json.write("\"nextcloud\":\"https://"+cloud_domaine+"\",")
fichier_json.write("\"rocketchat\":\"https://"+chat_domaine+"\",")
fichier_json.write("\"admin\":\"https://"+auth_keycloak_domaine+"\"")
fichier_json.write("}`;")
fichier_json.close()



if(auto == "True") or (auto == "true"):  
	print("C'EST PARTI en mode auto !!!!!!!!")
else: 
	print("C'EST PARTI  !!!!!!!!")

mk_docker_netwrok= "docker network create webproxy"
#A VERIFIER SI ON PEUT FAIRE CD Comme ca, ou si y a une methode chdir
reverse_proxy_dir= "docker-compose-letsencrypt-nginx-proxy-companion/"
lunch_reverse_proxy= "./start.sh"
reverse_proxy_back= ".."
dc_openid= "docker-compose up -d openid_keycloak"

os.popen(mk_docker_netwrok).read()
os.chdir(reverse_proxy_dir)
os.popen(lunch_reverse_proxy).read()
os.chdir(reverse_proxy_back)
os.popen(dc_openid).read()

##WAIT BLOQUANT ICI "verifier que keycloak s'est bien lancé et appuyez sur y"
if(auto == "True") or (auto == "true"): 
	#V1.1  attente et detection automatique quand ca marche 
	https_k_url = "https://"  + auth_keycloak_domaine +"/auth/"
	print("Veuillez patienter Nous verifions pour keycloack..." + https_k_url)
	while True:
		try:
			requestk = requests.get(https_k_url)
			getattr(requestk, 'status_code', 0)
		except:
			pass
		else:
			if requestk.status_code == 200:
				break
	print ("Keycloak est pret!")
	time.sleep(10)
	
else:
	print("Vérifiez que KeyCloak s'est bien lancé en visitant : https://" + auth_keycloak_domaine)
	time.sleep(8)
	try:
		input("Si tout fonctionne, appuyez sur Entrée pour continuer..")
	except SyntaxError:
		pass


# EXECUTEER COMMANDE R P 

openidlogin = "docker exec  $(sudo docker ps -qf \"name=openid_keycloak\") /opt/jboss/keycloak/bin/kcreg.sh config credentials --server https://"+auth_keycloak_domaine+"/auth --realm master --user "+user+" --password "+password
client_wp = "docker exec  $(sudo docker ps -qf \"name=openid_keycloak\") /opt/jboss/keycloak/bin/kcreg.sh  create -s clientId=wp_client -s 'redirectUris=[\"https://"+blog_domaine+"/*\"]'"
client_nxt = "docker exec  $(sudo docker ps -qf \"name=openid_keycloak\") /opt/jboss/keycloak/bin/kcreg.sh  create -s clientId=nc_client -s 'redirectUris=[\"http://"+cloud_domaine+"/*\"]'"
client_rkt = "docker exec  $(sudo docker ps -qf \"name=openid_keycloak\") /opt/jboss/keycloak/bin/kcreg.sh  create -s clientId=rkt_client -s 'redirectUris=[\"https://"+chat_domaine+"/*\"]'"

os.popen(openidlogin).read()
os.popen(client_wp).read()
os.popen(client_nxt).read()
os.popen(client_rkt).read()

secret_wp = "docker exec  $(sudo docker ps -qf \"name=openid_keycloak\") /opt/jboss/keycloak/bin/kcreg.sh  get wp_client"
secret_nc = "docker exec  $(sudo docker ps -qf \"name=openid_keycloak\") /opt/jboss/keycloak/bin/kcreg.sh  get nc_client"
secret_rkt = "docker exec  $(sudo docker ps -qf \"name=openid_keycloak\") /opt/jboss/keycloak/bin/kcreg.sh  get rkt_client"


json_wp = os.popen(secret_wp).read()
json_nc = os.popen(secret_nc).read()
json_rkt = os.popen(secret_rkt).read()

jsonload_wp=json.loads(json_wp)
jsonload_nc=json.loads(json_nc)
jsonload_rkt=json.loads(json_rkt)

fichier = open(".env",'a+')
fichier.write("wp_secret=" +  jsonload_wp["secret"] + "\n")
fichier.write("nc_secret=" + jsonload_nc["secret"] + "\n")
fichier.write("rkt_secret=" + jsonload_rkt["secret"] + "\n")
fichier.close()

# + EXECUTER UN DOCKER COMPOSE AVEC CERTAINES COMPO WP NC RCHAT

remaining_containers= "docker-compose up -d"

os.popen(remaining_containers).read()

# un 2e WAIT BLOQUANT ICI "verifier que nextcloud et wordpress sont prêts  et appuyez sur y"
if(auto == "True") or (auto == "true"): 
	print("Veuillez patienter nous verifions pour WP et NC...")
	while True:
		try:
			requestw = requests.get("https://"  + blog_domaine)
			getattr(requestw, 'status_code', 0)
			requestn = requests.get("https://"  + cloud_domaine)
			getattr(requestn, 'status_code', 0)
		except:
			pass
		else:
			if requestw.status_code == 200  and requestn.status_code == 200 :
				break
	
	time.sleep(25)
else:
	print("Vérifiez que NextCloud et WordPress se sont bien lancés sur : https://"+cloud_domaine+" et https://"+blog_domaine)
	time.sleep(8)
	try:
		input("Si c'est bon, appuyez sur Entrée pour continuer..")
	except SyntaxError:
		pass



# des fois l'installation de wordpress echoue, on relance l'installation juste au cas ou
install_wp = "docker-compose run -d wordpress-cli-no-sleep"
os.popen(install_wp).read()

# permette le temps pour l'installation ( si auto= false pas besoin car l'utilisar n'aurait pas appuyer tant l,installation n'est pas faite) 
if(auto == "True") or (auto == "true"): 
	time.sleep(65)

#install openid plugin for nextcloud
install_nc_sociallogin1= "docker exec --user www-data $(docker ps -qf \"name=sdtc_nextcloud\") php occ app:install sociallogin"
install_nc_sociallogin2= "docker exec --user www-data $(docker ps -qf \"name=sdtc_nextcloud\") php occ app:enable sociallogin"

os.popen(install_nc_sociallogin1).read()
os.popen(install_nc_sociallogin2).read()

# COMMANDE INSERTION DANS LES DB WP ET NC
chmod_conf = "chmod a+x"
oid_conf2DB = "./push_oid2db.sh"

os.popen(chmod_conf + " " + oid_conf2DB).read()
res_insertion=os.popen(oid_conf2DB).read()

print(res_insertion)
