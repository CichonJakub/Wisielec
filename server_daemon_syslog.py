import socket
import random
import time
import sys
import os
import syslog
from settings import *

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
            #print("exited first parent")
            sys.exit(0)
    except OSError as e:
        syslog.syslog("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
        #print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
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
            #print("exited second")
            #print("Daemon PID %d" % pid)
            sys.exit(0)
    except OSError as e:
        syslog.syslog("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        #print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)



    def __init__(self):
        self.sourceIP = "127.0.0.1"
        self.sourcePort = 8080
        self.serverAddress = (self.sourceIP, self.sourcePort)
        self.bufferSize = 1024

        #create UDP socket
        self.serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)


    def binding(self, serverAddress):
        #socket.bind((sourceIP, sourcePort))
        try:
            self.serverSocket.bind(serverAddress)
            syslog.syslog("I am listening :)")
            #print("I am listening :)")
        except:
            syslog.syslog("Bind error!")
            #print("Bind error!")

    def play(self):

        while(True):
            try:
                game = True
                syslog.syslog("LOOP")
                #print("LOOP")
                bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)
                message = bytesAddressPair[0]
                self.cliAddress = bytesAddressPair[1]

                category, word = random.choice(list(wordBank.items()))
                guessed_letters = []
                is_guessed = False
                break

            except:
            	syslog.syslog("Error when receiving message")
                #print("Error when receiving message")

        while(game):
            
            lives = 5

            clientMSG = "Message from Client: {}".format(message)
            clientIP = "Client IP Address:{}".format(self.cliAddress)
            syslog.syslog(clientMSG)
            syslog.syslog(clientIP)
            syslog.syslog(category)
            syslog.syslog(word)

            #print(clientMSG)
            #print(clientIP)
            #print(category)
            #print(word)

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

            while(lives > 1):
                # receiving letter from client
                isCorrect = False

                msgFromClient = self.serverSocket.recvfrom(self.bufferSize)
                guess = msgFromClient[0].decode()
                syslog.syslog(guess)
                #print(guess)

                if guess not in guessed_letters and len(guess) == 1:
                    for loc, letter in enumerate(word):
                        if guess == letter:
                            isCorrect = True
                            self.secretWord = self.secretWord[:loc*2] + guess + self.secretWord[loc*2+1:]
                    guessed_letters.append(guess)

                if len(guess) == len(word):
                    if guess == word:
                        self.secretWord = word
                        is_guessed = True

                # recv
                syslog.syslog(lives)
                #print(lives)
                if isCorrect and not is_guessed:
                    self.response( "Congrats, You guessed it !" )
                    self.response(self.secretWord)

                if not isCorrect and not is_guessed:
                    lives -= 1
                    self.response( "You have got {} lives, dont give up!".format(str(lives)) )
                    self.response(self.secretWord)

                if '_' not in self.secretWord:
                    self.response( "You guessed the phrase {} correctly, congratulations ! You won !".format(word) )
                    time.sleep(1)
                    game = False
                    break
            
            if lives < 1:
                self.response( "Unfortunately You lost, the phrase was {}. Good luck next time :)".format(word) )
                time.sleep(1)
                game = False
            
            # mozna tu jeszcze dopisac opcje wybrania kolejnej gry lub wylaczenie ale to wiecej rzeczy bedzie do spradzania, wykonalne owszem, czy potrzebne nie wiem :/

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
