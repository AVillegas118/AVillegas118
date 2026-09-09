# Escáner de puertos local con Python

Este ejercicio enseña cómo funciona una conexión TCP. Por seguridad, el programa
acepta únicamente direcciones de loopback (`127.0.0.0/8` o `::1`), es decir, el
propio equipo.

Un puerto abierto indica que algún programa aceptó una conexión. No demuestra que
exista una vulnerabilidad.

## Preparar una prueba controlada

Abre un servidor web temporal que sólo escuche en el equipo local:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Déjalo activo mientras pruebas el escáner y detenlo con `Ctrl+C` al terminar.

## Código completo

Guarda este archivo como `local_port_scanner.py`:

```python
import argparse
import ipaddress
import socket


def parse_port(value: str) -> int:
    try:
        port = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("el puerto debe ser un número entero") from error
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("el puerto debe estar entre 1 y 65535")
    return port


def is_open(host: str, port: int, timeout: float = 0.3) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (TimeoutError, ConnectionRefusedError, OSError):
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Comprueba puertos del equipo local")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--start", type=parse_port, required=True)
    parser.add_argument("--end", type=parse_port, required=True)
    args = parser.parse_args()

    try:
        address = ipaddress.ip_address(args.host)
    except ValueError:
        parser.error("--host debe ser una dirección IP válida")
    if not address.is_loopback:
        parser.error("esta práctica sólo permite direcciones loopback")
    if args.start > args.end:
        parser.error("--start no puede ser mayor que --end")
    if args.end - args.start + 1 > 1000:
        parser.error("el rango máximo para esta práctica es de 1000 puertos")

    for port in range(args.start, args.end + 1):
        if is_open(str(address), port):
            print(f"ABIERTO  {address}:{port}")


if __name__ == "__main__":
    main()
```

Ejecútalo alrededor del puerto de prueba:

```bash
python local_port_scanner.py --start 7998 --end 8002
```

Resultado esperado:

```text
ABIERTO  127.0.0.1:8000
```

## Explicación por partes

- `argparse` recibe y valida los argumentos.
- `ipaddress.ip_address` convierte el texto en una dirección válida.
- `is_loopback` impide utilizar el ejemplo contra equipos externos.
- `socket.create_connection` intenta completar una conexión TCP.
- `timeout` evita esperar demasiado por cada intento.
- `with` cierra el socket automáticamente.
- El límite de rango evita crear miles de conexiones por error.

Un puerto que no aparece puede estar cerrado, filtrado o simplemente no haber
respondido antes del timeout. Este programa no intenta identificar servicios ni
enviar cargas adicionales.

## Prueba manual de los controles

Estas ejecuciones deben producir un error comprensible:

```bash
python local_port_scanner.py --host 192.0.2.10 --start 80 --end 80
python local_port_scanner.py --start 9000 --end 8000
python local_port_scanner.py --start 0 --end 80
```

## Limitaciones

- Sólo comprueba TCP, no UDP.
- Sólo funciona contra el equipo local de forma intencional.
- Un timeout no permite distinguir todos los posibles estados.
- No identifica el programa ni la versión detrás del puerto.

## Siguientes pasos seguros

1. Añadir pruebas unitarias para `parse_port`.
2. Mostrar cuánto tardó cada conexión.
3. Comparar el resultado con `ss -lnt` en Linux.
4. Registrar los puertos esperados y avisar si aparece uno nuevo.

## Uso responsable

Un escaneo genera tráfico y puede activar controles de seguridad. Para estudiar
otros equipos utiliza exclusivamente un laboratorio propio o una autorización
explícita que indique alcance y horario.
