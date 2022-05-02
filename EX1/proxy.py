import socket
import threading

def handle_client_proxy(conn, addr) :
    while True :
        msg = conn.recv(2048)
        if msg.decode('utf-8') == "EXIT" :
            conn.close()
            return

        serverSocket.sendall(msg)
        modifiedMessage = serverSocket.recv(2048)
        conn.sendall(modifiedMessage)


serverName = 'localhost'
serverPort = 5678
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((serverName,serverPort))

proxyName = 'localhost'
proxyPort = 1234
proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxySocket.bind((proxyName,proxyPort))
proxySocket.listen()

print("proxy en marche")
while True:
    clientSocket, clientAddress = proxySocket.accept()
    thread = threading.Thread(target = handle_client_proxy, args = (clientSocket, clientAddress))
    thread.start()