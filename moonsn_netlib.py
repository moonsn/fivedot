# coding=utf-8
__author__ = 'moons'
from socket import *
import threading

# 获取本机IP
myIP = gethostbyname(gethostname())
PORT = 50005

class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.ADDR = ('', 50005)
        self.sock = socket(AF_INET, SOCK_DGRAM) # SOCK_DGRAM 是指报文格式传输(UDP)
        self.sock.bind(self.ADDR)
        self.thStop = True

    def __del__(self):
        self.sock.close()

    def transMsg(self):
        (data, curAddr) = self.sock.recvfrom(1024)
        print '< ' + data

    def run(self):
        while not self.thStop:
            self.transMsg()

    def stop(self):
        self.thStop = True

class Client(threading.Thread):

        def __init__(self, ip):
           threading.Thread.__init__(self)
           self.ADDR = (ip, 50005)
           self.sock = socket(AF_INET, SOCK_DGRAM)
           self.thStop = False

        def __del__(self):
            self.sock.close()

        def sendMsg(self,msg):
            self.sock.sendto(gethostname() + ": " + msg, self.ADDR)

        def run(self):
            while not self.thStop:
                msg = raw_input()
                if not msg.strip():
                    continue
                print "> " + msg
                self.sendMsg()

        def stop(self):
            self.sock.close()

def main():
    ip = ""
    ser = Server()
    cli = Client(ip)
    ser.run()
    cli.run()

if __name__ == '__main__':
    main()
