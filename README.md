# CS305 2023 Spring Assignment 1 - FTP Server

---

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

TBD

## Environment Setup

Python 3, preferably 3.9+, running on Linux system or WSL. Windows and macOS **may** also works, although they are not tested. Theoretically speaking, any system that can run Python and support `ftp` command should be fine.

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
