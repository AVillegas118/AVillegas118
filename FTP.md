## FTP
### Se Probaran transferencia de FTP  
___
#### Instalar FTP Server en Debian 11
- Se utilizara una maquina virtual Debian11 
___
1. Actualizamos la lista de repositorios: 
~~~
$sudo apt-get update 
~~~
___
2. Una vez actualizados los repositorios, instalamos un servidor ftp con:
~~~
$sudo apt-get install vsftpd
~~~
___
3. Validamos el servicio de ftp una vez instalado:
~~~
$sudo systemctl status vsftpd 
~~~
___
4. Vamos a realizar varios ajustes a la configuración que trae por default el servidor de FTP, usando un edito de texto (nano en este caso):
~~~
$sudo nano /etc/vsftpd.conf
~~~

En el archivo buscaremos que estén configuradas las siguientes opciones:

- anonymous_enable=NO
- local_enable=YES
- write_enable=YES 
___
5. Vamos a habilitar chroot jail, una propiedad que permite que usuarios de ftp no accedan más allá de los directorios permitidos con las siguientes directivas: 

- chroot_local_users=YES
- user_sub_toke=$USER
- local_root=/home/$USER/ftp
___
6. Al final del archivo agregamos directivas para limitar FTP en modo pasivo, con lo siguiente:

- pasv_min_port=30000
- pasv_max_port=31000 
___
7. Finalmente agregamos también al final del archivo que estamos modificando las siguientes directivas de control de usuarios:

- userlist_enable=YES
- userlist_file=/etc/vsftpd.user_list
- userlist_deny=NO 
___
8. Una vez guardados los cambios reiniciamos el servicio de ftp para aplicar los cambios en su archivo de configuración:
~~~
$sudo systemctl restart vsftpd
~~~

~~~
$sudo systemctl status vsftpd
~~~

![image](https://user-images.githubusercontent.com/111693854/204707640-27f8b0e9-5e82-4525-a8c4-7f028f5b0bc3.png)

___
9. Ahora vamos a crear un usuario para acceso al servidor de FTP
~~~
$sudo adduser <Nombre de el ususario>
~~~
___
10. Agregamos el usuario recién creado a lista de usuarios permitidos en FTP: 
~~~
$echo "<Nombre de el ususario>" | sudo tee -a /etc/vsftpd.user_list 
~~~
___
11.  Creamos los directorios de FTP y aplicamos los permisos correspondientes:
~~~
$sudo mkdir -p /home/<Nombre de el ususario>/ftp/upload 
~~~

~~~
$sudo chmod 500 /home/<Nombre de el ususario>/ftp
~~~

~~~
$sudo chmod 750 /home/<Nombre de el ususario>/ftp/upload 
~~~

~~~
$sudo chown -R <Nombre de el ususario>: /home/<Nombre de el ususario>/ftp
~~~
___

#### Probar transferencias FTP
___
**Desde la maquina host se abrira una ventana en CMD o PowerShell para realizar una transferencia. Es necesario conocer la direccion ip de la maquina virtual **

12. En la maquina virtual de powershell/CMD ejecutamos:
~~~
PS > ftp <ip de tu maquina debian>
~~~
- Usuario: 
- Contraseña:
___
13. Una vez que hayamos iniciado sesión vamos a ejecutar los siguientes comandos de FTP:

- **ls **: sirve para listar el contenido del directorio.
- **cd upload**: permite cambiar nuestra ubicación al directorio “upload”.
- **put ADVERTENCIA.txt**: permite cargar un archivo hacia el servidor 

Archivo ADVERTENCIA.txt
~~~
SE HA CONECTADO A UNA COMPUTADORA DEL GOBIERNO DE EE. UU. SI NO ESTÁ AUTORIZADO PARA ACCEDER A ESTE SISTEMA, 
DESCONECTE AHORA. Todos los intentos de acceder y utilizar este sistema y / o sus recursos están sujetos 
a la supervisión y grabación de pulsaciones de teclas. Todas las personas que usan este sistema consienten 
expresamente dicho monitoreo y se les aconseja que si revelan posibles evidencias de actividad criminal o 
abuso de autoridad, la información será reportada a las autoridades para que actúen. Los intentos de acceso 
no autorizados o el uso que exceda la autoridad documentada pueden someterlo a una multa y / o prisión 
de acuerdo con el Título 18, USC, Sección 1030 o sanciones administrativas o despido.
~~~

___
14. Dentro de nuestra maquina virtual en Debian 11 vamos a validar que el archivo se haya cargado correctamente con los siguientes comandos en terminal:
~~~
$ su - <Nombre de el ususario>
~~~

~~~
$cd ftp/upload
~~~

~~~
$ls
~~~

~~~
$cat ADVERTENCIA.txt
~~~
___
15. Una vez confirmado que el archivo fue cargado exitosamente, en nuestra ventana de
powershell/cmd ejecutamos el comado de FTP para salir: 
~~~
ftp>bye
~~~
