import socket
import threading
import time
import os

# Simple logging i implemented to see the timestamps of the messages
def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

# hardcoding server values
server_ip = "0.0.0.0"
server_port = 5000
num = 1  # setting counter to 1 for tracking in server

if not os.path.exists("messages.txt"):
    open("messages.txt", "w").write("=== Message Log ===\n")

# Convert numbers to words, this well be used by the server to track the counter in integer and manage the number strings from client 
def num2word(n):
    words = {1:"one", 2:"two", 3:"three", 4:"four", 5:"five", 6:"six", 
             7:"seven", 8:"eight", 9:"nine", 10:"ten", 11:"eleven", 
             12:"twelve", 13:"thirteen", 14:"fourteen", 15:"fifteen"}
    return words.get(n, f"number_{n}")

# Handle the two clients
def client_thread(conn, addr):
    global num
    
    try:
        # Get client ID
        conn.send(b"HELLO")
        client_id = int(conn.recv(1024).decode().strip())
        log(f"Client {client_id} connected")
        
        # Main client loop
        while True:
            try:
                # Check if it's this client's turn
                my_turn = (client_id == 1 and num % 2 == 1) or (client_id == 2 and num % 2 == 0)
                    
                if my_turn:
                    # It's this client's turn
                    word = num2word(num)
                    log(f"Sending SEND:{word} to client {client_id}")
                    conn.send(f"SEND:{word}".encode())
                    log(f"Waiting for response from client {client_id}")
                    
                    # Get response with timeout
                    conn.settimeout(5)  # 5 second timeout
                    try:
                        response = conn.recv(1024).decode().strip()
                        log(f"Client {client_id} responded: {response}")
                        
                        if response == word:
                            # Log correct response
                            with open("messages.txt", "a") as f:
                                f.write(f"Client {client_id}: {response}\n")
                            
                            num += 1
                            
                            # Send GOOD - important to send as separate message
                            time.sleep(0.1)  # Small delay to separate messages
                            conn.send(b"GOOD")
                            log(f"Sent 'GOOD' to client {client_id}")
                        else:
                            conn.send(b"BAD")
                    except socket.timeout:
                        log(f"Timeout waiting for client {client_id}")
                        raise Exception("Client timeout")
                else:
                    # Not this client's turn
                    log(f"Not client {client_id}'s turn, sending WAIT")
                    conn.send(b"WAIT")
                    time.sleep(1)
            
            except Exception as e:
                log(f"Error in client {client_id} loop: {e}")
                raise  # Re-raise to exit the thread
    
    except Exception as e:
        log(f"Client disconnected: {e}")
    
    log(f"Client {client_id} thread ended")
    conn.close()

# Create server socket
log("Server starting")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((server_ip, server_port))
s.listen(5)
log(f"Server ready on port {server_port}")

# Accept connections
while True:
    try:
        client, address = s.accept()
        t = threading.Thread(target=client_thread, args=(client, address))
        t.daemon = True
        t.start()
    except KeyboardInterrupt:
        break

log("Server shutting down")
s.close()
