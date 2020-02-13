Implantación de soluciones de alta disponibilidad
============================================================


Definición y objetivos.
-----------------------------------------------------------------------------------------------
En el tema "Pautas de seguridad informática" definíamos disponibilidad  de la siguiente manera: *capacidad de respuesta a una peticiones con las mínimas pausas por causas involuntarias* .

También decíamos que se mide la disponibilidad de un SI en "nueves".

* Se dice que un SI ofrece una disponibilidad de "2 nueves", si está disponible el 99% del tiempo.
* Se dice que un SI ofrece una disponibilidad de "3 nueves", si lo está al 99.9%.
* Se dice que un SI ofrece una disponibilidad de "4 nueves" si lo está al 99.99%.
* Se dice que un SI ofrece una disponibilidad de "5 nueves" si lo está al 99.999%

Evidentemente lograr una disponibilidad del 100% es imposible pero en este bloque analizaremos como lograr la máxima disponibilidad en un entorno informático.


Virtualización de sistemas.
-----------------------------------------------------------------------------------------------
Muchos sistemas operativos que tengan que trabajar como invitados pueden beneficiarse de ciertas posibilidades instalando un software que VirtualBox llama "Guest additions".

Las "Guest additions" ("añadidos para el sistema operativo invitado") son un conjunto de drivers y programas que mejoran la experiencia de uso y el rendimiento de los sistemas operativos invitados. En general, es buena idea instalarlas ya que ofrecen:

* Mejor soporte para el ratón, tarjeta de vídeo y comunicación entre el anfitrión  el invitado.
* Capacidad para compartir carpetas entre el anfitrión y el invitado.
* Mejor sincronización de la hora entre anfitrión e invitado.
* Posibilidad de compartir datos entre el portapapeles del anfitrión e invitado.
* Inicio de sesión automático.

Modos de red en VirtualBox
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A la hora de virtualizar un servicio es importante elegir correctamente el modo de funcionamiento del subsistema de red, ya que cada uno de ellos tiene sus ventajas e inconvenientes. En concreto VirtualBox ofrece los siguientes modos:

* No conectado.
* NAT: Network Address Translation es el proceso por el cual una máquina intercepta las peticiones de red de otra y las efectúa en su lugar (sustituyendo la IP). Cuando llega la respuesta, la máquina interceptora modifica esa respuesta para que la IP de destino sea la de la máquina interceptada. En el caso de VirtualBox el modo NAT hace que el programa VirtualBox “intercepte” las peticiones que salen desde el SO “invitado”. Si algún ordenador de fuera desea iniciar una conexión hacia el SO invitado, VirtualBox prohibirá dicha conexión. Será necesario abrir puertos.
* Red NAT: Facilita la creación de servidores protegidos detrás de un servicio NAT. Supongamos que queremos un servidor HTTP y uno FTP. Podríamos ponerlos en dos máquinas virtuales cada una con su NAT. Pero esto implicaría "tratar a las máquinas por separado". Creando una red NAT podemos simplificar un poco la apertura de puertos trabajando con una sola red NAT. De alguna manera esto implica poder fabricar grupos de máquinas virtuales gestionados por la misma red NAT,son máquinas que compartirán ese "router firewall NAT" virtual.
* Bridge/adaptador puente: el SO invitado no tendrá ninguna restricción y se portará como uno más de la red. El SO invitado necesitará su propia IP separada y distinta del anfitrión.
* Red interna: En este modo podemos crear "redes ficticias que no se ven desde fuera del anfitrión". Consiste en crear redes con un cierto nombre y los distintos invitados que estén asociados a esa "red ficticia" podrán verse entre sí  pero no podrán salir al exterior. 
* Solo anfitrión: el invitado solo “ve” al anfitrión.
* Red genérica: solo se usará cuando virtualicemos sistemas operativos que no tengan drivers para alguna de las tarjetas 


En la figura siguiente, sacada de la web de VirtualBox se ilustra "quien puede ver a quien"

.. figure:: img/modos_virtual_box.png
   :scale: 80%
   :alt: Hooks

   Modos de red en VirtualBox

Posibilidades de la virtualización de sistemas.
-----------------------------------------------------------------------------------------------
* Posibilidad de mover entornos a distintos lugares (remotos o no)
* Facilidad de recuperación de un entorno corrupto.
* Fácil replicación de entornos.


Herramientas para la virtualización.
-----------------------------------------------------------------------------------------------

* VirtualBox
* VMWare

Y para gestionar la virtualización tenemos:

* Vagrant
* Docker
* Kubernetes

Configuración y utilización de maquinas virtuales.
-----------------------------------------------------------------------------------------------
Durante el primer curso ya se ha explicado el funcionamiento básico de este software por lo que aquí no volveremos a repetir lo ya visto.

Alta disponibilidad y virtualización.
-----------------------------------------------------------------------------------------------

En pocas palabras podemos reconstruir un sistema virtualizado previamente usando solo estos comandos:

