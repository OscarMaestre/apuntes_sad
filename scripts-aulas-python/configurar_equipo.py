import subprocess
import json
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk


def obtener_discos_y_nombres():
  
  comando = """
  [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
  Get-Volume |
      Select DriveLetter, FileSystemLabel |
      ConvertTo-Json
  """

  resultado = subprocess.run(
      [
          "powershell",
          "-Command",
          comando
      ],
      capture_output=True,
      text=True,
      encoding="utf-8"
  )

  volumenes = json.loads(resultado.stdout)

  # Si solo hay un volumen, ConvertTo-Json devuelve un objeto en vez de una lista
  if isinstance(volumenes, dict):
      volumenes = [volumenes]

  tuplas_unidad_nombre_volumen=[]
  for v in volumenes:
      unidad = v["DriveLetter"]
      nombre = v["FileSystemLabel"]
      tuplas_unidad_nombre_volumen.append( (unidad,nombre))
      
  
  return tuplas_unidad_nombre_volumen


#Devuelve el codigo de error. Si el codigo es 0 entonces todo
#fue bien. Cualquier otro codigo es un error
def cambiar_ip_mascara_gateway(ip, mascara, gateway):  
  resultado = subprocess.run(
      [
          "netsh",
          "interface",
          "ip",
          "set",
          "address",
          'name=Ethernet',
          "static",
          ip,
          mascara,
          gateway
      ],
      capture_output=True,
      text=True
  )

  print("Código de salida:", resultado.returncode)
  print("Salida estándar:")
  print(resultado.stdout)
  print("Salida de error:")
  print(resultado.stderr)

#Devuelve una tupla  (error1,error2) con los codigos
#de error de cada cambio de dns
def cambiar_dns(dns1, dns2):
  # Primer DNS
  resultado = subprocess.run(
    [
        "netsh",
        "interface",
        "ip",
        "set",
        "dns",
        "Ethernet",
        "static",
        dns1
    ],
      capture_output=True,
      text=True
  )

  codigo_error_1=resultado.returncode



  resultado = subprocess.run(
        [
            "netsh",
            "interface",
            "ip",
            "add",
            "dns",
            "Ethernet",
            dns2
        ],
        capture_output=True,
        text=True
    )

  codigo_error_2=resultado.returncode
  return (codigo_error_1, codigo_error_2)


