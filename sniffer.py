#! /usr/bin/env python
import os
from scapy.all import *

# constantes
WHO_HAS = 1
IS_AT = 2

class sniffer:
    def __init__(self):
        self.cant_broadcast = 0
        self.cant_unicast = 0
        self.listado_paquetes = []
        self.cant_WH = 0
        self.cant_IA = 0

    def recibir_paquete(self, pkt):
        self.listado_paquetes.append(pkt)
        if pkt.dst == 'ff:ff:ff:ff:ff:ff':
            self.cant_broadcast += 1
        else:
            self.cant_unicast += 1
        actualizar_pantalla(self)

    def verWhoHas_IsAt(self,pkt):
        self.listado_paquetes.append(pkt)
        if ARP in pkt: # es arp
            if pkt[ARP].op == WHO_HAS: # operator = who has
                self.cant_WH += 1
            elif pkt[ARP].op == IS_AT: # operator = is at
                self.cant_IA += 1
        actualizar_pantalla(self, False)

    def iniciar_sniff(self):
        sniff(prn=self.recibir_paquete, filter='arp', store=0)

    def iniciar_sniffWH_IA(self):
        sniff(prn=self.verWhoHas_IsAt, filter="arp", store=0)

def actualizar_pantalla(sniff_obj,ej1=True):
    os.system("clear");
    print "-------------- LISTADO DE TRAFICO --------------"
    if ej1:
        print "S1 - Broadcast               " + str(sniff_obj.cant_broadcast)
        print "S2 - Unicast                 " + str(sniff_obj.cant_unicast)
        print ""
    else:
        print "S1 - Who Has               " + str(sniff_obj.cant_WH)
        print "S2 - Is At                 " + str(sniff_obj.cant_IA)
        print ""
    print "-------------- ULTIMOS 10 PAQUETES --------------"
    for paquete in sniff_obj.listado_paquetes[-10:]:
        print paquete.src + "   ->   " + paquete.dst


if os.system("whoami") != "root":
    print "Correlo con root chabon!"
    exit(1)
sniff_obj = sniffer()
#actualizar_pantalla(sniff_obj)
ejercicio = raw_input()
if ejercicio == "1":
    sniff_obj.iniciar_sniff()
else:
    sniff_obj.iniciar_sniffWH_IA()
