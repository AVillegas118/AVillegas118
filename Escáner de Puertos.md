## Escáner de Puertos
### Se verán varios ejercicios enfocados en el desarrollo de pequeñas piezas de software desarrolladas en Python para el scaneo de puertos 
___

#### ESCANER DE PUERTOS 
___

#### SCAN_PORTV1
___
1. En el siguiente script contiene las partes en las que:

- Se importan las librerías requeridas
- Se pedirán como argumentos del script la dirección ip y el rango de puertos a escanear
- El rango de puertos proporcionado como segundo argumento se transforma en una lista de la que se obtienen dos valores
- El argumento originalmente guardado como host se procesa con la función
gethostbyname para obtener una dirección ip; también se crea una lista para almacenar los
puertos que se encontraron abiertos
- Se inicia un bucle for para con sockets ir probando los puertos obtenidos del rango de puertos, si el resultado es 0 se agregan a la lista de opened_ports
- Se imprimen los resultados

~~~
#!/usr/bin/python
# -*- coding: utf-8 -*-
#Parte 1 
#Importamos librerias necesarias
import sys
from socket import *
#Parte 2
#Modo de ejecucion del script
# port_scan.py <host> <start_port>-<end_post>
#Primer argumento se guarda en variable host
#Segundo argumento de guarda en portstrs
host = sys.argv[1]
portstrs = sys.argv[2].split('-')
#Parte 3
#portstrs contiene dos valores que asignamos
#en start_port e valor de inicio
#en end_port el valor fin 
start_port = int(portstrs[0])
end_port = int(portstrs[1])
#Parte 4 
#Para usar en el socket sasignados lo de la
#variable host a target_ip
#Definimos una lista de puertos opened_ports
target_ip = gethostbyname(host)
opened_ports = []
#Parte 5 
#Iniciamos bucle for para probar los puertos 
for port in range (start_port, end_port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(10)
    result = sock.connect_ex((target_ip, port))
    if result == 0:
        opened_ports.append(port)
#Parte 6 
#Se imprime salida 
print("Opened ports:")
#
for i in opened_ports:
    print(i)
~~~
Al ejecutar el script nos dara un resultado parecido a lo siguiente: 

![image](https://user-images.githubusercontent.com/111693854/204716066-9456206e-ca31-47c2-99f4-94571279ba37.png)

___

#### SCAN_PORTV2 
___
2. A continuación, se construirá el script scan_portv2.py en base a las siguientes partes

- Se importan las librerías requeridas 
- Se define la función scan sobre la que usando sockets se estarán probando los diferentes puertos
- Se establece una lista de puertos, que para fines prácticos se recomienda sea un número limitado
-  Se crea un bucle for para por cada dirección de un segmento pre-establecido en la variable addr evaluar cada uno de los puertos en la variable ports
** Nota**: Para que el script funcione el segmento de red se deberá ajustar a la red que se tiene configurada en el host donde se prueba

~~~
#Parte 1 
#Importamos librerias requeridas
import socket
#Parte 2 
#Se define la funcion scan con la cual
#se utilizan sockets para probar los diferentes 
#puertos
def scan(addr, port):
    #Creando un nuevo socket 
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Estableciendo el timeout para el nuevo objeto tipo socket
    socket.setdefaulttimeout(1)

    #Conexion exitosa devuelve 0. Devuelve error en caso contrario
    result = socket_obj.connect_ex((addr,port)) #Direccion y puerto en tupla.

    #Se cierra el objeto
    socket_obj.close()

    return result
#Part 3
# lista de puertos a escanear
ports=[21, 22, 25, 80]
#Parte 4 
# bucle por todas las ip del rango 192.168.0.
for i in range (1,255):
    addr="192.168.0.".format(i)
    for port in ports:
        result=scan(addr, port)
        if result==0:
            print(addr, port, "OK")
        else:
            print(addr, port, "Failed")
~~~
Al ejectuarse se mostrara lo siguiente:

![image](https://user-images.githubusercontent.com/111693854/204716618-6a957593-ba35-4530-89f1-e4fa70b99d56.png)

___

#### SCAN_PORTV3
___
3. El siguiente script tiene la misma función que la v1, solo que se emplea threading para tener múltiples hilos y sus partes son en las cuales

- Se importan las librerías necesarias
- Se crea la función tcp_test con la cual se prueban los puertos abiertos usando sockets
- Se genera el bloque principal main de ejecución del script y se guardan los argumentos proporcionados en variables
- El argumento almacenado en portstrs se convierte en lista y sus valores los asignamos a nuevas variables
- Se obtiene la dirección ip del argumento almacenado en la variable host con la función gethostbyname
- Se genera bucle for para probar puertos usando la función tcp_test y generando un hilo por puerto

~~~
# Parte1
#Importamos librerias necesarias
import sys
import threading
from socket import *
#Parte 2 
#Creamos una funcion tcp_test la cual
#permite probar mediante socket los puertos
#abiertos, se le agrega lock.release()
def tcp_test(port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(10)
    result = sock .connect_ex((target_ip, port))
    if result == 0:
        print ("Opened Port:", port)
#Parte 3
#Establecemos el main del script
#Guardamos en variables host y portstrs
if __name__=='__main__':
    # portscan.py <host> <start_port>-<end_port>
    host = sys.argv[1]
    portstrs = sys.argv[2].split('-')
#Parte 4 
#portstrs se convierte en lista al momento
#de hacer split y de ahi obtener dos valores
start_port = int(portstrs[0])
end_port =  int(portstrs[1])
#Parte 5
#Usando la funcion gethostbyname se obtiene
#la direccion ip.
target_ip = gethostbyname(host)
#Parte 6 #Se inicia bucle para probar puertos
#usando la funcion tcp_test y generando
#un hilo por cada puerto a probar
hilos = []
for port in range(start_port, end_port):
    hilo = threading.Thread(target=tcp_test, args=(port,))
    hilos.append(hilo)
    hilo.start()
~~~
Al ejecutarse como resultado se mostrara lo siguiente : 

![image](https://user-images.githubusercontent.com/111693854/204717272-e28110e7-2759-41da-856b-df1cb40e145a.png)
