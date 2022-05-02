from socket import *
serverName = 'localhost'
serverPort = 1234
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print("Renter un site web en respectant la forme de l'exemple")
web_site = input('web site (ex : www.google.fr ; www.youtube.com ; www-npa.lip6.fr) : ')
print("this is my web site : ", web_site)
clientSocket.send(web_site.encode('utf-8'))
print("sending web_site to proxy-server")
modifiedweb_site = clientSocket.recv(2048)
print("web_site receving from proxy-server")
print("web_site : ",modifiedweb_site.decode('utf-8'))
clientSocket.close()
