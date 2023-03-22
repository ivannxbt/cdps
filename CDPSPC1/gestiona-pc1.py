#!/usr/bin/python3
import sys
import subprocess
import os
import json
from lxml import etree
import logging

vmName=["c1","lb"]

def pause():
	p = input("enter")

def create():
    #Servidores a crear
    logger.debug('Comenzando a crear')
    logger.debug('Guardando el numero de servidores en el JSON')
    #if debug :
    #    dictionary = {
    #            "num_serv":  nServ
    #            "debug" : true
    #        }
    #else :
    #    dictionary = {
    #        "num_serv":  nServ
    #    }

    dictionary = {
            "num_serv":  nServ
        }
    with open("gestiona-pc1.json", "w") as outfile:
        json.dump(dictionary,outfile)
    
    #Host configs
    os.system('sudo brctl addbr LAN1')
    os.system('sudo brctl addbr LAN2')
    os.system('sudo ifconfig LAN1 up')
    os.system('sudo ifconfig LAN2 up')
    
    os.system("sudo ifconfig LAN1 10.20.1.3/24")
    os.system("sudo ip route add 10.20.0.0/16 via 10.20.1.1")
    os.system("chmod +rwx cdps-vm-base-pc1.qcow2")

    #Creacion de MVs
    for x in vmName:

        logger.debug('Creando imagen')
        os.system("qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 "+x+".qcow2")
        os.system("cp plantilla-vm-pc1.xml "+x+".xml")

        #Modificacion XML
        logger.debug('Modificando el XML')
        tree = etree.parse('plantilla-vm-pc1.xml')
        root = tree.getroot()
        domain = root.find("domain")
        name = root.find("name")
        name.text = x
        source = root.find("./devices/disk/source")
        ruta = os.path.abspath(x+".qcow2")
        source.set("file", ruta)
        #Creacin de interfaces
        if x == "c1":
            interface = root.find("./devices/interface/source")
            interface.set("bridge", "LAN1")
        if x == "lb":
            interface = root.find("./devices/interface/source")
            interface.set("bridge", "LAN1")
            interface = root.find("./devices/interface/source")
            interface.set("bridge", "LAN2")
        if x == "lb":
            interface_tag = etree.Element("interface", type="bridge")
            devices_tag = root.find("devices")
            interface_tag.text = ""
            devices_tag.append(interface_tag)
            source_tag = etree.Element("source", bridge="LAN2")
            model_tag = etree.Element("model", type="virtio")
            interface_tag.append(source_tag)
            interface_tag.append(model_tag)
        if x == "s1" or x == "s2" or x == "s3" or x == "s4" or x == "s5":
            interface = root.find("./devices/interface/source")
            interface.set("bridge", "LAN2")

        tree.write(x+".xml")

        #Modificacion /etc/hostnames
        logger.debug('Se define las MV '+x+' con el xml')
        os.system("sudo virsh define "+x+".xml")
        logger.debug('Configurando del fichero hostname de '+x)
        os.system("touch hostname") #crear archivo vacío
        hostname = open ("hostname","w+") 
        hostname.write(x) #se escribe el nombre de la VM en el archivo hostname
        hostname.close()
        os.system("chmod +rwx hostname")
        os.system("sudo virt-copy-in -a "+x+".qcow2 hostname /etc") #copiar fichero hostname al directorio /etc de cada VM
        logger.debug('Configuración de los ficheros index.html para '+x)

        #Modificacion index.html
        if x == "s1" or x == "s2" or x == "s3" or x == "s4" or x == "s5":
            logger.debug('Copiando el archivo hostname ya que el contenido de ambos es el mismo')
            os.system("echo '<html><h1>"+x+"</h1></html>' > index.html")
            os.system("sudo virt-copy-in -a "+x+".qcow2 ./index.html /var/www/html/") #error: target ‘/var/www/html’ is not a directory 
        logger.debug('Configura el archivo hosts de '+x)
        os.system("cp /etc/hosts hosts")
        hosts = open ("hosts","w")
        etchosts = open ("/etc/hosts", "r")
        for line in etchosts: #cambie la entrada asociada a la dirección 127.0.1.1 nombre de cada máquina
            if "127.0.0.1" in line:
                hosts.write("127.0.1.1\t"+x+"\n")
            else:
                hosts.write(line)
        hosts.close()
        etchosts.close()

        #Escritura de interfaces
        os.system("sudo virt-copy-in -a "+x+".qcow2 hosts /etc")
        logger.debug('Configurando el archivo interfaces de '+x)
        os.system("touch interfaces")
        interfaces = open("interfaces","w+")
        if x == "lb":
            interfaces.write("auto lo \n")
            interfaces.write("iface lo inet loopback\n")
            interfaces.write("auto eth0 eth1\n")
            interfaces.write("iface eth0 inet static\n")
            interfaces.write("\taddress 10.20.1.1\n")
            interfaces.write("\tnetmask 255.255.255.0\n")
            interfaces.write("\tgateway 10.20.1.1 \n")
            interfaces.write("\tdns-nameservers 10.20.1.1\n")
            interfaces.write("iface eth1 inet static\n")
            interfaces.write("\taddress 10.20.2.1 \n")
            interfaces.write("\tnetmask 255.255.255.0\n")
            interfaces.write("\tgateway 10.20.2.1\n")

        elif x == "c1":
            interfaces.write("auto lo\n")
            interfaces.write("iface lo inet loopback\n")
            interfaces.write("auto eth0\n")
            interfaces.write("iface eth0 inet static\n")
            interfaces.write("\taddress 10.20.1.2 \n")
            interfaces.write("\tnetmask 255.255.255.0 \n")
            interfaces.write("\tgateway 10.20.1.1 \n")

        elif x == "s1":
            interfaces.write("auto lo \n")
            interfaces.write("iface lo inet loopback \n")
            interfaces.write("auto eth0 \n")
            interfaces.write("iface eth0 inet static \n")
            interfaces.write("\taddress 10.20.2.101 \n")
            interfaces.write("\tnetmask 255.255.255.0 \n")
            interfaces.write("\tgateway 10.20.2.1 \n")

        elif x == "s2":
            interfaces.write("auto lo\n")
            interfaces.write("iface lo inet loopback\n")
            interfaces.write("auto eth0 \n")
            interfaces.write("iface eth0 inet static\n")
            interfaces.write("\taddress 10.20.2.102\n")
            interfaces.write("\tnetmask 255.255.255.0 \n")
            interfaces.write("\tgateway 10.20.2.1 \n")

        elif x == "s3":
            interfaces.write("auto lo\n")
            interfaces.write("iface lo inet loopback\n")
            interfaces.write("auto eth0\n")
            interfaces.write("iface eth0 inet static\n")
            interfaces.write("\taddress 10.20.2.103\n")
            interfaces.write("\tnetmask 255.255.255.0\n")
            interfaces.write("\tgateway 10.20.2.1\n")

        elif x == "s4":
            interfaces.write("auto lo\n")
            interfaces.write("iface lo inet loopback\n")
            interfaces.write("auto eth0\n")
            interfaces.write("iface eth0 inet static \n")
            interfaces.write("\taddress 10.20.2.104\n")
            interfaces.write("\tnetmask 255.255.255.0\n")
            interfaces.write("\tgateway 10.20.2.1\n")

        elif x == "s5":
            interfaces.write("auto lo\n")
            interfaces.write("iface lo inet loopback\n")
            interfaces.write("auto eth0\n")
            interfaces.write("iface eth0 inet static\n")
            interfaces.write("\taddress 10.20.2.105\n")
            interfaces.write("\tnetmask 255.255.255.0\n")
            interfaces.write("\tgateway 10.20.2.1\n")
        interfaces.close()
        os.system("sudo virt-copy-in -a "+x+".qcow2 interfaces /etc/network") #copiar el fichero “interfaces” al directorio “/etc/network” de imagen x.qcow2
    logger.debug('Elimindo archivos no necesarios')
    os.system('rm interfaces')
    os.system('rm hostname')
    os.system('rm index.html')
    os.system('rm hosts')

