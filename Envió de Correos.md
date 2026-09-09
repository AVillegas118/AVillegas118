# Crear y enviar correos de laboratorio con Python

Primero construirás un archivo `.eml` y después lo enviarás a un servidor SMTP de
prueba en tu propio equipo. Así podrás ver el mensaje completo y entender el envío.

## Partes principales de un correo

- **From:** remitente declarado.
- **To:** destinatario declarado.
- **Subject:** asunto.
- **Cuerpo:** contenido en texto o HTML.
- **Adjunto:** archivo incluido dentro del mensaje.
- **MIME:** estándar que permite representar diferentes tipos de contenido.

Estos campos pueden ser falsificados. Ver un nombre conocido en `From` no demuestra
quién envió realmente el mensaje.

## Ejemplo seguro y local

Guarda el siguiente código como `create_email.py`:

```python
from email.message import EmailMessage
from pathlib import Path


OUTPUT = Path("correo-ejemplo.eml")


def build_message() -> EmailMessage:
    message = EmailMessage()
    message["From"] = "remitente@example.com"
    message["To"] = "destinatario@example.net"
    message["Subject"] = "Mensaje de laboratorio"
    message.set_content(
        "Este correo es ficticio y fue creado localmente para aprender.\n"
    )
    return message


def main() -> None:
    message = build_message()
    with OUTPUT.open("xb") as handle:
        handle.write(message.as_bytes())
    print(f"Correo guardado localmente en: {OUTPUT}")


if __name__ == "__main__":
    main()
```

Ejecuta:

```bash
python create_email.py
```

El programa no se conecta a Internet. Los dominios `example.com` y `example.net`
están reservados para documentación.
Si el archivo ya existe, el modo `xb` evita reemplazarlo; renómbralo para repetir.

## Añadir un adjunto ficticio

Dentro de `build_message()`, antes de `return message`, puedes añadir este bloque
si ya creaste un archivo ficticio `reporte.txt`:

```python
from pathlib import Path


attachment = Path("reporte.txt")
if attachment.stat().st_size > 1024 * 1024:
    raise ValueError("El adjunto de práctica debe medir como máximo 1 MiB")
data = attachment.read_bytes()

message.add_attachment(
    data,
    maintype="text",
    subtype="plain",
    filename=attachment.name,
)
```

Antes de leer un adjunto conviene comprobar que existe, limitar su tamaño y decidir
si realmente debe incluirse. El nombre debe obtenerse con `Path.name` para no
publicar accidentalmente una ruta completa del equipo.

## Enviar a un servidor SMTP local

Instala el servidor de prueba dentro de un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install aiosmtpd
python -m aiosmtpd -n -l 127.0.0.1:1025
```

La terminal quedará esperando. El manejador predeterminado muestra los correos
recibidos por consola. En otra terminal, en la carpeta de `create_email.py`, ejecuta
este archivo llamado `send_local_email.py`:

```python
import smtplib
from create_email import build_message


def main() -> None:
    message = build_message()
    try:
        with smtplib.SMTP("127.0.0.1", 1025, timeout=10) as server:
            server.send_message(message)
        print("Mensaje recibido por el servidor local; revisa su terminal.")
    except (smtplib.SMTPException, OSError) as error:
        print(f"No se pudo enviar al laboratorio: {error}")


if __name__ == "__main__":
    main()
```

Detén el servidor con `Ctrl+C`. Esta práctica transmite sólo dentro del propio
equipo y no entrega el correo a `example.net`.

Para enviar mediante un proveedor externo necesitarás su configuración actual,
cifrado TLS y autenticación. Un secreto debe obtenerse fuera del código; por
ejemplo, `getpass.getpass()` evita mostrarlo al escribirlo. No utilices el servidor
local sin cifrado como configuración para una cuenta real.

## Relación con la ciberseguridad

Un analista puede guardar un correo como `.eml` y revisar:

- Diferencias entre `From` y `Reply-To`.
- Enlaces HTTP o con direcciones IP literales.
- Adjuntos inesperados.
- Resultados de autenticación como SPF, DKIM y DMARC.

Una señal aislada no demuestra phishing; siempre hace falta contexto.

## Siguientes pasos

1. Añadir una versión HTML junto al texto plano.
2. Leer de nuevo el `.eml` con `email.parser.BytesParser`.
3. Extraer enlaces sin abrirlos.
4. Escribir pruebas para comprobar los encabezados.

## Referencias

La construcción de mensajes sigue los [ejemplos de email de Python](https://docs.python.org/3/library/email.examples.html).
El servidor de práctica usa la [CLI de aiosmtpd](https://aiosmtpd.aio-libs.org/en/latest/cli.html).

## Uso responsable

No automatices envíos masivos ni uses datos de otras personas. Nunca publiques
correos reales: pueden contener direcciones, identificadores, firmas y conversaciones
privadas.
