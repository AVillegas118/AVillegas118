# Fundamentos de scripting en PowerShell

Apunte de aprendizaje centrado en administración y seguridad defensiva. Practicarás
con variables, procesos, archivos y las comprobaciones de red del apunte original.
Los ejemplos de red empiezan en `127.0.0.1`, el propio equipo; para usar una VM,
introduce sólo una dirección de tu laboratorio.

Los cmdlets de red, eventos y tareas de estas notas están pensados para Windows.
PowerShell también existe en Linux, pero allí no están disponibles todos esos módulos.

## 1. Cmdlets y ayuda

PowerShell utiliza comandos con formato `Verbo-Sustantivo`:

```powershell
Get-Help Get-Process -Examples
Get-Process | Select-Object -First 5
```

`Get-Help` explica un cmdlet y `Get-Process` obtiene procesos. La tubería (`|`)
envía objetos completos, no sólo texto, al siguiente comando.

## 2. Variables y salida

```powershell
$ProjectName = "Laboratorio defensivo"
Write-Output "Proyecto: $ProjectName"
```

Los nombres descriptivos facilitan la lectura. No guardes contraseñas, tokens ni
claves API directamente en variables dentro de un script publicado.

## 3. Filtrar y seleccionar objetos

```powershell
Get-Process |
    Where-Object CPU -GT 10 |
    Sort-Object CPU -Descending |
    Select-Object -First 10 Name, Id, CPU
```

Este ejemplo muestra procesos que han consumido más de diez segundos de CPU. Un
consumo alto no implica malware; sólo es un dato que puede investigarse.

## 4. Calcular la huella de un archivo

```powershell
$Path = ".\configuracion.txt"

if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    Write-Error "No existe el archivo: $Path"
    exit 1
}

Get-FileHash -LiteralPath $Path -Algorithm SHA256
```

Un hash es una huella del contenido. Si cambia el archivo, normalmente cambia su
SHA-256. El hash no cifra ni protege el archivo por sí solo.

## 5. Script defensivo: inventario de procesos

Guarda este contenido como `Get-ProcessSnapshot.ps1`:

```powershell
[CmdletBinding()]
param(
    [string]$OutputPath = ".\process-snapshot.csv"
)

$Processes = Get-Process -ErrorAction Stop |
    Select-Object Name, Id, Path, StartTime

$Processes | Export-Csv -LiteralPath $OutputPath -NoTypeInformation -Encoding UTF8
Write-Output "Inventario guardado en: $OutputPath"
```

El resultado sirve para comparar el estado del equipo en distintos momentos. Puede
contener nombres de usuario o rutas internas; no lo subas automáticamente a un
repositorio público.

## 6. Revisar eventos de inicio de sesión fallido

En Windows, el evento de seguridad `4625` representa un inicio de sesión fallido:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = "Security"
    Id      = 4625
} -MaxEvents 10 |
    Select-Object TimeCreated, Id, Message
```

La lectura del registro `Security` puede requerir una terminal con permisos de
administrador. Los fallos también pueden tener causas legítimas, como una contraseña
antigua guardada en un servicio.

## 7. Manejo básico de errores

```powershell
try {
    Get-Content -LiteralPath ".\archivo.txt" -ErrorAction Stop
}
catch {
    Write-Error "No se pudo leer el archivo: $($_.Exception.Message)"
}
```

`-ErrorAction Stop` permite que `catch` reciba el error. Mostrar un mensaje claro es
mejor que ocultarlo con un bloque `catch {}` vacío.

## 8. Consultar IP y puerta de enlace

En Windows:

```powershell
Get-NetIPConfiguration |
    Select-Object InterfaceAlias, IPv4Address, IPv4DefaultGateway

Get-NetIPAddress -AddressFamily IPv4 |
    Select-Object InterfaceAlias, IPAddress, PrefixLength
