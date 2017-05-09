#! /usr/bin/env python
import os, math, time, csv
from operator import truediv
from scapy.all import *

# constantes
WHO_HAS = 1
IS_AT = 2
MAC_BROADCAST = "ff:ff:ff:ff:ff:ff"
SIMBOLO_BROADCAST = "Broadcast        "
SIMBOLO_UNICAST = "Unicast          "

class sniffer:
    def __init__(self, ejercicio, log_id):
        #-- generales
        self.ejercicio = ejercicio
        self.paquetes = []
        self.simbolos = {}
        if ejercicio == "1":
            self.simbolos[SIMBOLO_BROADCAST] = 0
            self.simbolos[SIMBOLO_UNICAST] = 0
        if log_id:
            #--vamos a guardar logs
            self.log_id = log_id
            self.log_paquetes = csv.writer(open(self.log_id + "_paquetes.csv", "wb"))
            self.log_paquetes.writerow(["tiempo", "origen", "destino", "tipo"])
            self.log_resultados = csv.writer(open(self.log_id + "_resultados.csv", "wb"))
            self.log_resultados.writerow(["tiempo", "simbolo", "probabilidad", "informacion", "cantidad de paquetes", "entropia"])

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
            if simbolo != "":
                #--guarda logs
                if self.log_paquetes:
                    self.log_paquetes.writerow([time.strftime("%H:%M:%S"), pkt.src, pkt.dst, "WHO_HAS"])
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
        #--guarda logs
        if sniff_obj.log_resultados:
            sniff_obj.log_resultados.writerow([time.strftime("%H:%M:%S"), simbolo, probabilidad, informacion, len(sniff_obj.paquetes), entropia])
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
log_id = raw_input("Ingrese el identificador de log (ENTER si no guarda logs): ")

sniff_obj = sniffer(ejercicio, log_id)
