## Envió de Correos
### Se realizaran ejercicios en Python para la conexión y posterior envío de correos electronicos
___
Para poder utilizar la cuenta Gmail para los ejercicios  se necesitara configurar un password de aplicacion desde el siguiente link :

https://myaccount.google.com/apppasswords

![image](https://user-images.githubusercontent.com/111693854/204849622-1bbba538-3199-42fe-86db-ef2a189d729c.png)

![image](https://user-images.githubusercontent.com/111693854/204849755-0052c96a-111a-4222-b3a9-b781e003c057.png)

![image](https://user-images.githubusercontent.com/111693854/204849942-22012ebd-7475-4615-a82f-d75e47edb253.png)

___

#### Probando envíos en IDLE
___
1. Abriremos una vnetana de Python IDLE  para probar si funciona la contraseña de la aplicacion ,tambien servira para vlaidar la comunicacion con el servidor de correo Gmail;Ejecutaremos los siguientes comandos 

~~~
import smtplib
~~~

~~~
conn = smptlib.SMTP(‘smtp.gmail.com’, 587)
~~~

~~~
conn.ehlo()
~~~

___
2. Después de establecer el saludo inicial, iniciamos una sesión TLS

~~~
conn.starttls()
~~~

___
3. Ahora proporcionamos la información de acceso, tu cuenta de Gmail y la contraseña de app creada previamente: 

~~~
conn.login(‘aquí va tu correo@gmail.com’, ‘aquí tu contraseña app’)
~~~

___
4. Una vez aceptadas las credenciales haremos una prueba de envió sencilla

~~~
conn.sendmail(‘origen@gmail.com’,’destino@dominio’,’Subject: TestPractica10\n\nHola\n\n Prueba de <matricula> - <Nombre>’) 
~~~
Si al ejecutar nos devuelve "{}" significa que el mensaje fue procesado exitosamente.
___
5. Cerramos la conexión
~~~
conn.quit()
~~~

___

####Script de muestra (Python)
___

~~~
import smtplib,ssl
import getpass

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Peticion de datos para el inicio de sesion 
correo_de_usuario = input("Ingresar tu correo: ")
contraseña = input("ingresa la contraseña: ")
destinatario = input("Ingrese destinatario: ")
asunto = input("Ingrese asunto: ")

#Creacion de un mensaje en html
mensaje = MIMEMultipart("alternative")
mensaje["Subject"] = asunto
mensaje["From"] = correo_de_usuario
mensaje["To"] = destinatario

html = f"""
<html>
<body>
    <b> Practica de envio de correos </b><br><br>
    Ejercicio de practica para envio de correos.<br><br>
    <b>Alumno:</b>(Ingresar nombre)<br><br>
    <b>Matricula:</b> 2013610<br>
</body>
</html>
"""
parte_html = MIMEText(html, "html")

#Agregar el html a mensaje 
mensaje.attach(parte_html)

#Ubicacion de la imagen a adjuntar 
archivo = input("ubicacion de el archivo imagen a mandar   :   ") 

#Codificacion de la imagen de forma estandar 
with open(archivo,"rb") as adjunto:
    contenido_adjunto = MIMEBase("application", "octet-stream")
    contenido_adjunto.set_payload(adjunto.read())

encoders.encode_base64(contenido_adjunto)
contenido_adjunto.add_header(
    "Content-Disposition",
    f"attachment; filename= {archivo}",
)

#Agregar la imagen codificada a mensaje
mensaje.attach(contenido_adjunto)
mensaje_final = mensaje.as_string()

#Envio del correo
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(correo_de_usuario,contraseña)
    server.sendmail(correo_de_usuario, destinatario, mensaje_final)
~~~
