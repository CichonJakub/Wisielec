import socket
import random
import time
from settings import *

sourceIP = "127.0.0.1"
sourcePort = 8080
bufferSize = 1024



#create UDP socket
socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#bind 
socket.bind((sourceIP, sourcePort))

print("I am listening :)")


while(True):
    game = True
    print("LOOP")
    bytesAddressPair = socket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    category, word = random.choice(list(wordBank.items()))

    while(game):
        
        lives = 5

        clientMSG = "Message from Client: {}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        print(clientMSG)
        print(clientIP)
        print(category)
        print(word)

        secret_word = ''
        
        #zamienienie liter na '_ '
        for letter in word:
            secret_word += '_ '

        msg = "WELCOME TO 'THE HANGMAN' GAME"
        bytesToSend = str.encode(msg)
        socket.sendto(bytesToSend, address)
        time.sleep(1)

        msg = "Phrase from category: {}".format(category)
        bytesToSend = str.encode(msg)
        socket.sendto(bytesToSend, address)
        time.sleep(1)

        msg = "Guess letter or entire phrase if You can ;)"
        bytesToSend = str.encode(msg)
        socket.sendto(bytesToSend, address)
        time.sleep(1)

        while(game):
            msg = "You have got {} lives, dont give up!".format(str(lives))
            bytesToSend = str.encode(msg)
            socket.sendto(bytesToSend, address)
            time.sleep(1)

            bytesToSend = str.encode(secret_word)
            socket.sendto(bytesToSend, address)
            time.sleep(1)

            game = False