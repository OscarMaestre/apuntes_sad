#!/usr/bin/python3

from utilidades.ficheros.GestorFicheros import GestorFicheros

gf=GestorFicheros()
lineas_fichero=gf.get_lineas_fichero("contenidos.txt")

for l in lineas_fichero:
    if l=="":
        continue
    nueva=l.replace("\n", "-------------------------------------------------------------")
    print(l+"\n-----------------------------------------------------------------------------------------------\n\n")