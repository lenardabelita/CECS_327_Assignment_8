import socket

# Define server details
HOST = 'localhost'
PORT = 9090

def main():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}\n")
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return

    while True:
        # Display menu options to the user
        print("Select a query:")
        print("1: Average moisture inside the fridge in the last 3 hours")
        print("2: Average water consumption per dishwasher cycle")
        print("3: Device with the highest electricity consumption")
        print("Type 'exit' to close the client\n")

        query = input("Enter your choice (1, 2, 3, or exit): ")

        # Exit the client
        if query.lower() == "exit":
            print("Closing the client.")
            client_socket.send(query.encode())
            break

        # Validate user input
        if query not in ["1", "2", "3"]:
            print("Invalid input. Please enter 1, 2, 3, or exit.")
            continue

        try:
            # Send query to server
            client_socket.send(query.encode())

            # Receive and display the server's response
            response = client_socket.recv(1024).decode()
            print(f"Response from server: {response}\n")
        except Exception as e:
            print(f"Error during communication: {e}")
            break

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    main()
