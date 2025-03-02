import socket
import threading
import base64
from tkinter import *
from tkinter import scrolledtext, simpledialog

# Client Configuration
PORT = 1234
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

class ChatClient:
    def __init__(self, username):
        self.username = username
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
    
    def connect_to_server(self):
        try:
            self.client.connect(ADDRESS)
            encoded_username = base64.b64encode(self.username.encode(FORMAT)).decode(FORMAT)
            self.client.send(encoded_username.encode(FORMAT))
        except Exception as e:
            print(f"Connection Error: {e}")
            exit()
    
    def send_message(self, message):
        try:
            encoded_msg = base64.b64encode(f"{self.username}: {message}".encode(FORMAT)).decode(FORMAT)
            self.client.send(encoded_msg.encode(FORMAT))
        except Exception as e:
            print(f"Send Error: {e}")
    
    def receive_messages(self, display_callback):
        while True:
            try:
                message = self.client.recv(1024).decode(FORMAT)
                decoded_msg = base64.b64decode(message).decode(FORMAT)
                display_callback(decoded_msg)
            except Exception as e:
                print(f"Receive Error: {e}")
                self.client.close()
                break

class ChatGUI:
    def __init__(self, client):
        self.client = client
        self.Window = Tk()
        self.Window.title(f"Chatroom - {self.client.username}")
        self.Window.geometry("500x600")
        self.Window.configure(bg="#1E1E1E")

        self.setup_ui()
        threading.Thread(target=self.client.receive_messages, args=(self.display_message,), daemon=True).start()
        self.Window.mainloop()

    def setup_ui(self):
        self.labelHead = Label(self.Window, text=f"Welcome, {self.client.username}!", fg="white", bg="#333", font=("Helvetica", 16, "bold"), pady=10)
        self.labelHead.pack(fill=X)
        
        self.textCons = scrolledtext.ScrolledText(self.Window, width=60, height=20, bg="#252525", fg="white", font=("Helvetica", 12))
        self.textCons.pack(padx=10, pady=5)
        self.textCons.config(state=DISABLED)
        
        self.bottomFrame = Frame(self.Window, bg="#333")
        self.bottomFrame.pack(fill=X, padx=10, pady=5)
        
        self.entryMsg = Entry(self.bottomFrame, bg="#2C3E50", fg="white", font=("Helvetica", 12))
        self.entryMsg.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        
        self.sendButton = Button(self.bottomFrame, text="Send", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=self.send_message)
        self.sendButton.pack(side=RIGHT, padx=5, pady=5)

    def send_message(self):
        msg = self.entryMsg.get()
        if msg:
            self.client.send_message(msg)
            self.display_message(f"You -> {msg}")
            self.entryMsg.delete(0, END)

    def display_message(self, message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, message + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

if __name__ == "__main__":
    username = simpledialog.askstring("Username", "Enter your name to join the chat:")
    if not username:
        exit()
    client = ChatClient(username)
    ChatGUI(client)
