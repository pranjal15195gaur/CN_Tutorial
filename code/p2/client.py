import socket
import argparse

HOST = '127.0.0.1'
PORT = 8082

def main():
    message = "hello world" # default client message for benchmarking 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server.")
        s.sendall(message.encode())
        print(f"Sent: {message}")
        data = s.recv(1024)
    
    print(f"Received: {data.decode()}")

if __name__ == "__main__":
    main()
