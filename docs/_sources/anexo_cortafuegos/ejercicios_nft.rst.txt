Anexo: ejercicios sobre ``nftables``
==============================================

Introducción
------------------------------------------------

En estos ejercicios se indican los hooks necesarios pero **en el examen no se hará así.** Por ello, se recomienda prestar atención al tipo de problema propuesto y pensar en el por qué el ejercicio sugiere el hook indicado. En los ejercicios también se usa a veces la política drop. Eso explica por qué en algunos ejercicios de quota o de limit rate indicamos solo una regla.

Ejercicio 1
------------------------------------------------

Crear un fichero de configuración para nftables que contenga una tabla ip llamada filtrado_ssh. Dentro de ella, definir una cadena de tipo filter con hook input llamada SSH_ENTRADA y política drop. La única regla debe ser aceptar (permitir) el tráfico TCP entrante al puerto 22 (SSH) que provenga exclusivamente de la dirección IP de origen 192.168.1.50::

    table ip filtrado_ssh {
        chain SSH_ENTRADA {
            type filter hook input priority 0; policy drop;
            ip saddr 192.168.1.50 tcp dport 22 accept
        }
    }


Ejercicio 2
------------------------------------------------
Crear un fichero de configuración que defina una tabla ip llamada filtro_ping con una cadena de tipo filter, hook input y política drop llamada ICMP_ENTRADA. Añadir una regla para aceptar todas las peticiones de eco ICMP entrantes (echo-request) dirigidas a la máquina::

    table ip filtro_ping {
        chain ICMP_ENTRADA {
            type filter hook input priority 0; policy drop;
            icmp type echo-request accept
        }
    }

Ejercicio 3
------------------------------------------------
Cree un fichero de configuración con una tabla ip y una cadena HTTP_LIMIT (tipo filter, hook input, política accept). La única regla debe descartar (drop) las conexiones TCP al puerto 80 (HTTP) cuando la tasa de llegada exceda los 100 kiloytes por segundo::

    table ip filter_limit {
        chain HTTP_LIMIT {
            type filter hook input priority 0; policy accept;
            tcp dport 80 limit rate over 10 kbytes/second drop
        }
    }

Ejercicio 4
------------------------------------------------
Configurar una tabla ip y una cadena FORWARD_FTP de tipo filter con hook forward y política drop. Añadir una regla para aceptar todo el tráfico que pase a través del firewall (tráfico forward) hacia el servidor FTP 172.16.0.10 solo hasta que se hayan transferido 50 Megabytes (MiB) de datos. Una vez superado el límite, el tráfico debe ser denegado automáticamente::

    table ip filter_quota {
        chain FORWARD_FTP {
            type filter hook forward priority 0; policy drop;
            ip daddr 172.16.0.10 quota until 50 mbytes accept
        }
    }


Ejercicio 5
------------------------------------------------

Crear un fichero que defina una tabla ip llamada "nat_web" y una cadena de tipo nat con hook prerouting y prioridad 0 llamada DNAT_WEB. Añadir una regla para interceptar el tráfico TCP entrante dirigido al puerto 443 (HTTPS) del firewall y redirigirlo internamente al servidor 10.0.0.25 en el puerto 8443:: 

    table ip nat_web {
        chain DNAT_WEB {
            type nat hook prerouting priority dstnat;
            tcp dport 443 dnat to 10.0.0.25:8443
        }
    }

Ejercicio 6
------------------------------------------------

Crear un fichero de configuración con una tabla ip llamada CONTADOR_PING. Dentro de esta tabla, definir una cadena SALIDA_ICMP (tipo filter, hook output, política accept). Añadir una regla que acepte todo el tráfico ICMP saliente (echo-reply y echo-request) y que, además, cuente (utilizando counter) el número de paquetes y bytes que coinciden con este criterio::

    table ip CONTADOR_PING {
        chain SALIDA_ICMP {
            type filter hook output priority 0; policy accept;
            icmp type echo-request counter accept
            icmp type echo-reply counter accept
        }
    }

Ejercicio 7
------------------------------------------------

Crear una tabla ip llamada SEGURIDAD_WEB y una cadena ENTRADA_WEB (tipo filter, hook input, política accept). Añadir una regla para registrar (utilizando log) todos los paquetes TCP dirigidos al puerto de destino 80 (HTTP) provenientes de la dirección IP de origen 203.0.113.1. Tras registrarlos, los paquetes deben ser descartados (drop). El prefijo del registro debe ser "POSIBLE_ESCANEADOR"::

    table ip SEGURIDAD_WEB {
        chain ENTRADA_WEB {
            type filter hook input priority 0; policy accept;
            ip saddr 203.0.113.1 tcp dport 80 log prefix "POSIBLE_ESCANEADOR " drop
        }
    }

Ejercicio 8
------------------------------------------------

Crear una tabla ip llamada CONTROL_FTP y una cadena REGLAS_AVANZADAS (tipo filter, hook forward, política drop). Añadir una regla que acepte el tráfico reenviado (forward) cuyo puerto de origen sea el 20 (FTP-Data), pero solo si la tasa no excede los 1000 bytes por segundo. Si excede el límite, el paquete debe ser descartado::

    table ip CONTROL_FTP {
        chain REGLAS_AVANZADAS {
            type filter hook forward priority 0; policy drop;
            tcp sport 20 limit rate over 1000 bytes/second drop
            tcp sport 20 accept
        }
    }

Ejercicio 9
------------------------------------------------

Nota: Este ejercicio incluye DOS criterios a la vez, cosa que no hemos hecho en clase. Sin embargo es útil para ver las capacidades de nftables.

Crear una tabla ip llamada DATOS_TEMPORALES y una cadena PROCESAMIENTO (tipo filter, hook forward, política drop). Configurar una regla para aceptar el tráfico reenviado hacia la IP de destino 172.30.0.5 solo si la cuota de 1 Gigabyte (GiB) aún no ha sido alcanzada y solo si la tasa de paquetes no excede los 20000 bytes por segundo. Si cualquiera de las dos condiciones falla, el paquete debe ser descartado (por la política o la falta de accept tras la cuota)::


    table ip DATOS_TEMPORALES {
        chain PROCESAMIENTO {
            type filter hook forward priority 0; policy drop;
            ip daddr 172.30.0.5 quota until 1 gbytes limit rate 20000 bytes/second accept
        }
    }

Ejercicio 10
------------------------------------------------

Crear una tabla ip llamada RED_INTERNA y una cadena PRE_TRADUCCION (tipo nat, hook prerouting, prioridad dstnat). Añadir una regla para traducir (DNAT) el tráfico TCP entrante al puerto 8080 del firewall solo si proviene de la red 192.168.0.0/24. El destino traducido debe ser el servidor 10.1.1.5 en el puerto 80::

    table ip RED_INTERNA {
        chain PRE_TRADUCCION {
            type nat hook prerouting priority 0;
            ip saddr 192.168.0.0/24 tcp dport 8080 dnat to 10.1.1.5:80
        }
    }