def start() : #arrancar las máquinas virtuales y mostrar su consola

    for x in vmName:
        logger.debug('Arrancando '+x)
        os.system('sudo virsh start '+x)

    
# Se lanzan las máquinas en terminales separados
    
    for x in vmName :
        os.system("xterm -e 'sudo virsh console "+x+"'&")


def startmaq() :
    if len(sys.argv)==3 :
        for x in vmName:
        
            if sys.argv[2]==x:
                logger.debug('Arrancando '+x)
                os.system('sudo virsh start '+x)
                os.system("xterm -e 'sudo virsh console "+x+"'&")
            else :
                logger.debug('No arranca')
    else:
        print('Debe introducir una máquina')


        
def stop(): # parar las máquinas virtuales (sin liberarlas)
    for x in vmName:
        logger.debug('Parando'+x)
        os.system('sudo virsh shutdown '+x)

def stopmaq() :
    if len(sys.argv)==3 :
        for x in vmName:
        
            if sys.argv[2]==x:
                logger.debug('Arrancando '+x)
                os.system('sudo virsh shutdown '+x)
            else :
                logger.debug('No para'+x)
    else:
        print('Debe introducir una máquina')

def destroy(): #liberar el escenario, borrando todos los ficheros creados
    for i in vmName:
        print('Destruyendo '+i)
        os.system('sudo virsh destroy '+i)
        os.system('sudo virsh undefine '+i)
        os.system('rm '+i+'.xml')
        os.system('rm '+i+'.qcow2')
    os.system('sudo ifconfig LAN1 down')
    os.system('sudo ifconfig LAN2 down')
    os.system('sudo brctl delbr LAN1')
    os.system('sudo brctl delbr LAN2')
    # Elimina el archivo JSON  
    os.system('rm gestiona-pc1.json')


    # @main
if len(sys.argv) >= 2:
    logger = logging.getLogger('gestiona-pc1')
    nServ = 2
    #debug=False
    if (len(sys.argv) == 3) & (sys.argv[1] == 'create') :
        logger.debug('El numero de servidores es'+str(sys.argv))
        nServ = int(sys.argv[2])
    else:
        logger.debug('El numero de servidores es 2')
    if os.path.isfile('./gestiona-pc1.json') :
        f = open('gestiona-pc1.json')
        data = json.load(f)
        logger.debug(data)
        nServ = data['num_serv']
        #debug= data['debug']
    else :
        logger = logging.getLogger('error: no hay gestiona-pc1')
    for i in range(1,nServ+1) :
        vmName.append(str('s'+str(i)))

    #if debug :
    #   logging.basicConfig(level=logging.DEBUG)
    #   logger = logging.getLogger('gestiona-pc1')
    #else :
    #   logging.basicConfig(level=logging.INFO)

    if sys.argv[1] == 'create' and len(sys.argv) <= 3:
        create()
    elif sys.argv[1] == 'start' and len(sys.argv) == 2:
        start()
    elif sys.argv[1] == 'stop' and len(sys.argv) == 2:
        stop()
    elif sys.argv[1] == 'destroy' and len(sys.argv) == 2:
        destroy()
    elif sys.argv[1] == 'startmaq' and len(sys.argv) <= 3:
        startmaq()
    elif sys.argv[1] == 'stopmaq' and len(sys.argv) <= 3:
        stopmaq()
    else:
        help()
else:
    print("\nAlgo no ha ido como debería")
