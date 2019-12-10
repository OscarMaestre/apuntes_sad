Instalación y configuración de cortafuegos
=================================================


Definición de cortafuegos
--------------------------------------------------------------------------------

Un cortafuegos o "firewall" es un programa que examina los paquetes de red entrantes y salientes y decide autorizar o no el paso en función de las reglas que dictamine el administrador.

A pesar de ser un software existen fabricantes de hardware que venden "dispositivos cortafuegos". Estos dispositivos suelen ser routers que incluyen de serie el software cortafuegos.

Recordatorio de los conceptos básicos de redes
--------------------------------------------------------------------------------

* Dirección IP: todo paquete de datos lleva una IP de origen y una de destino.
* Puerto: número asociado a un cierto programa o servicio. Todo paquete lleva un puerto de origen y un puerto de destino.

Cuando un paquete llega a una máquina es posible que haya que tomar una decisión como:

* Permitir el paso del paquete.
* Denegar el paso.
* Redirigirlo a otra máquina

Para ello podemos usar cualquier parámetro de TCP/IP, como por ejemplo.

* Autorizar o no dependiendo de la IP de origen.
* Autorizar o no dependiendo de la IP de destino.
* Basarnos en el puerto de destino. Dado que los puertos de origen suelen ser aleatorios **es muy poco probable que nos basemos en el puerto de origen** . Debe recordarse también que hay que indicar claramente si el puerto será **TCP o UDP**. 
* También es posible que usemos otros protocolos para tomar la decisión, por ejemplo ``<prohibir todos los paquetes ICMP>`` 
* Aunque es poco probable es posible que haya que examinar algún flag del protocolo (RST, SYN, ACK...)

Utilización de cortafuegos.
-----------------------------------------------------------------------------------------------

Un cortafuegos es un programa que se ejecuta en los niveles más básicos del sistema operativo. Para utilizar esta capacidad es posible que tengamos dos grandes tipos de interfaz.

* Un interfaz gráfico (estilo Windows): en este curso analizaremos como usar el cortafuegos de Windows 2016.
* Un interfaz basado en comandos (estilo Unix): en este curso veremos como funciona ``nftables`` 



Filtrado de paquetes de datos.
-----------------------------------------------------------------------------------------------
Una de las utilidades principales de un cortafuegos es denegar la entrada o salida de ciertos tipos de tráfico basándonos en distintos parámetros que ya se han mencionado antes:

* La IP de origen y/o destino.
* El puerto de origen y/o destino.
* El protocolo.
* Otros parámetros...

En los apartados posteriores veremos como usar un cortafuegos de red para permitir o denegar tráfico basándonos en estos datos.




Tipos de cortafuegos. Características. Funciones principales.
-----------------------------------------------------------------------------------------------

Hay muchas maneras de organizar la arquitectura del cortafuegos de una red. En este curso usaremos la más simple, reflejada en la figura siguiente. En ella, un dispositivo controla todo el tráfico de entrada y salida de una red. Por desgracia tiene el inconveniente de que si un intruso logra "saltarse" el cortafuegos tendrá acceso total a toda la red.


.. figure:: img/Cortafuegos.png
   :scale: 50%
   :align: center
   :alt: Estructura de un cortafuegos (Fuente:Wikipedia)
   
   Estructura de un cortafuegos (Fuente:Wikipedia)


El mecanismo más utilizado hoy en día es la creación de una "zona desmilitarizada" o DMZ y requiere varios dispositivos. También se conoce por el nombre de "screened host".





.. figure:: img/dmz.png
   :scale: 50%
   :align: center
   :alt: Arquitectura de una DMZ (Fuente: RedIris).

   Arquitectura de una DMZ (Fuente: RedIris).







Instalación de cortafuegos. Ubicación.
-----------------------------------------------------------------------------------------------

En GNU/Linux podemos instalar **NFTables**, una arquitectura de filtrado de paquetes que se integra con el núcleo de Linux y reemplaza al anterior **IPTables** . Para instalarlo podemos hacer lo siguiente:

