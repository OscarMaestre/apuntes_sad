Adopción de pautas de seguridad informática
=================================================





Fiabilidad, confidencialidad, integridad y disponibilidad.
-----------------------------------------------------------------------------------------------
A continuación definimos los siguientes términos

* Fiabilidad: la capacidad de conseguir que un SI ofrezca la información sin pausas entre peticiones.

* confidencialidad: capacidad de conseguir que la información se muestre solo a las personas que estén autorizadas para ello.

* Integridad: capacidad de conseguir que la información no se altere por causas involuntarias.

* Disponibilidad: capacidad de respuesta a una peticiones con las mínimas pausas por causas involuntarias.

En relación con el último punto, se mide la disponibilidad de un SI en "nueves".

* Se dice que un SI ofrece una disponibilidad de "2 nueves", si está disponible el 99% del tiempo.
* Se dice que un SI ofrece una disponibilidad de "3 nueves", si lo está al 99.9%.
* Se dice que un SI ofrece una disponibilidad de "4 nueves" si lo está al 99.99%.
* Se dice que un SI ofrece una disponibilidad de "5 nueves" si lo está al 99.999%


Ejercicio: Si un año tiene 365 días, calcular cuanto tiempo podría estar como "no disponible" cada uno de los sistemas que hemos enumerado en el punto anterior.



Elementos vulnerables en el sistema informático; hardware, software y datos.
-----------------------------------------------------------------------------------------------

"Vulnerable": medida de la capacidad de un sistema para fallar de manera inesperada. En pocas palabras una vulnerabilidad es un punto débil.

Como resulta evidente en un SI hay tres grandes elementos que son susceptibles de ser vulnerables:

* Hardware.
    * Fluido eléctrico.
    * Placa base.
    * RAM: errores muy difíciles de detectar.
    * Discos: hay abundantes estadísticas acerca de sus tasas de fallos.
    * Tarjetas gráficas.
    * Interconexiones. cables y/o soldaduras
* Software.
    * Sistema operativo: es importante tener activada la actualización automática que aplica "parches" sin necesidad de recordar aplicarlas manualmente. Para evitar la aplicación de actualizaciones que puedan estropear otras partes se suele aconsejar NO TENER ACTIVADA LA ACTUALIZACIÓN AUTOMÁTICA en equipos críticos y sí tenerla en otros equipos que actúen como "cobayas."
    * Aplicaciones. También pueden mostrar fallos que den lugar a consecuencias muy desagradables especialmente con los datos.
* Datos. Hoy en día son casi con total seguridad el activo más valioso de la empresa. Para protegerlos habrá que tomar muchas medidas de seguridad.





Análisis de las principales vulnerabilidades de un sistema informático.
-----------------------------------------------------------------------------------------------


Cuando se habla de vulnerabilidad, se asocia este término con problemas software. Una vulnerabilidad puede conllevar una serie de problemas muy graves:


* Que un intruso consiga permisos de administración en un sistema.
* Que un virus informático consiga tomar el control de los equipos de la empresa.
* Que un software o individuo consiga borrar/alterar/cifrar datos de la empresa.


En Internet todas las vulnerabilidades detectadas se publican como un informe CVE (Common Vulnerability Exposure)

Recientemente se han descubierto **vulnerabilidades a nivel de microprocesador**.
En entornos muy sofisticados existen unas vulnerabilidades llamadas TEMPEST.


Algunas aplicaciones basadas en bases de datos son susceptibles de sufrir "ataques SQL" o "inyecciones SQL" o "SQL injects".

Otro tipo de ataque común son los HTML/JS injects. 

En líneas generales, ningún programa web debe confiar en lo que escriben sus usuarios.




Amenazas. Tipos.
-----------------------------------------------------------------------------------------------

Clasificando por lugar

* Interna
* Externa

Clasificando por mecanismo

* Físicas
* Lógicas


Amenazas físicas.
-----------------------------------------------------------------------------------------------


Amenazas lógicas.
-----------------------------------------------------------------------------------------------


Seguridad física y ambiental
-----------------------------------------------------------------------------------------------


Ubicación y protección física de los equipos y servidores.
-----------------------------------------------------------------------------------------------


Sistemas de alimentación ininterrumpida.
-----------------------------------------------------------------------------------------------


Seguridad lógica.
-----------------------------------------------------------------------------------------------


Criptografía.
-----------------------------------------------------------------------------------------------


Listas de control de acceso.
-----------------------------------------------------------------------------------------------


Establecimiento de políticas de contraseñas.
-----------------------------------------------------------------------------------------------


Políticas de almacenamiento.
-----------------------------------------------------------------------------------------------


Copias de seguridad e imágenes de respaldo.
-----------------------------------------------------------------------------------------------


Medios de almacenamiento.
-----------------------------------------------------------------------------------------------


Sistemas biométricos. Funcionamiento. Estándares.
-----------------------------------------------------------------------------------------------


Análisis forense en sistemas informáticos
-----------------------------------------------------------------------------------------------


Funcionalidad y fases de un análisis forense.
-----------------------------------------------------------------------------------------------


Respuesta a incidentes.
-----------------------------------------------------------------------------------------------


Análisis de evidencias digitales.
-----------------------------------------------------------------------------------------------


Herramientas de análisis forense.
-----------------------------------------------------------------------------------------------



El sistema operativo Unix
--------------------------------------------------

A lo largo del curso usaremos GNU/Linux, un sistema operativo de tipo UNIX de libre distribución. Aunque GNU/Linux suele empaquetarse en "distribuciones" que suelen incluir un entorno gráfico en este módulo aprenderemos a movernos por el sistema utilizando los comandos.

* ``mkdir`` nos permite crear directorios.
* ``cd`` nos permite movernos a un directorio.
* ``rm`` nos permite borrar ficheros. 
* ``rmdir`` nos permite borrar un directorio **siempre y cuando esté vacío**.
* ``ls`` muestra los ficheros del directorio actual.
* ``cat`` nos permite imprimir un fichero por pantalla.
* ``man <comando>`` nos permite obtener ayuda sobre un cierto comando (o incluso fichero de configuración).
* ``pwd`` nos muestra el nombre del directorio actual.
* ``nano`` nos da acceso a un pequeño editor de texto que nos permitirá editar, entre otras cosas, los ficheros de configuración del sistema.
* Cuando se manipulan ficheros se puede ocultar un fichero *usando el punto como primer carácter de un fichero*.
* ``apt-get`` nos permitirá instalar sofware de los repositorios del empaquetador de la distribución.
* Se puede ejecutar un comando escribiendo el nombre de dicho comando. Si el comando no está en las rutas de búsqueda se puede escribir la ruta completa.
* Se puede redirigir la salida de un comando hacia un fichero (usando ``<comando> > <fichero>``  o redirigir la salida de un comando hacia otro comando con ``<comando> | <comando>`` 
* Un comando de cualquier tipo podría necesitar **permisos de administrador**. En ese caso tendremos que usar el comando ``sudo`` de esta manera: ``sudo <comando>`` .

