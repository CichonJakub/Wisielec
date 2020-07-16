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
            syslog.syslog("exited first parent")
            sys.exit(0)
    except OSError as e:
        syslog.syslog("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)
    

    home_dir = '.'
    os.chdir(home_dir)
    os.setsid()
    os.umask(0)
    
    try:
        pid = os.fork()
        if pid > 0:
            # exit second parent
            syslog.syslog("exited second parent")
            syslog.syslog("Daemon PID %d" % pid)
            sys.exit(0)
    except OSError as e:
        syslog.syslog("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)

    def __init__(self):
        self.sourceIP = "192.168.230.140"
        self.sourcePort = 8080
        self.serverAddress = (self.sourceIP, self.sourcePort)
        self.bufferSize = 1024
        self.mcast_grp = '224.0.0.2'
        self.serverAddressMul = ('', 10000)

        syslog.syslog("lool")

        # create UDP socket
        self.uniSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        syslog.syslog("UDP first socket created")
        # creating UDP multicast socket
        self.multiSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        syslog.syslog("UDP second socket created")

    def binding(self, serverAddress):
        try:
            self.uniSocket.bind(serverAddress)
            syslog.syslog("First socket binded")
            self.multiSocket.bind(self.serverAddressMul)
            syslog.syslog("Second socket binded")
            group = socket.inet_aton(self.mcast_grp)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            self.multiSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            syslog.syslog("Second socket multicast options added")

        except:
            syslog.syslog("Bind error!")

    def play(self):

        while (True):
            
            inputs = [ self.uniSocket, self.multiSocket ]
            outputs = [ ]

            while True:
                syslog.syslog("waiting...")
                readable,_,_  = select.select(inputs, outputs, inputs)
                syslog.syslog(str(readable))
                break
                

            if self.uniSocket in readable:
                try:   
                    syslog.syslog("received unicast connection")
                    bytesAddressPair = self.uniSocket.recvfrom(self.bufferSize)                        
                    message = bytesAddressPair[0]
                    syslog.syslog(str(message))
                    self.cliAddress = bytesAddressPair[1]                   
                except:
                    syslog.syslog("Error when receiving message")

            if self.multiSocket in readable:
                try:
                    syslog.syslog("received multicast connection")
                    bytesAddressPair2 = self.multiSocket.recvfrom(self.bufferSize)
                    syslog.syslog("odebralem")
                    self.cliAddress = bytesAddressPair2[1]
                    time.sleep(2)
                    self.response2("Hello my friendo !", self.cliAddress)
                    syslog.syslog("wyslalem")
                    # przejscie na unicast
                    bytesAddressPair = self.uniSocket.recvfrom(self.bufferSize)
                    message = bytesAddressPair[0]
                    syslog.syslog(str(message))
                    self.cliAddress = bytesAddressPair[1]                   
                except:
                    syslog.syslog("Error when recieving multicast message")
            break

        game = True
        syslog.syslog("Game loop entered !")
        
        category, word = random.choice(list(wordBank.items()))
        guessed_letters = []
        is_guessed = False
        lives = 5
        clientIP = "Client IP Address:{}".format(self.cliAddress)
        syslog.syslog(clientIP)
        syslog.syslog(category)
        syslog.syslog(word)

        self.secretWord = ''

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
                # receiving guesses from client
                isCorrect = False
                
                try:
                    self.uniSocket.settimeout(TIMEOUT)
                    msgFromClient = self.uniSocket.recvfrom(self.bufferSize)
                except socket.timeout:
                    syslog.syslog("TIMEOUT REACHED")
                    game = False
                    break
                
                
                if msgFromClient[1] == self.cliAddress:
                    guess = msgFromClient[0].decode()
                    syslog.syslog(str(guess))

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
                    # proba nie zgadniecia litery ani calego slowa tylko jakies krzaki
                    syslog.syslog("NOT EVEN CLOSE")
                    lives -= 1

                syslog.syslog(str(lives))
                syslog.syslog("CHECK")
                if lives <= 1 and not isCorrect:
                    self.response( "Unfortunately You lost, the phrase was {}. Good luck next time :)".format(word) )
                    time.sleep(1)
                    # ending game
                    game = False
                    break

                syslog.syslog(str(lives))

                if isCorrect and not is_guessed:
                    self.response( "Congrats, You guessed it !" )
                    self.response(self.secretWord)

                if not isCorrect and not is_guessed:
                    lives -= 1
                    self.response( "You have got {} lives, dont give up!".format(str(lives)) )
                    self.response(self.secretWord)

                if '_' not in self.secretWord:
                    self.response( "Congratulations you guessed the phrase {} correctly ! You won !".format(word) )
                    self.response("")
                    time.sleep(1)
                    # ending game
                    game = False
                    break
            
        self.binding(self.serverAddress)
        self.play()

    def response(self, msg):
        bytesToSend = str.encode(msg)

        self.uniSocket.sendto(bytesToSend, self.cliAddress)
        time.sleep(1)

    def response2(self, msg, destination):
        bytesToSend = str.encode(msg)
        self.multiSocket.sendto(bytesToSend, destination)
        time.sleep(1)


try:
    server = Server()
    server.binding(server.serverAddress)
    server.play()
except:
    print("sth goes wrong :/")
