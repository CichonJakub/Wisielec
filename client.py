import sys
import socket
import struct

msgFromClient       = "Hello slave!"
bytesToSend         = str.encode(msgFromClient)
#serverAddressPort   = ("127.0.0.1", 8080)
bufferSize          = 1024

# argument 0 to jest nazawa pliku jaki odpalamy, uwaga: dane zaczynaja sie od argv[1]
if len(sys.argv) == 3:
    serverAddressPort = (str(sys.argv[1]), int(sys.argv[2]))
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
else:
    MCAST_GRP = '224.1.1.5'
    MCAST_PORT = 5008

    #UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
    #UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #UDPClientSocket2.bind('', MCAST_PORT)
    
    #mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    #UDPClientSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

    UDPClientSocket.sendto(bytesToSend, (MCAST_GRP, MCAST_PORT))

    #creating normal socket to have responeses on unicast
    #serverAddressPort = ("127.0.0.1", 8080)
    #UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)



for i in range(5):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        print(msgFromServer[1])
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