* Ejecutar ``sudo apt-get update`` y ``sudo apt-get upgrade`` para asegurarnos de recargar la información de interés sobre paquetes.
* Ejecutar ``sudo apt-get remove iptables`` para asegurarnos de que no tengamos varios sistemas de filtrado ejecutándose a la vez.
* Ejecutar ``sudo apt-get install nftables`` para instalar **NFTables** .

Una vez hecho esto deberíamos tener disponible el comando ``nft`` que permite el acceso al sistema de filtrado.

.. WARNING::
   El comando ``nft`` debe ejecutarse **SIEMPRE** como administrador. Si olvidamos poner ``sudo nft ...`` es probable que el comando *no devuelva ningún error* ya que es posible permitir a otros usuarios ejecutar el comando. Así, aunque no se diga expresamente **DEBEREMOS EJECUTAR SIEMPRE ESTE COMANDO COMO SUPERUSUARIOS**  . Otra alternativa es convertirnos primero en superusuarios con ``sudo su`` y a partir de ahí lanzar todos los comandos que necesitemos.


En este tema usaremos unas de las configuraciones más habituales: situar el cortafuegos entre nuestra red y el resto de Internet, haciendo que nuestro equipo no solo haga NAT sino que también permita filtrar el tráfico entre ambas redes.



Reglas de filtrado de cortafuegos.
-----------------------------------------------------------------------------------------------



NFTables es la nueva arquitectura de filtrado y manipulación de paquetes de red en el núcleo de Linux.Como NFTables puede procesar muchos datos de red es importante saber que distingue entre varias "familias de protocolos de red". En concreto podemos usar estas familias:

* "ip": se refiere a IPv4
* "ip6": para IPv6
* "inet": para tratar tanto con IPv4 como IPv6.
* "arp": para tramas Ethernet. No lo usaremos en este tema.
* "bridge": para tramas Ethernet que "crucen" este equipo cuando esté siendo usado como switch. No lo usaremos en este tema.
* "netdev": en general solo para programadores que deseen examinar todo el tráfico que entre en la tarjeta.


El comando básico de acceso a todas las operaciones es ``nft``. En líneas generales ``nft`` examina los paquetes y analiza las reglas que se le dan para decidir que hacer con un paquete de red. Para ello es importante tener claro que ``nft`` usa "hooks", "tablas", "cadenas" y "reglas". 




Un "hook" es una etapa en la que está un paquete. En el dibujo siguiente se puede ver las etapas en las que está un paquete IP


.. figure:: img/hooks.png
   :scale: 80%
   :alt: Hooks

   "Hooks" o etapas de un paquete de red. (Figura sacada de la web de NFTables)
   

* "Prerouting": el paquete aún no ha entrado en la tabla de enrutamiento.
* "Input": el paquete era para nosotros pero aún no ha entrado en ningún programa.
* "Output": un paquete sale de un programa nuestro pero aún no se ha decidido qué hacer con él.
* "Postrouting": un paquete que sale de un programa nuestro ya ha cruzado la tabla de enrutamiento.
* "Forwarding": se usa para paquetes que "cruzan" nuestra máquina pero no van dirigidas a "esta máquina".

Es decir, el tráfico que "entre" verá los hooks "prerouting" e "input". El que sale de nuestro ordenador verá "ouput" y "postrouting". El tráfico que atraviesa nuestro equipo Linux cuando esté funcionando como router verá "forwarding".
	
	
* Una "tabla" indica el protocolo que queremos analizar, puede ser "ip", "ip6", "arp", "bridge" y otros. Así, tenemos comandos como ``nft list tables`` o ``nft list tables ip`` que nos permiten examinar qué hemos hecho con los distintos protocolos. Por ejemplo, podemos crear una tabla con el comando ``sudo nft add table ip TablaFiltradoSQL`` y la podemos borrar con ``sudo nft delete table ip TablaFiltradoSQL``. Es decir la pauta es ``sudo nft (add|remove) table <familia> <NombreDeLaTabla>``.

