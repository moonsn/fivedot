# coding=utf-8
__author__ = 'moons'
from socket import *
import threading

# 获取本机IP
myIP = gethostbyname(gethostname())
PORT = 50000

class Server(threading.Thread):

    def __init__(self, port, fun):
        threading.Thread.__init__(self)
        self.ADDR = ('', port)
        self.sock = socket(AF_INET, SOCK_DGRAM) # SOCK_DGRAM 是指报文格式传输(UDP)
        self.sock.bind(self.ADDR)
        self.thStop = False
        self.fun = fun
        print "listenAt: ", self.ADDR

    def __del__(self):
        self.sock.close()

    def transMsg(self):
        print "waiting..."
        (data, curAddr) = self.sock.recvfrom(1024)
        print "recved someing"
        print data
        self.fun(data)

    def run(self):
        while not self.thStop:
            self.transMsg()

    def stop(self):
        self.thStop = True

class Client(threading.Thread):

        def __init__(self, ip, port):
            threading.Thread.__init__(self)
            self.ADDR = (ip, port)
            self.sock = socket(AF_INET, SOCK_DGRAM)
            self.thStop = False
            print "sendTo:", self.ADDR


        def __del__(self):
            self.sock.close()

        def sendMsg(self,msg):
            self.sock.sendto(msg, self.ADDR)

        def run(self):
            while not self.thStop:
                msg = raw_input()
                if not msg.strip():
                    continue
                print "> " + msg
                self.sendMsg(msg)

        def stop(self):
            self.sock.close()

        def change_ip(self, ip, port):
            self.ADDR = (ip, port)
            print "change :",self.ADDR

def main():
    ip = ""
    ser = Server()
    cli = Client(ip)
    ser.run()
    cli.run()

if __name__ == '__main__':
    main()
