import socket

HOST = '127.0.0.1'
PORT = 8082

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server.")
        while True:
            print("\nMenu:")
            print("1. Change case of string")
            print("2. Evaluate mathematical expression")
            print("3. Reverse string")
            print("4. Exit")
            choice = input("Enter choice: ").strip()
            if choice == '4':
                break
            if choice not in ('1', '2', '3'):
                print("Invalid choice. Try again.")
                continue
            data = input("Enter input: ").strip()
            message = f"{choice}:{data}"
            s.send(message.encode())
            response = s.recv(1024).decode()
            print("Result:", response)
        print("Exiting.")

if __name__ == "__main__":
    main()