* Una "cadena" indica un conjunto de reglas que ``nft`` irá examinando por orden para decidir qué hacer con un paquete. Una cadena puede ser "base" o "no base". Una cadena "base" puede ver TODO el tráfico TCP y una "no base" al principio no ve nada. En una cadena hay que indicar:
	* Qué tipo de manipulación queremos aplicar en un protocolo. Las posibles manipulaciones son "filter", "route" y "nat". 
	* En una cadena también hay que indicar la etapa o hook.
	* Se debe indicar la prioridad, que es un número que determina el orden de las reglas. Una regla con la prioridad 20 se examina antes que una con prioridad 30.
	* Se debe indicar la política que será una de dos: ``accept`` o ``drop``. Si no se pone nada se asume que la política es "accept".
	
* Una "regla" siempre va metida dentro de una cadena. Toda regla tiene:
	* Un identificador o "handle", que podríamos también llamar el "código de regla".
	* Una posición dentro de la cadena. Si por ejemplo creamos primero la regla 10, y luego la 20, podemos despues insertar una regla entre medias con la posición 15. De hecho es aconsejable no usar números de regla consecutivos.
	* Una regla PUEDE llevar un "match" que permite crear "condiciones" para saber si una regla se aplica o no. Por ejemplo una regla se podría aplicar solo a paquetes que superen una cierta longitud.
	* Si ponemos un "match" entonces DEBE haber una sentencia, que indique lo que se tiene que hacer en ese caso.



Gestión de tablas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
En los puntos siguientes vemos algunas operaciones básicas con tablas:

* Crear una tabla que trabaje con el protocolo IPv4: ``nft add table ip filtradoBD`` 
* Crear una tabla que trabaje con IP en general (ya sea version 4 o 6): ``nft add table inet filtradoWeb`` 
* Ver las tablas del cortafuegos: ``nft list tables`` 
* Borrar una tabla: ``sudo nft delete table ip filtradoBD`` o ``sudo nft delete table inet filtradoWeb`` 

.. DANGER:: 
   Se puede borrar **absolutamente todas las tablas** usando el comando ``nft flush ruleset``.

Gestión de cadenas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Supongamos una tabla cualquiera de tipo "ip" y llamada por ejemplo "filtradoUsuarios". Podemos trabajar con ella con comandos como los siguientes:

* Creamos una cadena para examinar por ejemplo el trafico de entrada, pero refiriéndonos **"tráfico cuyo destino sera algún servidor que esté instalado en el mismo ordenador del cortafuegos** . Dicha cadena se llamara "traficoEntrada": ``sudo nft add chain ip filtradoUsuarios traficoEntrada {type filter hook input priority 0\; }`` 


Gestión de reglas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Supongamos una tabla cualquiera de tipo "ip" y llamada por ejemplo "filtradoUsuarios" y supongamos que dentro hay una cadena llamada "traficoEntrada" y que dicha regla examina el tráfico de entrada.

* Podemos por ejemplo rechazar que alguien se conecte desde fuera poniendo una regla que prohiba el tráfico de entrada que intente conectarse a nuestro puerto 22 (el de SSH). Recordemos que dichas personas usarán como puerto de destino el 22.
* Podemos borrar toda la cadena con ``nft flush chain ip filtradoUsuarios traficoEntrada`` 
* Podemos borrar una regla si conocemos su handle. Para averiguarlo podemos listar la tabla con ``nft list table ip filtradoUsuarios`` 

En general, en todos los casos necesitamos un mecanismo para **determinar qué campos de un paquete queremos examinar, los "matches"**. En NFTables, un match puede ser algo como esto:

