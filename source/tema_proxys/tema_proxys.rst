Instalación y configuración de servidores  proxy
====================================================


Material para la unidad
--------------------------------------------------------------------------------

Para esta unidad vas a necesitar dos máquinas virtuales.

* Una de las máquinas virtuales ejecutará Ubuntu 20 para escritorio y tendrá una tarjeta de red en modo puente. Si quieres puedes construir una con rapidez yendo a un directorio vacío y ejecutando los comandos ``vagrant init oscarmaestre/ubuntu20desktop`` y despues ``vagrant up``. No olvides añadir una segunda tarjeta en modo puente.
* La otra máquina virtual usará Ubuntu Server 20. Puedes construir una con ``vagrant init oscarmaestre/ubuntuserver20`` y con ``vagrant up``. No olvides añadir una segunda tarjeta en modo puente.

Habrá que configurar la IP en ambos casos y recuerda que es **imprescindible** que ambas máquinas puedan hacerse ping.

Tipos de  proxy . Características y funciones.
-----------------------------------------------------------------------------------------------

Antes de explicar los tipos de proxy es importante entender el concepto: básicamente, se puede decir que un proxy es un software que actúa como intermediario entre las peticiones de un cliente y un servidor. Si examinamos la figura siguiente veremos que ahora no hay solo una petición y una respuesta,sino que hay varios pasos más.


.. figure:: img/comportamiento_proxy.png
   :scale: 85%
   :alt: Ejemplos de permisos

   Comportamiento de un proxy

1. Un cliente solicita, por ejemplo, una web como http://acme.com
2. La petición pasa primero por el proxy, que la intercepta, la analiza y puede tomar decisiones sobre si permitirla o no. Si está permitida **es el proxy quien realiza la petición en el nombre del usuario**
3. El servidor contesta a la petición y dicha respuesta llega al proxy, quien a menudo conservará la respuesta en caché por si en el futuro alguien necesita la misma página web.
4. La respuesta finalmente llega al cliente. 

Una ventaja añadida de este caso del proxy es que si en el futuro otra máquina de la red necesita la misma web obtendrá la misma página pero a más velocidad, al no ser necesario hacer una conexión extra al exterior.

Una vez analizado el concepto de proxy se pueden encontrar distintos tipos de proxy

Tipos de proxy en función de la arquitectura de red.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Podemos distinguir entre proxy directo (o simplemente proxy), proxy abierto y proxy inverso.


El término proxy suele reservarse para esta arquitectura de red. En este caso, el proxy está dentro de nuestra red y nosotros como administradores tenemos el control y podemos tomar todas las decisiones que deseemos.

.. figure:: img/proxy.png
   :scale: 70%
   :alt: Ejemplos de permisos

   Proxy (en su configuración más típica)

En un proxy abierto el proxy no está bajo nuestro control, sino que está en alguna red intermedia y suele ofrecer servicios como ocultación de ip, privacidad y similares. No tenemos garantías de que realmente el proxy no registre nuestra actividad.

.. figure:: img/proxy_abierto.png
   :scale: 70%
   :alt: Ejemplos de permisos

   Proxy abierto

Un proxy inverso es aquel que se sitúa dentro de la red del servidor de manera que actúa como caché, distribuidor de carga o simplemente como respaldo.

.. figure:: img/proxy_inverso.png
   :scale: 70%
   :alt: Ejemplos de permisos

   Proxy inverso

Tipos de proxy en función de la aplicación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aunque mucho menos conocidos que los proxies web existen proxys para otras aplicaciones como FTP e IRC. En este módulo no se tratan estos programas aunque su funcionamiento en esencia es muy similar a los proxies web. 

Un tipo de proxy muy habitual fuera de HTTP es el proxy SOCKS. Estos proxies *trabajan a nivel de TCP* y no en la capa de aplicación. La versión 5 de SOCKS (llamada SOCKS5) permite incluso autenticación a nivel de TCP.

ICAP es otro protocolo para proxies que permite trabajar de varias maneras:

* Modo solicitud: el proxy redirige la petición y si los filtros lo permiten redirige la petición hacia el servidor. Esto lo hace útil para **filtra conexiones**
* Modo de respuesta: en este modo la petición se redirige y cuando llega la respuesta podemos procesarla con filtros y decidir qué hacer con el contenido que llega. Esto permite **filtrar contenidos**

En el resto del tema veremos como configurar SQUID, un proxy muy sofisticado con capacidad de procesar tráfico HTTP y FTP y capaz de actuar tanto en modo solicitud como en modo respuesta.

Instalación y configuración de clientes proxy.
-----------------------------------------------------------------------------------------------

Configurar un cliente para que utilice un proxy es bastante sencillo. En la imagen siguiente se muestra una captura de Firefox en el que se indica que la conexión debe hacerse a través de un proxy. Como puede apreciarse basta con rellenar la IP del servidor proxy y el puerto en el que escucha (Squid suele hacerlo en el 3128).






.. figure:: img/Proxy_en_firefox.jpg
   :scale: 50%
   :align: center
   :alt: Configuración de proxies en Firefox

   Configuración de proxies en Firefox


Sin embargo, aunque hayamos instalado Squid en la segunda máquina virtual veremos que el Firefox de la máquina cliente no funciona y muestra un mensaje como "El servidor proxy está rechazando las conexiones entrantes". Aún se tiene que configurar el servidor, cosa que haremos en los pasos siguientes.






Instalación de servidores proxy.
-----------------------------------------------------------------------------------------------
Squid permite descargarse el código fuente y recompilarlo usando la secuencia típica de comandos en GNU/Linux:

1. ``configure``
2. ``make``
3. ``make install``

Ofrece más eficiencia, al adaptar el programa a la máquina donde lo vamos a ejecutar. Sin embargo, dado que compilar es un proceso lento, en clase usaremos el comando típico ``sudo apt-get install squid``, que instalará el programa y todas sus dependencias.

Ficheros de interés
~~~~~~~~~~~~~~~~~~~~~

* El fichero ``/etc/squid/squid.conf`` contiene la configuración del proxy, se hablará detenidamente de él en seguida. Este fichero acepta procesar otros ficheros de configuración que estén en el directorio ``/etc/squid/conf.d``. Por tanto, **no es necesario meterlo todo siempre dentro del mismo fichero.** Esto permite trabajar más organizadamente, ya que como podrá apreciarse pronto, el fichero ``squid.conf`` es muy grande y localizar ciertos parámetros puede ser difícil.
* El directorio ``/var/spool/squid`` contiene los directorios que actuarán como caché de Squid.

Iniciando y parando el servicio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Se puede arrancar Squid usando ``sudo service squid start``, detenerlo con ``sudo service squid stop`` y hacer un reinicio del servicio con ``sudo service squid restart``. Sin embargo, antes de arrancar puede ser útil ejecutar ``sudo squid -k parse``, que analizará el fichero de configuración y nos dirá si hay algún fallo en alguna línea.

.. WARNING::
   Squid siempre muestra mucha información durante el análisis, así que puede ser interesante ejecutar algo como ``squid -k parse 2> errores.txt`` para poder leer los resultados tranquilamente con algo como ``nano errores.txt``. Si se prueba a introducir un error veremos como el fichero muestra no solo el error, sino también todo lo que funciona (lo que complica el localizar el error)

* Si hacemos un cambio en la configuración y deseamos que Squid tome la nueva configuración *sin reiniciar el servicio* se puede usar ``sudo squid -k reconfigure``.



ACLs en Squid. ACLS de origen.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Squid *no permite su uso a cualquier cliente.* Puede usar listas de control de acceso para determinar exactamente lo que se quiere hacer:

* Se puede restringir el uso a solo ciertas IPs origen.
* Se puede restrigir el acceso a determinados sitios web destino.
* Se pueden combinar ambos mecanismos para permitir el acceso solo a ciertas web y solo por parte de ciertos usuarios de la empresa.

Por defecto **Squid no permite a nadie la conexión.** Así que es necesario crear una ACL donde indiquemos una lista de máquinas y despues tendremos que dar permiso a esa lista de máquinas.