* ``vagrant init maquina/usr`` : Inicializa un directorio con la configuración de esa máquina (cuidado, en Windows hay que cambiar y en lugar de escribir cosas como ``vagrant init d:\directorio\maquina.box`` usar ``vagrant init d:/directorio/maquina.box``, es decir cambiar la barra \ por la /).
* ``vagrant up`` : "Levanta" la máquina, instalándola, recuperando su estado tal y como se hubiera quedado y configurándola desde cero. Por defecto, las máquinas suelen tener el usuario "vagrant" con la clave "vagrant".


Para "exportar" nuestra máquina y facilitar su gestión con Vagrant se debe:

* Instalar un sistema operativo como Windows 7 o superior o alguna variante de Linux.
* Al principio como mínimo se debe tener una tarjeta en modo NAT y además se debe anotar la MAC de dicha tarjeta.
* Si estamos en Linux se deben haber instalado los elementos que permiten añadir módulos al núcleo del sistema con ``sudo apt-get install linux-headers-$(uname -r) build-essential dkms`` 
* Se deben instalar las "Guest Additions" en el anfitrión.
* Se debe instalar OpenSSH con ``sudo apt-get install openssh-server``.
* Es recomendable crear el usuario "vagrant" y ponerle la clave Vagrant. También es importante permitir que ese usuario pueda ser administrador y que además no necesite indicar su clave de administrador cada vez. Esto puede hacerse editando los parámetros de administración con ``visudo`` y poniendo la línea ``vagrant ALL=(ALL) NOPASSWD: ALL``

* Se debe iniciar sesión en la máquina virtual con el usuario "vagrant" y la clave "vagrant". Nos conectaremos a nuestra propia máquina con ``ssh localhost`` y despues nos salimos (eso permite que se cree el directorio .ssh).  Se debe meter la clave pública de Vagrant dentro del directorio ssh con ``cat vagrant.pub > .ssh/authorized_keys`` 

* Vamos a permitir que todo el mundo pueda leer ese fichero y ese directorio de claves usando ``chmod 0700 .ssh`` 

* Una vez hecho todo esto podemos apagar la máquina virtual, cerrar VirtualBox y abrir la línea de comandos y crear un directorio vacío. Dentro de él inicializaremos el directorio para que sea un directorio inicializado por Vagrant con el comando ``vagrant init`` y luego exportaremos la máquina con ``vagrant package --base <nombredemaquina> --output Maquina.box`` .

Simulación de servicios con virtualización.
-----------------------------------------------------------------------------------------------


A continuación explicamos como virtualizar un servidor web "oculto" detrás del NAT de VirtualBox.

* Una vez instalado el sistema operativo dentro de VirtualBox deberemos configurar la red de dicho sistema operativo.
* Cuando estamos dentro de VirtualBox y con la tarjeta en modo NAT, VirtualBox se convierte en "router NAT" para sus invitados y les asigna una IP como 10.0.2.15/24 con gateway 10.0.2.2. Si nuestro invitado tiene la red en modo DHCP tomará esa IP aunque si queremos podemos modificarla.
* Un sistema operativo que esté dentro de una red con NAT **no puede recibir conexiones iniciadas en el exterior** por lo que habrá que abrir puertos dentro de VirtualBox.
* Para abrir puertos deberemos tener apagado el sistema operativo invitado.
* Una vez apagado, nos vamos a la configuración de la máquina virtual y en la categoría "Red" veremos que con la tarjeta en modo NAT podemos abrir un menú "Avanzado" que ofrece un botón "Reenvío de puertos".
* Si deseamos por ejemplo tener un servidor web seguro virtualizado podemos pedirle a VirtualBox que cuando alguien se conecte a la IP del anfitrión usando el puerto seguro redirija dicha conexión al sistema operativo invitado usando datos como los siguientes:


.. figure:: img/puertos_nat_vbox.png
   :scale: 50%
   :align: center
   :alt: Apertura de puertos en VirtualBox en modo NAT

   Apertura de puertos en VirtualBox en modo NAT






Análisis de configuraciones de alta disponibilidad
-----------------------------------------------------------------------------------------------

Para lograr la máxima disponibilidad podemos recurrir a distintas técnicas:

* Hardware duplicado.
* Virtualización.
* Tecnologías de contenedores.


Hardware duplicado
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un determinado servicio, p. ej. de bases de datos, podría estar replicado en varios equipos distintos. Diversos SGBD pueden hacer que cualquier inserción o borrado se replique automáticamente en todas las copias. Si se produce algún fallo en algún equipo, el resto de equipos pueden "repartirse" la carga extra de trabajo y conseguir así que los datos no dejen de estar disponibles en ningún momento.

Entre las ventajas podemos contar con que el rendimiento es el mejor de todas las configuraciones. Dado que los servicios se ejecutan directamente sobre el hardware tenemos casi la total garantía de que la ejecución y procesado de datos se harán con la máxima eficiencia, al no haber ninguna capa intermedia como las que veremos en los apartados siguientes.

