import socket

FICHERO_CONEXIONES="conexiones.txt"


def conectar_con(host, puerto):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(puerto)))
        print("BIEN:"+host+" puerto TCP "+puerto)
    except TimeoutError:
        print("MAL :"+host+" puerto TCP "+puerto)

def probar_conexiones():
    with open("conexiones.txt") as fichero:
        lineas=fichero.readlines()
        contador=1
        for l in lineas:
            trozos=l.split(":")
            host=trozos[0].strip()
            puerto=trozos[1].strip()
            conectar_con(host, puerto)
            contador=contador+1



try:
    probar_conexiones()
except FileNotFoundError:
    print("No tienes el fichero "+FICHERO_CONEXIONES)
    
input("Pulsa una tecla para cerrar");
