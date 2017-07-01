import csv, os

## ESTRUCTURA NODO
# - ID: numero unico, se usa para compararlos
# - IP
# - IMPORTANCIA: numero que trata de reflejar que tan importante es el nodo

## ESTRUCTURA ARISTA
# - IP
# - ARISTAS (arreglo)
#   - IP
#   - PESO: cantidad de paquetes que se enviaron entre ambos

#-- indice de columna del identificador de origen (ip o mac)
INDEX_ORIGEN = 1
#-- indice de columna del identificador de destino (ip o mac)
INDEX_DESTINO = 3
#-- indice de columna del identificador de modo
INDEX_MODO = 5

NODO_MAX_HEIGHT = 2
NODO_MIN_FONTSIZE = 10
NODO_MAX_FONTSIZE = 20

ARISTA_MIN_WIDTH = 0.2
ARISTA_MAX_WIDTH = 3
ARISTA_COLOR = 'black'

MODO_BRvsUN = 1
MODO_HOSTS = 2
IP_DEFAULT = '0.0.0.0'

IMPORTANCIA_ORIGEN = 0
IMPORTANCIA_DESTINO = 0
IMPORTANCIA_VARIEDAD_ORIGENES = 10
IMPORTANCIA_VARIEDAD_DESTINOS = 2
NODOS_OBLIGATORIOS = ['10.210.126.212', '10.210.210.2', '10.210.210.1', '10.210.210.56', '10.210.210.41', '10.210.144.75', '10.210.210.248', '10.210.210.249']

