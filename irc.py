import socket
import time
import sys

class IRC:

        irc = socket.socket()

        def __init__(self):
                self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def send(self, chan, msg):
                self.irc.send("PRIVMSG " + chan + " " + msg + "n")

        def connect(self, server, channel, botnick):
                # defines the socket
                print "connecting to:"+server
                self.irc.connect((server, 6667))
		self.irc.send("USER " + botnick + " * 8 :OatTheGoat" + "n")
		self.irc.send("NICK " + botnick + "n")
                self.irc.send("JOIN " + channel + "n")


        def get_text(self):
                # receive text from socket
                text = self.irc.recv(512)

                # respond to all pings
                if 'PING' in text != -1:
			print text
                        self.irc.send('PONG ' + text.split() [1] + 'rn')

                return text

