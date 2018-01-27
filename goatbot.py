from irc import *
import os
import random

channel = "#DnetTest"
server = "losangeles.ca.us.undernet.org"
nickname = "DnetPY"

irc = IRC()
irc.connect(server, channel, nickname)

while 1:
	text = irc.get_text()
	print text

	if "PRIVMSG" in text and channel in text and "snakes" in text:
		irc.send(channel, "Hisssssssss")

