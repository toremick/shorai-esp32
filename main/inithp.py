from time import sleep
from machine import UART
uart = UART(1, 9600)
uart.init(9600,bits = 8,parity = 0,stop = 1,rx = 32,tx = 33,)


def handshake():
    bootlist = []
    bootlist.append((2,255,255,0,0,0,0,2))
    bootlist.append((2,255,255,1,0,0,1,2,254))
    bootlist.append((2,0,0,0,0,0,2,2,2,250))
    bootlist.append((2,0,1,129,1,0,2,0,0,123))
    bootlist.append((2,0,1,2,0,0,2,0,0,254))
    bootlist.append((2,0,2,0,0,0,0,254))
    return bootlist

def aftershake():
     bootlist = []
     bootlist.append((2,0,2,1,0,0,2,0,0,251))
     bootlist.append((2,0,2,2,0,0,2,0,0,250))
     return bootlist
     
  

def start_handshake():
    print("starting handshake")
    bootliste = handshake()
    afterlist = aftershake()
    for i in bootliste:
        print(bytearray(i))
        uart.write(bytearray(i))
        sleep(0.2)
    sleep(2)
    for j in afterlist:
        print(bytearray(j))
        uart.write(bytearray(j))
        sleep(0.2)
    print("handshake done")
   