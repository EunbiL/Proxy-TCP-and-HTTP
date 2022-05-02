from socket import *
serverPort = 56789
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen()
print('Serveur en marche')

while True:
	connectionproxy, address = serverSocket.accept()
	print("Une nouvelle requete http pour le server. ")
	print("Tcp handshake : du proxy-client vers le serveur.")
	web_site = connectionproxy.recv(2048)
	print("Reception des donnees du proxy-client vers le serveur.")
	
	web_host = web_site.decode('utf-8')
	web_port = 80  # port number service www 80/tcp
	server_tcp = socket(AF_INET,SOCK_STREAM)  
	server_tcp.connect((web_host,web_port)) 
	
	request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % web_host
	
	server_tcp.send(request.encode('utf-8'))  
	page = server_tcp.recv(2048)  
	print("Reponse de la requete web : " , page)
	print("Envoie de la reponse du serveur au proxy-client.")
	connectionproxy.send(page)
	print("Fermeture de la connection du proxy-client au serveur.")
	connectionproxy.close()
	
