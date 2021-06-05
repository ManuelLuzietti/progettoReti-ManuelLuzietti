# -*- coding: utf-8 -*-
import socket 
import signal 
import sys

#funzione usata per interrompere e chiudere server e relativi socket
def signal_handler(signal,frame):
    print("exiting")
    try:
        if(socket):
            socket.close()
        if(sock):
            sock.close()
    finally:
        sys.exit()

print("Server started")
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.bind(("localhost",8100))
socket.listen(1)
#setto timeout così da rendere accept() e recv() non completamente bloccanti,
#così da poter ancora interrompere l'applicativo al bisogno
socket.settimeout(5)
sock = None
signal.signal(signal.SIGINT, signal_handler)
while True:
    try:
        #accetta connessione tcp e riceve dati
        sock, addr = socket.accept()
        message =  sock.recv(1024).decode()
        print(message)
        sock.close()
    except:
        pass

        