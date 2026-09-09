# Codificación, cifrado y hashing

Estos conceptos suelen confundirse, pero resuelven problemas diferentes.

| Concepto | Objetivo | Se puede revertir | Necesita secreto |
| --- | --- | --- | --- |
| Codificación | Representar datos en otro formato | Sí | No |
| Cifrado | Proteger confidencialidad | Sí, con la clave | Sí |
| Hash | Crear una huella | No de forma directa | No |

**Base64 es codificación, no cifrado.** Cualquier persona puede decodificarlo, por lo
que nunca debe usarse para proteger contraseñas o secretos.

## 1. Base64 en Python

```python
import base64


text = input("Texto de práctica: ")
encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
decoded = base64.b64decode(encoded, validate=True).decode("utf-8")

print(f"Base64: {encoded}")
print(f"Original: {decoded}")
```

El recorrido es:

```text
texto → bytes UTF-8 → bytes Base64 → texto ASCII
```

Para regresar se realiza el orden inverso. `validate=True` rechaza caracteres que
no pertenecen al formato Base64 esperado.

## 2. Codificar y restaurar un archivo

Este ejemplo es apropiado sólo para archivos pequeños:

```python
import base64
from pathlib import Path


source = Path("ejemplo.bin")
encoded_path = Path("ejemplo.bin.b64")
restored_path = Path("ejemplo-restaurado.bin")

data = source.read_bytes()
encoded_path.write_bytes(base64.b64encode(data))
restored_path.write_bytes(base64.b64decode(encoded_path.read_bytes(), validate=True))
```

Después puedes comparar el original y el restaurado con SHA-256:

```bash
sha256sum ejemplo.bin ejemplo-restaurado.bin
```

Que ambos hashes coincidan indica que el contenido es igual. No demuestra quién
creó el archivo ni lo protege contra modificaciones futuras.

## 3. Base64 en PowerShell

```powershell
$Text = Read-Host "Texto de práctica"
$Encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Text))
$Decoded = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($Encoded))

Write-Output "Base64: $Encoded"
Write-Output "Original: $Decoded"
```

Es importante utilizar la misma codificación (`UTF8` en este caso) en ambos sentidos.

## 4. SHA-256 en Python

```python
import hashlib
from pathlib import Path


path = Path("ejemplo.bin")
digest = hashlib.sha256(path.read_bytes()).hexdigest()
print(digest)
```

Para archivos grandes conviene leer por bloques, como hace el proyecto
`file-integrity-monitor`, en lugar de cargar todo en memoria.

## Seguridad

- No ejecutes automáticamente datos después de decodificarlos.
- Una cadena Base64 puede contener comandos, malware o contenido engañoso.
- No pegues secretos en decodificadores web: estarías compartiéndolos con terceros.
- Para contraseñas se necesitan algoritmos especializados como Argon2, scrypt o
  bcrypt, junto con una sal; SHA-256 directo no es suficiente.
- Para cifrar usa bibliotecas mantenidas y formatos autenticados; no inventes un
  algoritmo propio.

## Siguientes pasos

1. Modificar un byte y comprobar cómo cambia el hash.
2. Procesar Base64 inválido y mostrar un error comprensible.
3. Calcular SHA-256 por bloques de 64 KiB.
4. Cambiar un byte de un mensaje cifrado y comprobar que se rechaza.

## 5. Cifrado autenticado: ejemplo con Fernet

El ejercicio original también utilizaba `cryptography`. Puedes conservar ese
aprendizaje con un mensaje ficticio y una clave que sólo existe durante la ejecución.
Instala `cryptography` en tu entorno virtual con `python -m pip install cryptography`:

```python
from cryptography.fernet import Fernet, InvalidToken


key = Fernet.generate_key()
cipher = Fernet(key)
token = cipher.encrypt("Mensaje de laboratorio".encode("utf-8"))
print("Cifrado:", token.decode("ascii"))

try:
    original = cipher.decrypt(token).decode("utf-8")
    print("Descifrado:", original)
except InvalidToken:
    print("El mensaje fue alterado o la clave no corresponde.")
```

La clave permite recuperar el contenido; la autenticación también detecta cambios
en el mensaje cifrado. Al cerrar el programa se pierde la clave de esta práctica.
En una aplicación real tendrías que protegerla y conservarla por separado. La
biblioteca resuelve la criptografía, pero no administra por ti el almacenamiento
seguro de claves.

## Referencias

- [Base64 de Python](https://docs.python.org/3/library/base64.html): formatos y validación.
- [Fernet de cryptography](https://cryptography.io/en/latest/fernet/): cifrado autenticado y claves.
