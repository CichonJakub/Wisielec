import sys
import socket
import struct
import signal
from settings import TIMEOUT
from IPy import IP

def handler(signum, frame):
    print ('Timeout called with signal alarm')
    sys.exit(0)

# Set the signal handler
signal.signal(signal.SIGALRM, handler)

msgFromClient = "Hello!"
bytesToSend = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 8080)
bufferSize = 1024

if len(sys.argv) == 3:
    try:
    	IP(sys.argv[1])
    	ip_addr = sys.argv[1]
    except ValueError:
    	ip_addr = socket.gethostbyname(sys.argv[1])
    
    if(sys.argv[2].isdecimal()):
    	port_number = sys.argv[2]
    else:
    	port_number = socket.getservbyname(sys.argv[2])
    
    serverAddressPort = (str(ip_addr), int(port_number))
    uniSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    uniSocket.sendto(bytesToSend, serverAddressPort)
    
else:
    multicast_group = ('224.0.0.2', 10000)

    multiSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
    multiSocket.settimeout(5)
    ttl = struct.pack('b', 1)
    multiSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    multiSocket.sendto(bytesToSend, multicast_group)
    
    # przejscie na unicast
    uniSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    infoFromServer = multiSocket.recvfrom(bufferSize)
    serverAddressPort = infoFromServer[1]

    serverAddressPort = (serverAddressPort[0], 8080)
    uniSocket.sendto(bytesToSend, serverAddressPort)

# 5 odnosi sie do liczby wiadomosci startowych przed samym zgadywaniem liter
for i in range(5):
    msgFromServer = uniSocket.recvfrom(bufferSize)
    msg = msgFromServer[0].decode()
    print(msg)

game = True
timeout = False
while (game):

    signal.alarm(TIMEOUT)
    msg = input()
    bytesToSend = str.encode(msg)
    uniSocket.sendto(bytesToSend, serverAddressPort)
    signal.alarm(0)    

    for i in range(2):
        msgFromServer = uniSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode()
        print(msg)

        isFinished = msg.split()
        if isFinished[0] == "Unfortunately" or isFinished[0] == "Congratulations":
            game = False
            break
