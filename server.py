import socket

def main():
    #Get user input, IP and server_port
    server_host = input("Enter the server IP address: ")
    server_port = int(input("Enter the server serverport number: "))

    #Creating socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        #Bind Socket to server host and server port
        server_socket.bind((server_host, server_port))
        #Listen for any incoming connection
        server_socket.listen(1)
        print("Server is listening on", (server_host, server_port))
        #Accept the connection that is made
        client_connection, client_addr = server_socket.accept()
        with client_connection:
            print('Connected by', client_addr)
            while True:
                #Get Data
                data = client_connection.recv(1024)
                if not data:
                    break
                print("Received message:", data.decode())
                #Translate data to uppercase
                reply = data.decode().upper()
                #Send data back
                client_connection.sendall(reply.encode())

if __name__ == "__main__":
    main()
