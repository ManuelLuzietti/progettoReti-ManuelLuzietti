# -*- coding: utf-8 -*-
import time
import signal
import sys
from socket import *
import random
import datetime
from threading import *



#lista di thread in esecuzione
DeviceThreads = []
#num di device creati
NUM_DEVICE = 4
IP_NETWORK_PART = "192.168.1."
thread_lock = Lock()

#funzione per interrompere tutti i device e relativi socket
def signal_handler(signal,frame):
    print("exiting")
    try:
        for device in DeviceThreads:
            device.stop()
            if device.socket_device:
                device.socket_device.close()
            device.join()
    finally:
        sys.exit()
        
def readData(name): 
    fd = open("data\\" + name + ".txt","r")
    lines = fd.readlines()
    fd.close()
    fd = open("data\\" + name + ".txt","w")
    fd.write("".join(lines[1:]))
    fd.close()        
    return lines[0]

#classe device, invece di creare un sorgente per ogni device ho deciso di optare per una versione multithread
class DeviceClass(Thread):
    def __init__(self,ip,fileName,gatewayAddress=("localhost",8000),secs=15):
        Thread.__init__(self)
        self.ip_device = ip
        self.socket_device = socket(AF_INET,SOCK_DGRAM)
        self.running = True
        self.fileName = fileName
        self.gateway_address = gatewayAddress
        self.secs = secs
    def stop(self):
        self.running = False
    def run(self):
        while self.running:
            #generazione dati
            try:
                message = self.ip_device + " - " + readData(self.fileName).rstrip('\n')
            except:
                sys.exit(0)
            #calcolo trasmission delay
            thread_lock.acquire()
            print(self.ip_device + "sending data to Gateway on interface 192.168.1.0")
            thread_lock.release()
            time0 = time.perf_counter()
            self.socket_device.sendto(message.encode(), self.gateway_address)
            time1 = time.perf_counter()
            #acquisisco lock così da stampare su terminale in modo ordinato
            thread_lock.acquire()
            print(self.ip_device , " message --trasmission time: ", time1-time0, " data: ",'\n'+message+'\n')
            thread_lock.release()
            #attesa a prossima generazione dati 
            for i in range(self.secs):
                #ciclo di sleep(1) così da non bloccare device per tutta la durata dell' attesa
                time.sleep(1)
                if not self.running:
                    break

 
if __name__ == '__main__':
    signal.signal(signal.SIGINT,signal_handler)
    #creao un thread per ogni device
    for x in range(NUM_DEVICE):
        newThreadDevice = DeviceClass(IP_NETWORK_PART + str(x+2),"data" + str(x+1))
        DeviceThreads.append(newThreadDevice)
        newThreadDevice.start()
        print("Device ", newThreadDevice.ip_device, " started")
    while True:
        pass
        
        
