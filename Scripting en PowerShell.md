## Scripting en Powershell
### Se reforza el conocimiento sobre PowerShell a travez de la ejecucion de varios cmd-let propios de la herramienta.
___
#### PARTE 1 – ESCANEO DE EQUIPOS ACTIVOS
**Nota**: Se esta utilizando Powershell ISE o CLI de Powershell
1. Se determina al Gateway de la red interna: 
~~~
$subred = (Get-NetRoute -DestinationPrefix 0.0.0.0/0.NextHop
Write-Host "Tu gateway es: "$subred
~~~
Al ejecutarlo se monstrara algo como lo siguiente

![image](https://user-images.githubusercontent.com/111693854/204615043-fdab6fa2-edc4-44b9-a25e-0fba4e22ffa2.png)

___
2. Obteniendo el rango de la subred interna
~~~
$rango = $subred.Substring(0,$subred.IndexOf('.') + 1 + $subred.Substring(subred.IndexOf('.') + 3 )
echo $rango
~~~
Al ejecutarlo se monstrara algo como lo siguiente

![image](https://user-images.githubusercontent.com/111693854/204615135-49ac21ee-2f61-4cd2-ae93-056311a2631a.png)

___
3. Probando “Test-Connection” para validar respuesta de un servidor, probaremos con el
Gateway de nuestra red (ej. 192.68.1.254): 
~~~
$respuesta = Test-Connection 192.168.1.254 -Quiet -Count 1
Write-Host $respuesta
~~~
Al ejecutar si hay respuesta el resultado de la variables $respuesta es "True"

___
4. Generar una prueba de bucle foreach para procesar valores de un array
**Ejemplo**:
~~~
$rango_ip = @(1..254)
foreach ( $ip in rango_ip )
{
Write-Host "Direccion ip :"$ip
}
~~~

___
5. Una vez que ya obtuvimos el rango de nuestra subred, también sabemos cómo probar una
conexión hacia algún equipo de nuestra subred y sabemos hacer un bucle foreach, el paso a seguir es construir nuestro script de escaneo de equipos activos en nuestra subred.

~~~
# Determinando gateway 
$subred = (Get-NetRoute -DestinationPrefix 0.0.0.0/0).NextHop
Write-Host "== Determinando tu gateway ..."
Write-Host "Tu gateway: $subred " 
#
# Determinando rango de subred 
#
$rango = $subred.Substring(0,$subred.IndexOf('.') + 1 + $subred.Substring($subred.IndexOf('.') + 1).IndexOf('.') + 3)
Write-Host "== Determinando tu rango de subred ..."
echo $rango 
#
# Determinando si rango termina en "."
#
$punto = $rango.Endswith('.')
if ( $punto -like "False" )
{
	$rango = $rango + '.' 
}
#
# Creamos un array con 254 numeros ( 1 a 254 )
#
$rango_ip = @(1..254)
#
# Generamos un bucle ferach para validar hosts activos en nuestra subred
#
Write-Output ""
Write-Host "-- Subred actual:"
Write-Host "Escaneando: " -NoNewline ; Write-Host $rango -NoNewline; Write-Host "0/24" -ForegroundColor Red
Write-Output ""
foreach ( $r in $rango_ip ) 
{
	$actual = $rango + $r 
	$responde = Test-Connection $actual -Quie -Count 1
	if ($responde -eq "True" ) 
	{
		Write-Output ""
		Write-Host " Host responde: " -NoNewline; Write-Host $actual -ForegroundColor Green
	}

}
~~~
Guardamos el script con el nombre scan_alive1.ps1
**Para ejecutar el script se coloca en Powershell ".\scan_alive1.ps1"**

Al ejecutar el script scan_alive1.ps1 se mostrara algo como lo siguiente 

![image](https://user-images.githubusercontent.com/111693854/204619580-399734eb-4059-4e4f-a1cc-4786acdce345.png)

___

#### PARTE 2 – Escaneo puertos de un equipo en la subred
___
1. Determinamos la dirección de ip de nuestro equipo ejecutan “ipconfig” en nuestra terminal de powershell:
~~~
ipconfig
~~~
Se mostrara algo como lo siguiente 

![image](https://user-images.githubusercontent.com/111693854/204620392-398d3e45-8f40-45c2-a070-d71a64006a34.png)

**En mi caso la direccion es "192.168.1.67"**
___
8. Ahora verificaremos que varios puertos estén activos o abiertos en dicho equipo de esta manera
~~~
try{ $resultado = $TCPObject.ConnectAsync("192.168.1.67",139).Wait(100)}catch{}
echo $resultado
~~~

~~~
try{ $rsultado = $TCPObject.ConnectAsync("192.168.1.67",445).Wait(100)}catch{}
echo $resultado
~~~

___
9. Reutilizaremos el mismo código utilizado en “scan_alivev1.ps1” en lo siguiente:
~~~
#
#Escaneo de puertos (mas comunes) en equipos de la misma subred
#Determinando gateway 
#
$subred = (Get-NetRoute -DestinationPrefix 0.0.0.0/0).NextHop
Write-Host "== Determinando tu gateway ..."
Write-Host "Tu gateway: $subred " 
#
# Determinando rango de subred 
#
$rango = $subred.Substring(0,$subred.IndexOf('.') + 1 + $subred.Substring($subred.IndexOf('.') + 1).IndexOf('.') + 3)
Write-Host "== Determinando tu rango de subred ..."
echo $rango 
#
# Determinando si rango termina en "."
#
$punto = $rango.Endswith('.')
if ( $punto -like "False" )
{
	$rango = $rango + '.' 
}
#
#Definimos un array con puertos a escanear 
#Establecemos una variable para Waittime
#
$portstoscan = @(20,21,22,23,25,50,53,80,110,119,135,136,137,138,139,143,161,162,389,443,445,636,1025,1443,3389,5985,5986,8080,10000)
$waittime = 100
#
# Solicitamos dirreccion ip a escanear: 
#
Write-Host "Direccion Ip a scanear: " -NoNewline
$direccion = Read-Host
#
# Generamos bucle foreach para evaluar cada puerto en $portstoscan 
#
foreach ($p in  $portstoscan )
{
    $TCPObject = New-Object System.Net.Sockets.TcpClient
    try{ $resultado = $TCPObject.ConnectAsync($direccion,$p).Wait($waittime)}catch{}
    if ( $resultado -eq "True" )
    {
        Write-Host "Puerto Abierto:" -NoNewline;Write-Host $p -ForegroundColor Green
    }
}
~~~

Igual que en el caso de scan_alive, guardaremos el script con el nombre de
“scan_portv1.ps1”, y lo mandaremos ejecutar así: 
**"./scan_portv1.ps1"**

Se mostrara algo como lo siguiente

![image](https://user-images.githubusercontent.com/111693854/204624637-3ab3339c-db2f-472f-95e7-a555df80ec1d.png)
