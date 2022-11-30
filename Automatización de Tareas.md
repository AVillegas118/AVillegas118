## Automatización de Tareas
### La automatización de tareas es una tarea inevitable y en muchas de las ocasiones necesaria, y es que a fin de hacer más eficiente el trabajo automatizar es una actividad vital
___

#### Automatizando tareas en Linux 
___
**Nota**: Se utilizara una mauina Debian11
1. Usando cualquier editor de texto de tu preferencia guardar el siguiente código con el nombre “proc_mon.sh” 
~~~
#!/bin/bah
#
# Script para listar procesos ejecutandose 
# en el servidor.
#
## Variables
#
TIME='date +%d-%m-Y %H:%M:5'
FECHA='date +%d-%m-%Y'
#
## Creando directorio de Log
#
if [ ! -d "$HOME/log" ]
then
        mkdir $HOME/log
fi
#
## Listando procesos
#
echo "#" >> '$HOME'/log/procesos_'${FECHA}'.log
echo "###############################################################" >> $HOME/log/procesos_${FECHA}.log
echo "#" >> '$HOME'/log/procesos_${FECHA}.log
echo "Hora:"$TIME >> $HOME/log/procesos_${FECHA}.log
ps -ef >> $HOME/log/procesos_${FECHA}.log
echo "TOTAL DE PROCESOS: "'ps -ef |wc -1' >> $HOME/log/procesos_${FECHA}.log
echo "Hora:"$TIME >> $HOME/log/procesos_${FECHA}.log
#
~~~
___
2. Le asignamos los permisos 
~~~
$chmod +x proc_mon.sh
~~~
Al ejecutarse  manual mente deberia de verse asi 

![image](https://user-images.githubusercontent.com/111693854/204856761-cf310818-cf74-4cdb-8dba-0bfe57ae0aff.png)

___
3. Ahora vamos a automatizar dicho proceso mediante la programación de la ejecución de este script cada cierto tiempo , en este caso seran cada 5 minutos
~~~
$EDITOR=nano; export EDITOR
~~~

~~~
$crontab -e
~~~

![image](https://user-images.githubusercontent.com/111693854/204857169-14548439-37db-4984-9e07-92b15284e9a2.png)

___
4. Confirmamos los cambios
~~~
$crontab -l
~~~

___
5. Despues de 5 minutos ejecutaremos el siguiente comando 
~~~
$tail -f procesos-<fecha>.log
~~~

![image](https://user-images.githubusercontent.com/111693854/204857556-a0357f0c-1e29-4d31-b814-d7cb78203972.png)

___

#### Automatizando tareas en Windows
___

#### Task con PowerShell
___
1. En una ventana de powershell probaremos los cmd-let básicos para programación de tareas con powershell
~~~
PS> $tarea = New-ScheduledTaskAction -Execute ‘calc.exe’
~~~

___
2. Ahora dentro de la variable “trigger” estableceremos cuando se ejecutará dicha tarea, para este ejemplo será solo una vez (Once)
~~~
PS> $trigger = New-ScheduledTasktrigger -Once -At 08:45am 
~~~
**Nota**: La hora es a su preferencia 

___
3. Finalmente vamos a programa la tarea de la siguiente manera
~~~
Register-ScheduledTask -Action $tarea -Trigger $trigger -TaskPath “MisTareas” -TaskName “ArrancaCalc” -Description “Tarea que abre la Calculadora” 
~~~
**Esperamos a la hora puesta y veremos los siguiente**

![image](https://user-images.githubusercontent.com/111693854/204858598-2b6bd215-92f5-4407-b820-373e560056d9.png)

___

#### SEND_SYSINFO
___
Este es un script que manda correos ,se deben de cambiar las direcciones de correos ,y colocar la contraseña de aplicacion del correo gmail

~~~
#
# Script de PowerShell que obtiene información basica de un equipo
# lo guarda en un archivo csv
# Posteriormente envia ese archivo a través de correo electronico
# usando una cuenta de gmail.
#
############ Get Information 
#
$computer=hostname
$query = Get-WmiObject -Class win32_computersystem -ComputerName $computer
$name = $query.Name
$make = $query.Manufacturer
$model = $query.Model
$ram = $query.TotalPhysicalMemory/1Gb
$os = (Get-WmiObject -Class win32_operatingsystem -ComputerName $computer).Caption
$cpu = (Get-WmiObject -Class Win32_processor -ComputerName $computer).Name
$users = $query.Username
#
# Llenando arraya para generación de csv
#
$Object = New-Object PSObject
$Object | Add-Member -MemberType NoteProperty -Name "ComputerName" -Value $name
$Object | Add-Member -MemberType NoteProperty -Name "Make" -Value $make
$Object | Add-Member -MemberType NoteProperty -Name "Model" -Value $model
$Object | Add-Member -MemberType NoteProperty -Name "RAM" -Value $ram
$Object | Add-Member -MemberType NoteProperty -Name "OS" -Value $os
$Object | Add-Member -MemberType NoteProperty -Name "CPU" -Value $cpu
$Object | Add-Member -MemberType NoteProperty -Name "LoggedOnUsers" -Value $users
$array = $Object
$array | Export-Csv -Path c:\scripts\test.csv -NoTypeInformation # Aqui se genera archivo csv
#
#### Para Envio de correo
#
$Username = "@gmail.com"; # Aqui va tu cuenta de gmail
$Password = "clave super secreta";      # Aqui va tu password de aplicación
$path = "C:\scripts\test.csv";       # Aqui va la ruta de el archivo csv generado previamente
function Send-ToEmail([string]$email, [string]$attachmentpath){
    $message = new-object Net.Mail.MailMessage;
    $message.From = "@gmail.com"; # Aqui va tu cuenta de gmail.
    $message.To.Add($email);
    $message.Subject = "<Aqui va el asunto>."; #Asunto del correo
    $message.Body = "<Aqui va el cuerpo del mensaje"; #Cuerpo o Mensaje del correo.
    $attachment = New-Object Net.Mail.Attachment($attachmentpath);
    $message.Attachments.Add($attachment);
    $smtp = new-object Net.Mail.SmtpClient("smtp.gmail.com", "587");
    $smtp.EnableSSL = $true;
    $smtp.Credentials = New-Object System.Net.NetworkCredential($Username, $Password);
    $smtp.send($message);
    write-host "Mail Sent" ; 
    $attachment.Dispose();
 }
 Send-ToEmail  -email "destinario@dominio.com" -attachmentpath $path; # En email pones el destinatario
~~~

___

#### Automatizacion de scripts
___
En este caso se utilizara el archivo .py llamado SEND_SYSINFO


![image](https://user-images.githubusercontent.com/111693854/204860037-a1388b60-399f-4d01-ad7f-c93da71ef479.png)

Comprobamos que se ejecuto correctamente revisando nuestra bandeja de entrada 

![image](https://user-images.githubusercontent.com/111693854/204860184-850f720f-d87c-46b3-8c65-290360ece03c.png)


