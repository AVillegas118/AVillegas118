## Nmap
### Se utilizara una de las herramientas mas usadas en el ambiente de la ciberseguridad: **nmap**
___

#### Requerimientos de práctica 
- Nmap instalado en la maquina virtual con Debian 11.
- Una máquina virtual Kioptrix 
___

#### Informacion de red 
___
1. En una ventana de terminal ejecutar lo siguiente a fin a determinar la información de red de tu maquina Debian 11: 
~~~
$ip addr show
~~~
El resultado será similar a lo siguiente: 

![image](https://user-images.githubusercontent.com/111693854/204702211-797c44b1-0407-41d3-8322-9e2d35cd46eb.png)

En este ejemplo mi maquina tiene la dirección 192.168.227.135/24, por lo que se puede deducir
de ella mi subred que sería: 192.168.227.0/24

___

#### A secanear
___
2. Con la información de la subred ya en nuestras manos, busquemos que dispositivos están conectados con:
~~~
$nmap -sn <aquí va tu subred>
~~~
___
3. ya sabemos cuál es nuestra ip, por lo tanto, quedan 2 opciones más, probemos para determinar cual de ellas es la maquina Kioptrix con: 
~~~
$nmap -v -A <aquí va la ip de un dispositivo>
~~~

Se mostrara algo como lo siguiente despues de algunos minutos

![image](https://user-images.githubusercontent.com/111693854/204702786-dbfee04f-f6cb-4a91-84a5-bf9a0570faeb.png)

___
4. evaluamos algunas vulnerabilidades sobre puertos/servicios que el equipo escaneado tiene disponibles, por ejemplo, el puerto 443 (SSL)
~~~
$nmap --script ssl-poodle <aquí va la ip de un dispositivo> 
~~~

___
5. Podemos evaluar alguna otra vulnerabilidad respecto a ese servicio
~~~
$nmap --script ssl-ccs-injection <ip victima> -oN ccs_injections_test.txt
~~~
