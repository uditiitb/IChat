import threading
import socket

HOST = 'localhost'
PORT = 10000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message.encode('ascii'))

def broadcast_2(message,client):
    for c in clients:
        if(c!=client):
            c.send(message.encode('ascii'))
    

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast_2(message,client)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!')
            nicknames.remove(nickname)
            client.close()
            break

def recieve():
    while True:
        client,address = server.accept()
        print(f'Connected with str{address}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client) 

        print(f'Nickname of client is: {nickname}')
        broadcast(f'{nickname} joined the chat!')
        client.send('Connected to Server!'.encode('ascii'))

        thread = threading.Thread(target = handle,args= ((client,)))
        thread.start()

print('server is listening!')
recieve()
