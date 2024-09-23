import tkinter as tk
from tkinter import scrolledtext, simpledialog, ttk
import threading
import socket
from datetime import datetime

class WhatsAppStyleChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("IChat")
        master.geometry("400x600")
        master.configure(bg="#ECE5DD")

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TButton', background="#25D366", foreground="white", borderwidth=0, font=('Arial', 10, 'bold'))
        self.style.map('TButton', background=[('active', '#128C7E')])

        self.header_frame = tk.Frame(master, bg="#075E54", height=50)
        self.header_frame.pack(fill=tk.X)
        self.header_label = tk.Label(self.header_frame, text="WhatsApp Chat", fg="white", bg="#075E54", font=('Arial', 16, 'bold'))
        self.header_label.pack(pady=10)

        self.chat_frame = tk.Frame(master, bg="#ECE5DD")
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, state='disabled', bg="#ECE5DD", font=('Arial', 10))
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input_frame = tk.Frame(master, bg="#ECE5DD")
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.msg_entry = tk.Entry(self.input_frame, font=('Arial', 10), bg="white", relief=tk.FLAT)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.send_message, style='TButton', width=10)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

        self.connect_button = ttk.Button(master, text="Connect", command=self.connect_to_server, style='TButton')
        self.connect_button.pack(pady=10)

        self.client = None
        self.nickname = None
        self.connected = False

    def connect_to_server(self):
        if not self.connected:
            self.nickname = simpledialog.askstring("Nickname", "Choose a nickname:", parent=self.master)
            if not self.nickname:
                return

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client.connect(('localhost', 10000))
                self.connected = True
                self.connect_button.config(text="Disconnect")
                
                threading.Thread(target=self.receive_messages, daemon=True).start()
            except Exception as e:
                self.update_chat(f"Connection failed: {str(e)}")
        else:
            self.disconnect_from_server()

    def disconnect_from_server(self):
        if self.connected:
            self.client.close()
            self.connected = False
            self.connect_button.config(text="Connect")
            self.update_chat("Disconnected from server")

    def send_message(self, event=None):
        if self.connected and self.msg_entry.get():
            message = self.msg_entry.get()
            formatted_message = f"{self.nickname}: {message}"
            self.client.send(formatted_message.encode('ascii'))
            self.msg_entry.delete(0, tk.END)
            self.update_chat(formatted_message, is_self=True)

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    self.update_chat(message)
            except:
                self.update_chat('Disconnected from server')
                self.disconnect_from_server()
                break

    def update_chat(self, message, is_self=False):
        self.chat_display.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M")
        
        if is_self:
            self.chat_display.insert(tk.END, f"\n{message}\n", "right")
            self.chat_display.insert(tk.END, f"{timestamp}\n", "right_time")
        else:
            self.chat_display.insert(tk.END, f"\n{message}\n", "left")
            self.chat_display.insert(tk.END, f"{timestamp}\n", "left_time")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
        self.chat_display.tag_configure("right", justify="right", background="#DCF8C6", lmargin1=50, rmargin=10)
        self.chat_display.tag_configure("left", justify="left", background="white", lmargin1=10, rmargin=50)
        self.chat_display.tag_configure("right_time", justify="right", foreground="gray", font=('Arial', 8))
        self.chat_display.tag_configure("left_time", justify="left", foreground="gray", font=('Arial', 8))

if __name__ == "__main__":
    root = tk.Tk()
    chat_client = WhatsAppStyleChatGUI(root)
    root.mainloop()

