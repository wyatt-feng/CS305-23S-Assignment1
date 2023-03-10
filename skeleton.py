'''
Example:
    1. Finish the server, and run it in an arbitrary directory.
    ```sh
    sudo python server.py
    ```

    2. In another directory, download any file in the folder.
    ```sh
    ftp -Aa 127.0.0.1:server.py
    ```
    In this example we download the script itself.

Remember to rename it.
'''
import socket

# Listening on port 21
s = socket.socket()
s.bind(("0.0.0.0", 21))
s.listen(5)

while True:
    client, addr = s.accept()

    # Send welcome message
    client.send(b"220 Welcome to CS305 Demo - SID\r\n")

    line = client.recv(1024).decode('ascii').strip()
    while line != "QUIT":
        if line[:4] == "USER":

            # Send welcome message
            pass

        elif line[:4] == "PORT":

            # Parse the data coonection ip and port
            pass

        elif line[:4] == "EPRT":

            # Same as PORT
            pass

        elif line[:4] == "STOR":

            # Establish data connection
            pass

        elif line[:4] == "RETR":

            # Same as STOR
            pass

        elif line[:4] == "SIZE":

            pass

        else:

            pass

        line = client.recv(1024).decode('ascii').strip()

    client.close()
