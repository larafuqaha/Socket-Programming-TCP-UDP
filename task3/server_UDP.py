# Lara Foqaha 1220071 / Fadi Bassous 1221005 / Veronica Wakileh 1220245
import socket
import random
import time


SERVER_IP = socket.gethostbyname(socket.gethostname()) 
PORT = 5689
BUFFER_SIZE = 5000
ROUND_TIME = 30
QUESTION_TIME = 30


QUESTIONS_DB = [
    ("What is the capital of Palestine?", "Jerusalem"),
    ("What is 5 multiplied by 6?", "30"),
    ("What is the largest planet in our solar system?", "Jupiter"),
    ("What is the square root of 64?", "8"),
    ("10 + 10 = ?", "20"),
    ("What is the chemical symbol for water?", "H2O"),
    ("What is the longest river in the world?", "Nile")
]

active_clients = [] # tracking active clients
scores = {}  # tracking clients scores
answered_clients = {}  # tracking answered clients
client_usernames = {}  # saving clients usernames


def handle_client(data, client_address, server_socket):
    active_clients.append(client_address)
    username = data.decode() 
    scores[client_address] = 0
    client_usernames[client_address] = username 
    answered_clients[client_address] = False  
    print(f"{username} joined the game from ({client_address})")
    broadcast_message(f"{username} joined the game!", server_socket)
    broadcast_message(f"Current number of players: {len(active_clients)}\n", server_socket)

def broadcast_message(message, server_socket):
    for client in active_clients:
        server_socket.sendto(message.encode(), client)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, PORT))

    print(f"Trivia game server started. Listening on IP: {SERVER_IP}, Port: {PORT}")

    # Wait for at least 2 players to join
    while len(active_clients) < 2:
        print("Waiting for at least two players to join the game...")
        try:
            server_socket.settimeout(3)
            data, client_address = server_socket.recvfrom(BUFFER_SIZE)
            if client_address not in active_clients:
                handle_client(data, client_address, server_socket)
        except socket.timeout:
            continue
        time.sleep(1)

    if len(active_clients) > 1:
        print(f"\nStarting the game round in {QUESTION_TIME} seconds!\n")
        broadcast_message(f"Starting the game round in {QUESTION_TIME} seconds. Get ready!\n", server_socket)

    start_time = time.time()
    while time.time() - start_time < QUESTION_TIME:
        try:
            server_socket.settimeout(1)
            data, client_address = server_socket.recvfrom(BUFFER_SIZE)
            if client_address not in active_clients:
                handle_client(data, client_address, server_socket)
        except socket.timeout:
            continue

    while True:
        selected_questions = random.sample(QUESTIONS_DB, 3) # choosing 3 unique random questions 
        counter = 1 # keeping track of the number of clients
        inactive_clients = set() # keeping track of clients who didn't answer any question in the round

        for question, correct_answer in selected_questions: 
            if len(active_clients) < 2:  # checking player count before starting the question
                print("Not enough players to continue the game.")
                broadcast_message("Not enough players to continue the game.",server_socket)
                break

            broadcast_message(f"Question {counter}: {question}", server_socket)
            print(f"Question {counter}: {question}")

            # Reset answered_clients at the start of each round
            for client in answered_clients:
                answered_clients[client] = False

            start_time = time.time()
            while time.time() - start_time < ROUND_TIME:  # Allow up to specified seconds for answers
                try:
                    server_socket.settimeout(1)
                    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
                    if (client_address in active_clients) & (answered_clients[client_address] == False):
                        answer = data.decode()
                        username = client_usernames[client_address]
                        if answer.lower() == "exit": #if the client exited
                            broadcast_message(f"{username} exited the game.\n",server_socket)
                            active_clients.remove(client_address)
                            break
                        elif answer.lower() == correct_answer.lower(): # if the client answered correctly
                            response_time = time.time() - start_time
                            points = max(1, int(ROUND_TIME - response_time))  # more points for quicker responses
                            scores[client_address] += points
                            print(f"Received answer from {username} ({client_address}): {answer.lower()} - Correct!\n")
                        else:
                            print(f"Received answer from {username} ({client_address}): {answer.lower()} - Wrong!\n")
                        answered_clients[client_address] = True
                except socket.timeout:
                    continue

            # handling players who didn't answer in time
            for client_address, answered in answered_clients.items():
                if not answered:
                    username = client_usernames[client_address]
                    print(f"{username} ({client_address}) did not answer in time. - Wronge!\n")
                    inactive_clients.add(client_address)

            # Broadcast the correct answer after each question
            broadcast_message(f"\nTime is up! The correct answer was: {correct_answer}\n", server_socket)
            print("\nTime is up!\n")
            # Broadcast the leaderboard after each question
            leaderboard = "Current Scores:\n"
            for client_address in active_clients:  # Iterate over active clients
                username = client_usernames[client_address]  # Get username or fallback to "Unknown"
                score = scores[client_address]  # Get score or fallback to 0
                leaderboard += f"{username}: {score} points\n"

            broadcast_message(leaderboard, server_socket)
            counter = counter + 1

        for client_address in inactive_clients:
            if client_address in active_clients:
                username = client_usernames[client_address]
                print(f"{username} ({client_address}) is inactive and will be removed from the game.")
                broadcast_message(f"{username} has been removed from the game due to inactivity.", server_socket)
                active_clients.remove(client_address)

        print("\nGame over!")
        broadcast_message("\nGame over!\n", server_socket)
        if active_clients:
            max_score = max(scores.values())
            winners = []  # empty list to store the winners
            for client, score in scores.items():
                if score == max_score:  # if the client's score matches the maximum score
                    winners.append(client_usernames[client])  # add the username to the winners list
            if len(winners) == 1:
                winner_message = f"\nThe winner of this round is {winners[0]} with {max_score} points!\n"
            else:
                winner_message = f"\nThe winners of this round are: {', '.join(winners)} with {max_score} points each!\n"
        else:
            print("No active players remaining. Ending game.")
            broadcast_message("No active players remaining. Ending game.", server_socket)
            break

        broadcast_message(winner_message, server_socket)
        # sleep before starting the next round
        broadcast_message(f"Starting the game round {ROUND_TIME} in seconds. Get ready!",server_socket)
        time.sleep(ROUND_TIME)
        

if __name__ == "__main__":
    start_server()
