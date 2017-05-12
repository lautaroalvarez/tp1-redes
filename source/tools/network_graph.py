import csv, os

## ESTRUCTURA NODO
# - ID: numero unico, se usa para compararlos
# - IP
# - PESO: cantidad de paquetes que envio

## ESTRUCTURA ARISTA
# - IP
# - ARISTAS (arreglo)
#   - IP
#   - PESO: cantidad de paquetes que se enviaron entre ambos

#-- un nodo suma peso si es el origen de un paquete
SUMA_ORIGEN = 1
#-- un nodo suma peso si es el destino de un paquete
SUMA_DESTINO = 2

#-- indice de columna del identificador de origen (ip o mac)
INDEX_ORIGEN = 1
#-- indice de columna del identificador de destino (ip o mac)
INDEX_DESTINO = 2

NODO_MAX_HEIGHT = 2
NODO_MIN_FONTSIZE = 6
NODO_MAX_FONTSIZE = 20

ARISTA_MIN_WIDTH = 0.2
ARISTA_MAX_WIDTH = 3
ARISTA_COLOR = 'black'

class graficador:
    def __init__(self, input_file):
        self.nodos = {}
        self.aristas = {}
        self.input_file = input_file
        self.suma_peso = SUMA_ORIGEN

        self.maximo_peso = 0
        self.importarDatos()

    def importarDatos(self):
        datos_entrada = csv.reader(open(input_file, "rb"))
        header = 1
        ultimo_id = 0
        for paquete in datos_entrada:
            if header:
                header = 0
            else:
                #----- NODO ORIGEN
                #-- si no existe el nodo se lo crea e inicializa
                if paquete[INDEX_ORIGEN] not in self.nodos.keys():
                    ultimo_id += 1
                    self.nodos[paquete[INDEX_ORIGEN]] = {}
                    self.nodos[paquete[INDEX_ORIGEN]]['id'] = ultimo_id
                    self.nodos[paquete[INDEX_ORIGEN]]['ip'] = paquete[INDEX_ORIGEN]
                    self.nodos[paquete[INDEX_ORIGEN]]['peso'] = 0
                if self.suma_peso == SUMA_ORIGEN:
                    #-- se suma el paquete al nodo
                    self.nodos[paquete[INDEX_ORIGEN]]['peso'] += 1
                    #-- se guarda el maximo peso
                    if self.nodos[paquete[INDEX_ORIGEN]]['peso'] > self.maximo_peso:
                        self.maximo_peso = self.nodos[paquete[INDEX_ORIGEN]]['peso']
                #-- se guarda como minimo id de los dos nodos
                nodo_min = self.nodos[paquete[INDEX_ORIGEN]]

                #----- NODO DESTINO
                #-- si no existe el nodo se lo crea e inicializa
                if paquete[INDEX_DESTINO] not in self.nodos.keys():
                    ultimo_id += 1
                    self.nodos[paquete[INDEX_DESTINO]] = {}
                    self.nodos[paquete[INDEX_DESTINO]]['id'] = ultimo_id
                    self.nodos[paquete[INDEX_DESTINO]]['ip'] = paquete[INDEX_DESTINO]
                    self.nodos[paquete[INDEX_DESTINO]]['peso'] = 0
                if self.suma_peso == SUMA_DESTINO:
                    #-- se suma el paquete al nodo
                    self.nodos[paquete[INDEX_DESTINO]]['peso'] += 1
                    #-- se guarda el maximo peso
                    if self.nodos[paquete[INDEX_DESTINO]]['peso'] > self.maximo_peso:
                        self.maximo_peso = self.nodos[paquete[INDEX_DESTINO]]['peso']
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

    def exportarGrafo(self, output_file):
        f = open('graph.tmp','w')
        f.writelines('digraph G {\n')
        for i in self.nodos:
            #-- calcula tamanos de nodo y fuentes
            peso_nodo = self.nodos[i]['peso']
            height = peso_nodo * NODO_MAX_HEIGHT / self.maximo_peso
            font_size = (peso_nodo * (NODO_MAX_FONTSIZE - NODO_MIN_FONTSIZE) / self.maximo_peso) + NODO_MIN_FONTSIZE
            f.writelines('"' + self.nodos[i]['ip'] + '" [label="' + self.nodos[i]['ip'] + '",fontsize=' + str(font_size) + ',height=' + str(height) + ',regular=true]\n')
        for i in self.aristas:
            for j in self.aristas[i]['aristas']:
                #-- calcula ancho de aristas1
                peso_arista = self.aristas[i]['aristas'][j]['peso']
                width = (peso_arista * (ARISTA_MAX_WIDTH - ARISTA_MIN_WIDTH) / self.maximo_peso) + ARISTA_MIN_WIDTH
                f.writelines('"' + self.aristas[i]['ip'] + '" -> "' + self.aristas[i]['aristas'][j]['ip'] + '" [dir=none,penwidth=' + str(width) + ',color=' + ARISTA_COLOR + '];\n')
        f.writelines('}')
        f.close()
        os.system("dot -Tpng -o" + output_file + ".png graph.tmp")
        os.system("rm graph.tmp")


input_file = raw_input("Ingrese el archivo de entrada: ")
output_file = raw_input("Ingrese el nombre de la imagen de salida: ")

graficador_obj = graficador(input_file)
graficador_obj.exportarGrafo(output_file)
