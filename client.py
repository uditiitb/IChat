import threading
import socket

# st.title('IChat')
# Host and port
HOST = 'localhost'
PORT = 10000

# Create a socket object
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))

# function to send messages to server
def write():
    while True:
        try:
            message1 = '{} : {}'.format(nickname,message)
            client.send(message1.encode())
        except:
            break

# function to receive messages from server
def send_nickname(nickname):
    client.send('NICK'.encode())
    client.send(f'{nickname}'.encode())

# function to read messages
def recieve():
    while True:
        try:
            message = client.recv(1024).decode()
            return message
        except:
            break
            

thread_write = threading.Thread(target=write)
thread_recieve = threading.Thread(target=recieve)

# nickname = st.text_input("Enter your nickname: ")
# st.button(label='Send',key=1,on_click=send_nickname(nickname))

# message = st.text_input("Type your message here...")
# st.button(label='Send',key=2,on_click=thread_write.start())

# # txt = st.text_area('')
# txt=str(thread_recieve.start())

# st.write(txt)

# from flask import Flask, render_template, request
# from flask_socketio import SocketIO, send
# import threading
# import socket

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

# # Host and port
# HOST = 'localhost'
# PORT = 10000

# # Create a socket object
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((HOST, PORT))

# messages = []

# def receive_messages():
#     while True:
#         try:
#             message = client.recv(1024).decode()
#             socketio.emit('message', message)
#         except:
#             break

# receiving_thread = threading.Thread(target=receive_messages)
# receiving_thread.daemon = True
# receiving_thread.start()

# @app.route("/", methods=["GET", "POST"])
# def index():
#     return render_template("index.html")

# @socketio.on('send_nickname')
# def handle_nickname(nickname):
#     client.send('NICK'.encode())
#     client.send(nickname.encode())

# @socketio.on('send_message')
# def handle_message(message_data):
#     full_message = f'{message_data["nickname"]}: {message_data["message"]}'
#     client.send(full_message.encode())

# if __name__ == "__main__":
#     socketio.run(app, debug=True)


            



