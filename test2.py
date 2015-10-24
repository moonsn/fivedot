# coding=utf-8
__author__ = 'moons'
from socket import *
import threading
import json

# 获取本机IP
myIP = gethostbyname(gethostname())
PORT = 50001
PORT_TO = 50000

class Server(threading.Thread):

    def __init__(self, fun):
        threading.Thread.__init__(self)
        self.ADDR = ('127.0.0.1', PORT)
        self.sock = socket(AF_INET, SOCK_DGRAM) # SOCK_DGRAM 是指报文格式传输(UDP)
        self.sock.bind(self.ADDR)
        self.thStop = False
        self.fun = fun
        print "listenAt:", self.ADDR

    def __del__(self):
        self.sock.close()

    def transMsg(self):
        (data, curAddr) = self.sock.recvfrom(1024)
        print 'recv < ' + data
        self.fun(data)

    def run(self):
        while not self.thStop:
            self.transMsg()

    def stop(self):
        self.thStop = True

class Client(threading.Thread):

    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ADDR = (ip, PORT_TO)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.thStop = False
        print "sendto: ",self.ADDR


    def __del__(self):
        self.sock.close()

    def sendMsg(self,msg):
        self.sock.sendto(msg, self.ADDR)

    def run(self):
        while not self.thStop:
            row = raw_input("inputrow:")
            col = raw_input("inputcol:")
            msg = [{'row': int(row), 'col': int(col)}]
            msg = json.dumps(msg)
            self.sendMsg(msg)

    def stop(self):
        self.sock.close()

def main():
    ip = "127.0.0.1"
    ser = Server(call)
    cli = Client(ip)
    ser.start()
    cli.start()

def call(str):
    print str

if __name__ == '__main__':
    main()

