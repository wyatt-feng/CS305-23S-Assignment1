# This is the source code of the testing script. My apology if the code stinks... The functions are unordered because it will make later obfuscation more effective.
from ftplib import FTP
from ftplib import (error_reply, error_temp, error_perm, error_proto)
from hashlib import sha3_256
from io import BytesIO
import re
import socket
import struct
import threading
import uuid


class DataConn(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        ds = socket.socket()
        ds.bind((self.ip, self.port))
        ds.listen(1)
        clientsocket, _ = ds.accept()
        clientsocket.recv(1)
        clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
        clientsocket.close()


class FtpTest:
    def __init__(self) -> None:
        self.hash = sha3_256
        self.addr = '127.0.0.1'
        self.port = 52305
        self.score = 0
        self.sid = ''
        self.h = 'cs305hashing'

    def t11(self):
        ftp = FTP()
        ftp.set_pasv(False)
        try:
            ftp.connect(self.addr, self.port)
            welcome = re.search(r'\d{8}', ftp.getwelcome())
            ftp.quit()
            if welcome != None:
                self.sid = welcome.group(0)
            else:
                return False
            self.score += 10
            return True
        except:
            return False

    def t13(self):
        result = False
        ftp = FTP()
        ftp.set_pasv(False)
        filename = str(uuid.uuid1())
        content = uuid.uuid1().bytes
        try:
            ftp.connect(self.addr, self.port)
            ftp.login()
            with BytesIO(content) as file:
                ftp.storbinary('STOR '+filename, file)
                self.score += 20
            with BytesIO() as file:
                ftp.retrbinary('RETR '+filename, file.write)
                if file.getvalue() == content:
                    self.score += 20
                    result = True
            ftp.quit()
            return result
        except (error_reply, error_temp, error_perm, error_proto):
            ftp.quit()
            return False
        except:
            return False

    def t12(self):
        ftp = FTP()
        ftp.set_pasv(False)
        try:
            ftp.connect(self.addr, self.port)
            ftp.login()
            ftp.quit()
            self.score += 10
            return True
        except:
            return False

    def t22(self):
        result0, result1 = False, False
        ftp = FTP()
        ftp.set_pasv(False)
        try:
            ftp.connect(self.addr, self.port)
            ftp.retrbinary("RETR server.py", print)
        except (error_reply, error_temp, error_perm, error_proto) as err:
            if str(err)[:3] == '530':
                result0 = True
        except:
            return False
        try:
            ftp.sendcmd("USER")
        except (error_reply, error_temp, error_perm, error_proto):
            result1 = True
        except:
            return False

        if result0 and result1:
            self.score += 10
        ftp.quit()
        return result0 and result1

    def token(self):
        digest = self.hash()
        msg = self.h + self.sid + str(self.score)
        digest.update(msg.encode('ascii'))
        return digest.hexdigest()[:6]

    def t23(self):
        result0, result1 = False, False
        ftp = FTP()
        ftp.set_pasv(False)
        try:
            ftp.connect(self.addr, self.port)
            ftp.login()
            ftp.sendcmd("EPRT |1|127.0.0.1|1024|")
            ftp.sendcmd("RETR server.py")
            return False
        except (error_reply, error_temp, error_perm, error_proto):
            try:
                ftp.sendcmd("PORT 127,0,0,1,1,1")
                ftp.sendcmd("RETR server.py")
                return False
            except (error_reply, error_temp, error_perm, error_proto):
                result0 = True
            except:
                return False
        except:
            return False
        _ = DataConn("127.0.0.1", 52306)
        try:
            ftp.login()
            ftp.sendcmd("EPRT |1|127.0.0.1|52306")
            ftp.sendcmd("RETR server.py")
            return False
        except (error_reply, error_temp, error_perm, error_proto):
            result1 = True
        except:
            return False
        if result0 and result1:
            self.score += 10
        ftp.quit()
        return result0 and result1

    def t21(self):
        result0, result1 = False, False
        ftp = FTP()
        ftp.set_pasv(False)
        ftp.connect(self.addr, self.port)
        ftp.login()
        content = uuid.uuid1().bytes
        try:
            with BytesIO(content) as file:
                ftp.storbinary('STOR .', file)
        except (error_reply, error_temp, error_perm, error_proto):
            result0 = True
        except:
            return False
        try:
            ftp.retrbinary('RETR \\', print)
        except (error_reply, error_temp, error_perm, error_proto):
            result1 = True
        except:
            return False
        if result0 and result1:
            self.score += 10
        ftp.quit()
        return result0 and result1

    def test(self):
        print("Now start testing")
        print("Task 1:")
        print("Handling connections   ", end="")
        print(self.t11())
        print("Anonymous login        ", end="")
        print(self.t12())
        print("Transfer files         ", end="")
        print(self.t13())
        tok = self.token()
        print("Task 1 finished. Now task 2:")
        print("File errors            ", end="")
        print(self.t21())
        print("Command errors         ", end="")
        print(self.t22())
        print("Connection errors      ", end="")
        print(self.t23())
        print(f"[{tok}] Test for tasks 1 and 2 are done. Your score is {self.score}")


if __name__ == "__main__":
    test = FtpTest()
    test.test()