class graficador:
    def __init__(self, input_file, modo):
        self.nodos = {}
        self.aristas = {}
        self.input_file = input_file
        self.modo = modo
        self.filtra_limite = False

        self.maxima_importancia = 0
        self.maximo_peso_arista = 0
        self.importarDatos()

    def importarDatos(self):
        datos_entrada = csv.reader(open(input_file, "rb"))
        header = 1
        ultimo_id = 0
        for paquete in datos_entrada:
            if header:
                header = 0
            elif int(paquete[INDEX_MODO]) == MODO_HOSTS and not (paquete[INDEX_ORIGEN] == IP_DEFAULT):
                #----- NODO ORIGEN
                #-- si no existe el nodo se lo crea e inicializa
                if paquete[INDEX_ORIGEN] not in self.nodos.keys():
                    ultimo_id += 1
                    self.nodos[paquete[INDEX_ORIGEN]] = {}
                    self.nodos[paquete[INDEX_ORIGEN]]['id'] = ultimo_id
                    self.nodos[paquete[INDEX_ORIGEN]]['ip'] = paquete[INDEX_ORIGEN]
                    self.nodos[paquete[INDEX_ORIGEN]]['origen_de'] = []
                    self.nodos[paquete[INDEX_ORIGEN]]['destino_de'] = []
                    self.nodos[paquete[INDEX_ORIGEN]]['cant_origenes'] = 0
                    self.nodos[paquete[INDEX_ORIGEN]]['cant_destinos'] = 0
                #-- sumo 1 a la cantidad de veces que fue origen
                self.nodos[paquete[INDEX_ORIGEN]]['cant_origenes'] += 1
                #-- se guarda el destino al que le mando el paquete (si es que no lo tenia guardado)
                if paquete[INDEX_DESTINO] not in self.nodos[paquete[INDEX_ORIGEN]]['origen_de']:
                    self.nodos[paquete[INDEX_ORIGEN]]['origen_de'].append(paquete[INDEX_DESTINO])

                #-- se guarda como minimo id de los dos nodos
                nodo_min = self.nodos[paquete[INDEX_ORIGEN]]

                #----- NODO DESTINO
                #-- si no existe el nodo se lo crea e inicializa
                if paquete[INDEX_DESTINO] not in self.nodos.keys():
                    ultimo_id += 1
                    self.nodos[paquete[INDEX_DESTINO]] = {}
                    self.nodos[paquete[INDEX_DESTINO]]['id'] = ultimo_id
                    self.nodos[paquete[INDEX_DESTINO]]['ip'] = paquete[INDEX_DESTINO]
                    self.nodos[paquete[INDEX_DESTINO]]['origen_de'] = []
                    self.nodos[paquete[INDEX_DESTINO]]['destino_de'] = []
                    self.nodos[paquete[INDEX_DESTINO]]['cant_origenes'] = 0
                    self.nodos[paquete[INDEX_DESTINO]]['cant_destinos'] = 0
                #-- sumo 1 a la cantidad de veces que fue destino
                self.nodos[paquete[INDEX_DESTINO]]['cant_destinos'] += 1
                #-- se guarda el origen que le mando el paquete (si es que no lo tenia guardado)
                if paquete[INDEX_ORIGEN] not in self.nodos[paquete[INDEX_DESTINO]]['destino_de']:
                    self.nodos[paquete[INDEX_DESTINO]]['destino_de'].append(paquete[INDEX_ORIGEN])

                #-- se verifica si es el de minimo id de los dos nodos
                if nodo_min['id'] > self.nodos[paquete[INDEX_DESTINO]]['id']:
                    nodo_max = nodo_min
                    nodo_min = self.nodos[paquete[INDEX_DESTINO]]
                else:
                    nodo_max = self.nodos[paquete[INDEX_DESTINO]]

                #----- ARISTA
                #-- si no existe el nodo se lo crea e inicializa
                if nodo_min['ip'] not in self.aristas.keys():
                    self.aristas[nodo_min['ip']] = {}
                    self.aristas[nodo_min['ip']]['ip'] = nodo_min['ip']
                    self.aristas[nodo_min['ip']]['aristas'] = {}
                #-- si no existe la arista entre los nodos se la crea e inicializa
                if nodo_max['ip'] not in self.aristas[nodo_min['ip']]['aristas'].keys():
                    self.aristas[nodo_min['ip']]['aristas'][nodo_max['ip']] = {}
                    self.aristas[nodo_min['ip']]['aristas'][nodo_max['ip']]['ip'] = nodo_max['ip']
                    self.aristas[nodo_min['ip']]['aristas'][nodo_max['ip']]['peso'] = 0
                #-- se suma el paquete a la arista
                self.aristas[nodo_min['ip']]['aristas'][nodo_max['ip']]['peso'] += 1

    def calcularImportancia(self):
        for ip in self.nodos:
            imp_por_origen = IMPORTANCIA_ORIGEN * self.nodos[ip]['cant_origenes']
            imp_por_destino = IMPORTANCIA_DESTINO * self.nodos[ip]['cant_destinos']
            imp_por_variedad_origenes = IMPORTANCIA_VARIEDAD_ORIGENES * len(self.nodos[ip]['origen_de'])
            imp_por_variedad_destinos = IMPORTANCIA_VARIEDAD_DESTINOS * len(self.nodos[ip]['destino_de'])
            self.nodos[ip]['importancia'] = imp_por_origen + imp_por_destino + imp_por_variedad_origenes + imp_por_variedad_destinos
            if self.nodos[ip]['importancia'] > self.maxima_importancia:
                self.maxima_importancia = self.nodos[ip]['importancia']

    def filtrarCantidad(self, limite):
        self.filtra_limite = True

        tuplas_nodos = []
        for ip in self.nodos:
            tuplas_nodos.append((ip, self.nodos[ip]['importancia']))
        tuplas_nodos = sorted(tuplas_nodos, key=lambda x: -x[1])
        tuplas_nodos = tuplas_nodos[:limite]

        self.nodos_a_mostrar = []
        for tupla in tuplas_nodos:
            self.nodos_a_mostrar.append(tupla[0])
        for ip_obligada in NODOS_OBLIGATORIOS:
            self.nodos_a_mostrar.append(ip_obligada)

    def calcularMaximoPeso(self):
        #- calcula el maximo peso (dentro de los)
        for origen_ip in self.aristas:
            for destino_ip in self.aristas[origen_ip]['aristas']:
                if not self.filtra_limite or (origen_ip in self.nodos_a_mostrar and destino_ip in self.nodos_a_mostrar):
                    if self.maximo_peso_arista < self.aristas[origen_ip]['aristas'][destino_ip]['peso']:
                        self.maximo_peso_arista = self.aristas[origen_ip]['aristas'][destino_ip]['peso']

    def exportarGrafo(self, output_file):
        f = open('graph.tmp','w')
        f.writelines('digraph G {\n')
        for ip in self.nodos:
            if not self.filtra_limite or ip in self.nodos_a_mostrar:
                #-- calcula tamanos de nodo y fuentes
                importancia_nodo = self.nodos[ip]['importancia']
                height = importancia_nodo * NODO_MAX_HEIGHT / self.maxima_importancia
                font_size = (importancia_nodo * (NODO_MAX_FONTSIZE - NODO_MIN_FONTSIZE) / self.maxima_importancia) + NODO_MIN_FONTSIZE
                f.writelines('"' + ip + '" [label="' + ip + '",fontsize=' + str(font_size) + ',height=' + str(height) + ',regular=true]\n')
        for origen_ip in self.aristas:
            for destino_ip in self.aristas[origen_ip]['aristas']:
                if not self.filtra_limite or (origen_ip in self.nodos_a_mostrar and destino_ip in self.nodos_a_mostrar):
                    #-- calcula ancho de aristas1
                    peso_arista = self.aristas[origen_ip]['aristas'][destino_ip]['peso']
                    width = (peso_arista * (ARISTA_MAX_WIDTH - ARISTA_MIN_WIDTH) / self.maximo_peso_arista) + ARISTA_MIN_WIDTH
                    f.writelines('"' + origen_ip + '" -> "' + destino_ip + '" [dir=none,penwidth=' + str(width) + ',color=' + ARISTA_COLOR + '];\n')
        f.writelines('}')
        f.close()
        os.system("dot -Tpng -o" + output_file + ".png graph.tmp")
        os.system("rm graph.tmp")


input_file = raw_input("Ingrese el archivo de entrada: ")
output_file = raw_input("Ingrese el nombre de la imagen de salida: ")
limite = raw_input("Ingrese la cantidad maxima de hosts (ENTER: sin limite): ")

graficador_obj = graficador(input_file, MODO_HOSTS)
graficador_obj.calcularImportancia()
if limite != '':
    graficador_obj.filtrarCantidad(int(limite))
graficador_obj.calcularMaximoPeso()
graficador_obj.exportarGrafo(output_file)
