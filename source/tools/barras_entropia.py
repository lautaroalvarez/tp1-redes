import csv, math
from operator import truediv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

INDEX_ORIGEN_IP = 1
INDEX_DESTINO_IP = 3
INDEX_DESTINO_MAC = 4
INDEX_MODO = 5
MODO_BRvsUN = 1
MODO_HOSTS = 2
IPS_MALAS_MODO_HOSTS = ['0.0.0.0', 'Broadcast', 'Unicast']
MAC_BROADCAST = "ff:ff:ff:ff:ff:ff"

class Graficador():
    def __init__(self, archivo_entrada, modo, limite):
        self.archivo_entrada = archivo_entrada
        self.limite = 0
        if limite != '':
            self.limite = int(limite)
        self.modo = int(modo)
        self.cant_paquetes = 0
        self.simbolos = {}
        if self.modo == MODO_BRvsUN:
            self.simbolos['Broadcast'] = {}
            self.simbolos['Broadcast']['cant_paquetes'] = 0
            self.simbolos['Unicast'] = {}
            self.simbolos['Unicast']['cant_paquetes'] = 0
        self.leer_entrada()
        self.calcular_probabilidades()
        self.calcular_entropia()
        # self.mostrar_simbolos()
        self.graficar_barras()

    def leer_entrada(self):
        with open(self.archivo_entrada, 'rb') as archivocsv:
            lector = csv.reader(archivocsv)
            primera_linea = 1
            for paquete in lector:
                if primera_linea:
                    primera_linea = 0
                elif self.modo == MODO_HOSTS and int(paquete[INDEX_MODO]) == MODO_HOSTS and paquete[INDEX_ORIGEN_IP] not in IPS_MALAS_MODO_HOSTS:
                    self.cant_paquetes += 1
                    if paquete[INDEX_ORIGEN_IP] not in self.simbolos.keys():
                        self.simbolos[paquete[INDEX_ORIGEN_IP]] = {}
                        self.simbolos[paquete[INDEX_ORIGEN_IP]]['cant_paquetes'] = 0
                    self.simbolos[paquete[INDEX_ORIGEN_IP]]['cant_paquetes'] += 1
                elif self.modo == MODO_BRvsUN and int(paquete[INDEX_MODO]) == MODO_BRvsUN:
                    self.cant_paquetes += 1
                    simbolo = 'Unicast'
                    if paquete[INDEX_DESTINO_MAC] == MAC_BROADCAST:
                        simbolo = 'Broadcast'
                    self.simbolos[simbolo]['cant_paquetes'] += 1

    def calcular_probabilidades(self):
        cant_simbolos = len(self.simbolos.keys())
        for simbolo_id in self.simbolos.keys():
            self.simbolos[simbolo_id]['probabilidad'] = truediv(self.simbolos[simbolo_id]['cant_paquetes'], self.cant_paquetes)
            if self.simbolos[simbolo_id]['probabilidad'] == 0:
                self.simbolos[simbolo_id]['informacion'] = 1
            else:
                self.simbolos[simbolo_id]['informacion'] = - math.log(self.simbolos[simbolo_id]['probabilidad'], cant_simbolos)

    def calcular_entropia(self):
        self.entropia = 0
        cant_hosts = len(self.simbolos.keys())
        for simbolo_id in self.simbolos.keys():
            self.entropia += self.simbolos[simbolo_id]['probabilidad'] * self.simbolos[simbolo_id]['informacion']

    def mostrar_simbolos(self):
        for simbolo_id in self.simbolos.keys():
            print str(simbolo_id) + " -> " + str(self.simbolos[simbolo_id]['probabilidad']) + '  -  ' + str(self.simbolos[simbolo_id]['informacion'])
        print ''
        print 'ENTROPIA: ' + str(self.entropia)

    def graficar_barras(self):
        tuplas_simbolos = []
        for simbolo_id in self.simbolos.keys():
            tuplas_simbolos.append((simbolo_id, self.simbolos[simbolo_id]['informacion']))
        # ordena por informacion
        tuplas_simbolos = sorted(tuplas_simbolos, key=lambda x: x[1])

        if self.limite > 0:
            tuplas_simbolos = tuplas_simbolos[:self.limite]

        ids = []
        infos = []
        numeracion = []
        cont = 0
        for simbolo in tuplas_simbolos:
            ids.append(simbolo[0])
            infos.append(simbolo[1])
            numeracion.append(cont)
            cont += 1

        entropia_max = truediv(1,len(self.simbolos.keys()))
        print entropia_max

        fig, ax = plt.subplots()
        ax.set_xlim([min(min(infos) - 0.03 * abs(max(infos)-min(infos)), 0), max(infos) + 0.03 * abs(max(infos)-min(infos))])
        ax.set_ylim([-1, len(ids)])
        ax.barh(numeracion, infos, align='center')
        ax.set_yticks(numeracion)
        ax.set_yticklabels(ids, fontsize=17)
        ax.invert_yaxis()
        ax.set_xlabel('Informacion', fontsize=14)
        ax.set_title('Informacion por simbolo vs Entropia de la fuente', fontsize=16)
        sns.set_style("darkgrid")
        box = ax.get_position()
        ax.set_position([0.25, box.y0, box.width - 0.05, box.height])
        ax.plot([self.entropia, self.entropia], [-1, len(ids)], "r--")
        ax.plot([entropia_max, entropia_max], [-1, len(ids)], "g--")
        plt.show()

archivo_entrada = raw_input("Ingrese el archivo de paquetes: ")
limite = raw_input("Ingrese la cantidad maxima de hosts (ENTER: sin limite): ")
print 'Modos:'
print '1. Broadcast vs Unicast'
print '2. Hosts'
modo = raw_input("Ingrese el modo: ")
graph = Graficador(archivo_entrada, modo, limite)
