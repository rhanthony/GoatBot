from irc import *
import os
import random

channel = "#Dashin"
server = "losangeles.ca.us.undernet.org"
nickname = "ElecMoBot"

irc = IRC()
irc.connect(server, channel, nickname)

while 1:
	text = irc.get_text()
	print text

	if 'PING' in text != -1:
		irc.send('PONG ' + text.split() [1] + 'rn')

	if "PRIVMSG" in text and channel in text and "snakes" in text:
		hiss = "Hi" + random.randint(7,14)
		irc.send(channel, hiss)