* Comprobar la IP de origen; ``sudo nft add rule ip filtradoUsuarios traficoEntrada ip saddr 192.168.47.5 drop``. Esta regla **descarta** (drop) paquetes cuya IP de origen (Source ADDRess) sea 192.168.47.5.
* Comprobar la IP de destino; ``sudo nft add rule ip filtradoUsuarios traficoEntrada ip daddr 10.45.10.10 drop``. Esta regla **descarta** (drop) paquetes cuya IP de destino (Destination ADDRess) sea 10.45.10.10.
* Se pueden usar rangos de IP: ``sudo nft add rule ip filtradoUsuarios traficoEntrada ip daddr 10.45.10.0/24 drop``. Esta regla **descarta** (drop) paquetes cuya IP de destino (Destination ADDRess) sea del tipo 10.45.10.xxx.
* Comprobar ambos campos a la vez: ``sudo nft add rule ip filtradoUsuarios traficoEntrada ip saddr 192.168.47.5 daddr 10.45.10.10 drop``. Esta regla descarta los paquetes cuya IP de origen sea 192.168.47.5 y vayan destinados a la IP 10.45.10.10.
* Comprobar el puerto de origen: ``sudo nft add rule ip filtradoUsuarios traficoEntrada tcp dport 80 drop``. Esta regla descarta **TODO EL TRÁFICO** cuyo puerto de destino sea el 80.
* Mezclar campos: ``sudo nft add rule ip filtradoUsuarios traficoEntrada tcp dport 80 drop ip saddr 192.168.47.5 tcp dport 443``. Esta regla **descarta todo el tráfico cuyo IP de origen sea 192.168.47.5 y cuyo puerto de destino sea el 443** 
* Usar rangos de puertos incluso mezclando con rangos de IP:  ``sudo nft add rule ip filtradoUsuarios traficoEntrada tcp dport 80 drop ip saddr 192.168.1.0/24 tcp dport 1-1024``. Esta regla **descarta todo el tráfico cuyo IP de origen sea 192.168.1.xxx y cuyo puerto de destino esté entre 1 y 1024** 
* Usar cantidad de tráfico: examinemos las siguientes reglas:

    * ``sudo nft add rule ip filtradoUsuarios traficoEntrada ip saddr 192.168.1.45 limit rate 100kbytes/second accept`` : se autoriza el tráfico desde la IP que se mantenga en un ratio de hasta 100kbytes por segundos.
    * La regla de arriba no basta para limitar el tráfico, pero si ahora añadimos esto ``sudo nft add rule ip filtradoUsuarios traficoEntrada ip saddr 192.168.1.45 limit rate over 100kbytes/second drop`` ahora tenemos una segunda regla que indica que **si se excede el límite de 100kbytes/seg entonces el tráfico se descarta**. Esto constituye un mecanismo excelente para "regular el tráfico".


Acciones sobre paquetes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hemos visto hasta ahora la acción ``drop`` (descartar), pero se pueden usar también:

