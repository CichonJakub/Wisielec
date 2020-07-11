import socket
import random
import time
from settings import *
import struct
import select
import syslog
import os
import sys


class Server:


    try:
        syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL7)
    except:
        print("could not handle syslog")

    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            #syslog.syslog("exited first parent")
            print("exited first parent")
            sys.exit(0)
    except OSError as e:
        #syslog.syslog("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)
    

    home_dir = '.'
    os.chdir(home_dir)
    os.setsid()
    os.umask(0)
    
    try:
        pid = os.fork()
        if pid > 0:
            # exit second parent
            #syslog.syslog("exited second parent")
            #syslog.syslog("Daemon PID %d" % pid)
            print("exited second")
            print("Daemon PID %d" % pid)
            sys.exit(0)
    except OSError as e:
        #syslog.syslog("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    def __init__(self):
        self.sourceIP = "10.0.2.15"
        self.sourcePort = 8080
        self.serverAddress = (self.sourceIP, self.sourcePort)
        self.bufferSize = 1024
        # multicast
        self.mcast_grp = '224.0.0.2'
        #self.mcast_grp = '224.3.29.71'
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

    def play(self):

        while (True):
            
            inputs = [ self.serverSocket, self.serverSocket2 ]
            outputs = [ ]

            while True:
                print('waiting...')
                readable,_,_  = select.select(inputs, outputs, inputs)
                print(readable)
                break
                

            if self.serverSocket in readable:
                try:   
                    print('received unicast connection')
                    bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)                        
                    message = bytesAddressPair[0]
                    print(message)
                    self.cliAddress = bytesAddressPair[1]                   
                except:
                    print("Error when receiving message")

            if self.serverSocket2 in readable:
                try:
                    print('received multicast connection')
                    bytesAddressPair2 = self.serverSocket2.recvfrom(self.bufferSize)
                    print('odebralem')
                    self.cliAddress = bytesAddressPair2[1]
                    time.sleep(2)
                    self.response2("Hello my friendo !", self.cliAddress)
                    #self.cliAddress = (self.cliAddress[0], 8080)
                    print('wyslalem')
                    # przejscie na unicast
                    bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)
                    message = bytesAddressPair[0]
                    print(message)
                    self.cliAddress = bytesAddressPair[1]                   
                except:
                    print('Error when recieving multicast message')
            break

        game = True
        print("LOOP")
        
        category, word = random.choice(list(wordBank.items()))
        guessed_letters = []
        is_guessed = False
        lives = 5
        clientIP = "Client IP Address:{}".format(self.cliAddress)
        print(clientIP)
        print(category)
        print(word)

        self.secretWord = ''

        # zamienienie liter na '_ '
        for letter in word:
            self.secretWord += '_ '

        while (game):
            
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