```

La IP identifica una interfaz del equipo. La puerta de enlace permite llegar a
otras redes. `PrefixLength` describe qué parte de la dirección corresponde a la
red. Una VPN o varias tarjetas pueden mostrar varias entradas; no supongas que
la primera corresponde a tu laboratorio.

El código antiguo intentaba construir la subred recortando el texto de la puerta
de enlace. Eso falla con prefijos distintos de `/24` y con varias rutas. Para esta
práctica usa una lista explícita de las IP que quieres comprobar.
Referencia: [Get-NetIPConfiguration](https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-netipconfiguration?view=windowsserver2025-ps).

## 9. Comprobar equipos con `Test-Connection` y `foreach`

Guarda este script como `scan_alive1.ps1`:

```powershell
[CmdletBinding()]
param(
    [string[]]$TargetAddresses = @("127.0.0.1")
)

foreach ($Address in $TargetAddresses) {
    $Responds = Test-Connection -ComputerName $Address -Count 1 -Quiet
    [pscustomobject]@{
        Address = $Address
        RespondsToPing = $Responds
    }
}
```

`foreach` repite el bloque para cada elemento del array. `-Quiet` devuelve un
booleano (`True` o `False`) en vez del informe completo. Un equipo que no responde
a ping puede seguir encendido y ofrecer servicios: algunos bloquean ICMP.

```powershell
.\scan_alive1.ps1
# Ejemplo opcional: reemplaza estas IP por dos VM de tu laboratorio.
.\scan_alive1.ps1 -TargetAddresses "192.168.56.10", "192.168.56.11"
```

Referencia: [Test-Connection](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-connection).

## 10. Comprobar puertos TCP de un equipo

Guarda como `scan_portv1.ps1`:

```powershell
[CmdletBinding()]
param(
    [string]$TargetAddress = "127.0.0.1",
    [ValidateRange(1, 65535)]
    [int[]]$Ports = @(22, 80, 443)
)

foreach ($Port in $Ports) {
    $Connected = Test-NetConnection -ComputerName $TargetAddress `
        -Port $Port -InformationLevel Quiet

    [pscustomobject]@{
        Address = $TargetAddress
        Port = $Port
        TcpConnectionSucceeded = $Connected
    }
}
```

```powershell
.\scan_portv1.ps1
.\scan_portv1.ps1 -TargetAddress "127.0.0.1" -Ports 8000
```

`True` significa que se pudo establecer una conexión TCP; `False` sólo indica que
la conexión no se completó. No distingue por sí solo un puerto cerrado de un
firewall o un problema de red. Es normal que las comprobaciones fallidas tarden.

Este ejemplo usa un cmdlet de Windows para que se entienda el bucle. En el original,
`TcpClient` debía crearse antes de cada intento, reiniciar el resultado y cerrarse
en `finally`; de otro modo quedaban conexiones sin liberar o resultados anteriores.
Referencia: [Test-NetConnection](https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection).

## Ejecutar un script local

```powershell
.\Get-ProcessSnapshot.ps1
```

Si la política impide la ejecución durante una práctica autorizada, consulta antes
su valor:

```powershell
Get-ExecutionPolicy -List
```

No desactives permanentemente los controles del sistema sólo para ejecutar un
ejemplo descargado.

## Errores comunes

- Confundir objetos de PowerShell con texto plano.
- Ocultar todos los errores mediante `catch {}`.
- Usar `Write-Host` cuando la salida debe continuar por la tubería.
- Publicar archivos CSV con información del equipo.
- Copiar scripts y ejecutarlos con privilegios sin revisarlos.

## Siguientes pasos

1. Comparar dos inventarios de procesos con `Compare-Object`.
2. Exportar eventos seleccionados a JSON.
3. Añadir parámetros de fecha al análisis de eventos.
4. Escribir pruebas con Pester.

## Uso responsable

Consulta registros y comprueba conexiones sólo en tu equipo o laboratorio autorizado.
Revisa los inventarios antes de compartirlos para quitar datos personales.
