import socket
import random
import time
from settings import *

class Server:

    def __init__(self):
        self.sourceIP = "192.168.230.140"
        self.sourcePort = 8080
        self.serverAddress = (self.sourceIP, self.sourcePort)
        self.bufferSize = 1024

        #create UDP socket
        self.serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)


    def binding(self, serverAddress):
        try:
            self.serverSocket.bind(serverAddress)
            print("I am listening :)")
        except:
            print("Bind error!")

    def play(self):

        while(True):


            try:
                game = True
                print("LOOP")
                bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)
                message = bytesAddressPair[0]
                self.cliAddress = bytesAddressPair[1]

                print("siema")
                category, word = random.choice(list(wordBank.items()))
                guessed_letters = []
                is_guessed = False
                break

            except:
                print("Error when receiving message")

        while(game):
            
            lives = 5

            clientMSG = "Message from Client: {}".format(message)
            clientIP = "Client IP Address:{}".format(self.cliAddress)

            print(clientMSG)
            print(clientIP)
            print(category)
            print(word)

            self.secretWord = ''
            
            #zamienienie liter na '_ '
            for letter in word:
                self.secretWord += '_ '

            self.response( "WELCOME TO 'THE HANGMAN' GAME" )
            time.sleep(1)

            self.response( "Phrase from category: {}".format(category) )
            time.sleep(1)

            self.response( "Guess letter or entire phrase if You can ;)" )
            time.sleep(1)

            self.response( "You have got {} lives".format(lives) )

            self.response( self.secretWord )
            time.sleep(1)

            while(lives >= 1):
                # receiving letter from client
                isCorrect = False
                while(True):
                    msgFromClient = self.serverSocket.recvfrom(self.bufferSize)
                    if msgFromClient[1] == self.cliAddress:
                        guess = msgFromClient[0].decode()
                        print(guess)
                        break

                if guess not in guessed_letters and len(guess) == 1:
                    for loc, letter in enumerate(word):
                        if guess == letter:
                            isCorrect = True
                            self.secretWord = self.secretWord[:loc*2] + guess + self.secretWord[loc*2+1:]
                    guessed_letters.append(guess)

                elif len(guess) == len(word):
                    if guess == word:
                        self.secretWord = word
                        isCorrect = True
                        is_guessed = True
                    else:
                        lives -= 1

                else:
                    # proba nie zgadniecia litery ani calego slowa tylko jakies bzdury
                    print('NOT EVEN CLOSE')
                    lives -= 1

                print(lives)
                print('CHECK')
                if lives <= 1 and not isCorrect:
                    self.response( "Unfortunately You lost, the phrase was {}. Good luck next time :)".format(word) )
                    time.sleep(1)
                    game = False
                    break

                print(lives)
                if isCorrect and not is_guessed:
                    self.response( "Congrats, You guessed it !" )
                    self.response(self.secretWord)

                if not isCorrect and not is_guessed:
                    lives -= 1
                    self.response( "You have got {} lives, dont give up!".format(str(lives)) )
                    self.response(self.secretWord)

                if '_' not in self.secretWord:
                    self.response( "You guessed the phrase {} correctly, congratulations ! You won !".format(word) )
                    self.response("")
                    time.sleep(1)
                    game = False
                    break
            

    def response(self, msg):
        bytesToSend = str.encode(msg)
        self.serverSocket.sendto(bytesToSend, self.cliAddress)
        time.sleep(1)

try:
    server = Server()
    server.binding(server.serverAddress)
    server.play()
except:
    print("sth goes wrong :/")