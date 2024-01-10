#!/usr/bin/python3

from ipaddress import IPv4Network
from random import randint, choice,shuffle
from utilidades.ip.nuevo_generador import Generator
from utilidades.netplan.netplan import NetplanGenerator



HACER_NAT="""
table ip {nombretabla} {{
    chain  {cadenanatentrada} {{
        type nat hook prerouting priority 0; policy accept;
    }}
    chain {cadenanatsalida}  {{
        type nat hook postrouting priority 100; policy accept;
        oifname "{tarjetasalida}" masquerade
    }}
}}

"""
HACER_FILTRADO="""
table ip {nombrefiltrado} {{
    {cadenas}
}}
"""

CADENA_FILTRADO="""
    chain {nombrecadena} {{
        type filter hook {hook} priority 0;policy accept;
        {reglas}
    }}
"""

ACCION_ACEPTAR   = "accept"
ACCION_DESCARTAR = "drop"
ACCION_REGISTRAR = "log"
ACCION_CONTAR    = "counter"

DIC_COMENTARIOS={
    ACCION_ACEPTAR:"Aceptar",
    ACCION_DESCARTAR:"Descartar",
    ACCION_REGISTRAR:"Registrar",
    ACCION_CONTAR:"Contabilizar"
}
def get_ip_origen(ip):
    return f"saddr {ip}"

def get_ip_destino(ip):
    return f"daddr {ip}"

def get_protocolo(protocolo, lugar_puerto, lista_puertos):
    if len(lista_puertos==1):
        return f"{protocolo} {lugar_puerto} {lista_puertos[0]}"
    else:
        puertos=",".join(lista_puertos)
        return f"{protocolo} {lugar_puerto}  {puertos}"

def generar_comentario(ip_origen, ip_destino, accion, puerto_origen=None, puerto_destino=None):
    accion=DIC_COMENTARIOS[accion]
    if puerto_origen==None:
        desde=f"tráfico desde la IP {ip_origen}"
    else:
        origenes=",".join(puerto_origen)
        desde=f"tráfico desde la IP {ip_origen}"
def de_ip_a_ip(ip_origen, ip_destino, accion, puerto_origen=None, puerto_destino=None):
    lineas=[]
    if accion==ACCION_ACEPTAR:
        comentario=f"#Aceptar tráfico desde {ip_origen} a {ip_destino}"
        elementos_regla=[
            "ip",
            get_ip_origen(ip_origen),
            
        ]

tablas_nat=[
    ("operacionesnat", "natentrada", "natsalida"),
    ("op_nat", "traficonatentrada", "traficonatsalida"),
]

def append_tabs(cad, prefix_char="\t", num_of_prefix_chars=1):
    lines=cad.split("\n")
    tabs=prefix_char*num_of_prefix_chars
    lines_with_tabs=[f"{tabs}{line}" for line in lines]
    return "\n".join(lines_with_tabs)
    

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
        return generador_netplan.get_str_with_tabs()
    
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


    def _get_operaciones_nat(self):
        nombres_nat=choice(tablas_nat)
        return HACER_NAT.format(nombretabla=nombres_nat[0], 
                                cadenanatentrada=nombres_nat[1], 
                                cadenanatsalida=nombres_nat[2],
                                tarjetasalida=self.tarjeta_externa)

    def _get_nf_conf(self):
        nat=self._get_operaciones_nat()
        with_tabs=append_tabs(nat)
        return with_tabs
    
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
            f"Puerta de enlace   :{self.gw_windows}",
            "","","",
            "Configuración de Ubuntu",
            "-------------------------",
            "","","",
            "Fichero de netplan",
            "~~~~~~~~~~~~~~~~~~~~~~~~",
            "","Fichero `/etc/netplan/00-installer.yaml` de Ubuntu::","",
            self.fichero_netplan,
            "","","",
            "Fichero `/etc/nftables.conf`",
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
            "","","",
            self._get_nf_conf()
            
            
        ]
        return "\n".join(info)

        

        
    

def test1():
    g1=GeneradorEjerciciosNFT()
    g1.generar_ejercicio()
    print(g1)
    
if __name__=="__main__":
    test1()