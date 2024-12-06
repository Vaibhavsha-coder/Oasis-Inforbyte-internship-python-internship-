import socket
import threading
import sys

class ChatServer:
    def __init__(self, host='127.0.0.1', port=55555):
        """
        Initialize the chat server with a host and port.
        
        :param host: Server IP address (default is localhost)
        :param port: Port number to listen on (default 55555)
        """
        self.host = host
        self.port = port
        
        # Store connected clients
        self.clients = []
        
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to a specific address and port
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)  # Allow up to 5 queued connections
            print(f"[*] Server listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"[!] Error binding to {self.host}:{self.port}: {e}")
            sys.exit(1)
    
    def handle_client(self, client_socket, client_address):
        """
        Handle communication with an individual client.
        
        :param client_socket: Socket object for the connected client
        :param client_address: Address of the connected client
        """
        try:
            # Send a welcome message
            client_socket.send("Welcome to the Chat Server!".encode('utf-8'))
            
            while True:
                # Receive message from client
                message = client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                # Broadcast message to all other clients
                print(f"[*] Received from {client_address}: {message}")
                self.broadcast(message, client_socket)
        
        except Exception as e:
            print(f"[!] Error handling client {client_address}: {e}")
        
        finally:
            # Remove client from list and close connection
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
    
    def broadcast(self, message, sender_socket):
        """
        Send a message to all connected clients except the sender.
        
        :param message: Message to broadcast
        :param sender_socket: Socket of the client sending the message
        """
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    # Remove client if unable to send
                    self.clients.remove(client)
    
    def start(self):
        """
        Start the server and accept incoming client connections.
        """
        try:
            while True:
                # Wait for a client connection
                client_socket, client_address = self.server_socket.accept()
                print(f"[*] Accepted connection from {client_address}")
                
                # Add client to list of connected clients
                self.clients.append(client_socket)
                
                # Start a thread to handle this client
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, client_address)
                )
                client_thread.start()
        
        except KeyboardInterrupt:
            print("\n[*] Server shutting down...")
        
        finally:
            # Close all client connections
            for client in self.clients:
                client.close()
            
            # Close the server socket
            self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
