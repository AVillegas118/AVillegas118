# Fundamentos de scripting en Bash

Apunte de aprendizaje para practicar Bash con ejemplos pequeños y defensivos. Los
comandos se pueden ejecutar en una máquina virtual de Linux sin conectarse a otros
equipos.

## 1. Primer script

Crea `welcome.sh`:

```bash
#!/usr/bin/env bash

name="${1:-mundo}"
printf 'Hola, %s\n' "$name"
```

La primera línea indica que el sistema debe buscar Bash en el entorno actual. Para
dar permiso de ejecución y probarlo:

```bash
chmod u+x welcome.sh
./welcome.sh Ana
```

También se puede ejecutar con `bash welcome.sh Ana` sin cambiar sus permisos.
Usar `. welcome.sh` es diferente: ejecuta el contenido dentro de la terminal actual
y puede modificar sus variables. No conviene usarlo por costumbre.

## 2. Permisos básicos

```bash
ls -l welcome.sh
chmod 700 welcome.sh
```

`700` concede lectura, escritura y ejecución únicamente al propietario. `755`
también permite que otras personas lean y ejecuten el archivo. Se debe elegir el
permiso mínimo necesario.

## 3. Variables y comillas

```bash
project_name="laboratorio defensivo"
printf 'Proyecto: %s\n' "$project_name"
printf 'Directorio actual: %s\n' "$PWD"
```

Las comillas alrededor de `"$project_name"` evitan que Bash divida el valor por
espacios o expanda caracteres especiales. Es una práctica importante para evitar
errores y comportamientos inesperados.

Para consultar variables del entorno:

```bash
printenv
printf '%s\n' "$PATH"
```

No publiques la salida completa de `printenv`: puede contener rutas, tokens u otros
datos del equipo.

## 4. Leer datos del usuario

```bash
#!/usr/bin/env bash

read -r -p "Escribe tu nombre: " name
printf 'Hola, %s\n' "$name"
```

`-r` evita que las barras invertidas se interpreten como caracteres especiales.
Las contraseñas no deben recibirse ni mostrarse con este ejemplo.

## 5. Combinar comandos

Una tubería (`|`) envía la salida de un comando al siguiente:

```bash
ps -ef | wc -l
ip addr show | grep -w inet
```

El primer ejemplo cuenta líneas de procesos. El segundo filtra direcciones IP del
propio equipo. `grep` puede terminar con código `1` cuando no encuentra resultados;
eso no siempre significa que el programa esté roto.

## 6. Mini ejercicio defensivo: resumir fallos SSH

Este script sólo lee un archivo local. Guárdalo como `failed_ssh_summary.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
    printf 'Uso: %s <archivo-auth.log>\n' "$0" >&2
    exit 1
fi

log_file=$1
if [[ ! -r "$log_file" ]]; then
    printf 'Error: no se puede leer %s\n' "$log_file" >&2
    exit 1
fi

awk '
    /Failed password/ {
        for (i = 1; i <= NF; i++) {
            if ($i == "from") {
                failures[$(i + 1)]++
            }
        }
    }
    END {
        for (ip in failures) {
            printf "%5d  %s\n", failures[ip], ip
        }
    }
' "$log_file" | sort -nr
```

Qué aporta cada parte:

- `set -euo pipefail` hace visibles varios errores que Bash suele ignorar.
- `[[ ! -r ... ]]` comprueba que el archivo se puede leer.
- `awk` localiza la palabra `from` y cuenta la IP que aparece después.
- `sort -nr` ordena el resultado de mayor a menor.

Pruébalo únicamente con logs ficticios o que tengas autorización para consultar.
Un log real puede contener usuarios, IPs y nombres internos.

## Errores comunes

- Escribir variables sin comillas: usa `"$variable"` salvo que necesites división.
- Copiar el símbolo `$` del prompt dentro del comando.
- Ejecutar todo con `sudo` aunque no sea necesario.
- Descargar y ejecutar scripts sin leerlos.
- Guardar contraseñas o tokens directamente en un archivo `.sh`.

## 7. Conservar las prácticas de red: destinos explícitos

El ejercicio original descubría toda una subred a partir de la IP. Eso puede fallar
si hay varias interfaces o si la red no usa `/24`. Para empezar, indica directamente
los equipos del laboratorio que quieres consultar. Guarda `network_hosts.sh`:

```bash
#!/usr/bin/env bash

if (( $# == 0 )); then
    set -- 127.0.0.1
fi

for target in "$@"; do
    if ping -n -c 1 -W 1 -- "$target" >/dev/null 2>&1; then
        printf 'Responde: %s\n' "$target"
    else
        printf 'Sin respuesta: %s (puede bloquear ICMP)\n' "$target"
    fi
done
```

`./network_hosts.sh` prueba tu propio equipo. Para practicar con tus VMs, pasa sus
IPs como argumentos. El script recorre únicamente esa lista y no deduce una red.
Las opciones mostradas corresponden a `ping` de Linux.

También puedes probar una conexión TCP local con Bash:

```bash
timeout 1 bash -c 'exec 3<>"/dev/tcp/$1/$2"' bash 127.0.0.1 8000
```

Arranca antes `python3 -m http.server 8000 --bind 127.0.0.1` en otra terminal.
Una conexión exitosa devuelve código `0`; consulta el resultado con `echo "$?"`
justo después. `/dev/tcp` es una función especial de Bash y no un archivo normal.

## Siguientes pasos

1. Validar que el argumento termine en `.log`.
2. Añadir una opción para mostrar sólo IPs con cinco o más fallos.
3. Crear pruebas con [Bats](https://github.com/bats-core/bats-core).
4. Revisar scripts con `shellcheck` antes de publicarlos.

## Uso responsable

Los ejemplos trabajan con el equipo local. No escanees ni consultes sistemas que no
sean tuyos o para los que no tengas autorización explícita.
