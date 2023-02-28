Instalación y configuración de servidores  proxy
====================================================


Material para la unidad
--------------------------------------------------------------------------------

Para esta unidad vas a necesitar dos máquinas virtuales.

* Una de las máquinas virtuales ejecutará Ubuntu 20 para escritorio y tendrá una tarjeta de red en modo puente. Si quieres puedes construir una con rapidez yendo a un directorio vacío y ejecutando los comandos ``vagrant init oscarmaestre/ubuntu20desktop`` y despues ``vagrant up``. No olvides añadir una segunda tarjeta en modo puente y una carpeta compartida con el anfitrión.
* La otra máquina virtual usará Ubuntu Server (versión 22 o superior). No olvides añadir una segunda tarjeta en modo puente y una carpeta compartida con el anfitrión.

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
   :alt: Proxy directo

   Proxy (en su configuración más típica)

En un proxy abierto el proxy no está bajo nuestro control, sino que está en alguna red intermedia y suele ofrecer servicios como ocultación de ip, privacidad y similares. No tenemos garantías de que realmente el proxy no registre nuestra actividad.

.. figure:: img/proxy_abierto.png
   :scale: 70%
   :alt: Un proxy abierto

   Proxy abierto

Un proxy inverso es aquel que se sitúa dentro de la red del servidor de manera que actúa como caché, distribuidor de carga o simplemente como respaldo.

.. figure:: img/proxy_inverso.png
   :scale: 70%
   :alt: Ejemplos de proxy inverso

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

Instalación de servidores proxy
--------------------------------------------------------------------------------

La opción más sencilla es simplemente ejecutar ``sudo apt-get install squid-openssl``. Esto descarga, instala y arranca el servicio. Observa que es importante instalar ``squid-openssl`` y no ``squid`` ya que el primero permite trabajar también con conexiones HTTPS.

En los dos puntos siguientes se ilustra, solo como curiosidad, como reconstruir Squid desde su código fuente. Si ``sudo apt-get install squid-openssl`` te ha funcionado no es necesario que recompiles el programa.


Instalación de servidores proxy con ``apt source``
--------------------------------------------------------------------------------

.. WARNING::
   Este paso lo ilustramos solo para mostrar al menos una vez como recompilar un programa desde cero. Salvo problemas, por favor instala Squid en clase con ``sudo apt-get install squid-openssl``

En general las distribuciones de Linux no solo permiten descargar programas listos para ejecutar sino también su *código fuente*. Para ello, las herramientas como ``apt`` utilizan listas de repositorios con un aspecto como este::

    deb http://archive.ubuntu.com/ubuntu/ jammy main restricted universe multiverse
    # deb-src http://archive.ubuntu.com/ubuntu/ jammy main restricted universe multiverse

    deb http://archive.ubuntu.com/ubuntu/ jammy-updates main restricted universe multiverse
    # deb-src http://archive.ubuntu.com/ubuntu/ jammy-updates main restricted universe multiverse

    deb http://archive.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse
    # deb-src http://archive.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse

Como vemos, este fichero está configurado solamente para descargar programas, pero si queremos poder usar código fuente de programas podemos descomentar las líneas con ``deb-src`` o simplemente copiar líneas reemplazando ``deb`` por ``deb-src``. Una vez hecho podremos usar ``apt-get update`` y tener actualizados los repositorios de nuestras máquinas.

Compilar Squid con soporte para hacer operaciones SSL requiere también instalar algunos paquetes extra::

    sudo apt-get install openssl devscripts

Una vez hecho esto podremos partir del código fuente de Squid que hay en los repositorios de Ubuntu y compilar Squid. Para ello podemos hacer esto::


    #Descargar todo lo que sea necesario para
    #compilar el paquete Squid
    sudo apt-get build-dep squid
    #Descargar el código fuente de Squid. NO NECESITAS SER root
    apt-get source squid
    #Entramos en el directorio de squid
    cd squid-5.2
    #Añadimos las opciones --enable-ssl-crtd y --with-openssl
    nano debian/rules 
    #Y fabricamos los paquetes .deb
    sudo debuild -b -uc -us
    #Por último instalamos estos paquetes 
    #No nos harán falta todos los que construye
    #apt-get, solo ponemos estos y en este orden
    sudo dpkg -i squid-common.deb

    



