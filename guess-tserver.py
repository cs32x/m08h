### m08/guess-tserver.py
import random
import threading
from socket32 import create_new_socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


def main():
    with create_new_socket() as s:
        # Bind socket to address and queue connection requests
        s.bind(HOST, PORT)
        s.listen()
        print("GUESS-THE-NUMBER server started. Listening on", (HOST, PORT))

        while True:
            # Answer incoming connection
            conn2client, addr = s.accept()
            threading.Thread(
                target=handle_client,
                args=(conn2client, addr),
            ).start()


def handle_client(conn2client, addr):
    print('Connected by', addr)

    with conn2client:
        # Create a secret for this connection
        secret = random.randint(1, 100)

        # Send and receive messages through the connection
        while True:   # message processing loop
            msg = conn2client.recv()
            if msg == '':
                break
            guess = int(msg)

            # Check guess against secret and respond
            if guess == secret:
                conn2client.sendall('Exactly! You win!')
            elif guess < secret:
                conn2client.sendall('Too small!')
            else:
                conn2client.sendall('Too big!')

    print('Disconnected', addr)


if __name__ == '__main__':
    main()
