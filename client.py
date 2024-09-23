import threading
import socket

# Host and port
HOST = 'localhost'
PORT = 10000

nickname = input('Choose a nickname: ')

# Create a socket object
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))

# function to receive messages from server
def send_nickname(nickname):
    client.send('NICK'.encode())
    client.send(f'{nickname}'.encode())

# function to send messages to server
def write():
    while True:
        try:
            message = f'{nickname}: {input("")}'
            client.send(message.encode('ascii'))
        except:
            break


# function to read messages
def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('Error occurred')
            client.close()
            break
            

thread_recieve = threading.Thread(target=recieve)
thread_recieve.start()
thread_write = threading.Thread(target=write)
thread_write.start()




            



