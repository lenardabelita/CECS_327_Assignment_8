import socket

def get_server_info():
    while True:
        #Get user input, IP and Port
        server_ip = input("Enter the server IP address: ")
        server_port = input("Enter the server port number: ")

        if not server_port.isdigit():
            print("Port number should be a positive integer.")
            continue

        return server_ip, int(server_port)

def main():
    # Get server IP and port from user
    server_ip, server_port = get_server_info()

    while True:
        #Prompt user to enter a message to send to desired server
        message = input("Enter a message to send to the server (type 'quit' to exit): ")
        if message.lower() == 'quit':
            break

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                #Connect to server
                server_socket.connect((server_ip, server_port))
                #Send message to server
                server_socket.sendall(message.encode())

                #Receive the message from the server
                data = server_socket.recv(1024)
                print("Server reply:", data.decode())
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
