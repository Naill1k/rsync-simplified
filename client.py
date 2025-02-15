import message, sender, receiver, os, sys, socket

def client(STATE) :
    if STATE['connection'] == 'daemon' :
        message.log('[CLIENT] Creating socket to daemon', STATE['-v'], 1)
        connect2daemon(STATE)

    # Sends STATE dictionnary to server
    message.log(f'[CLIENT] Sending STATE dictionnary', STATE['-v'], 2)
    message.send(STATE)
    message.receive()  # ACK from server
    message.send(None)
    message.log('[CLIENT] Sent STATE dictionnary', STATE['-v'], 2)
    
    if STATE['mode'] == 'PULL' :
        message.log('[CLIENT] Becoming receiver', STATE['-v'], 2)
        receiver.receiver(STATE)  # Actually destination files
    
    else :
        message.log('[CLIENT] Becoming sender', STATE['-v'], 2)
        sender.sender(STATE)
    



def connect2daemon(STATE) :
    # Creating socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to daemon
    server_address = (STATE['host'], STATE['--port'])
    try :
        sock.connect(server_address)

    except ConnectionRefusedError :
        message.log('ERROR : Unable to connect to daemon', STATE['-v'], 0)
        sys.exit(10)

    os.dup2(sock.fileno(), 0)
    os.dup2(sock.fileno(), 1)