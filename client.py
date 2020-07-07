import sys
import socket


# argument 0 to jest nazawa pliku jaki odpalamy, uwaga: dane zaczynaja sie od argv[1]
if len(sys.argv) != 1:
    serverAddressPort = (str(sys.argv), int(sys.argv))
else:
    # MCAST_GRP = '224.1.1.1'
    # MCAST_PORT = 5007
    #
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    # sock.sendto('Hello World!', (MCAST_GRP, MCAST_PORT))
    serverAddressPort   = ("127.0.0.1", 8080)

msgFromClient       = "Hello slave!"
bytesToSend         = str.encode(msgFromClient)
#serverAddressPort   = ("127.0.0.1", 8080)
bufferSize          = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

for i in range(5):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode()
        print(msg)

while(True):
    
    msg = input()
    bytesToSend = str.encode(msg)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    for i in range(2):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode()
        print(msg)