# flaskapi
![image](https://github.com/user-attachments/assets/fa7183a5-c377-4246-ab09-a48b099301dc)


##### 1/ Mise en place
### create venv 
# go to repository all venv 
cd ~/Desktop/DevOps
mkdir venv_all
cd venv_all

# create venv named "fask_venv"
python3 -m venv fask_venv

# activate venv "fask_venv"
source fask_venv/bin/activate


##### 2/ installation de flask et permière application flask
### create flaskapi
# create flaskapi repository
cd ~/Desktop/DevOps
mkdir flaskapi
cd flaskapi

# installer package flask
pip install flask


# edit file app.py 
# exécute app.py 
python3 app.py

# arreter le serveur 
> Ctrl + C 


##### 3/ Installation de gunicron et livraison de l'api avec gunicron 
# traiter le message de warning
# WARNING: This is a development server. Do not use it in a production deployment.
Cela indique que  serveur de développement Flask n'est pas destiné à être utilisé en production. 
Pour un déploiement en production, il est recommandé d'utiliser un serveur WSGI 
(comme Gunicorn ou uWSGI) qui est plus performant et sécurisé.
# installer gunicron 
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
    -w 4 : Le nombre de travailleurs (workers) pour gérer les requêtes. Cela peut être ajusté en fonction de ton CPU.
    -b 0.0.0.0:5000 : Spécifie l'adresse et le port. Ici, cela écoute sur toutes les interfaces réseau à 8000.
    app:app : Indique que l'application Flask est définie dans app.py et que l’instance de Flask s'appelle app


# on peu modifie rle lancement de gunicorn en créant un fichier wsgi.py
echo "from app import app as application" > wsgi.py
gunicorn --bind 0.0.0.0:5000 wsgi 


##### 4/ Installation de nginx et livraison de l'api avec nginx 
# securité de l'api
# Pour des raisons de performance et de sécurité, 
# il est recommandé de placer un reverse proxy (comme Nginx ou Apache) devant Gunicorn, 
# pour gérer le routage, les certificats SSL, et la mise en cache

sudo apt update
sudo apt install nginx
    # si erreur lors de l'installation : 
    sudo apt remove --purge nginx nginx-core nginx-common
    sudo apt autoremove
    sudo apt autoclean
    sudo apt update
    sudo apt install nginx

    # vérifier les dépendances
    sudo apt-cache depends nginx

    # Vérifier les dépôts et la version Ubuntu
    nano /etc/apt/sources.list
    ls /etc/apt/sources.list.d/

    # si un service apache est actife il peux créer des conflits avec les port utilisé par nginx et nginx pourrai ne pas démarrer 
    # donc il faut deactiver apache
    sudo systemctl stop apache2
    # et lempecher de démarer au démarage du pc si on n'en veuc plus 
    sudo systemctl disable apache2

    # verifier l'état de nginx 
    sudo systemctl status nginx

    # le démarer à nouveau et revérifier 
    sudo systemctl start nginx
    sudo systemctl status nginx

    # si tout est bon alors redémamer le service nginx
    sudo systemctl restart nginx
    sudo systemctl status nginx



# maintenant que nginx est bien configuré, on peu continuer
ls /etc/nginx/sites-available/
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/nginx_flask_api
sudo nano /etc/nginx/sites-available/nginx_flask_api

server {
    # 8080 si appache est dejà sur le port 80 
    listen 8080; 
    #server_name votre_nom_de_domaine.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

ls /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/nginx_flask_api 
sudo ln -s /etc/nginx/sites-available/nginx_flask_api /etc/nginx/sites-enabled/
sudo systemctl restart nginx
# nginx
http://192.168.1.36:8080


gunicorn --bind 0.0.0.0:5000 wsgi 
# gunicorn
http://192.168.1.36:5000
# nginx
http://192.168.1.36:8080


##### 5/ création du requirements.txt 
# recupérer la liste de tous les packages et envoyer dans le requierment 
pip freeze > requirements.txt 

# Vérifier le contenu du fichier
cat requirements.txt

# Pour installer les packages dans un autre environnement
# pip install -r requirements.txt


##### 6/ envoie du projet sur github
# connexion à github  

# création du projet ayant le même nom que le dossier de mon projet physique sur github 
# creation du token api 

# creation de keys.config et sauvegarde du token 
echo > keys.config

# renseigner le fichier keys.config
# flaskapi_token_github
GITHUB_TOKEN=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

source keys.config
curl -O https://raw.githubusercontent.com/AinaKIKISAGBE/tools_public/refs/heads/main/create_repos_on_gith/create_repos_on_gith_with_token.py
python create_repos_on_gith_with_token.py --github_token $GITHUB_TOKEN --name flaskapi --private false --description "begin flaskapi" 
rm create_repos_on_gith_with_token.py

### envoie du projet sur guthub 
## installation de git 
sudo apt update
sudo apt install git

## envoie du projet sur guthub 
echo "# flaskapi" >> README.md
echo "keys.config" >> .gitignore

echo git config --global user.name "AinaKIKISAGBE" >> env.config
echo git config --global user.email "aina.kiki.sagbe@gmail.com" >> env.config
echo "env.config" >> .gitignore




git init
# git remote add origin https://github.com/AinaKIKISAGBE/flaskapi.git
source env.config
source keys.config
# git remote add origin https://your_token_github@github.com/AinaKIKISAGBE/venv_scoring.git
git remote add origin https://${GITHUB_TOKEN}@github.com/AinaKIKISAGBE/flaskapi.git
# git remote remove origin
# mettre à jour l'url sans suprimer 
# git remote set-url origin https://${GITHUB_TOKEN}@github.com/AinaKIKISAGBE/flaskapi.git



# changer de branche et aller sur la branche welcome
#git checkout main
#git pull origin main
git add .
git commit -m " premier depot de flaskapi"
# nomer, renommer ou écraser une branche si elle existe déjà
git branch -M master
git push origin master

# afficher la brabche en cours
git branch

# créer une nouvelle branche et y accéder 
git checkout -b main2

# changer de branche
git checkout main
#git pull origin master


# suprimer une branche en local # mais ceci ne nous sera pas très utils
git branch
git branch -D main2
git branch

# suprimer une branche distant : ceci est 
git push origin --delete main2
git branch







Différence entre Nginx et Gunicorn
Nginx et Gunicorn sont deux outils souvent utilisés ensemble pour déployer des applications web, mais ils remplissent des rôles très différents dans le stack d'une application. 
1. Rôle et Fonctionnalité
•	Nginx :
o	Type : Serveur web et reverse proxy.
o	Fonction : Nginx est principalement utilisé pour servir des fichiers statiques (comme HTML, CSS, JavaScript, images, etc.) et pour agir comme un reverse proxy pour des applications en backend. Il gère également la répartition de charge, la gestion SSL, la mise en cache, et peut servir de point d'entrée pour les requêtes HTTP(S).
o	Usage : Il est utilisé pour gérer la connexion entre les utilisateurs et les applications, permettant ainsi de déléguer la gestion des requêtes à des serveurs d'application comme Gunicorn.
•	Gunicorn :
o	Type : Serveur d'applications WSGI.
o	Fonction : Gunicorn (Green Unicorn) est un serveur Python qui sert des applications conformes à l'interface WSGI (Web Server Gateway Interface). Il exécute des applications Python, en traitant les requêtes HTTP et en les envoyant à l'application pour traitement.
o	Usage : Il est conçu pour exécuter des applications Python, comme celles développées avec Flask ou Django, et traite les requêtes générées par Nginx.
2. Gestion des Requêtes
•	Nginx :
o	Nginx peut gérer un grand nombre de connexions simultanées et est particulièrement efficace pour les fichiers statiques.
o	Il redirige les requêtes vers Gunicorn (ou un autre serveur d'application) pour le traitement des requêtes dynamiques.
•	Gunicorn :
o	Gunicorn crée plusieurs processus (workers) pour gérer les requêtes, permettant ainsi d'augmenter la capacité de traitement.
o	Il est plus adapté pour gérer des requêtes dynamiques générées par des frameworks Python.
3. Performances
•	Nginx :
o	Connu pour sa rapidité et son efficacité, en particulier lorsqu'il s'agit de servir des fichiers statiques.
o	Il est optimisé pour gérer des milliers de connexions simultanées avec une faible consommation de ressources.
•	Gunicorn :
o	Bien qu'il soit performant pour exécuter des applications Python, il n'est pas conçu pour servir des fichiers statiques. Par conséquent, il est souvent combiné avec Nginx pour obtenir de meilleures performances.
4. Utilisation Commune
Dans un déploiement typique d'une application web Python, Nginx est utilisé comme serveur web devant Gunicorn. Voici comment ils interagissent :
1.	Nginx reçoit les requêtes des clients (navigateur, API, etc.).
2.	Il traite les requêtes statiques (fichiers HTML, CSS, etc.) directement.
3.	Pour les requêtes dynamiques (API, pages générées par le serveur), Nginx les transmet à Gunicorn.
4.	Gunicorn exécute l'application Python, traite la requête, et renvoie la réponse à Nginx.
5.	Enfin, Nginx envoie la réponse finale au client.
Conclusion
En résumé, Nginx est principalement un serveur web et un reverse proxy, tandis que Gunicorn est un serveur d'applications qui exécute des applications Python. Ensemble, ils offrent une solution robuste pour le déploiement d'applications web modernes


####################################################
docker network create -d macvlan --subnet=192.168.1.0/24 --gateway=192.168.1.1 -o parent=eth0 macvlan_network_aina
docker run -d --name flask_api_server --network macvlan_network_aina --ip 192.168.1.100 my_image
docker run -d --name flask_api_server --network macvlan_network_aina --ip 192.168.1.100 debian:latest bash -c "apt-get update && apt-get install -y nginx && service nginx start && tail -f /dev/null"


docker run -d -p 8080:80 -p 5000:5000 -p 2222:22 --name flask_api_server --network macvlan_network_aina --ip 192.168.1.100 debian:latest bash -c "apt-get update && apt-get install -y nginx && service nginx start && tail -f /dev/null"

# 1. Tirer l'image de base (debian:slim)
docker pull debian:latest

# 2. Lancer le conteneur avec nginx sur le port 80
docker run -d -p 8080:80 -p 5000:5000 -p 2222:22 --name flask_api_server debian:latest bash -c "apt-get update && apt-get install -y nginx && service nginx start && tail -f /dev/null"
192.168.1.18 -p 2222
192.168.1.18:8080


# 3. Vérifier le conteneur en cours d'exécution
docker ps

# 4. Accéder à http://localhost

# 5. Arrêter le conteneur (optionnel)
docker stop flask_api_server

# 6. Supprimer le conteneur (optionnel)
docker rm flask_api_server



# Mettez à jour les paquets
apt update

# Installez sudo
apt install -y sudo

# Créer un utilisateur nommé "aina"
# RUN useradd -ms /bin/bash aina

# Changer l’utilisateur courant à "aina"
# USER aina



