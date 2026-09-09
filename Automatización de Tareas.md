# Automatización segura de tareas

Automatizar significa programar una tarea repetitiva para que se ejecute de manera
consistente. Este apunte crea inventarios locales de procesos; no envía información
fuera del equipo.

## Riesgos que debemos considerar

- Un script automático repite también sus errores.
- Las tareas heredarán permisos del usuario que las ejecuta.
- Los archivos de salida pueden contener información sensible.
- Una frecuencia excesiva puede llenar el disco o consumir recursos.
- Las rutas relativas pueden apuntar a lugares inesperados.

Primero prueba el script manualmente y usa el mínimo privilegio necesario.

## Linux: guardar un resumen de procesos

Guarda `process_snapshot.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

output_dir="${XDG_STATE_HOME:-$HOME/.local/state}/process-snapshots"
timestamp=$(date -u +'%Y-%m-%dT%H-%M-%SZ')

umask 077
mkdir -p -- "$output_dir"
ps -eo pid,user,comm --sort=pid > "$output_dir/processes-$timestamp.txt"

printf 'Inventario guardado en %s\n' "$output_dir/processes-$timestamp.txt"
```

Detalles importantes:

- `set -euo pipefail` hace visibles varios errores.
- La fecha UTC evita nombres ambiguos.
- `umask 077` limita los nuevos archivos al usuario actual.
- `ps -eo` selecciona sólo las columnas necesarias.
- No se necesita `sudo`.

Prueba manual:

```bash
chmod u+x process_snapshot.sh
./process_snapshot.sh
```

## Programarlo con cron

Consulta tus tareas actuales antes de editar:

```bash
crontab -l
crontab -e
```

Ejemplo para ejecutar una vez cada hora:

```cron
0 * * * * /ruta/absoluta/process_snapshot.sh >> /ruta/absoluta/cron.log 2>&1
```

Usa rutas absolutas porque el entorno de cron es más limitado que una terminal.
Después comprueba `cron.log` y el directorio de resultados.

Los cinco campos son minuto, hora, día del mes, mes y día de la semana. Para
reproducir la frecuencia de cinco minutos del apunte original, cambia `0 * * * *`
por `*/5 * * * *`. Para empezar, una vez por hora genera menos archivos. `tail -f`
permite seguir el registro mientras se ejecuta: `tail -f /ruta/absoluta/cron.log`.
Referencia: [formato de crontab en Debian](https://manpages.debian.org/trixie/cron/crontab.5.en.html).

Para dejar de ejecutar la tarea, elimina únicamente esa línea mediante `crontab -e`.
No uses `crontab -r`, porque borraría todas las tareas del usuario.

## Windows: tarea programada con PowerShell

Primero prepara una carpeta de práctica dentro de tu perfil:

```powershell
$LabDirectory = Join-Path $env:LOCALAPPDATA "CyberLab"
New-Item -ItemType Directory -Path $LabDirectory -Force | Out-Null
Write-Output $LabDirectory
```

Guarda el siguiente archivo como `Get-ProcessSnapshot.ps1` dentro de esa carpeta:

```powershell
$OutputDirectory = Join-Path $env:LOCALAPPDATA "ProcessSnapshots"
$Timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH-mm-ssZ")

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
Get-Process |
    Select-Object Name, Id, CPU |
    Export-Csv -Path (Join-Path $OutputDirectory "processes-$Timestamp.csv") `
        -NoTypeInformation -Encoding UTF8
```

Prueba el archivo manualmente. Después, desde la misma ventana de PowerShell:

```powershell
$ScriptPath = Join-Path $LabDirectory "Get-ProcessSnapshot.ps1"
& $ScriptPath

$Action = New-ScheduledTaskAction `
    -Execute "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
    -Argument ('-NoProfile -File "{0}"' -f $ScriptPath)

$Trigger = New-ScheduledTaskTrigger -Daily -At 10:00
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$Principal = New-ScheduledTaskPrincipal -UserId $CurrentUser `
    -LogonType Interactive -RunLevel Limited

Register-ScheduledTask `
    -TaskName "ProcessSnapshotLab" `
    -Action $Action `
    -Trigger $Trigger `
    -Principal $Principal `
    -Description "Inventario local de procesos para aprendizaje"
```

La **acción** dice qué ejecutar, el **desencadenador** dice cuándo y el **usuario**
define con qué permisos. Este ejemplo se ejecuta con tu sesión iniciada y sin
elevación. Si una política del equipo impide crear tareas, consulta esa restricción.
No se añade una contraseña al script.
Referencia: [usuario de una tarea programada](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtaskprincipal?view=windowsserver2025-ps).

Para revisar y retirar sólo esta tarea:

```powershell
Get-ScheduledTask -TaskName "ProcessSnapshotLab"
Unregister-ScheduledTask -TaskName "ProcessSnapshotLab" -Confirm
```

## Práctica corta del apunte original: abrir la calculadora

Con `$Principal` definido en el ejemplo anterior, programa una sola ejecución
dentro de dos minutos. Así puedes ver el resultado mientras tienes sesión iniciada:

```powershell
$CalculatorAction = New-ScheduledTaskAction -Execute "$env:SystemRoot\System32\calc.exe"
$OnceTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2)

Register-ScheduledTask -TaskName "CalculatorLab" -Action $CalculatorAction `
    -Trigger $OnceTrigger -Principal $Principal `
    -Description "Práctica de una tarea de una sola ejecución"
```

Después de observarla puedes retirar sólo esa tarea:

```powershell
Unregister-ScheduledTask -TaskName "CalculatorLab" -Confirm
```

## Inventario del sistema: la parte de `SEND_SYSINFO`

El apunte original también recogía información del sistema. Este ejemplo conserva
esa práctica y guarda su resultado localmente. `Get-CimInstance` consulta las
clases del sistema y `[pscustomobject]` reúne los datos en una fila:

```powershell
$Computer = Get-CimInstance -ClassName Win32_ComputerSystem
$OperatingSystem = Get-CimInstance -ClassName Win32_OperatingSystem
$Processors = Get-CimInstance -ClassName Win32_Processor
$InventoryPath = Join-Path $env:LOCALAPPDATA "system-inventory.csv"

[pscustomobject]@{
    ComputerName = $Computer.Name
    Manufacturer = $Computer.Manufacturer
    Model = $Computer.Model
    RAM_GB = [math]::Round($Computer.TotalPhysicalMemory / 1GB, 2)
    OS = $OperatingSystem.Caption
    CPU = ($Processors.Name -join "; ")
    LoggedOnUser = $Computer.UserName
} | Export-Csv -LiteralPath $InventoryPath -NoTypeInformation -Encoding UTF8

Write-Output "Inventario guardado en: $InventoryPath"
```

Guárdalo como otro archivo `.ps1` si quieres programarlo con el mismo procedimiento.
Referencia: [Get-CimInstance](https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance?view=powershell-7.5).

Para continuar con la parte de correo, revisa [Envío de correos](Envi%C3%B3%20de%20Correos.md).
Prueba primero el envío con contenido ficticio y verifica el destinatario. Un
inventario real contiene nombres de equipos y usuarios; no lo envíes ni publiques
automáticamente como salida de la práctica.

## Siguientes pasos

1. Eliminar automáticamente inventarios de más de siete días.
2. Registrar errores con fecha y código de salida.
3. Comparar dos inventarios para localizar procesos nuevos.
4. Añadir una prueba que escriba sólo dentro de un directorio temporal.
