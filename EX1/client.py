import socket

server = ''
port = 1234
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server,port))

def send(msg) :
    message = msg.encode('utf-8')
    client.send(message)

    print(client.recv(2048).decode('utf-8'))

while True:
    send(input("something to say :"))