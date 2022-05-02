from socket import *
import time 

def website_in(site):
	"""
	verifie si le site web est un site que le client a deja visite ou non
	si c'est le cas, la fonction renvoie la position du site web dans l'historique  
	"""
	for element in range (len(historique)) :
		if historique[element] == site :
			return element
		else:
			return -1

def create_cache(name, message):
	"""
	creation d'un nouveau fichier texte, qui represente la cache du site web recherche  
	"""
	File_cache = open(name,"a")
	File_cache.write(message.decode('utf-8'))
	File_cache.close()
	
def in_cache(name):
	"""
	Le site web est present en cache, on recupere les datas sur le cache correspondant
	"""
	File_cache = open(name, "r")
	print("Recuperation des donnees en cache. ")
	data = File_cache.read()
	File_cache.close()
	return data 

def forbid(name):
	"""
	Verifie si le site web est autorise ou non.
	renvoie True si il est interdit,
	sinon renvoie false
	"""
	for element in range(len(forbidden)):
		if forbidden[element] == name : 
			return True
	
	return False 

def log_client(request,address):
	"""
	archive des requetes get des clients, ainsi que leurs adresse ip et numero de port   
	"""
	File_client = open("log_client", "a")
	sentence = "GET / HTTP/1.1 " + str(request) + " by adress : " + str( address ) + " and time "+ time.ctime()  +" \n "
	File_client.write(sentence)
	File_client.close()
	
	
def log_server(respond):
	"""
	Archive des reponses get du serveur
	"""
	File_server = open("log_server", "a")
	File_server.write(respond)
	File_server.close()

	
serverPort = 1234
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen()
historique = []
forbidden = ["www.youtube.com","www.youporn.com"]

print("Proxy web en marche")
print("Etat du cache a l' instant initial. ", historique)


def proxy():

	while True:
		print("historique : " , historique)	
		connectionSocket, address = serverSocket.accept()
		web_site = connectionSocket.recv(2048)
		print("web_site du client vers le proxy : ", web_site)
		
		# archive de la requete client
		log_client(web_site.decode('utf-8'),address)
		
		# verification pour site non interdits
		pegit = forbid(web_site.decode('utf-8'))
		print("pegit : " , pegit)
		
		if pegit :
			print("Le site est inaproprie, vous allez etre diriges vers une fenetre interdit")
			request = "GET / HTTP/1.1 403 Forbidden"
			print("envoie des donnees")
			connectionSocket.send(request.encode('utf-8'))
			print("fermeture de la socket client. ")
			proxy()		
		
		cache = website_in(web_site)
		print("valeur du cache : ", cache)
		
		"""
		On verifie si le site web est connu du cache.
		La fonction website_in renvoie la position du cache dans la liste historique
		Sinon, renvoie -1  
		"""
		
		if cache == None or cache == -1:
			historique.append(web_site)
			print("Mise en memoire des informations sur la requete. ")
			print("Voici l'etat du cache : ", historique)	
			
		else :
			"""
			il faut chercher la requete depuis le fichier cache
			"""
			
			print("Lecture de la cache.")
			data = in_cache(web_site)
			print("envoie des donnees depuis le cache correspondant")
			connectionSocket.send(data.encode('utf-8'))
			
			# le log_server continu a archiver les reponses, meme si elles sont comprises dans le cache
			log_server(data)
			
			print("fermeture de la socket client. ")
			proxy()
		
		# sinon on continue tout : la requete n'est pas dans le cache --> nouvelle requete
		print("Changement du numero de port pour ouvrir la connection vers le serveur en tant que client-proxy)")
		serverName = 'localhost'
		serverPort = 56789
		proxySocket = socket(AF_INET,SOCK_STREAM)
		proxySocket.connect((serverName,serverPort))
		print("tcp handshake : proxy-client vers serveur")	
		proxySocket.send(web_site)
		print("envoie des donnees de proxy-client au serveur ")
		modifiedweb_site = proxySocket.recv(2048)
		print("reception des donnees du serveur")
		
		# mise a jour du cache, apres reception des donnees
		create_cache(web_site,modifiedweb_site)
		# mise a jour du log_server 
		log_server(modifiedweb_site.decode('utf-8'))
		
		connectionSocket.send(modifiedweb_site)
		print("envoie des donnees du proxy-server au client")
		print("fermeture de la connection client au proxy-server")
		connectionSocket.close()
	

proxy()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