Como hemos dicho antes, no es necesario meter todo en el fichero ``/etc/squid.conf``, así que vamos a definir nuestro propio acceso en un fichero como ``/etc/squid/conf.d/accesopropio.acl``. Supongamos que la red de nuestra empresa tiene el prefijo 192.168.1.0/24...

.. code-block:: bash

    acl red_empresa src 192.168.1.0/24
    http_access allow red_empresa

Si ponemos esto en el fichero ``/etc/squid/conf.d/accesopropio.acl`` y ejecutamos ``sudo squid -k parse`` podremos ver si hay algún error. Si lo hay lo corregiremos y si no podremos ejecutar ``sudo service squid restart`` para que el proxy empiece a funcionar. Si nos vamos a la máquina cliente y probamos alguna URL veremos que ahora sí estamos navegando a través del proxy. Si se desea comprobar si realmente navegamos a través del proxy podemos detener el proxy en el servidor con ``sudo service squid stop`` y ver que Firefox deja de funcionar. Por supuesto, si reiniciamos el proxy Firefox volverá a poder navegar con normalidad.

ACLs en Squid. ACLS de destino.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Una vez que hemos visto como procesar las IPs de origen que pueden navegar nos interesan otros parámetros de Squid como las listas ``dstdomain.`` Estas listas permiten tomar decisiones sobre dominios de destino por los cuales quieren navegar los clientes (y normalmente querremos saberlo para denegarles el permiso). Supongamos que hay un dominio llamado ``http://marca.com`` al cual deseamos prohibir el acceso. Podemos poner un fichero como ``/etc/squid/conf.d/accesopropio.acl`` en el que escribamos

.. code-block:: bash

    acl prohibidos dstdomain .marca.com
    http_access deny prohibidos

.. WARNING::
   El orden de las ACLS es **importantísimo**. Si en el apartado anterior habíamos dado permiso a ciertos usuarios ese "permiso para salir" ya fue concedido así que intentar denegar no funcionará.

Este fichero **no deniega el acceso al periódico**

.. code-block:: bash

    acl red_empresa src 192.168.1.0/24
    http_access allow red_empresa
    acl prohibidos dstdomain .marca.com
    http_access deny prohibidos


Este fichero **sí deniega el acceso al periódico**

.. code-block:: bash

    acl prohibidos dstdomain .marca.com
    http_access deny prohibidos
    acl red_empresa src 192.168.1.0/24
    http_access allow red_empresa
    

En el caso de las restricciones a sitios web es frecuente que haya varios, así que un fichero podría ser algo así:

.. code-block:: bash

    acl prohibidos dstdomain .marca.com .sport.es 
    http_access deny prohibidos
    acl red_empresa src 192.168.1.0/24
    http_access allow red_empresa

Pero es habitual tener muchos nombres de dominio. Para simplificar esto, Squid permite cargar datos desde ficheros externos usando las comillas. Por ejemplo, supongamos que queremos tener todos los dominios prohibidos en un fichero llamado por ejemplo "/etc/squid/sitios_prohibidos.txt". Podemos usar este fichero:

.. code-block:: bash

    acl prohibidos dstdomain "/etc/squid/sitios_prohibidos.txt"
    http_access deny prohibidos
    acl red_empresa src 192.168.1.0/24
    http_access allow red_empresa

Y por supuesto poner en el fichero ``/etc/sitios_prohibidos.txt`` una lista de dominios no permitidos, como:

.. code-block:: bash

    .marca.com
    .sport.es
    .mundodeportivo.com
    ...


Configuración del almacenamiento en la caché de un  proxy .
-----------------------------------------------------------------------------------------------


Configuración de filtros.
-----------------------------------------------------------------------------------------------


Métodos de autenticación en un  proxy .
-----------------------------------------------------------------------------------------------


Proxys  inversos.
-----------------------------------------------------------------------------------------------


Proxys  encadenados.
-----------------------------------------------------------------------------------------------


Pruebas de funcionamiento. Herramientas gráficas.
-----------------------------------------------------------------------------------------------

