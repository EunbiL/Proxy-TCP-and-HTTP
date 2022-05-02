import socket

serverName = 'localhost'
serverPort = 5678
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverName,serverPort))
serverSocket.listen(10)
print("server ready")

proxySock, proxyAddr = serverSocket.accept()
print("tcp handshake with proxy")

while True :
    print("Waiting for the msg from proxy...")
    message = proxySock.recv(2048)
    print("Received message :", message.decode('utf-8'))
    modifiedMessage = message.upper()
    print("Sending response: ", modifiedMessage)
    proxySock.sendall(modifiedMessage)