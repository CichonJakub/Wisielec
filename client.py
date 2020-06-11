import socket

msgFromClient       = "Hello slave!"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 8080)
bufferSize          = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)



while(True):
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = msgFromServer[0]
    print(msg)