Instalación de servidores proxy desde cero.
-----------------------------------------------------------------------------------------------


.. WARNING::
   Este paso es todavía más extremo que el anterior. Lo recomendable en clase es instalar Squid con ``sudo apt-get install squid-openssl``.  

El paso anterior se puede llevar todavía más lejos y trabajar directamente con el código fuente del programa en lugar de con el código fuente que almacena Ubuntu. Squid permite descargarse el código fuente y recompilarlo usando la secuencia típica de comandos en GNU/Linux:

1. ``configure``
2. ``make``
3. ``make install``


* Lo primero que debemos hacer es descargar el código fuente de squid con algo como ``wget http://www.squid-cache.org/Versions/v5/squid-5.3.tar.gz``. Si no tenemos wget lo instalamos con ``sudo apt-get install wget``.
* Despues descomprimimos el archivo con ``tar -xzf squid-5.3.tar.gz``
* El programa necesita el compilador ``g++`` y el intérprete ``perl``. Los instalamos con ``sudo apt-get install g++ perl``.
* Nos metemos en el directorio de squid con ``cd squid-5.3``.
* Ejecutamos ``./configure``. El programa analizará nuestro sistema y preparará todo para la recompilación de Squid. Si falta algo por instalar nos lo dirá.
* Ejecutamos ``make``. Esto reconstruirá el programa desde 0 y lo optimizará para la ejecución en nuestra máquina. Este proceso puede necesitar bastante tiempo.
* Lo instalamos con ``sudo make install``
* Una vez hecho esto, Squid se habrá instalado en el directorio ``/usr/local/squid`` y allí tendremos todos los ficheros.
* Squid se ejecuta con su propio usuario. Debemos crearlo con ``sudo adduser squid``.
* Squid necesitará un directorio donde dejar los logs. Lo creamos con ``sudo mkdir -p /usr/local/squid/log``. La opción ``-p`` significa "crear con los mismos permisos del directorio padre".
* Squid necesitará un directorio donde dejar datos durante la ejecución. Lo creamos con ``sudo mkdir -p /usr/local/squid/run``.
* El usuario ``squid`` debe ser el propietario de los ficheros y directorios donde se instaló el programa. ejecutaremos esto:

    * ``sudo chown -R squid:squid /usr/local/squid/log``
    * ``sudo chown -R squid:squid /usr/local/squid/var``
    * ``sudo chown -R squid:squid /usr/local/squid/run``

* Para ejecutarlo podemos usar convertirnos en el usuario ``squid`` con ``su squid`` y luego ejecutar ``/usr/local/squid/sbin/squid``. Podremos ver el número de proceso de Squid con ``ps -e  | grep squid``.

Todo este proceso ofrece más eficiencia, al adaptar el programa a la máquina donde lo vamos a ejecutar. Sin embargo, dado que compilar es un proceso lento, en sistemas tipo Debian/Ubuntu también puede usarse ``sudo apt-get install squid-openssl``, que instalará el programa y todas sus dependencias. Si hay algún problema probablemente se resuelva despues de actualizar los repositorios e instalar actualizaciones pendientes::

    sudo apt-get install update
    sudo apt-get install upgrade -y
    sudo apt-get install squid-openssl

Ficheros de interés
~~~~~~~~~~~~~~~~~~~~~

* El fichero ``/etc/squid/squid.conf`` contiene la configuración del proxy, se hablará detenidamente de él en seguida. Este fichero acepta procesar otros ficheros de configuración que estén en el directorio ``/etc/squid/conf.d``. Por tanto, **no es necesario meterlo todo siempre dentro del mismo fichero.** Esto permite trabajar más organizadamente, ya que como podrá apreciarse pronto, el fichero ``squid.conf`` es muy grande y localizar ciertos parámetros puede ser difícil.
* El directorio ``/var/spool/squid`` contiene los directorios que actuarán como caché de Squid.

Iniciando y parando el servicio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Se puede arrancar Squid usando ``sudo service squid start``, detenerlo con ``sudo service squid stop`` y hacer un reinicio del servicio con ``sudo service squid restart``. Sin embargo, antes de arrancar puede ser útil ejecutar ``sudo squid -k parse``, que analizará el fichero de configuración y nos dirá si hay algún fallo en alguna línea. También está la posibilidad de usar ``sudo squid -k check`` que nos mostrará solo los errores.

