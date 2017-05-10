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

SUMA_ORIGEN = 1
SUMA_DESTINO = 2

INDEX_ORIGEN = 1
INDEX_DESTINO = 2

class graficador:
    def __init__(self, input_file):
        self.nodos = {}
        self.aristas = {}
        self.input_file = input_file
        self.suma_peso = SUMA_DESTINO

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
            f.writelines('"' + self.nodos[i]['ip'] + '" [label="' + self.nodos[i]['ip'] + '"]\n')
        for i in self.aristas:
            for j in self.aristas[i]['aristas']:
                f.writelines('"' + self.aristas[i]['ip'] + '" -> "' + self.aristas[i]['aristas'][j]['ip'] + '" [dir=none,penwidth=0.5,color=black];\n')
        f.writelines('}')
        f.close()
        os.system("dot -Tjpg -o" + output_file + ".jpg graph.tmp")
        os.system("rm graph.tmp")


input_file = raw_input("Ingrese el archivo de entrada: ")
output_file = raw_input("Ingrese el nombre de la imagen de salida: ")

graficador_obj = graficador(input_file)
graficador_obj.exportarGrafo(output_file)
