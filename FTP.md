# FTP en un laboratorio aislado

FTP es un protocolo clásico para transferir archivos. En su forma normal **no cifra
usuarios, contraseñas ni contenido**, por lo que no es apropiado para enviar datos
sensibles a través de redes no confiables.

Esta práctica sirve para comprender un protocolo antiguo dentro de una máquina
virtual aislada. Para sistemas reales suelen preferirse SFTP (sobre SSH) o una
configuración FTPS administrada correctamente.

## Conceptos

- **Servidor:** recibe conexiones y ofrece los archivos permitidos.
- **Cliente:** programa que se conecta al servidor.
- **Modo pasivo:** el servidor abre un rango adicional de puertos para los datos.
- **Chroot:** limita al usuario a una parte del sistema de archivos.
- **Texto claro:** información que viaja sin cifrado.

## Requisitos del laboratorio

- Una máquina virtual Debian sin puertos publicados hacia Internet.
- Una instantánea de la VM para poder regresar al estado anterior.
- Un usuario y contraseña ficticios usados sólo en el laboratorio.

## 1. Instalar y detener antes de configurar

```bash
sudo apt update
sudo apt install vsftpd
sudo systemctl stop vsftpd
sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.backup
```

Detener el servicio permite revisar la configuración antes de exponerlo incluso en
la red del laboratorio.

## 2. Configuración mínima de práctica

Edita `/etc/vsftpd.conf` con `sudo nano /etc/vsftpd.conf`. Ajusta las directivas
existentes y añade sólo las que falten; conserva el resto del archivo de Debian,
incluido `pam_service_name=vsftpd`. No dejes una opción repetida con otro valor.

```ini
listen=YES
listen_ipv6=NO
listen_address=127.0.0.1
anonymous_enable=NO
local_enable=YES
write_enable=YES
chroot_local_user=YES
user_sub_token=$USER
local_root=/home/$USER/ftp
userlist_enable=YES
userlist_file=/etc/vsftpd.user_list
userlist_deny=NO
pasv_min_port=30000
pasv_max_port=30010
```

- `listen` y `listen_ipv6` no pueden estar activos a la vez. Aquí usamos IPv4.
- `listen_address` permite empezar con conexiones desde la misma VM.
- El acceso anónimo queda desactivado.
- La lista permite únicamente usuarios seleccionados.
- `chroot_local_user` limita su vista del sistema de archivos.
- El rango pasivo es pequeño para facilitar el laboratorio.

`$USER` se escribe literalmente en este archivo; vsftpd lo sustituye por el usuario
que inicia sesión. Un `chroot` no sustituye el cifrado.

Referencia: [opciones de vsftpd](https://security.appspot.com/vsftpd/vsftpd_conf.html).

## 3. Crear un usuario exclusivo

```bash
sudo adduser ftp-lab
printf '%s\n' 'ftp-lab' | sudo tee /etc/vsftpd.user_list
sudo mkdir -p /home/ftp-lab/ftp/upload
sudo chown root:root /home/ftp-lab/ftp
sudo chmod 755 /home/ftp-lab/ftp
sudo chown ftp-lab:ftp-lab /home/ftp-lab/ftp/upload
sudo chmod 750 /home/ftp-lab/ftp/upload
```

La raíz pertenece a `root` y el usuario sólo puede escribir dentro de `upload`.

## 4. Arrancar y revisar errores

vsftpd no ofrece una opción de comprobación de sintaxis sin arrancar. Inícialo con
el servicio y revisa su estado:

```bash
sudo systemctl restart vsftpd
sudo systemctl status vsftpd --no-pager
sudo journalctl -u vsftpd -n 30 --no-pager
```

El estado esperado es `active (running)`. Si falla, revisa el mensaje del registro,
el nombre de las opciones y que sólo un modo de escucha esté activo. Ejecutar
`vsftpd -olisten=NO /etc/vsftpd.conf` **no es una validación**: carga opciones y
lanza el servidor; el archivo incluso puede sobrescribir `listen=NO`.
Consulta el [manual de ejecución de vsftpd en Debian](https://manpages.debian.org/trixie/vsftpd/vsftpd.8.en.html).

## 5. Probar desde la misma máquina

En la VM instala el cliente y prepara un archivo de texto sin información personal:

```bash
sudo apt install ftp
printf 'Archivo de ejemplo del laboratorio FTP.\n' > ejemplo.txt
ftp 127.0.0.1
```

Introduce el usuario y después la contraseña cuando el cliente los pida. Ya dentro
de FTP, ejecuta los comandos que aparecen tras `ftp>`; no copies ese indicador:

```text
Name: ftp-lab
Password: <contraseña ficticia del laboratorio>
ftp> cd upload
ftp> put ejemplo.txt
ftp> ls
ftp> bye
```

`put` sube un archivo desde el directorio donde abriste el cliente; `ls` lista
los archivos del servidor y `bye` cierra la sesión. Comprueba el contenido recibido:

```bash
sudo cat /home/ftp-lab/ftp/upload/ejemplo.txt
```

Debe mostrar la misma frase. Si `put` indica que no encuentra el archivo, comprueba
el directorio local. Si rechaza la escritura, revisa que estés dentro de `upload`
y los permisos del paso 3.

## Prueba opcional desde Windows u otra máquina del laboratorio

En la VM usa `ip -brief address` para consultar su IP de la red aislada. Sustituye
`listen_address=127.0.0.1` por esa IP y reinicia el servicio. Desde un cliente FTP
con modo pasivo, conecta a esa dirección, puerto `21`, con `ftp-lab`. Repite la
transferencia y la comprobación del archivo. Si hay un firewall, permite desde el
cliente del laboratorio TCP `21` y `30000–30010`; no abras puertos del router.

Comprueba que el cliente elegido esté configurado en modo pasivo para practicar
con el rango definido; el modo activo usa otra dirección de conexión. Al terminar vuelve
a `listen_address=127.0.0.1` y reinicia, o detén el laboratorio en el siguiente paso.

## 6. Limpiar el laboratorio

```bash
sudo systemctl disable --now vsftpd
```

Después puedes restaurar la instantánea de la máquina virtual. Si conservas la VM,
elimina el usuario ficticio y la configuración cuando ya no se necesiten.

## Qué demuestra la práctica

- Diferencia entre cliente y servidor.
- Permisos y separación de directorios.
- Riesgo de protocolos sin cifrado.
- Importancia de limitar usuarios, red y tiempo de exposición.

## Siguientes pasos

1. Capturar tráfico dentro del laboratorio y observar por qué FTP no protege las
   credenciales; nunca captures tráfico de otras personas.
2. Repetir la transferencia con SFTP y comparar los protocolos.
3. Documentar qué puertos necesita el modo pasivo.
