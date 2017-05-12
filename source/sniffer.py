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
NOMBRES_MODOS = ["","Broadcast vs Unicast", "Diferenciar Hosts"]

class sniffer:
    def __init__(self, modo, log_id):
        #-- generales
        self.modo = int(modo)
        self.paquetes = []
        self.simbolos = {}
        if modo == 1:
            self.simbolos[SIMBOLO_BROADCAST] = 0
            self.simbolos[SIMBOLO_UNICAST] = 0
        self.log_id = 0
        if log_id:
            #--vamos a guardar logs
            self.log_id = log_id
            self.log_paquetes = csv.writer(open(self.log_id + "_paquetes.csv", "wb"))
            self.log_paquetes.writerow(["tiempo", "origen_ip", "origen_mac", "destino_ip", "destino_mac", "modo"])
            self.log_resultados = csv.writer(open(self.log_id + "_resultados.csv", "wb"))
            self.log_resultados.writerow(["tiempo", "simbolo", "probabilidad", "informacion", "cantidad de paquetes", "entropia"])
            self.ultimo_log = time.time()

        actualizar_pantalla(self)
        self.iniciar_sniff()

    def recibir_paquete(self, pkt):
        if ARP in pkt: # es arp
            simbolo = ""
            if modo == 1:
                #-- ejercicio 1
                if pkt.dst == MAC_BROADCAST:
                    simbolo = SIMBOLO_BROADCAST
                else:
                    simbolo = SIMBOLO_UNICAST
            else:
                #-- ejercicio 2
                if pkt[ARP].op == WHO_HAS:
                    simbolo = pkt[ARP].psrc
            if simbolo != "":
                #--guarda logs
                if self.log_id:
                    self.log_paquetes.writerow([time.strftime("%H:%M:%S"), pkt[ARP].psrc, pkt.src, pkt[ARP].pdst, pkt.dst, self.modo])
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
    loguear = 0
    if sniff_obj.log_id and time.time() - sniff_obj.ultimo_log > 60:
        sniff_obj.ultimo_log = time.time()
        loguear = 1
    print "--------------------------------------------------------------------"
    print "-- Modo: " + NOMBRES_MODOS[sniff_obj.modo]
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
        if loguear:
            sniff_obj.log_resultados.writerow([time.strftime("%H:%M:%S"), simbolo, probabilidad, informacion, len(sniff_obj.paquetes), entropia])
    print ""
    print "--------------------------------------------------------------------"
    print "------------------------ ULTIMOS 10 PAQUETES -----------------------"
    print "--------------------------------------------------------------------"
    print "Origen                       Destino"
    for paquete in sniff_obj.paquetes[-10:]:
        print paquete[ARP].psrc + "     ->     " + paquete[ARP].pdst

usuario = os.popen("whoami").read()
usuario = usuario[:-1] # saco el eol del final
if usuario != "root":
    print "Correlo con root chabon!"
    exit(1)
print "Elija un modo:"
print "1. Broadcast vs Unicast"
print "2. Diferenciar Hosts"
modo = raw_input("Opcion elegida: ")
log_id = raw_input("Ingrese el identificador de log (ENTER si no guarda logs): ")

sniff_obj = sniffer(modo, log_id)
