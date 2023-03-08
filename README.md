# CS305 2023 Spring Assignment 1 - FTP Server

## Introduction to the Assignment

Quote from Wikipedia:

> The **File Transfer Protocol (FTP)** is a standard communication protocol used for the transfer of computer files from a server to a client on a computer network. FTP is built on a C/S model architecture using **separate control and data connections** between the client and the server.

The goal of this assignment is to implement an **FTP Server** in Python. Minimally, it should be able to support file retrieving and storing. To achieve a satisfactory score, it should be capable of handling errors and avoiding crashes. After finishing this assignment, you will be able to conveniently share files with your friends and between your devices in a geeky, nostalgic, and interesting way.

Unfortunately, FTP is a highly developed protocol, so there is not much information or blog posts about the details. We try to include everything you need in this document, but if there is anything we ignore, feel free to reach out to your SA. Because SA may not be available promptly upon asking, you can alternatively read the following document and figure it out for your own sake:

- Wikipedia:
  - [File Transfer Protocol](https://en.wikipedia.org/wiki/File_Transfer_Protocol)
  - [List of FTP commands](https://en.wikipedia.org/wiki/List_of_FTP_commands)
  - [List of FTP server return codes](https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes)
- [RFC 959](https://datatracker.ietf.org/doc/html/rfc959): Definition of FTP
- [RFC 2428](https://datatracker.ietf.org/doc/html/rfc2428): Definition of EPRT and EPSV commands
- [RFC 5797](https://datatracker.ietf.org/doc/html/rfc5797): List of all FTP commands

In case you know nothing about RFC, A **Request for Commands**(RFC) is a publication in a series from IETF who is in charge of setting the standards. Basically all internet standards are defined in RFCs. Unluckily, they are also known to be notoriously incomprehensible. If you need extra help reading them, refer to [this](https://www.mnot.net/blog/2018/07/31/read_rfc).

Don't be frightened - you only need ~3 hours to score 60, and another ~2 hours can help you score 90. Seems pretty easy to finish in 2 weeks, right?

## Introduction to FTP

FTP protocol uses TCP(you can use socket in python) link for file transmission. There are two modes for FTP: standard mode and passive mode. In standard mode, before transmitting the files, the client will send the server the address and the port number of the client, and then the server will connect the designated address. In passive mode, the server will open a port and send the port number to the client, and after that, the server will wait for the client to connect it. For this assignment, you only need to implement standard mode.

FTP uses those following command to control its status:

| Command | Description                                                                | Usage                          |
| ------- | -------------------------------------------------------------------------- | ------------------------------ |
| USER    | Authentication username.                                                   | USER username                  |
| PORT    | Specifies an address and port to which the server should connect.          | PORT xxx,xxx,xxx,xxx,yyy,yyy   |
| EPRT    | Specifies an extended address and port to which the server should connect. | EPRT\|xxx.xxx.xxx.xxx\|yyyyy\| |
| QUIT    | Disconnect.                                                                | QUIT                           |
| STOR    | Accept the data and to store the data as a file at the server site.        | STOR filename                  |
| RETR    | Retrieve a copy of the file.                                               | RETR filename                  |
| SYST    | Return system type.                                                        | SYST                           |
| SIZE    | Return the size of a file.                                                 | SIZE filename                  |

In the above table, xxx represents a segment of IP address, and yyy represents the port number. For example, if the server IP is 127.0.0.1, and the port number for the data connection is 34567, then the PORT and the EPRT command sent by the client should be

```
PORT 127,0,0,1,135,7
EPRT |127.0.0.1|34567|
```

Note the port number in the PORT command. It calculated like this: $135 \times 256+7=34567$(256 is a constant). In one connection, either PORT or EPRT will be sent by the client; usually, EPRT is the preferred, and if it not supported, PORT will be used.

Each command should be ended with `\r\n`, not `\r` or `\n`. Otherwise, the command will be considered incomplete.

In response to the commands, the server will respond a 3-digit status code, followed by a sentence explaining the status code. For the meaning and common usage, you can refer to [this](https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes). The same as commands, each response must be ended with `\r\n`.

Here are some common responses:

- 220 CS305 FTP server ready. (Welcome message. You can modify the name of the server name.)
- 331 Username ok, send password. (Optional)
- 230 Login successful.
- 200 Type set to: Binary.
- 213 xxxx (xxxx represents the size of the file)
- 200 Active data connection established.
- 125 Data connection already open. Transfer starting.
- 226 Transfer complete.
- 221 Goodbye.
- 504 Command not implemented for that parameter.
- 502 Command not implemented.
- 421 Service not available, closing control connection.
- 425 Can't open data connection.
- 426 Connection closed; transfer aborted.
- 430 Invalid username or password.
- 530 Not logged in.
- 534 Request denied for policy reasons.

Basically, the code is for the server, and the sentence is for the user. So you can customize the messages, as long as the code is correct. These are not compulsory, i.e. you do not need to implement all of them.

To give you an overview of a complete connection, here is a screenshot of packets:

![](ftp_packets.png)

In this screenshot, the commands are the ones after "Request: ", and the responses are after "Response: ". CRLF(`\r\n`) is ignored in the screenshot but you should **not** forget it. The grey items are TCP connections for data transfer.

## Environment Setup

Python 3, preferably 3.9+, running on Linux system or WSL. Windows and macOS **may** also works, although they are not tested. Theoretically speaking, any system that can run Python and support `ftp` command should be fine.

## Hand-by-hand Tutorial

To implement the FTP server protocol, you need to handle various client commands. As an example, let's consider the `USER` command. In this example, we will assume that the client is in anonymous mode, i.e., the client does not have to provide any user identification information to the server.

When the server receives the `USER` command from the client, it should record the information of the client and send a message back to inform the client that it has been logged on. You can use the `client.send()` method to send a message to the client through the control connection socket that has already been established.

Here's an example code block that implements this behavior:

```python
if line[:4] == "USER":

    message = "203 Logged on.\r\n"
    client.send(message.encode())

```

Note that the message needs to be encoded as bytes before sending, as data transmission is implemented in binary. Also, make sure to include the \r\n characters at the end of the message to indicate the end of the message or command. Keep in mind that this is a simple example and you may need to modify this code block to match your specific needs. Additionally, it's important to note that re-establishing a socket to the same client with the same port will result in an error, so be careful not to do this.

Another example is give in this part:

```python
 elif line[:4] == "STOR":

            # Establish data connection
            data_sock = socket.socket()
            data_sock.connect((client_ip, client_port))
            client.send(b"125 Data connection already open. Transfer starting.\r\n")

            filename = line[5:]
            with open(filename, 'wb') as f:
                data = data_sock.recv(1024)
                f.write(data)
            client.send(b"226 Transfer complete.\r\n")
            data_sock.close()

```

In this part you will handle command for `STOR`. This example is the utmost simple one. In this example, the server should first establish a socket to handle data transmission connection, using recorded client info. With `with` block you can handle file IO easily. Do not forget to close the socket after finishing transfer. This example is just a simple example, and *IS NOT* expected to work correctly. You HAVE TO implement this case by your own needs.

## Tasks (100 pts max)

In the following tasks you can **ONLY** use the python standard library, **excluding** the `ftplib` module. Failure to comply to the rule will lead to 0 score for this assignment, and the result cannot be appealed.

### Task 1: Implement basic file transferring (60 pts)

TBD

### Task 2: Error handling (30 pts)

TBD

### Bonus Task (20 pts)

TBD

## Grading

### What to submit

You should turn in a **zip** file *and* a **pdf** file. The zip file should include all of your code, and the pdf file should include the screenshots of each task and some brief explanations. If there are any bonus points implemented, their functionality should be included in the pdf file, **otherwise they will not be considered!**

### Environment

Your script will be running on Python 3.10 running on Ubuntu 22.10.

### Criteria

TBD