.. WARNING::
   Squid siempre muestra mucha información durante el análisis, así que puede ser interesante ejecutar algo como ``squid -k parse 2> errores.txt`` para poder leer los resultados tranquilamente con algo como ``nano errores.txt``. Si se prueba a introducir un error veremos como el fichero muestra no solo el error, sino también todo lo que funciona (lo que complica el localizar el error)

* Si hacemos un cambio en la configuración y deseamos que Squid tome la nueva configuración *sin reiniciar el servicio* se puede usar ``sudo squid -k reconfigure``.

Squid y SSL/TLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Squid es básicamente un proxy HTTP, lo que significa que en principio no puede manejar HTTPS. Sin embargo, se puede recurrir a **certificados falsos** emitidos por una **autoridad certificadora falsa** los cuales al ser instalados en los navegadores de los usuarios darán por buena una conexión HTTPS aunque sea interceptada por Squid. Para ello hay que dar varios pasos.

En primer lugar fabricaremos un directorio para poner los certificados y generaremos los datos necesarios para poder generar certificados con rapidez::

    cd /etc/squid
    sudo mkdir certificados_ssl
    #Esto genera una tabla de números primos
    #que pueden ser usados a la hora de generar los
    #certificados falsos
    sudo openssl dhparam -outform PEM -out /etc/squid/parametros_dh.pem 2048
    #Esto genera un certificado autofirmado
    sudo openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout ClaveCertificado.key -out Certificado.crt

En segundo lugar generamos una base de datos de certificados (en realidad será un directorio) con un programa llamado ``/usr/lib/squid/security_file_certgen`` que está incluido al instalar ``squid`` (podría estar también en ``/usr/lib64`` )::
    
    #Esto crea (-c) una base de datos (o directorio) llamada (-s) base_de_datos_ssl
    #y no permitirá que la base de datos ocupe más de (-M) 50MB
    #Puede que necesites usar sudo
    /usr/lib/squid/security_file_certgen  -c -s /etc/squid/certificados_ssl -M 50MB
    #El propietario de los directorios también podría ser squid
    sudo chown proxy:proxy /etc/squid/certificados_ssl

En tercer lugar nos vamos al fichero de configuración que estemos usando e indicamos que está permitido traer certificados añadiendo estas líneas **al principio del fichero** (si no lo hacemos así es posible que nunca se autorice el inicio de la conexión segura) ::

    acl traer_certificados transaction_initiator certificate-fetching
    http_access allow traer_certificados

En cuarto lugar nos vamos **al final del fichero de configuración** e indicamos qué programa va a gestionar los certificados y el directorio donde puede trabajar::

    
    sslcrtd_program /usr/lib/squid/security_file_certgen   -s /etc/squid/certificados_ssl -M 50MB
    #Esto indica que Squid debe pasar por alto los errores de validación
    #que es justo lo que queremos
    sslproxy_cert_error allow all 
    #Y esto hace que Squid observe todos los certificados
    #tanto de emisor como de cliente
    ssl_bump stare all

Y por último buscamos en ``squid.conf`` la línea "http_port 3128" y la reemplazamos por esto (los simbolos *backslash*  sirven para poder continuar en la línea siguiente)::

     http_port 3128 tcpkeepalive=60,30,3 ssl-bump \
         generate-host-certificates=on \
         dynamic_cert_mem_cache_size=50MB \
         tls-cert=/etc/squid/Certificado.crt \
         tls-key=/etc/squid/ClaveCertificado.key

Si cogemos el fichero ``Certificado.crt`` y lo importamos en el navegador podremos navegar por Internet con normalidad, pero permitiendo que Squid observe las conexiones SSL.

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

Configuración de filtros.
-----------------------------------------------------------------------------------------------

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

En general, se pueden usar las comillas en todas las listas de acceso. Si Squid encuentra algo entre comillas, asumirá que es la ruta de un fichero y que debe tomar todas las líneas de dicho fichero.