class VentanaPrincipal(object):
  def __init__(self):
    self.tuplas_nombre_volumen=obtener_discos_y_nombres()
    self.cantidad_padding_x=10
    self.cantidad_padding_y=self.cantidad_padding_x
    self.numeros_aula=[8,9,10,11,12,13,14,15]
    self.prefijo_aula="AULA-B"
    
    self.mostrar_ventana_principal()
  def get_nombres_discos(self):
    nombres=[]
    for (unidad,nombre) in self.tuplas_nombre_volumen:
      nombres.append(f"{unidad}: {nombre}")
    return nombres
  def _get_numero_con_dos_cifras(self,numero):
    numero_con_dos_cifras=f"{numero:02d}"
    return numero_con_dos_cifras
  
  def get_nombres_aula(self):
    nombres=[]
    for num_aula in self.numeros_aula:
      num_con_ceros=self._get_numero_con_dos_cifras(num_aula)
      texto_anadir=f"{self.prefijo_aula}{num_con_ceros}"
      nombres.append(texto_anadir)
    return nombres
  
  def get_nombres_equipo(self):
    nombres_pc=[]
    for num_equipo in range(0,31):
      if num_equipo==0:
        nombres_pc.append("PC-PROFESOR")
      else:
        num_equipo=self._get_numero_con_dos_cifras(num_equipo)
        nombres_pc.append(f"PC-{num_equipo}")
    return nombres_pc

  def ejecutar_paso_1(self):
    algo_ha_fallado=False
    self.mostrar_mensaje("Cambiando IP...")
    if algo_ha_fallado==False:
      mb.showinfo("OK", "Parece que todo ha ido bien, reinicia el equipo por favor")
  def ejecutar_paso_2(self):
    algo_ha_fallado=False
    self.mostrar_mensaje("Uniendo el equipo al dominio...")
    if algo_ha_fallado==False:
      mb.showinfo("OK", "El equipo se ha unido al dominio, reinicia el equipo por favor.")

  def ejecutar_paso_3(self):
    algo_ha_fallado=False
    self.mostrar_mensaje("Cambiando los permisos en discos...")
    if algo_ha_fallado==False:
      mb.showinfo("OK", "Los permisos se han cambiado correctamente")

  def mostrar_mensaje(self, mensaje):
    print(mensaje)
    self.log.insert(tk.END, mensaje+"\n")
  def mostrar_ventana_principal(self):
    MAX_FILAS=12
    MAX_COLUMNAS=9
    #Ventana principal
    raiz=tk.Tk()
    
    raiz.geometry("700x700")
    raiz.title="Configurador de equipos"
    lista_aulas=ttk.Combobox(raiz, 
                             values=self.get_nombres_aula(),
                             state="readonly",
                             ) 
    lista_aulas.current(0)
    lista_aulas.grid(row=0, column=0, columnspan=5, 
                     sticky="nsew",
                     padx=self.cantidad_padding_x,
                     pady=self.cantidad_padding_y)
    
    self.lista_equipos=ttk.Combobox(raiz, 
                             values=self.get_nombres_equipo(),
                             state="readonly",
                             ) 
    self.lista_equipos.current(0)
    self.lista_equipos.grid(row=0, column=5, columnspan=5, 
                     sticky="nsew",
                     padx=self.cantidad_padding_x,
                     pady=self.cantidad_padding_y)
    
    #Esto da el primer paso y cambia la IP, mascara, nombre del
    #PC y la clave por defecto del profesor
    self.boton_paso_1=tk.Button(master=raiz, text="Paso 1: Cambiar IP,mascara,gateway, clave y nombre de equipo",
                                command=self.ejecutar_paso_1)
    self.boton_paso_1.grid(row=1, column=0, columnspan=12, padx=self.cantidad_padding_x, pady=self.cantidad_padding_y, sticky="nsew")

    #Esto une el equipo al dominio
    self.boton_paso_2=tk.Button(master=raiz, text="Paso 2: Unir el equipo al dominio", command=self.ejecutar_paso_2)
    self.boton_paso_2.grid(row=3, column=0, columnspan=12, padx=self.cantidad_padding_x, pady=self.cantidad_padding_y, sticky="nsew")


    label_discos=tk.Label(master=raiz, text="Antes de pulsar el botón de cambiar permisos en discos...\nPOR FAVOR ASEGÚRATE DE QUE\n INDICAS ARRIBA EL AULA CORRECTA", font=("Arial", 16, "bold"))
    label_discos.grid(row=5, column=0, columnspan=12, padx=self.cantidad_padding_x, pady=self.cantidad_padding_y)

    label_manana=tk.Label(master=raiz, text="Disco de mañana")
    label_manana.grid(row=6, column=0, columnspan=2, padx=self.cantidad_padding_x, pady=self.cantidad_padding_y)
    
    self.disco_manana=ttk.Combobox(master=raiz, values=self.get_nombres_discos(), state="readonly")
    self.disco_manana.grid(row=6, column=2,columnspan=2,padx=self.cantidad_padding_x, pady=self.cantidad_padding_y)
    #Y cambiamos los permisos de los discos
    self.disco_manana.current(0)


    label_tarde=tk.Label(master=raiz, text="Disco de tarde")
    label_tarde.grid(row=6, column=5, columnspan=2, padx=self.cantidad_padding_x, pady=self.cantidad_padding_y)
    
    self.disco_tarde=ttk.Combobox(master=raiz, values=self.get_nombres_discos(), state="readonly")
    self.disco_tarde.grid(row=6, column=7,columnspan=2,padx=self.cantidad_padding_x, pady=self.cantidad_padding_y)
    self.disco_tarde.current(0)
    #Y cambiamos los permisos de los discos

    self.boton_paso_3=tk.Button(master=raiz, text="Paso 3: Cambiar permisos en discos", command=self.ejecutar_paso_3)
    self.boton_paso_3.grid(row=8, column=0, columnspan=12, padx=self.cantidad_padding_x, pady=self.cantidad_padding_y, sticky="nsew")
    

    self.log=tk.Text(master=raiz)
    self.log.grid(row=9, column=0, columnspan=12, padx=self.cantidad_padding_x, pady=self.cantidad_padding_y, sticky="we", rowspan=1)
    #Por ahora cada fila pesa igual
    for fila in range(0, MAX_FILAS):
      raiz.grid_rowconfigure(fila, weight=1)
    #Y configuramos también el peso de las columnas
    for columna in range(0, MAX_COLUMNAS):
        raiz.grid_columnconfigure(columna, weight=1)
    #Ejecutamos el bucle de gestión de eventos
    self.mostrar_mensaje("Listo.")
    raiz.mainloop()

if __name__=="__main__":
  v=VentanaPrincipal()