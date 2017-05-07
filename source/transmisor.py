#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  transmisor.py
#  
#  Copyright 2017 root <root@puppypc>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
from scapy.all import *

ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24"),timeout=10)
lista_ips = []
for i in ans.res:
	lista_ips.append(i[1][0].psrc)
print lista_ips
lista_paquetes = []
for ip in lista_ips:
	sys.stdout.write("Se le quiere enviar un paquete a la ip "+ip+' \n')
	p=sr1(IP(dst=ip)/ICMP())
	if p:
		lista_paquetes.append(p)

for paquete in lista_paquetes:
	print paquete.show()
