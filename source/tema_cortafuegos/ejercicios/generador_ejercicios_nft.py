#!/usr/bin/python3

from ipaddress import IPv4Network
from random import randint, choice,shuffle
from utilidades.ip.nuevo_generador import Generator
from utilidades.netplan.netplan import NetplanGenerator

class GeneradorEjerciciosNFT(object):
    def __init__(self):
        self.generador = Generator()
        self.tarjetas  = ["enp0s3", "enp0s8"]
    
    def _generar_red_interna(self):
        #Se ejecuta al azar un método que genera una dirección
        #de red privada
        metodos=[
            Generator.generar_direccion_de_red_privada_de_clase_b,
            Generator.generar_direccion_de_red_privada_de_clase_c,
        ]
        metodo_azar=choice(metodos)
        return metodo_azar()

    def generar_netplan_ubuntu(self):
        prefijo_interno=self.red_interna.prefixlen
        prefijo_externo="16"
        direccion_ip_interna=f"{self.ip_interna_ubuntu}/{prefijo_interno}"
        direccion_ip_externa=f"{self.ip_externa_ubuntu}/{prefijo_externo}"
        
        generador_netplan=NetplanGenerator()
        generador_netplan.add_wired_network_card_with_ip(self.tarjeta_interna,[direccion_ip_interna], [])
        generador_netplan.add_wired_network_card_with_ip(self.tarjeta_externa,[direccion_ip_externa], ["10.14.0.254"])
        return str(generador_netplan)
    
    def generar_ejercicio(self):
        #Prefijo de la 10.14
        prefijo_red_14="0000101000001110"
        shuffle(self.tarjetas)

        self.tarjeta_interna   = self.tarjetas[0]
        self.tarjeta_externa   = self.tarjetas[1]
        self.red_interna       = self._generar_red_interna()
        self.red_externa       = Generator.generar_direccion_de_red_a_partir_de_prefijo_binario(prefijo_red_14)
        self.ip_interna_ubuntu = list(self.red_interna.hosts())[0]
        self.ip_externa_ubuntu = list(self.red_externa.hosts())[0]
        self.fichero_netplan   = self.generar_netplan_ubuntu()

        self.ip_windows      = list(self.red_interna.hosts())[8]
        self.mascara_windows = self.red_interna.netmask
        self.gw_windows      = self.ip_interna_ubuntu

    def __str__(self) -> str:
        info=[
            f"Red interna        : {self.red_interna}",
            f"Tarjeta interna    : {self.tarjeta_interna}",
            f"IP Ubuntu          : {self.ip_interna_ubuntu}",
            #f"Red externa        : {self.red_externa}",
            f"Tarjeta externa    : {self.tarjeta_externa}",
            f"IP externa Ubuntu  : {self.ip_externa_ubuntu}"
            "","","",
            "Configuración de Windows",
            "--------------------------",
            f"IP Windows         :{self.ip_windows}",
            f"Máscara Windows    :{self.mascara_windows}",
            f"Puerta de enlace   :{self.gw_windows}"
            "","","",
            "Configuración de Ubuntu",
            "-------------------------",
            "","","",
            "Fichero de netplan",
            "~~~~~~~~~~~~~~~~~~~~~~~~",
            self.fichero_netplan
            
            
        ]
        return "\n".join(info)

        

        
    

def test1():
    g1=GeneradorEjerciciosNFT()
    g1.generar_ejercicio()
    print(g1)
    
if __name__=="__main__":
    test1()