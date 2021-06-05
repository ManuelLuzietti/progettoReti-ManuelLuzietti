# -*- coding: utf-8 -*-
import socket
import sys
import signal
import time


#funzione usata per chiudere gateway e relativi socket all' occorrenza
def signal_handler(signal,frame):
    print("exiting")
    try:
        if(gateway_socket):
            gateway_socket.close()
        if(gateway_socket_TCP):
            gateway_socket_TCP.close()
    finally:
        sys.exit()

print("Gateway started")
signal.signal(signal.SIGINT,signal_handler)
#lista di messaggi arrivati tramite protocollo udp
device_message = []
#lista degli ip da cui ho ricevuto i messaggi
deviceip_received = []
server_address = ("localhost",8100)
gateway_socket_TCP = None
gateway_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#setto timeout così da non rendere alcune funzioni completamente bloccanti
gateway_socket.settimeout(5)
gateway_socket.bind(("localhost",8000))
#numero di device di cui attendere messagio prima di inviare a server dati raccolti
NUM_DEVICE = 4
while True:
    while len(device_message) < NUM_DEVICE:
        try:
            #prova a ricevere dati, messo all' interno di blocco try perchè il socket non è bloccante
            #dopo 5 secondi da timeout exception, così da poter ancora bloccare applicazione all' occorrenza
            message, addr = gateway_socket.recvfrom(1024)
            message_ip = message.decode().split("-")[0]
            #controlla che ip di mittente messaggio non sia già in lista
            if message_ip not in deviceip_received:
                print("receiving data on interface 192.168.1.0 from " + message_ip)
                device_message.append(message.decode())
                deviceip_received.append(message_ip)
        except:
            pass
    try:
        gateway_socket_TCP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #apre connessione tcp 
        gateway_socket_TCP.connect(server_address)
        data = str("\n").join(device_message)
        #calcolo trasmission delay 
        time0 = time.perf_counter()
        gateway_socket_TCP.send(data.encode())
        time1 = time.perf_counter()
        #chiude connessione tcp
        gateway_socket_TCP.close()
        print("data sent on interface 10.10.10.0 , trasmission delay: ", time1-time0)
        #pulisco lista di messaggi raccolti e di ip 
        device_message.clear()
        deviceip_received.clear()
    except Exception as s:
        print("error occurs: ",s)
        if gateway_socket_TCP:
            gateway_socket_TCP.close()
    
    