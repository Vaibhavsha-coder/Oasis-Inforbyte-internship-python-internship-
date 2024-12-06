import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='127.0.0.1', port=55555):
        """
        Initialize the chat client.
        
        :param host: Server IP address to connect to
        :param port: Server port number
        """
        self.host = host
        self.port = port
        
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Connect to the server
            self.client_socket.connect((self.host, self.port))
            print(f"[*] Connected to {self.host}:{self.port}")
        except Exception as e:
            print(f"[!] Error connecting to server: {e}")
            sys.exit(1)
    
    def receive_messages(self):
        """
        Continuously receive and display messages from the server.
        """
        try:
            while True:
                # Receive message from server
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                print(f"\n{message}")
        
        except Exception as e:
            print(f"[!] Error receiving messages: {e}")
        
        finally:
            self.client_socket.close()
    
    def send_messages(self):
        """
        Allow user to send messages to the server.
        """
        try:
            # Get username
            username = input("Enter your username: ")
            
            while True:
                # Read user input
                message = input()
                
                # Prepend username to message
                full_message = f"{username}: {message}"
                
                # Send message to server
                self.client_socket.send(full_message.encode('utf-8'))
                
                # Exit if user types 'quit'
                if message.lower() == 'quit':
                    break
        
        except Exception as e:
            print(f"[!] Error sending messages: {e}")
        
        finally:
            self.client_socket.close()
    
    def start(self):
        """
        Start the client by creating threads for sending and receiving messages.
        """
        # Thread for receiving messages
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        
        # Send messages in main thread
        self.send_messages()

if __name__ == "__main__":
    client = ChatClient()
    client.start()
