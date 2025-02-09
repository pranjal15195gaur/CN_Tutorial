import socket
import os
import signal
import threading
import sys

HOST = '127.0.0.1'
PORT = 8082

def handle_client(conn):
    
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        parts = data.split(':', 1)
        if len(parts) < 2:
            response = "Invalid request format"
            conn.send(response.encode())
            continue
        task, input_data = parts
        if task == '1':
            result = input_data.swapcase()
        elif task == '2':
            try:
                result = str(eval(input_data))
            except Exception as e:
                result = f"Error: {e}"
        elif task == '3':
            result = input_data[::-1]
        else:
            result = "Invalid task"
        conn.send(result.encode())
    conn.close()
    print("Client disconnected")

def single_process_server():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Single-process server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Accepted connection from {addr}")
            handle_client(conn)

def multi_process_server():
    
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Multi-process server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Accepted connection from {addr}")
            pid = os.fork()
            if pid == 0:
                s.close()
                handle_client(conn)
                os._exit(0)
            else:
                conn.close()

def multi_threaded_server():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Multi-threaded server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Accepted connection from {addr}")
            thread = threading.Thread(target=handle_client, args=(conn,))
            thread.start()

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <server_type>")
        sys.exit(1)
    server_type = sys.argv[1]
    if server_type == "single":
        single_process_server()
    elif server_type == "multi-process":
        multi_process_server()
    elif server_type == "multi-thread":
        multi_threaded_server()
    else:
        print("Invalid server type. Use 'single', 'multi-process', or 'multi-thread'")
        
if __name__ == "__main__":
    main()
