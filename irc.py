import socket
import time
import sys

class IRC:

        irc = socket.socket()

        def __init__(self):
                self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def send(self, target, msg):
                self.irc.send("PRIVMSG " + target + " " + msg + "n")

        def connect(self, server, channel, botnick):
                # defines the socket
                print "connecting to:"+server
                self.irc.connect((server, 6667))
		print "CONNECTED!"
		time.sleep(5)

		print "Sending USER information..."
		self.irc.send("USER " + botnick + " * 8 :OatTheGoat" + "\r\n")

		#print("Sending NICK change to " + botnick)
		#self.irc.send("NICK " + botnick)

		#print("Sending JOIN command for " + channel)
                #self.irc.send("JOIN " + channel)

        def get_text(self):
                # receive text from socket
                text = self.irc.recv(512)

                # respond to all pings
                if 'PING ' in text != -1:
                        self.irc.send('PONG ' + text.split() [1] + 'rn')

                return text

