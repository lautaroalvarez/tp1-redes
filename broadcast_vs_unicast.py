#! /usr/bin/env python
import os
from scapy.all import *

class sniffer:
    def __init__(self):
        self.cant_broadcast = 0
        self.cant_unicast = 0
        self.listado_paquetes = []

    def recibir_paquete(self, pkt):
        self.listado_paquetes.append(pkt)
        if pkt.dst == 'ff:ff:ff:ff:ff:ff':
            self.cant_broadcast += 1
        else:
            self.cant_unicast += 1
        actualizar_pantalla(self)

    def iniciar_sniff(self):
        sniff(prn=self.recibir_paquete, filter='arp', store=0)

def actualizar_pantalla(sniff_obj):
    os.system("clear");
    print "-------------- LISTADO DE TRAFICO --------------"
    print "S1 - Broadcast               " + str(sniff_obj.cant_broadcast)
    print "S2 - Unicast                 " + str(sniff_obj.cant_unicast)
    print ""
    print "-------------- ULTIMOS 10 PAQUETES --------------"
    for paquete in sniff_obj.listado_paquetes[-10:]:
        print paquete.src + "   ->   " + paquete.dst


sniff_obj = sniffer()
actualizar_pantalla(sniff_obj)
sniff_obj.iniciar_sniff()