* ``counter``: nos permite hacer un recuento de bytes/paquetes que cumplen una cierta regla (y por ejemplo "llevar la contabilidad de descargas".
* ``accept`` : si una cadena utiliza por defecto la acción ``drop`` es posible que nos interese permitir algunos paquetes.

Pruebas de funcionamiento. Sondeo.
-----------------------------------------------------------------------------------------------


Registros de sucesos de un cortafuegos.
-----------------------------------------------------------------------------------------------


Cortafuegos integrados en los sistemas operativos.
-----------------------------------------------------------------------------------------------


Cortafuegos libres y propietarios.
-----------------------------------------------------------------------------------------------


Distribuciones libres para implementar cortafuegos en máquinas dedicadas.
-----------------------------------------------------------------------------------------------


Cortafuegos hardware.
-----------------------------------------------------------------------------------------------


Anexo: configuración de IP en Linux con Netplan
--------------------------------------------------------------------------------


La herramienta ``netplan`` utiliza ficheros YAML para configurar la IP en Linux. En distribuciones Linux orientadas a servidores es la herramienta que se usará en el futuro para configurar todos los parámetros de red. La estructura de estos ficheros permite indicar parámetros y subparámetros de configuración usando 4 espacios. Así, el fichero típico de ``netplan`` es como sigue:

.. code-block:: YAML

    network:
        version: 2 #Version de YAML que se usan
        ethernets: #Configuración de tarjetas Ethernet
            enp0s3:#Nombre de la tarjeta a configurar
                #Se pueden poner muchas direcciones
                #usando corchetes y separando por comas
                addresses: [192.168.100/24]
                #Dirección del router que nos permitirá
                #salir al exterior
                gateway4: 192.168.100.1
                nameservers:
                    addresses: [10.15.0.220, 8.8.8.8]

Anexo: ejercicio de configuración
--------------------------------------------------------------------------------

.. figure:: img/Esquema-de-red.png
   :scale: 50%
   :alt: Ejemplos de permisos

   Ejemplos de configuración de una red.
   
  
Se supone que tenemos dos máquinas

* La máquina de la izquierda es un cliente. Todo su tráfico pasa por la máquina central que no solo hace NAT sino que también regula el tráfico de entrada y salida por medio de un cortafuegos. La máquina de la izquierda puede ser de cualquier tipo, en nuestro caso usaremos una máquina con Windows 7.
* La máquina central será una Ubuntu Server con dos tarjetas de red configuradas mediante ``netplan``.

En la Ubuntu Server habrá que hacer algunas operaciones:

* Se debe activar el enrutamiento. Esto puede hacerse con el comando ``echo 1 > /proc/sys/net/ip_forward``  pero se desactivará en el siguiente reinicio. Por eso es mejor dejar activado el enrutamiento en el arranque editando el fichero ``/etc/sysctl.conf`` . Se debe escribir una línea en el fichero que ponga "net.ipv4.ip_forward=1" (es muy posible que ya exista la línea y solo haya que quitar el comentario inicial). Una vez modificado se puede ejecutar ``sysctl -p`` para iniciar el servicio (que quedará activado para siempre).

* Se debe instalar en Ubuntu el servidor web con ``sudo apt-get install apache2`` 
* Se debe poner en marcha el NAT. Para ello podemos añadir algo como lo siguiente al fichero ``/etc/nftables.conf``. Por favor, recuerda cambiar el nombre de la interfaz de salida, es posible que en tu máquina no se llame ``enp0s8``  

.. code-block:: none


    table ip nat {
        chain prerouting {
            type nat hook prerouting priority 0; policy accept;
        }
        chain postrouting {
            type nat hook postrouting priority 100; policy accept;
            oifname "enp0s8" masquerade
        }
    }

Ejemplo: denegación del servidor web al exterior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se nos pide lo siguiente: *"permitir que los clientes de dentro de la red SÍ puedan ver el servidor web instalado en el propio servidor donde está el cortafuegos"* 

.. WARNING::
   En los párrafos siguientes se muestra una decisión que "técnicamente funciona" pero que puede ser una mala decisión por motivos que se comentarán despues.

Supongamos que creamos una tabla donde meteremos todas las decisiones que afectan al servidor web. Usaremos ``nft add table ip filtradoweb``.

Supongamos también que creamos una cadena que se ocupará de denegar el tráfico web en la etapa de "prerouting" con ``nft add chain ip filtradoweb denegacionApache {type filter hook prerouting priority 0 \; policy accept \;}`` 


Comentario: antes hemos dicho que hay malas decisiones.

* Por ejemplo, la política por defecto es "accept". Quizá fuera más seguro poner por defecto "drop" y luego permitir solo lo que nos interese.
* Examinamos el tráfico en la etapa de "prerouting" pero eso obliga al sistema operativo a comprobar muchísimos paquetes, algunos de los cuales no irán dirigidos a nosotros. Otra posibilidad sería vincular nuestra cadena a la etapa "input"

Anexo: resolución de problemas
--------------------------------------------------------------------------------

Si algo va mal comprueba lo siguiente:

* Lanza el comando ``nft``  como superusuario, es decir en realidad debes hacer ``sudo nft``.
* Si has aplicado una regla y parece que no funciona, asegúrate de que la pones en el "hook" correcto.
* Si no puedes enrutar, asegúrate de que has activado el enrutado o "forwarding" en el núcleo. Repasa el fichero y ábrelo con ``sudo nano /etc/sysctl.conf`` . La línea que controla el forwarding debe ser así ``net.ipv4.forward=1`` .

Un ejercicio comentado
--------------------------------------------------------------------------------

Supongamos que tenemos la misma configuración de siempre, que volvemos a mostrar en la figura siguiente:

.. figure:: img/Esquema-de-red.png
   :scale: 50%
   :alt: Ejemplos de permisos

   Ejemplos de configuración de una red.
   
Y supongamos que nos piden lo siguiente:

    *Asumiendo que los ordenadores de la izquierda son una "red interna" y que el resto son "el exterior" instalar un servidor web en el equipo del cortafuegos y conseguir que solo "el interior" pueda conectarse al servidor web* 

Solución 1 (errónea)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Ejecutamos ``sudo nft flush ruleset`` para limpiar el cortafuegos.
2. Construimos una tabla con ``sudo nft add table ip filtradoWeb`` y comprobamos su creación con ``sudo nft list tables`` 
3. Comprobamos que realmente ni siquiera hay cadenas en la tabla creada con ``sudo nft list table ip filtradoWeb`` 


.. DANGER::
   A partir de aquí lo vamos a hacer mal simplemente para hacer la prueba

4. Construimos una cadena que examine el tráfico en ``prerouting`` con ``sudo nft add chain ip filtradoWeb filtradoApache { type filter hook prerouting priority 0\; policy accept\;   }`` 

5. Comprobamos que la cadena se ha creado con ``sudo nft list table ip filtradoWeb`` 

6. Prohibimos el tráfico cuyo puerto de destino sea el 80 con ``sudo nft add rule ip filtradoWeb filtradoApache tcp dport 80 drop`` 

Por desgracia aquí hay algunos problemas:

* En primer lugar, esta configuración **NO FUNCIONA** . Se ha prohibido *todo el tráfico web* incluyendo, sin querer, a los de la red interna.
* Además, hemos añadido comprobaciones en la etapa ``prerouting`` lo que sobrecarga mucho el cortafuegos, al obligarle a examinar **TODO EL TRÁFICO**. En realidad solo nos interesaba el tráfico de entrada, así que probablemente deberíamos haber usado la etapa ``input`` 

Una solución un poco mejor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Borramos las reglas con ``sudo nft flush ruleset`` 
2. Reconstruimos la tabla con ``sudo nft add table ip filtradoWeb`` 
3. Reconstruimos la cadena con ``sudo nft add chain ip filtradoWeb filtradoApache { type filter hook prerouting priority 0\; policy accept\;   }`` 
4. Prohibimos el tráfico de las direcciones de la red "externa" con ``sudo nft add rule ip filtradoWeb filtradoApache ip saddr 10.0.0.0/8 drop `` 

Esto funciona un poco mejor, pero en realidad "fuera" podría haber muchos rangos distintos, por lo que quizá hubiera que poner muchos (y quizá demasiados) rangos de IPs.

Una solución (un poco mejor)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Borramos las reglas con ``sudo nft flush ruleset`` 
2. Reconstruimos la tabla con ``sudo nft add table ip filtradoWeb`` 
3. Reconstruimos la cadena con ``sudo nft add chain ip filtradoWeb filtradoApache { type filter hook prerouting priority 0\; policy accept\;   }`` 
4. Ejecutamos ``sudo nft add rule ip filtradoWeb filtradoApache iifname enp0s8 tcp dport 80 drop`` 

Esta última regla es un poco mejor, porque ahora descartamos indicando que "prohibimos el tráfico que intente entrar al puerto 80 usando como interfaz de entrada (iifname o "input interface name") la tarjeta enp0s8" (o la que sea)
