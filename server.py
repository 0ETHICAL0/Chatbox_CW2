import socket
import threading
import base64

# Server Configuration
PORT = 1234
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

class ChatServer:
    """
    Represents a chat server handling multiple clients using multithreading.
    Demonstrates Encapsulation by keeping connection details private.
    """
    def _init_(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDRESS)
        self.server.listen()
        self.clients = {}
        print("Server is running...")
    
    def start(self):
        """Starts the server and listens for incoming connections."""
        while True:
            client, addr = self.server.accept()
            threading.Thread(target=self._handle_client, args=(client,)).start()
    
    def _handle_client(self, client):
        """Encapsulated method to handle an individual client."""
        try:
            username = base64.b64decode(client.recv(1024)).decode(FORMAT)
            self.clients[client] = username
            print(f"{username} joined the chat.")
            self.broadcast(f"{username} joined the chat!", client)
            
            while True:
                message = client.recv(1024).decode(FORMAT)
                if not message:
                    break
                decoded_msg = base64.b64decode(message).decode(FORMAT)
                self.broadcast(decoded_msg, client)
        except Exception as e:
            print(f"Client Error: {e}")
        finally:
            self.remove_client(client)
    
    def broadcast(self, message, sender_client):
        """Polymorphic method to send messages to all connected clients."""
        encoded_msg = base64.b64encode(message.encode(FORMAT)).decode(FORMAT)
        for client in self.clients:
            if client != sender_client:
                try:
                    client.send(encoded_msg.encode(FORMAT))
                except Exception as e:
                    print(f"Broadcast Error: {e}")
                    self.remove_client(client)
    
    def remove_client(self, client):
        """Encapsulated method to remove a client from the chat."""
        if client in self.clients:
            username = self.clients[client]
            del self.clients[client]
            print(f"{username} left the chat.")
            self.broadcast(f"{username} left the chat.", client)
            client.close()

if _name_ == "_main_":
    server = ChatServer()
    server.start()