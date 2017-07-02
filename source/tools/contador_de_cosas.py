import csv, math

INDEX_ORIGEN_IP = 1
INDEX_DESTINO_IP = 3
INDEX_MODO = 5
MODO_BRvsUN = 1
MODO_HOSTS = 2
IPS_MALAS = ['0.0.0.0', 'Broadcast', 'Unicast']

class Contador():
    def __init__(self, archivo_entrada):
        self.archivo_entrada = archivo_entrada
        self.hosts = {}
        self.leer_entrada()
        # self.mostrar_hosts()
        # self.graficar_barras()

    def leer_entrada(self):
        with open(self.archivo_entrada, 'rb') as archivocsv:
            lector = csv.reader(archivocsv)
            primera_linea = 1
            for paquete in lector:
                if primera_linea:
                    primera_linea = 0
                elif int(paquete[INDEX_MODO]) == MODO_HOSTS and paquete[INDEX_ORIGEN_IP] not in IPS_MALAS:
                    #- HOST ORIGEN
                    #- si no esta el host lo agrega
                    if paquete[INDEX_ORIGEN_IP] not in self.hosts.keys():
                        self.hosts[paquete[INDEX_ORIGEN_IP]] = {}
                        self.hosts[paquete[INDEX_ORIGEN_IP]]['mensajes_a'] = {}
                        self.hosts[paquete[INDEX_ORIGEN_IP]]['mensajes_de'] = {}
                    #- si no esta el host destino lo agrega
                    if paquete[INDEX_DESTINO_IP] not in self.hosts[paquete[INDEX_ORIGEN_IP]]['mensajes_a'].keys():
                        self.hosts[paquete[INDEX_ORIGEN_IP]]['mensajes_a'][paquete[INDEX_DESTINO_IP]] = 0
                    #- suma 1 mensaje al destino
                    self.hosts[paquete[INDEX_ORIGEN_IP]]['mensajes_a'][paquete[INDEX_DESTINO_IP]] += 1

                    #- HOST DESTINO
                    #- si no esta el host lo agrega
                    if paquete[INDEX_DESTINO_IP] not in self.hosts.keys():
                        self.hosts[paquete[INDEX_DESTINO_IP]] = {}
                        self.hosts[paquete[INDEX_DESTINO_IP]]['mensajes_a'] = {}
                        self.hosts[paquete[INDEX_DESTINO_IP]]['mensajes_de'] = {}
                    #- si no esta el host origen lo agrega
                    if paquete[INDEX_ORIGEN_IP] not in self.hosts[paquete[INDEX_DESTINO_IP]]['mensajes_de'].keys():
                        self.hosts[paquete[INDEX_DESTINO_IP]]['mensajes_de'][paquete[INDEX_ORIGEN_IP]] = 0
                    #- suma 1 mensaje al origen
                    self.hosts[paquete[INDEX_DESTINO_IP]]['mensajes_de'][paquete[INDEX_ORIGEN_IP]] += 1

    def mostrar_hosts(self):
        for ip in self.hosts.keys():
            print ip
            for destino_ip in self.hosts[ip]['mensajes_a'].keys():
                print '   ' + destino_ip + ' [' + str(self.hosts[ip]['mensajes_a'][destino_ip]) + ']'

    def envios_entre_hosts(self, hosts):
        text = '\\begin{tabular}{| c |'
        for ip in hosts:
            text += ' c |'
        text += '}'
        print text
        print '\hline'
        text = ''
        for ip in hosts:
            text += '& \\textbf{' + ip + '} '
        text += ' \\\\ \\hline'
        print text
        for ip in hosts:
            text = '\\textbf{' + ip + '}'
            for destino_ip in hosts:
                if destino_ip == ip:
                    text += ' & -'
                elif destino_ip in self.hosts[ip]['mensajes_a'].keys():
                    text += ' & ' + str(self.hosts[ip]['mensajes_a'][destino_ip])
                else:
                    text += ' & 0'
            text += ' \\\\ \hline'
            print text
        print '\\end{tabular}'

    def mostrar_preguntas_por(self, listar_hosts, host):
        print 'Mensajes de hosts que preguntaron por el host ' + host
        total = 0
        for origen_ip in self.hosts[host]['mensajes_de']:
            total += self.hosts[host]['mensajes_de'][origen_ip]
            if listar_hosts:
                print '  ' + origen_ip + ' -> ' + str(self.hosts[host]['mensajes_de'][origen_ip])
        print 'Cantidad total: ' + str(total)
        print 'Distintos hosts: ' + str(len(self.hosts[host]['mensajes_de']))

    def mostrar_preguntas_de(self, listar_hosts, host):
        print 'Mensajes que envio el host ' + host
        total = 0
        for destino_ip in self.hosts[host]['mensajes_a']:
            total += self.hosts[host]['mensajes_a'][destino_ip]
            if listar_hosts:
                print '  ' + destino_ip + ' -> ' + str(self.hosts[host]['mensajes_a'][destino_ip])
        print 'Cantidad total: ' + str(total)
        print 'Distintos hosts: ' + str(len(self.hosts[host]['mensajes_a']))

    def mostrar_preguntas_en_comun(self, listar_hosts, hosts):
        texto = 'Host por los cuales preguntaron'
        for ip in hosts:
            texto += ' - ' + ip
        print texto
        total = 0
        host = hosts[0]
        hosts_en_comun = []
        for destino_ip in self.hosts[host]['mensajes_a']:
            comun = True
            for host_ip in hosts:
                if destino_ip not in self.hosts[host_ip]['mensajes_a'].keys():
                    comun = False
            if comun:
                hosts_en_comun.append(destino_ip)
            if listar_hosts:
                print '  ' + destino_ip
        print 'Cantidad total: ' + str(len(hosts_en_comun))

    def mostrar_host_que_preguntaron_por_todos(self, listar_hosts, hosts):
        texto = 'Host que preguntaron por todos los hostsde la lista'
        for ip in hosts:
            texto += ' - ' + ip
        print texto
        total = 0
        host = hosts[0]
        hosts_en_comun = []
        for origen_ip in self.hosts[host]['mensajes_de']:
            comun = True
            for host_ip in hosts:
                if origen_ip not in self.hosts[host_ip]['mensajes_de'].keys():
                    comun = False
            if comun:
                hosts_en_comun.append(origen_ip)
            if listar_hosts:
                print '  ' + origen_ip
        print 'Cantidad total: ' + str(len(hosts_en_comun))


archivo_entrada = raw_input("Ingrese el archivo de paquetes: ")
contador = Contador(archivo_entrada)
# hosts_a_ver = ['10.210.210.199', '10.210.126.212']
# contador.envios_entre_hosts(hosts_a_ver)
# contador.mostrar_preguntas_por(False, '10.210.126.212')
# contador.mostrar_preguntas_por(False, '10.210.210.199')
# contador.mostrar_preguntas_de(False, '10.210.126.212')
# contador.mostrar_preguntas_de(False, '10.210.210.199')
contador.mostrar_preguntas_en_comun(False, ['10.210.210.199', '10.210.126.212'])
contador.mostrar_host_que_preguntaron_por_todos(False, ['10.210.210.199', '10.210.126.212'])