ACLs basadas en la URL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A veces no es suficiente con fabricar una lista de páginas web prohibidas porque simplemente puede haber demasiadas. En esos casos se pueden usar ACLs que examinan el nombre de dominio de la web y si dicho nombre se ajusta una regla entonces denegarlo.

Por ejemplo, supongamos que hay una serie de páginas que se desea prohibir como ``http://violencia.com`` , ``http://violencia.net`` , ``http://masviolencia.com`` , ``http://todoviolencia.com`` , ``http://muchaviolencia.es`` , etc... Como vemos, la lista de páginas podría ser enorme. En ese caso, podemos usar una regla como esta:

.. code-block:: bash

    acl prohibicion_violencia url_regex violen
    http_access deny prohibicion_violencia

Así, todas página que tengan un nombre de dominio que incluya de alguna manera la cadena "violen" serán denegadas.

ACLs basadas en la ruta
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si el sistema anterior no es suficiente se puede utilizar el análisis de las rutas. Por ejemplo, si examinamos una página como ``http://acme.com/violencia`` veremos que claramente contiene un término que deseamos prohibir. Para prohibir páginas Web en las que ocurra esto se pueden usar las ACLs basadas en ruta de esta manera:

.. code-block:: bash

    acl prohibicion_ruta_violencia urlpath_regex violen
    http_access deny prohibicion_ruta_violencia

.. WARNING::

   Hoy en día cada vez más páginas, incluidos los buscadores usan cifrado en las conexiones. Eso significa que estos bloqueos podrían no funcionar ya que lo primero que hace el navegador es establecer una conexión cifrada (que Squid no puede descifrar) y despues solicitar la página concreta
    
ACLs basadas en el tipo de archivo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En Internet hay una definición general de tipos de archivo llamada "tipos MIME" (Multimedia Internet Mail Extensions, se definieron para transportar archivos en el correo electrónico). Si lo que nos interesa en bloquear el acceso a ciertos tipos de contenido como vídeo o audio podemos bloquear usando el análisis del tipo de petición MIME al servidor de esta manera. En este caso bloqueamos los "webm" que es un tipo de vídeo muy utilizado, aunque no el único (de hecho YouTube ofrece diversos tipos):

.. code-block:: bash

    acl bloquear_video req_mime_type video/webm
    http_access deny bloquear_video

