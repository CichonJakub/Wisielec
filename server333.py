import socket
import random
import time
from settings import *
import struct
import _thread
import threading

class Server:

    values = []

    def __init__(self):
        self.sourceIP = "192.168.230.139"
        self.sourcePort = 8080
        self.serverAddress = (self.sourceIP, self.sourcePort)
        self.bufferSize = 1024
        # multicast
        #self.mcast_grp = '224.0.0.1'
        self.mcast_grp = '224.3.29.71'
        self.serverAddressMul = ('', 10000)

        print('lool')

        # create UDP socket
        self.serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        print('lol2')
        # creating UDP multicast socket
        self.serverSocket2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        print('lool3')

    def binding(self, serverAddress):
        # socket.bind((sourceIP, sourcePort)) + multicast gniazdo 2
        try:
            self.serverSocket.bind(serverAddress)
            print("I am listening :)")
            self.serverSocket2.bind(self.serverAddressMul)
            group = socket.inet_aton(self.mcast_grp)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            self.serverSocket2.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        except:
            print("Bind error!")


    def multi(self):
        try:

            print('xD')
            # bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)
            # print(bytesAddressPair[0])
            bytesAddressPair2 = self.serverSocket2.recvfrom(self.bufferSize)
            print('odebralem')
            message2 = bytesAddressPair2[0]
            self.cliAddress = bytesAddressPair2[1]
            print(message2)
            print(self.cliAddress)
            # connection = self.sourceIP + ':' + str(self.sourcePort)
            # print(connection)
            time.sleep(2)
            # self.response("Hello my friendo !")
            self.response2("Hello my friendo !", self.cliAddress)
            print('wyslalem')

        except:
            print('Error when recieving multicast message')


    def uni(self):
        try:
            game = True
            print("LOOP")
            bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)
            message = bytesAddressPair[0]
            print(message)
            self.cliAddress = bytesAddressPair[1]
            category, word = random.choice(list(wordBank.items()))
            guessed_letters = []
            is_guessed = False
            stop = True
            #break

            global values

            values.append(game)
            values.append(message)
            values.append(self.cliAddress)
            values.append(category)
            values.append(word)
            values.append(guessed_letters)
            values.append(is_guessed)
            values.append(stop)

            return values

        except:
            print("Error when receiving message")


    def play(self):
        stop = False
        while (True):

            _thread.start_new_thread(self.multi())


            # 2 try do multicastu
            # try:
            #
            #     print('xD')
            #     #bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)
            #     #print(bytesAddressPair[0])
            #     bytesAddressPair2 = self.serverSocket2.recvfrom(self.bufferSize)
            #     print('odebralem')
            #     message2 = bytesAddressPair2[0]
            #     self.cliAddress = bytesAddressPair2[1]
            #     print(message2)
            #     print(self.cliAddress)
            #     #connection = self.sourceIP + ':' + str(self.sourcePort)
            #     #print(connection)
            #     time.sleep(2)
            #     #self.response("Hello my friendo !")
            #     self.response2("Hello my friendo !", self.cliAddress)
            #     print('wyslalem')
            #
            # except:
            #     print('Error when recieving multicast message')
            print('hej')


            _thread.start_new_thread(self.uni(), )
            # try:
            #     game = True
            #     print("LOOP")
            #     bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)
            #     message = bytesAddressPair[0]
            #     print(message)
            #     self.cliAddress = bytesAddressPair[1]
            #     category, word = random.choice(list(wordBank.items()))
            #     guessed_letters = []
            #     is_guessed = False
            #     break
            #
            # except:
            #     print("Error when receiving message")
            print('siema')
            # values.append(game)
            # values.append(message)
            # values.append(self.cliAddress)
            # values.append(category)
            # values.append(word)
            # values.append(guessed_letters)
            # values.append(is_guessed)
            # values.append(stop)

            self.game = values[0]
            self.message = values[1]
            self.cliAddress = values[2]
            self.categoty = values[3]
            self.word = values[4]
            self.guessed_letters = values[5]
            self.is_guessed = values[6]
            self.stop = values[7]

            if self.stop == True:
                break





        while (game):
            print('ccc')
            lives = 5

            clientMSG = "Message from Client: {}".format(self.message)
            clientIP = "Client IP Address:{}".format(self.cliAddress)

            print(clientMSG)
            print(clientIP)
            print(self.category)
            print(self.word)

            self.secretWord = ''

            # zamienienie liter na '_ '
            for letter in self.word:
                self.secretWord += '_ '

            self.response("WELCOME TO 'THE HANGMAN' GAME")
            time.sleep(1)

            self.response("Phrase from category: {}".format(self.category))
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

                if guess not in self.guessed_letters and len(guess) == 1:
                    for loc, letter in enumerate(self.word):
                        if guess == letter:
                            isCorrect = True
                            self.secretWord = self.secretWord[:loc * 2] + guess + self.secretWord[loc * 2 + 1:]
                    self.guessed_letters.append(guess)

                if len(guess) == len(self.word):
                    if guess == self.word:
                        self.secretWord = self.word
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
                    self.response("You guessed the phrase {} correctly, congratulations ! You won !".format(self.word))
                    time.sleep(1)
                    game = False
                    break

            if lives < 1:
                self.response("Unfortunately You lost, the phrase was {}. Good luck next time :)".format(self.word))
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