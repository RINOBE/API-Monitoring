SERVER  MONITORING API:

Cette app est la partie API du Projet Monitoring de serveur linux
Il faut l'installer au niveau du serveur de surveillance
le projet a pour objectif de surveiller l'utilisation des ressources systèmes linux: CPU,RAM, Disque Dure, et débit de la connexion internet.
Il permet aussi de surveiller les commandes lancés par les utilisateurs du serveurs.


Participant:
Kazuki, Djarina, Stéphanie, Mendrika, Rino

Fonctionnement:
Au démarrage, lorsqu'il n'y a pas d'utilisateur, FastAPI crée l'utilisateur:"ADMIN" avec mot de passe "Test2001"
Ce programme utilise un ORM asynchrone performant SQLAlchemy, la structure de la base est directement créer dans le programme donc on n'a pas besoin d'un dump de la base de donnée pour que le programme fonctionne.
Il utilise des websockets pour communiquer de manière fluide avec les serveurs à surveiller, l'authentification des serveurs à surveiller est réaliser à l'aide d'un mécanisme OAuth avec un nom d'utilisateur et un mot de passe qui permettra au serveur à surveiller d'obtenir un token d'accès permettant de poster des informations leurs concernants

Installation:
Environnement de test
- Machine physique
- Système d'exploitation: Windows 10
- CPU Architecture: X86_64
- Database PostgreSQL 16

Pour installer cette partie serveur, il faut suivre les étapes suivantes:
- Récupérer tous les fichiers nécéssaires  ce sont:
databases.py,main.py,models.py,requirements.txt,routes.py,schemas.py,security.py
-Installer PostgreSQL
- installer les dépendances nécessaires:
pip install -r requirements.txt
Pour lancer le serveur:
- python main.py
- Vous pouvez modifier les paramètre uvicorn de main.py pour correspondre à vos besoin:
uvicorn.run(app, host="0.0.0.0", port=8000, ws_ping_interval=300,ws_ping_timeout=300,reload=True)
Avantages:
-Théoriquement stable et performant avec l'utilisation d'un framework performant et asynchrone.
L'utilisation des websockets rend le traffic des données de monitoring plus fluides
-Sécurisé avec l'utilisation de OAuth2 comme authentification des clients et peut très bien intégrés le chiffrement ssl ou Tls (https pour le web et wss pour les websockets)
Limites:





