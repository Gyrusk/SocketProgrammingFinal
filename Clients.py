import socket
import time
import random
import sys
import os

# Simple logging i implemented to keep track of timestamps in various messages
def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

# Server info for the client to connect to
SERVER = os.environ.get("SERVER_HOST", "localhost")
PORT = 5000

# Get client ID
client_id = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("CLIENT_ID", "1"))
log(f"Starting client {client_id}")

# Connection loop to keep trying to connect to server
while True:
    try:
        # Connect to server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER, PORT))
        log("Connected to server")
        
        # Handle initial greeting
        greeting = s.recv(1024).decode()
        if greeting == "HELLO":
            s.send(str(client_id).encode())
            log(f"Sent client ID: {client_id}")
        
        # Main loop
        while True:
            log("Waiting for server command")
            data = s.recv(1024).decode()
            log(f"Server sent: '{data}'")
            
            if not data:
                log("Server disconnected")
                break
                
            if data.startswith("SEND:"):
                word = data[5:]
                log(f"Server asked for word: '{word}'")
                
                # Simulate thinking
                time.sleep(random.uniform(1.0, 2.0))
                
                # Send response
                log(f"Sending response: '{word}'")
                s.send(word.encode())
                log("Waiting for server's response")
                
                # Get confirmation
                reply = s.recv(1024).decode()
                log(f"Server replied: '{reply}'")
                
                if reply == "GOOD":
                    log("Response was correct")
                else:
                    log("Response was incorrect")
                    
            elif data == "WAIT":
                log("Not my turn yet")
                time.sleep(1)  # Not our turn
            else:
                log(f"Unexpected server response: '{data}'")
                
    except Exception as e:
        log(f"Connection error: {str(e)}")
    
    # Reconnect delay
    time.sleep(random.randint(1, 3))
    log("Reconnecting...")
