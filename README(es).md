# webticket

Este script con python esta diseñado para comprobar webs HTTP/HTTPS existentes en los puertos 80, 8080 y 443 de la IP a comprobar.

Verificar esto de manera manual con curl, burpsuite or el navegador puede tomar algo de tiempo y es posible saltarse alguna web existente.

El objetivo es automatizar esta tarea para ahorar tiempo y evitar despistes.

### Uso

Ejecuta el script con python3.

Proporciona la IP o hostname a tratar. El programa enviara una peticion a cada uno de los puertos por HTTP/HTTPS (o ambos), y solo se enfocara en las que respondan con codigo 2xx [OK] o 3xx [Forbidden]

Tras comprobar las peticiones, se ejecuta 'whatweb' _(programa externo)_ por cada peticion afirmativa.

Si tu IP/hostname objetivo cuenta con una pagina HTTPS, el programa comprobara el certificado ssl para luego mostrarlo.

Toda esta informacion se muestra en tu consola en forma de 'ticket'.

Importante: Si no estas bajo un sistema Linux enfocado al pentesting como Kali, Parrot,... es probable que tengas que installar 'whatweb' y 'openssl' a traves del "packet manager" de tu distribucion para obtener maxima funcionalidad sobre el script.

__________________________

Puedes añadir mas puertos editando la linea 8.

_________________________

###### Cualquier problema, duda, idea que surja sera un placer leerla. 

###### Herramienta creada por Exbinary
