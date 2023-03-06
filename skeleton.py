'''
This is a 59-score demo FTP server. It can only upload files
to clients and only supports standard mode. If it can successfull
handle STOR command, it can score 60. If it can handle designated
exceptions, it may score 90. Bonus points including user access
control, PASV mode, ASCII mode, and more commands.

List of supported commands:
    - USER (Annonymous login only)
    - PORT
    - EPRT
    - STOR (Not tested)
    - RETR
    - SIZE
    - QUIT

Example:
    1. Run this demo in an arbitrary directory.
    ```sh
    sudo python ftp_srv.py
    ```

    2. In another directory, download any file in the folder.
    ```sh
    ftp -Aa 127.0.0.1:ftp_srv.py
    ```
    In this example we download the script itself.
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