El inconveniente más destacado es el coste. El hardware de servidores suele tener un coste muy alto, el cual puede multiplicarse aún más si necesitamos aumentar el número de equipos.


Virtualización
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Programas como VirtualBox o VMWare permiten instalar un servicio dentro de un sistema operativo llamado "invitado". Esta "máquina virtual" puede copiarse y moverse con facilidad pero la tenemos en ejecución en un solo equipo. Si hay un problema de hardware podemos mover esta máquina virtual en poco tiempo y así lograr una alta disponibilidad.

La mayor ventaja es que ahorramos mucho. Podemos tener un solo servidor de gama alta ejecutando dicha máquina virtual. Si este equipo falla, podemos mover la máquina virtual a otro ordenador (aunque sea un poco menos potente) que permita cubrir las necesidades hasta que reparemos/sustituyamos el otro equipo.

El inconveniente es que en realidad estamos "ejecutando un sistema operativo dentro de otro sistema operativo" con la enorme pérdida de rendimiento que esto supone


Contenedores
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los contenedores son un software del sistema operativo capaz de "encerrar y aislar otros programas o ficheros", consiguiendo que la ejecución de los mismos sea muy segura pero sin necesitar otro sistema operativo. Además los contenedores son programables mediante scripts lo que nos facilita mucho la tarea de desplegar servicios sin necesidad de perder rendimiento. La comparación entre arquitecturas es la siguiente (imagen tomada de la web de Docker)




.. figure:: img/contenedores.png
   :scale: 70%
   :align: center
   :alt: Comparación entre arquitecturas

   Comparativa entre arquitectura de virtualización y contenedores



Usando Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Docker puede instalarse en Linux añadiendo sus repositorios a la lista de repositorios de nuestro sistema, podemos usar estos comandos.

.. code-block:: bash

    sudo apt-get remove docker docker-engine docker.io containerd runc
    sudo apt-get update
    sudo apt-get -y install apt-transport-https ca-certificates  curl  gnupg-agent software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get -y install docker-ce docker-ce-cli containerd.io


Docker incluye un repositorio con imágenes de muchos servicios listos para descargar y ejecutarse simplemente usando scripts. Por ejemplo, ejecutemos un programa simple que se limita a saludar en pantalla con ``sudo docker run dockerinaction/hello_world`` (Se dice que ``dockerinaction`` es un "espacio de nombres", en concreto es del autor de un libro llamado precisamente "Docker in action").

El programa "se ha ejecutado dentro de un contenedor". Despues ha terminado y ha salido. Como programa es bastante simple, sin embargo, podemos ejecutar un Apache dentro de un contenedor con algo como esto (cuidado, si ya se tiene instalado Apache en Ubuntu esta ejecución fallará, se debe desinstalar primero). Si ejecutamos ``docker run httpd`` veremos como Docker descarga e "instala una imagen de Apache".

En este último ejemplo no hemos puesto espacio de nombres, así que Docker asume que se debe buscar en los "repositorios oficiales de imágenes". Una vez ejecutado **Apache se queda en ejecución y se "apodera" de la consola** . Esto es normal, así que si queremos que el servidor Web se vaya a un segundo plano deberemos cerrar el programa (Ctrl-C) y ejecutar ``sudo docker run --detach httpd`` o ``sudo docker run -d httpd`` .

Podemos ver que Apache se está ejecutando en un contenedor con ``sudo docker ps`` y "apagar" el contenedor con   ``sudo docker stop <identificador>`` o incluso "terminarlo" ``sudo docker kill <identificador>`` (no hace falta escribir todo el ID del container, basta con escribir las primeras letras).

También podemos reiniciar un servicio con ``sudo docker restart <id_container>`` e incluso ver los logs del servicio con ``sudo docker logs <id_container>`` .


Si queremos tener el mismo servicio para distintos clientes está claro que no podremos u    sar el mismo nombre, podemos lanzar un servicio con distintos nombres usando algo como ``sudo docker run -d --name ApacheCliente1 httpd`` lo que **crea y ejecuta un contenedor llamado ApacheCliente1** . Hay que recordar que aunque lo paremos no podremos volver a ejecutarlo con ``sudo docker run -d --name ApacheCliente1 httpd`` ya que eso ``intentaría volver a crear el contenedor`` (cosa imposible porque ya existe). Un contenedor puede volver a ejecutarse con ``sudo docker restart ApacheCliente1`` 

Funcionamiento ininterrumpido.
-----------------------------------------------------------------------------------------------


Integridad de datos y recuperación de servicio.
-----------------------------------------------------------------------------------------------


Servidores redundantes.
-----------------------------------------------------------------------------------------------


Sistemas de  clusters.
-----------------------------------------------------------------------------------------------


SAN, NAS, FiberChannel
-----------------------------------------------------------------------------------------------


Balanceadores de carga.
-----------------------------------------------------------------------------------------------


Instalación y configuración de soluciones de alta disponibilidad.
-----------------------------------------------------------------------------------------------


