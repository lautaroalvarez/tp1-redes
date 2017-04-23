#! /usr/bin/env python
import os
from scapy.all import *

# constantes
WHO_HAS = 1
IS_AT = 2
MAC_BROADCAST = 'ff:ff:ff:ff:ff:ff'

class sniffer:
    def __init__(self, ejercicio):
        #-- generales
        self.ejercicio = ejercicio
        self.listado_paquetes = []
        #-- ejercicio 1
        self.cant_broadcast = 0
        self.cant_unicast = 0
        #-- ejercicio 2
        self.hosts = {}
        self.cant_paquetes = 0

        actualizar_pantalla(self)
        self.iniciar_sniff()

    def recibir_paquete(self, pkt):
        if ARP in pkt: # es arp
            self.listado_paquetes.append(pkt)
            if ejercicio == "1":
                #-- ejercicio 1
                if pkt.dst == MAC_BROADCAST:
                    self.cant_broadcast += 1
                else:
                    self.cant_unicast += 1
            else:
                #-- ejercicio 2
                if pkt[ARP].op == WHO_HAS:
                    self.cant_paquetes += 1
                    #-- si no estaba en el diccionario lo crea
                    if pkt.src not in self.hosts.keys():
                        self.hosts[pkt.src] = 0
                    #-- se suma el paquete
                    self.hosts[pkt.src] += 1
            actualizar_pantalla(self)

    def iniciar_sniff(self):
        sniff(prn=self.recibir_paquete, filter='arp', store=0)

def actualizar_pantalla(sniff_obj):
    os.system("clear");
    print "-- Corriendo el ejercicio: " + sniff_obj.ejercicio
    print "-------------- LISTADO DE HOSTS --------------"
    if sniff_obj.ejercicio == "1":
        print "S1 - Broadcast               " + str(sniff_obj.cant_broadcast)
        print "S2 - Unicast                 " + str(sniff_obj.cant_unicast)
        print ""
    else:
        for host in sniff_obj.hosts.keys():
            print host + "               " + str(sniff_obj.hosts[host])
        print ""
    print "-------------- ULTIMOS 10 PAQUETES --------------"
    for paquete in sniff_obj.listado_paquetes[-10:]:
        print paquete.src + "   ->   " + paquete.dst


#if os.system("whoami") != "root":
#    print "Correlo con root chabon!"
#    exit(1)
ejercicio = raw_input("Ingrese el numero de ejercicio: ")
sniff_obj = sniffer(ejercicio)
