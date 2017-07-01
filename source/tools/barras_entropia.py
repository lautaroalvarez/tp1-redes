import csv, math
from operator import truediv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

INDEX_ORIGEN_IP = 1
INDEX_DESTINO_IP = 3
INDEX_MODO = 5
MODO_BRvsUN = 1
MODO_HOSTS = 2
IPS_MALAS = ['0.0.0.0', 'Broadcast', 'Unicast', '10.210.210.199']

class Graficador():
    def __init__(self, archivo_entrada, limite):
        self.archivo_entrada = archivo_entrada
        self.limite = 0
        if limite != '':
            self.limite = int(limite)
        self.cant_paquetes = 0
        self.hosts = {}
        self.leer_entrada()
        self.calcular_probabilidades()
        self.calcular_entropia()
        # self.mostrar_hosts()
        self.graficar_barras()

    def leer_entrada(self):
        with open(self.archivo_entrada, 'rb') as archivocsv:
            lector = csv.reader(archivocsv)
            primera_linea = 1
            for paquete in lector:
                if primera_linea:
                    primera_linea = 0
                elif int(paquete[INDEX_MODO]) == MODO_HOSTS and paquete[INDEX_ORIGEN_IP] not in IPS_MALAS:
                    self.cant_paquetes += 1
                    if paquete[INDEX_ORIGEN_IP] not in self.hosts.keys():
                        self.hosts[paquete[INDEX_ORIGEN_IP]] = {}
                        self.hosts[paquete[INDEX_ORIGEN_IP]]['cant_paquetes'] = 0
                    self.hosts[paquete[INDEX_ORIGEN_IP]]['cant_paquetes'] += 1

    def calcular_probabilidades(self):
        cant_hosts = len(self.hosts.keys())
        for ip in self.hosts.keys():
            self.hosts[ip]['probabilidad'] = truediv(self.hosts[ip]['cant_paquetes'], self.cant_paquetes)
            self.hosts[ip]['informacion'] = - math.log(self.hosts[ip]['probabilidad'], cant_hosts)

    def calcular_entropia(self):
        self.entropia = 0
        cant_hosts = len(self.hosts.keys())
        for ip in self.hosts.keys():
            self.entropia += self.hosts[ip]['probabilidad'] * self.hosts[ip]['informacion']

    def mostrar_hosts(self):
        for ip in self.hosts.keys():
            print str(ip) + " -> " + str(self.hosts[ip]['probabilidad']) + '  -  ' + str(self.hosts[ip]['informacion'])
        print ''
        print 'ENTROPIA: ' + str(self.entropia)

    def graficar_barras(self):
        tuplas_hosts = []
        for ip in self.hosts.keys():
            tuplas_hosts.append((ip, self.hosts[ip]['informacion']))
        # ordena por informacion
        tuplas_hosts = sorted(tuplas_hosts, key=lambda x: x[1])

        if self.limite > 0:
            tuplas_hosts = tuplas_hosts[:self.limite]

        ips = []
        infos = []
        numeracion = []
        cont = 0
        for host in tuplas_hosts:
            ips.append(host[0])
            infos.append(host[1])
            numeracion.append(cont)
            cont += 1

        fig, ax = plt.subplots()
        ax.set_xlim([min(infos) - 0.03 * abs(max(infos)-min(infos)), max(infos) + 0.03 * abs(max(infos)-min(infos))])
        ax.set_ylim([-1, len(ips)])
        ax.barh(numeracion, infos, align='center')
        ax.set_yticks(numeracion)
        ax.set_yticklabels(ips, fontsize=17)
        ax.invert_yaxis()
        ax.set_xlabel('Informacion', fontsize=14)
        ax.set_title('Informacion por host vs Entropia de la fuente', fontsize=16)
        sns.set_style("darkgrid")
        box = ax.get_position()
        ax.set_position([0.25, box.y0, box.width - 0.05, box.height])
        ax.plot([self.entropia, self.entropia], [-1, len(ips)], "r--")
        plt.show()

archivo_entrada = raw_input("Ingrese el archivo de paquetes: ")
limite = raw_input("Ingrese la cantidad maxima de hosts (ENTER: sin limite): ")
graph = Graficador(archivo_entrada, limite)
