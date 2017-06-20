#! /usr/bin/env python
import os, math, time, csv
from operator import truediv
from scapy.all import *
import collections

# constantes
WHO_HAS = 1
IS_AT = 2
MAC_BROADCAST = "ff:ff:ff:ff:ff:ff"
SIMBOLO_BROADCAST = "Broadcast        "
SIMBOLO_UNICAST = "Unicast          "

class sniffer:
    def __init__(self,log_id):
        #-- generales
        self.paquetes = []
        self.paquetesWH = []
        self.simbolos = {}
        self.simbolos = collections.OrderedDict(self.simbolos)
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
            #-- ejercicio 1
            if pkt.dst == MAC_BROADCAST:
                simbolo = SIMBOLO_BROADCAST
            else:
                simbolo = SIMBOLO_UNICAST
            if simbolo != "":
                #--guarda logs
                if self.log_id:
                    self.log_paquetes.writerow([time.strftime("%H:%M:%S"), pkt[ARP].psrc, pkt.src, pkt[ARP].pdst, pkt.dst,1])
                self.paquetes.append(pkt)
                #-- si no estaba en el diccionario lo crea
                if simbolo not in self.simbolos.keys():
                    self.simbolos[simbolo] = 0
                #-- se suma el paquete
                self.simbolos[simbolo] += 1
            #-- ejercicio 2
            if pkt[ARP].op == WHO_HAS:
                simbolo = pkt[ARP].psrc
                #--guarda logs
                if self.log_id:
                    self.log_paquetes.writerow([time.strftime("%H:%M:%S"), pkt[ARP].psrc, pkt.src, pkt[ARP].pdst, pkt.dst,2])
                self.paquetesWH.append(pkt)
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
    print "-- Cantidad de Simbolos: " + str(len(sniff_obj.simbolos))
    print "-- Cantidad de Paquetes: " + str(len(sniff_obj.paquetes))
    entropia = "-"
    entropiaUniBro = "-"
    if len(sniff_obj.paquetes) > 0 and len(sniff_obj.simbolos) > 1:
        entropia = 0
        entropiaUniBro = 0
        print sniff_obj.simbolos
        for i in range(0, len(sniff_obj.simbolos)):
            simbolo = sniff_obj.simbolos.keys()[i]
            if i < 2:
                if sniff_obj.simbolos[simbolo] > 0:
                    probabilidadUniBro = truediv(sniff_obj.simbolos[simbolo],len(sniff_obj.paquetes))
                    entropiaUniBro += (-math.log(probabilidadUniBro, 2) * probabilidadUniBro)
            else:
                if len(sniff_obj.simbolos) > 3:
                    if sniff_obj.simbolos[simbolo] > 0:
                        probabilidad = truediv(sniff_obj.simbolos[simbolo], len(sniff_obj.paquetesWH))
                        entropia += (-math.log(probabilidad, len(sniff_obj.simbolos)-2) * probabilidad)
    print "-- Entropia IPs: "+str(entropia)
    print "-- Entropia unicast vs broadcast: " + str(entropiaUniBro)
    print "--------------------------------------------------------------------"
    print "--------------------------------------------------------------------"
    print "Simbolo                    Probabilidad                  Informacion"
    for i in range(0,len(sniff_obj.simbolos)):
        simbolo = sniff_obj.simbolos.keys()[i]
        probabilidad = "-"
        informacion = "-"
        if len(sniff_obj.paquetes) > 0:
            if i < 2:
                probabilidad = truediv(sniff_obj.simbolos[simbolo], len(sniff_obj.paquetes))
                if probabilidad > 0 and len(sniff_obj.simbolos) > 1:
                    informacion = -math.log(probabilidad, len(sniff_obj.simbolos))
            else:
                probabilidad = truediv(sniff_obj.simbolos[simbolo], len(sniff_obj.paquetesWH))
                if probabilidad > 0 and len(sniff_obj.simbolos)-2 > 1:
                    informacion = -math.log(probabilidad, len(sniff_obj.simbolos)-2)
        print simbolo + "               " + str(probabilidad) + "                     " + str(informacion)
        #--guarda logs
        if loguear:
            sniff_obj.log_resultados.writerow([time.strftime("%H:%M:%S"), simbolo.strip(), probabilidad, informacion, len(sniff_obj.paquetes), entropia])
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
log_id = raw_input("Ingrese el identificador de log (ENTER si no guarda logs): ")

sniff_obj = sniffer(log_id)