Métodos de autenticación en un  proxy .
-----------------------------------------------------------------------------------------------
Aparte de usar direcciones IP podemos hacer que un proxy exija a un usuario el proporcionar un usuario  y contraseña si desea navegar por Internet. Existen diversos como mecanismos como NTLM (que usar autenticación Windows) o LDAP (que usa un servidor LDAP). Dado que estamos usando Unix y que en este módulo no se menciona LDAP usaremos el mecanismo NCSA que usará un fichero de usuarios y claves externo gestionado por una herramienta externa, en concreto usaremos la herramienta ``httpasswd`` (si no la tenemos habrá que instalarla con ``sudo apt-get install -y apache2-utils`` 

Una vez la tengamos instalada tenemos que decidir donde ubicar el fichero de credenciales, que por supuesto debe ser un lugar protegido de los usuarios normales. Elegiremos ``/etc/squid/credenciales`` y empezaremos insertando un usuario llamado "contabilidad" de esta manera: ``sudo htpasswd -c /etc/squid/credenciales contabilidad``. La herramienta nos pedirá que indiquemos la clave de este usuario.

.. WARNING::
   La opcion ``-c`` es para *crear el fichero*, así que solo la usaremos una vez.

A continuación crearemos por ejemplo otro usuario llamado "gerencia" con ``sudo htpasswd /etc/squid/credenciales gerencia`` . En este punto ya tenemos un fichero con dos usuarios. Puede mostrarse el contenido de este fichero con ``sudo cat /etc/squid/credenciales`` y veremos que aparecen los usuarios y su clave cifrada.

Una vez hecho esto debemos configurar la autenticación de Squid usando estos parámetros:

1. "program": se usa un módulo de Squid llamado ``ncsa_auth`` que debería estar dentro de ``/usr/lib/squid3`` probablemente con la ruta ``/usr/lib/squid3/basic_ncsa_auth`` . 
2. "children": indica el número de módulos hijo que deben estar listos para atender peticiones de autenticación. Este valor dependerá de cuantas personas como máximo se vayan a conectar al proxy. Para nuestro ejemplo un valor de 10 será suficiente.
3. "realm": un texto que aparecerá a los usuarios que inicien sesión.
4. "credentialsttl": tiempo máximo que se almacena la sesión de alguien antes de volver a pedirle la clave.

Así, si queremos crear una lista en la que estén los usuarios autenticados podríamos configurar y crear todo con algo como esto:

.. code-block:: bash

    #El orden en estos ficheros es fundamental
    #Primero creamos permisos básicos para usuarios
    #que no tengan que proporcionar una clave de acceso
    acl marca_permitido src 10.8.0.250
    acl resto_personas  src 10.8.0.0/24
    acl periodicos      dstdomain .marca.com .as.com

    #Esto permite a una IP (¿del jefe?) acceder
    #a periódicos
    http_access allow marca_permitido periodicos
    #El jefe también entra en este grupo y también
    #puede ver otras cosas que no sean periódicos
    http_access allow resto_personas !periodicos

    #A partir de aquí creamos una configuración de seguridad

    #Esto indica que para un esquema de configuración de nivel básico
    #usaremos el programa basic_ncsa_auth con el fichero de credenciales /etc/squid/credenciales
    auth_param basic program /usr/lib/squid3/basic_ncsa_auth /etc/squid/credenciales

    #Se deben poder autenticar hasta a 10 usuarios a la vez
    auth_param basic children 10

    #Texto que se envía a los usuarios que inicien sesión
    auth_param basic realm Indique sus credenciales

    auth_param basic credentialsttl 2 hours

    #Esto fabrica una lista para indicar "usuarios que están autenticados".
    acl autenticados proxy_auth REQUIRED

    #Esto indica la lista de periodicos deportivos
    acl deportes dstdomain .marca.com

    #Y aqui está la clave, COMBINAR listas
    #Se deniega el acceso al periodico a 
    #aquellos usuarios que NO estén autenticados
    http_access deny deportes !autenticados



auth_param basic program /usr/lib/squid3/basic_ncsa_auth /etc/squid/credenciales.txt
auth_param basic realm   Indique su clave por favor
auth_param basic children 10
auth_param basic credentialsttl 4 hours 

acl programadores proxy_auth REQUIRED 

http_access allow programadores 
http_access deny  resto_personas




Configuración del almacenamiento en la caché de un proxy .
-----------------------------------------------------------------------------------------------
En general los valores por defecto de Squid suelen considerarse bastante apropiados, pero pueden modificarse algunos de ellos si se desea obtener más rendimiento.

.. code-block:: bash

    cache_dir ufs /var/spool/squid 20000 64 1024

Esta caché acepta hasta 20.000MB de datos organizándonos en 64 directorios de hasta 1024 subdirectorios cada uno

.. code-block:: bash

    cache_mem 16MB

Indica que se deben tener preparados unos 16MB de RAM para los objetos populares en cache (páginas o archivos muy solicitados). 

.. WARNING::

   Hay que tener cuidado con cuanta memoria RAM consume Squid ya que si tenemos muy poca la caché empezará a desviar objetos a "swap" y el rendimiento bajará en picado. En general la ``cache_mem`` debe ser como un tercio de la RAM disponible y luego añadir unos 14MB por cada GB de caché en disco. Esto significa que si en nuestro ejemplo tenemos 20GB de caché en disco y una ``cache_mem`` de 16MB debemos asegurarnos de tener como minimo (16*3)+(20*14)=48+280=328MB como minimo de RAM.

Squid rota los ficheros de caché automáticamente y borra los ficheros menos usados para dar cabida a los nuevos. Si de todas maneras se desea saber cuanto espacio está ocupando la cache puede usarse el comando ``du -h /var/spool/squid`` para ver cuanto espacio en disco ocupa la caché.







Proxys  inversos.
-----------------------------------------------------------------------------------------------
Como ya hemos visto antes, un proxy inverso es aquel que se sitúa delante de un servidor Web con el objetivo de "descargarle de trabajo", como señala la figura siguiente:

.. figure:: img/proxy_inverso.png
   :scale: 70%
   :alt: Ejemplos de proxy inverso

   Proxy inverso

Para experimentar con esta configuración necesitaremos esto:

* Dos máquinas virtuales, ambas con Ubuntu Server.
* En una de ellas (que llamaremos "Proxy") pondremos el proxy Squid (si no se tiene, se debe instalar con ``sudo apt-get install squid`` 
* En la otra (que llamaremos "Servidor Web") pondremos el servidor Web Apache, PHP y Links (se puede instalar con ``sudo apt-get install apache2 php`` ). Asegúrate de que tenga una carpeta compartida con el anfitrión para que podamos pasar con comodidad ficheros entre ambas máquinas.
* Las dos máquinas deben tener una tarjeta de red en modo puente, deben tener un IP de la misma red y deben poder hacerse ping entre ellas.

Dentro del servidor Web pondremos una pequeña página PHP que simplemente muestre información de la fecha y hora, como esta. La llamaremos ``index.php`` y debe estar en el directorio ``/var/www/html`` (asegúrate también de que la página la puede leer todo el mundo con ``sudo chmod a+r /var/www/html/index.php`` :


.. literalinclude:: pagina_proxy_inverso.php
   :language: php

Si está todo bien, en el Servidor Web podremos ejecutar ``links http://127.0.0.1`` y veremos la página generada en el servidor donde nos dirá la fecha y la hora.

Una vez configurado el Servidor Web toca configurar Squid. En Squid un "proxy inverso" se denomina un "acelerador". En realidad, la configuración básica es muy sencilla y aun así ya ofrece mucha mejora en el rendimiento:


.. code-block:: bash

    http_port 80 accel defaultsite=192.168.1.130 no-vhost
    cache_peer 192.168.1.30 parent 80 0 no-query originserver name=AceleradorWebLocal
    refresh_pattern -i \.php 2 50% 9

¿Qué significa todo esto?

* La primera línea indica que Squid va aceptar peticiones en el puerto 80 pero esto va a servir para acelerar un sitio web en el que no hay hosting virtual.
* La segunda línea indica que vamos a cachear tales peticiones conectando con el sitio web principal ("parent) y que cuando se conecten a nuestro puerto 80 no nos conectaremos a ningún otro puerto ICP (sirve para proxies encadenados), y que como no haremos encadenamiento de proxies no hay que hacer consultas ("no-query") sino que esto es el servidor real de origen ("originserver"). A este servidor cacheado le hemos puesto un nombre que luego podríamos proteger con ACLs.
* La tercera línea indica que cualquier petición que termine en PHP debe ser cacheada durante al menos 2 minutos y como máximo 9 minutos. Si alguna petición *no lleva indicado el tiempo máximo por parte del navegador* se asume que se conserva en caché hasta que llega a la mitad de su edad. Por ejemplo si alguien pidió un PHP hace 6 horas y han pasado 3 se considera que el objeto ya no debe estar en caché.

.. WARNING::
   En algunos Squid hay una línea como esta en el fichero ``/etc/squid.conf`` que hace que por defecto 

Para comprobar que esto funciona abre varias pestañas en tu navegador (no vale pulsar F5 porque el navegador solicita entonces actualizar las cachés) y verás que todas llevan la misma hora de generación.


.. WARNING::

   Lo siguiente **es una violación del protocolo HTTP:** Si realmente queremos ignorar a los usuarios que pulsen F5 se puede añadir una opción al final de la línea y dejarla como ``refresh_pattern php$ 2 50% 9 ignore-reload`` Con ello, Squid ignorará todas las peticiones de recarga incluso aunque se pulse F5

Para aprender realmente todo lo que envía y recibe el navegador utiliza las herramientas del desarrollador (usa la tecla F12) y explora las distintas cabeceras que envía Firefox/Chrome/Edge.


Proxys  encadenados.
-----------------------------------------------------------------------------------------------


Pruebas de funcionamiento. Herramientas gráficas.
-----------------------------------------------------------------------------------------------
En Ubuntu es posible instalar un programa llamado ``squidclient`` que permite hacer consultas sencillas al servidor Squid y obtener muchas estadísticas sobre el uso de memoria, CPU y disco. Para instalarlo puede usarse ``sudo apt-get install squidclient`` y una vez instalado usar ``squidclient mgr:info`` para obtener los valores de uso.
