#! /usr/bin/env python
import os, math
import time
from operator import truediv
from scapy.all import *

# constantes
WHO_HAS = 1
IS_AT = 2
MAC_BROADCAST = 'ff:ff:ff:ff:ff:ff'
SIMBOLO_BROADCAST = "Broadcast        "
SIMBOLO_UNICAST = "Unicast          "

class sniffer:
    def __init__(self, ejercicio):
        #-- generales
        self.ejercicio = ejercicio
        self.paquetes = []
        self.simbolos = {}
        if ejercicio == "1":
            self.simbolos[SIMBOLO_BROADCAST] = 0
            self.simbolos[SIMBOLO_UNICAST] = 0

        actualizar_pantalla(self)
        self.iniciar_sniff()

    def recibir_paquete(self, pkt):
        if ARP in pkt: # es arp
            simbolo = ""
            if ejercicio == "1":
                #-- ejercicio 1
                if pkt.dst == MAC_BROADCAST:
                    simbolo = SIMBOLO_BROADCAST
                else:
                    simbolo = SIMBOLO_UNICAST
            else:
                #-- ejercicio 2
                if pkt[ARP].op == WHO_HAS:
                    simbolo = pkt.src
                elif pkt[ARP].op == IS_AT:
                    simbolo = pkt.src
            if simbolo != "":
                self.paquetes.append(pkt)
                #-- si no estaba en el diccionario lo crea
                if simbolo not in self.simbolos.keys():
                    self.simbolos[simbolo] = 0
                #-- se suma el paquete
                self.simbolos[simbolo] += 1
                actualizar_pantalla(self)

    def iniciar_sniff(self):
        sniff(prn=self.recibir_paquete, filter='arp', store=0)

def actualizar_pantalla(sniff_obj):
    os.system("clear")
    print "--------------------------------------------------------------------"
    print "-- Ejercicio: " + sniff_obj.ejercicio
    print "-- Cantidad de Simbolos: " + str(len(sniff_obj.simbolos))
    print "-- Cantidad de Paquetes: " + str(len(sniff_obj.paquetes))
    entropia = "-"
    if len(sniff_obj.paquetes) > 0 and len(sniff_obj.simbolos) > 1:
        entropia = 0
        for simbolo in sniff_obj.simbolos:
            if sniff_obj.simbolos[simbolo] > 0:
                probabilidad = truediv(sniff_obj.simbolos[simbolo], len(sniff_obj.paquetes))
                entropia += (-math.log(probabilidad, len(sniff_obj.simbolos)) * probabilidad)
    print "-- Entropia: " + str(entropia)
    print "--------------------------------------------------------------------"
    print "--------------------------------------------------------------------"
    print "Simbolo                    Probabilidad                  Informacion"
    for simbolo in sniff_obj.simbolos:
        probabilidad = "-"
        informacion = "-"
        if len(sniff_obj.paquetes) > 0:
            probabilidad = truediv(sniff_obj.simbolos[simbolo], len(sniff_obj.paquetes))
            if probabilidad > 0 and len(sniff_obj.simbolos) > 1:
                informacion = -math.log(probabilidad, len(sniff_obj.simbolos))
        print simbolo + "               " + str(probabilidad) + "                     " + str(informacion)
        # escritura en el archivo para el experimentacion
        os.system("echo "+time.strftime("%H:%M:%S")+","+simbolo+","+str(probabilidad)+","+str(informacion)+","+str(len(sniff_obj.paquetes))+","+str(entropia)+" >> resultado.csv")
    print ""
    print "--------------------------------------------------------------------"
    print "------------------------ ULTIMOS 10 PAQUETES -----------------------"
    print "--------------------------------------------------------------------"
    print "Origen                       Destino"
    for paquete in sniff_obj.paquetes[-10:]:
        print paquete.src + "     ->     " + paquete.dst

usuario = os.popen("whoami").read()
usuario = usuario[:-1] # saco el eol del final
if usuario != "root":
    print "Correlo con root chabon!"
    exit(1)
ejercicio = raw_input("Ingrese el numero de ejercicio: ")
os.system("echo '' > resultado.csv")
os.system("echo tiempo,simbolo,probabilidad,informacion,cantidad de paquetes,entropia >> resultado.csv")
sniff_obj = sniffer(ejercicio)
