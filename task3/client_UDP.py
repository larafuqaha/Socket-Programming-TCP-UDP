# Lara Foqaha 1220071 / Fadi Bassous 1221005 / Veronica Wakileh 1220245
import socket

BUFFER_SIZE = 5000

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)  # Set a timeout to prevent blocking indefinitely

    while True:
        try:
            # Input server details and username
            server_ip = input("Enter the server IP address: ")
            server_port = int(input("Enter the server port number: "))
            username = input("Enter your username: ")

            # Send the username to the server to join the game
            client_socket.sendto(username.encode(), (server_ip, server_port))
            print(f"Connected to the trivia server at IP {server_ip}, port {server_port}!\nWaiting for the game to start...\n")
            break

        except Exception as e:
            print(f"Error: {e}. Try again, server not found.")

    try:
        while True:
            try:
                # Try to receive a message from the server
                data, _ = client_socket.recvfrom(BUFFER_SIZE)
                message = data.decode()
                print(message)

                # If the server sends a question, allow the client to answer
                if "Question" in message:
                    answer = input("Your answer (or type 'exit' to quit): ")
                    if answer.lower() == "exit":
                        print("Exiting the game...")
                        client_socket.sendto("exit".encode(), (server_ip, server_port))  # Notify the server about exiting
                        break

                    client_socket.sendto(answer.encode(), (server_ip, server_port))
            except socket.timeout:
                # Continue waiting for server messages if no data is received within the timeout
                continue
    except KeyboardInterrupt:
        print("\nDisconnected from server.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
