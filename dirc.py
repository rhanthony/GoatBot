import socket
import random

# Set version number
# Major.Minor.DATE
VERSION = '0.1.20170130'

# IRC connection parameters
HOST = 'amsterdam.nl.eu.undernet.org'
PORT = 6667
NICK = 'Larry'
CHAN = '#dashin'

# Users allowed to send protected commands
ADMIN = 'ElecMoHwk'

# Start up in G mode
# Modes are like movie ratings.
# Available modes are:
#    G - general
#    R - a little rebellious
MODE = 'G'

# this is the function I will use when I want to send a message to the IRC server
def send_line(irc:socket.socket, line:str):
    print(f'=> {line}')
    # add \r\n to the end of the line and convert it from string to bytes, then send
    irc.send(f'{line}\r\n'.encode())


# this is the function I will use when I want to process a message I received from the IRC server
def handle_line(irc: socket.socket, line: bytes):

    # Import globaal variables so we can change them
    global MODE
    global NICK

    # convert line from bytes to string, and remove leading and trailing whitespace
    line = line.decode().strip()
    print(f'<= {line}')
    # split the line on whitespace into a list of tokens
    tokens = line.split()

    # For showing elements of each line and their respective 'token' position
    # eventually this should show up with a -debug flag
    #
    for line in range(1):
        total = len(tokens)
        print(f'{total} elements found ... ')
        for t in range(total):
            print(f'tokens{t}={tokens[x]}')
    #
    #

    if tokens[0] == 'PING':
        # when the server sends PING, I automatically reply with PONG
        send_line(irc, f'PONG {tokens[1]}')

    elif tokens[1] in ('376', '422'):
        # 376 means the server has finished sending the message of the day
        # 422 means there is no message of the day to send
        # in any case, now I can join my channel
        send_line(irc, f'JOIN {CHAN}')

    # If the line is a direct message to the bot - respond to commands
    #elif ( len(tokens) >=4 and tokens[2] == '{NICK}'):
    elif (tokens[1] == 'PRIVMSG' and tokens[2] == NICK):

        if (tokens[3] == ':!status'):
            print(f'COMMAND: Show status')
            TARGET = ADMIN
            send_line(irc, f'PRIVMSG {TARGET} :Status:  Alive and kickin\'')
            send_line(irc, f'PRIVMSG {TARGET} :Version: {VERSION}')
            send_line(irc, f'PRIVMSG {TARGET} :Owners:  {ADMIN}')
            send_line(irc, f'PRIVMSG {TARGET} :Channel: {CHAN}')
            send_line(irc, f'PRIVMSG {TARGET} :Mode:    {MODE}')


	# Command and control triggers
        if (tokens[3] == ':!come'):
            print(f'COMMAND: Come home')
            send_line(irc, f'PRIVMSG {ADMIN} :Woof!')
            send_line(irc, f'JOIN {CHAN}')

        if (tokens[3] == ':!fort'):
            print(f'COMMAND: Go to my fort')
            send_line(irc, f'PRIVMSG {ADMIN} :Going to my fort...')
            send_line(irc, f'PART {CHAN}')

        if (tokens[3] == ':!topic'):
            topic = ' '.join(tokens[4:])
            print(f'COMMAND: Topic change for: {CHAN}')
            print(f'NEW TOPIC: {topic}')
            send_line(irc, f'TOPIC {CHAN} :{topic}')

        # Nickname change requires variable blackmagic...
        if (tokens[3] == ':!changename'):
            NICK = tokens[4]
            print(f'COMMAND: Change nickname to {NICK}')
            send_line(irc, f'NICK {NICK}')

        # Set mode to G
        if (tokens[3] == ':!gmode'):
            send_line(irc, f'PRIVMSG {CHAN} :\x01ACTION takes a deep breath and composes himself...')
            MODE = 'G'
            print(f'COMMAND: Language limits! - Mode set to \'{MODE}\'')

        # Set mode to R
        if (tokens[3] == ':!rmode'):
            send_line(irc, f'PRIVMSG {CHAN} :\x01ACTION is feeling rebellious...')
            MODE = 'R'
            print(f'COMMAND: Rebellious! - Mode set to \'{MODE}\'')

    # If the line is a full message from the channel we are in - respond to commands
    elif (tokens[1] == 'PRIVMSG' and tokens[2] == CHAN):

        if (tokens[3] == ':!joke'):
            print(f'COMMAND: Joke')
            with open('txt/jokes.txt') as f:
                jokes = f.readlines()
                joke = random.choice(jokes)
            send_line(irc, f'PRIVMSG {CHAN} :{joke}')

        if (tokens[3] == ':!jump'):
            print(f'COMMAND: Jump')
            send_line(irc, f'PRIVMSG {CHAN} :\x01ACTION does jumping jacks!')

        # Add additional layer here to verify admin is issuing command for anything below

# this is where I start my work
def main():
    irc = socket.socket()
    irc.connect((HOST, PORT))
    print(f'** connected to {HOST}')
    # identify myself to the IRC server
    send_line(irc, f'NICK {NICK}')
    send_line(irc, f'USER {NICK} {HOST} x :{NICK}')

    # set up a buffer that I can use to receive messages from the server
    buffer = b''
    while True:
        # receive what the server has sent me
        buffer = buffer + irc.recv(4096)
        # split it into lines
        lines = buffer.split(b'\n')
        # the last line might be incomplete, put it back in the buffer
        buffer = lines.pop()
        # handle each of the lines that the server sent me
        for line in lines:
            handle_line(irc, line)


if __name__ == '__main__':
    main()
