import sys
import socket
import struct
import signal
from settings import TIMEOUT

def handler(signum, frame):
    print ('Timeout called with signal alarm')
    sys.exit(0)

# Set the signal handler
signal.signal(signal.SIGALRM, handler)

msgFromClient = "Hello slave!"
bytesToSend = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 8080)
bufferSize = 1024

# argument 0 to jest nazawa pliku jaki odpalamy, uwaga: dane zaczynaja sie od argv[1]
if len(sys.argv) == 3:
    serverAddressPort = (str(sys.argv[1]), int(sys.argv[2]))
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    # UDPClientSocket.bind(('127.0.0.2', 8081))
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
else:
    multicast_group = ('224.0.0.2', 10000)

    

    UDPClientSocket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
    print('1')
    UDPClientSocket2.settimeout(5)
    print('1.5')
    ttl = struct.pack('b', 1)
    UDPClientSocket2.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    print('1.75')
    

    UDPClientSocket2.sendto(bytesToSend, multicast_group)
    print('2')
    
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    print('hi')
    infoFromServer = UDPClientSocket2.recvfrom(bufferSize)
    print(infoFromServer[0])
    serverAddressPort = infoFromServer[1]

    serverAddressPort = (serverAddressPort[0], 8080)
    print(serverAddressPort)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    print('sent')

for i in range(5):
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = msgFromServer[0].decode()
    print(msg)

game = True
timeout = False
while (game):

    signal.alarm(TIMEOUT)
    msg = input()
    bytesToSend = str.encode(msg)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    signal.alarm(0)    

    for i in range(2):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode()
        print(msg)

        isFinished = msg.split()
        if isFinished[0] == "Unfortunately" or isFinished[0] == "Congratulations":
            game = False
            break