import socket
import random
import time
from settings import *
import struct


class Server:

    def __init__(self):
        self.sourceIP = "127.0.0.2"
        self.sourcePort = 8080
        self.serverAddress = (self.sourceIP, self.sourcePort)
        self.bufferSize = 1024
        # multicast
        self.mcast_grp = '224.1.1.2'
        self.mcast_port = 5007

        print('lool')

        # create UDP socket
        self.serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        print('lol2')
        # creating UDP multicast socket
        self.serverSocket2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        print('lool3')
        try:
            self.serverSocket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            print('tutaj')
        print('lol4')
        self.serverSocket2.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        print('lol5')
        self.serverSocket2.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        print('lol6')

    def binding(self, serverAddress):
        # socket.bind((sourceIP, sourcePort)) + multicast gniazdo 2
        try:
            self.serverSocket.bind(serverAddress)
            print("I am listening :)")
            self.serverSocket2.bind(('', self.mcast_port))
            print('przed laczenie')
            mreq = struct.pack("4sl", socket.inet_aton(self.mcast_grp), socket.INADDR_ANY)
            print('laczenie')
            self.serverSocket2.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            print('I am listening too :D')
        except:
            print("Bind error!")

    def play(self):

        while (True):
            # 2 try do multicastu
            try:
                bytesAddressPair2 = self.serverSocket2.recvfrom(self.bufferSize)
                message2 = bytesAddressPair2[0]
                self.cliAddress = bytesAddressPair2[1]
                connection = self.sourceIP + ':' + str(self.sourcePort)
                print(connection)
                self.response2(connection, self.cliAddress)
                print('wyslalem')

            except:
                print('Error when recieving multicast message')

            try:
                game = True
                print("LOOP")
                bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)
                message = bytesAddressPair[0]
                self.cliAddress = bytesAddressPair[1]
                category, word = random.choice(list(wordBank.items()))
                guessed_letters = []
                is_guessed = False
                break

            except:
                print("Error when receiving message")

        while (game):

            lives = 5

            clientMSG = "Message from Client: {}".format(message)
            clientIP = "Client IP Address:{}".format(self.cliAddress)

            print(clientMSG)
            print(clientIP)
            print(category)
            print(word)

            self.secretWord = ''

            # zamienienie liter na '_ '
            for letter in word:
                self.secretWord += '_ '

            self.response("WELCOME TO 'THE HANGMAN' GAME")
            time.sleep(1)

            self.response("Phrase from category: {}".format(category))
            time.sleep(1)

            self.response("Guess letter or entire phrase if You can ;)")
            time.sleep(1)

            self.response("You have got {} lives".format(lives))

            self.response(self.secretWord)
            time.sleep(1)

            while (lives > 1):
                # receiving letter from client
                isCorrect = False

                msgFromClient = self.serverSocket.recvfrom(self.bufferSize)
                guess = msgFromClient[0].decode()
                print(guess)

                if guess not in guessed_letters and len(guess) == 1:
                    for loc, letter in enumerate(word):
                        if guess == letter:
                            isCorrect = True
                            self.secretWord = self.secretWord[:loc * 2] + guess + self.secretWord[loc * 2 + 1:]
                    guessed_letters.append(guess)

                if len(guess) == len(word):
                    if guess == word:
                        self.secretWord = word
                        is_guessed = True

                # recv
                print(lives)
                if isCorrect and not is_guessed:
                    self.response("Congrats, You guessed it !")
                    self.response(self.secretWord)

                if not isCorrect and not is_guessed:
                    lives -= 1
                    self.response("You have got {} lives, dont give up!".format(str(lives)))
                    self.response(self.secretWord)

                if '_' not in self.secretWord:
                    self.response("You guessed the phrase {} correctly, congratulations ! You won !".format(word))
                    time.sleep(1)
                    game = False
                    break

            if lives < 1:
                self.response("Unfortunately You lost, the phrase was {}. Good luck next time :)".format(word))
                time.sleep(1)
                game = False

            # mozna tu jeszcze dopisac opcje wybrania kolejnej gry lub wylaczenie ale to wiecej rzeczy bedzie do spradzania, wykonalne owszem, czy potrzebne nie wiem :/

    def response(self, msg):
        bytesToSend = str.encode(msg)
        self.serverSocket.sendto(bytesToSend, self.cliAddress)
        time.sleep(1)

    def response2(self, msg, destination):
        bytesToSend = str.encode(msg)
        self.serverSocket2.sendto(bytesToSend, destination)
        time.sleep(1)


try:
    server = Server()
    print('1')
    server.binding(server.serverAddress)
    print('2')
    server.play()
    print('3')
except:
    print("sth goes wrong :/")