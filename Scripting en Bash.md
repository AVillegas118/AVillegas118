## Scripting en Bash
### Aqui se veran varios scripts en Bash en los que se pondra a prueba 
- Permisos y formas de ejecucion de scripts 
- Manejo de variables de ambiente 
- Lectura de entradas 
- Combinacion de comandos

___
#### Permisos y formas de ejecución 

**Nota**:Se estara utilizando una máquina virtual Debian11

1. Abrimos una sesión de terminal y usando un editor de texto vamos crear un script llamado welcome.sh con lo siguiente:

![image](https://user-images.githubusercontent.com/111693854/204634546-511660fd-767e-4fd3-b629-9d2217b663b2.png)

___
2. Antes de ejecutarlo vamos a asignarle permisos de ejecución, cualquiera de las siguientes opciones funciona:
~~~
$ chmod 0755 welcome.sh 
~~~

~~~
$ chmod 0700 welcome.sh 
~~~

~~~
$ chmod u+x welcome.sh 
~~~

Si queremos ver los permisos del script ejecutamos:
~~~
$ ls -l welcome.sh
~~~

Se deberia de mostrar algo parecido a esto:

![image](https://user-images.githubusercontent.com/111693854/204635476-d550fcf2-f2be-4d41-b955-f54ba6adfe1f.png)

___
3. También hay diferentes formas de ejecutar el script, veamos algunas: 
~~~
$ ./welcome.sh
~~~

~~~
$ bash welcome.sh
~~~

~~~
$ . welcome.sh
~~~

~~~
$ /home/<username>/welcome.sh
~~~

Y el resultado sería algo parecido a esto:

![image](https://user-images.githubusercontent.com/111693854/204636112-80007dde-8802-4487-8f81-678e85f22306.png)
___
4. Ahora modifica el script welcome.sh y agrega lo siguiente al principio del archivo:

~~~
#!/bin/bash
# Script welcome.sh
# <Fecha actual> - < aquí va tu nombre >
#
~~~
___

#### Manejando Variables
___
5. Como en todo sistema existen variables de ambiente, para conocer algunas de las variables de ambiente que se manejan en Bash, basta ejecutar:
~~~
$ env 
~~~

~~~
$ printenv
~~~

6.  Para visualizar el contenido de una variable se procede así: 
~~~
$ echo $HOME 
~~~

~~~
$ echo ${HOME} 
~~~
Es posible ver el contenido de cualquier variable de ambiente con esas dos formas prueba con: $LOGNAME, $HOSTNAME, $PWD, $PATH, $SHELL 
___
7. Existe también el comando printf para desplegar el contenido de variables o escribir mensajes en la salida estándar:
~~~
$ printf “El path esta establecido en: %s\n “ $PATH
~~~
___
8. Es posible crear variables propias y/o asignarles valores a las variables:
~~~
Es posible crear variables propias y/o asignarles valores a las variables:
~~~

~~~
$ myhome=/home/<username>/Documents 
~~~

___
9. Y al igual que con las variables de ambiente podemos ver su contenido con:
~~~
$ echo $myhome
~~~
___

#### Leyendo entrada de usuario 
___
10. El comando read nos permite leer la entrada estándar en CLI, su sintaxis es así: read –p “Mensaje” variable1 variable2 variableN . Veamos los siguientes scripts de ejemplo:

Crear el script llamado bro.sh con el siguiente contenido:
~~~
#!/bin/bash
read -p "Escribe tu nombre: " nombre
echo "Hola, $nombre. Seamos amigos!"
~~~
Asignamos permisos y ejecutamos así:
~~~
$ chmod +x bro.sh
~~~

~~~
$./bro.sh 
~~~
___
11. Vamos a crear ahora un script que se llama number.sh que contenga lo siguiente:
 
 ![image](https://user-images.githubusercontent.com/111693854/204643373-ef3c9a7f-8814-4f64-9c7e-b2ae2836d673.png)
 
___

Reduciendo 
___
12. Los siguientes comandos tienen como objetivo mostrarte la combinación de comandos mediante | (pipe) de manera que la salida de un comando se procesa por un segundo y así sucesivamente. 
~~~
$ ip addr show
~~~

~~~
$ ip addr show |grep -w inet
~~~

~~~
$ ip addr show |grep -w inet | grep -v “127.0.0.1” 
~~~

~~~
$ ip addr show |grep -w inet | grep -v “127.0.0.1” | awk ‘{print $2}’ 
~~~

~~~
$ date 
~~~
___

Netdiscover.sh
___
13. Crearemos un script para descubrir los equipos conectados a la red interna, el script se llamará netdiscover.sh:
~~~
#!/bin/bash
#
# Escaner de red publico en BASH
# 
# Determinando el segmento de red
which if config && { echo "Comando ifconfig existe...";
                    direccion_ip='ifconfig |grep inet |grep -v "127.0.0.1" |awk '{print $2}''
                    echo "Esta es tu direciion ip: "direccion_ip;
                    subred='ifconfig |grep inet |grep -v "127.0.0.1" |awk '{ print $2}'|awk -F. '{print $1"."$2"."$3"."}'';
                    echo " Esta es tu subred: "$subred;
                    }\
                || { echo "No existe el comando ifconfig...usando ip ";
                    direccion_ip='ip addr show |grep inet | grep -v  "127.0.0.1" |awk '{ print $2}'';
                    echo " Esta es tu direccion ip:"$direccion_ip;
                    subred= 'ip addr show |grep inet | grep -v "127.0.0.1" |awk '{ print $2}'|awk -F. '{print $1"."$2"."$3"."}'';
                    echo " Esta es tu subred: "$subred;
                    }
for ip in {1..254}
do
    ping -q -c 4 ${subred}${ip} > /dev/null
    if [ $? -eq 0 ]
    then
        echo "Host responde: " ${subred}${ip}
    fi
done      
~~~
___
14. Es necesario darle permisos de ejecución al script recién creado:

~~~
$ chmod +x netdiscover.sh
~~~
___
15. Y para ejecutarlo: 
~~~
$ ./netdiscover.sh 
~~~
___

Portscanv1.sh 
___
16. Ahora crearemos el siguiente script para escaneo de puertos, portscanv1.sh :
~~~
#!/bin/bash
#
# Escaner de puertos usando archivo especial en /dev
# escrito en BASH
#
# Definicion de variables
direccion_ip=$1
puertos="20,21,22,23,25,50,51,53,80,110,119,135,136,137,138,139,143,161,162,389,443,445,636,1025,1443,3389,5985,5986,8080,10000"
# Verificando que parametro ip no vengan vacio
[ $# -eq 0 ] && { echo "Modo de uso: $0 <direccion ip>"; exit 1; }
#
# Bucle for para cada puerto en $puertos
#
IFS=,
for port in $puertos
do
    timeout 1 bash -c "echo > /dev/tcp/$direccion_ip/$port > /dev/null 2>&1" &&\
    echo $direccion_ip":"$port" is open"\
    ||\
    echo $direccion_ip":"$port" is closed
done
~~~
___
17.  Le asignamos permisos de ejecución al script:
~~~
$ chmod +x portscanv1.sh
~~~
___
18. Y para ejecutarlo se procede así:
~~~
$ ./portscanv1.sh
~~~
