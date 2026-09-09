# Cómo usar estos apuntes

Este repositorio reúne prácticas de aprendizaje. Cada página explica un tema,
presenta ejemplos y propone ejercicios pequeños para seguir avanzando.

## Orden sugerido

Si redes es un tema nuevo para ti, empieza por [Redes desde cero](REDES-DESDE-CERO.md)
y [Puertos y seguridad básica](PUERTOS-Y-SEGURIDAD.md). Después puedes seguir
las [lecturas y ejercicios de repaso](LECTURAS-DE-SEGURIDAD.md).

1. Bash o PowerShell: aprende comandos, variables, condiciones y bucles.
2. Encoding: distingue codificación, cifrado y hashes.
3. APIs y web scraping: obtiene datos y maneja respuestas y errores.
4. Puertos y Nmap: interpreta conexiones y resultados en un laboratorio.
5. FTP y correo: entiende transferencias, mensajes y sus riesgos.
6. Automatización: programa tareas que ya comprobaste manualmente.

## Cómo estudiar cada práctica

Lee el objetivo, prepara el entorno indicado y ejecuta un ejemplo pequeño. Cambia
un dato y observa qué sucede. Anota qué aprendiste, qué error encontraste y cómo lo
resolviste. Esas observaciones son buenas aportaciones para tus siguientes commits.

Los comandos que instalan servicios, cambian permisos o programan tareas se realizan
en tu VM de práctica. Los ejemplos de Python necesitan Python 3.11 o posterior.

## Pruebas del repositorio

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install requests beautifulsoup4 cryptography
python -m unittest discover -s tests -v
```

En Windows usa `.venv\Scripts\Activate.ps1` para activar el entorno.
Las pruebas de Python usan datos ficticios y respuestas simuladas. Los servicios
FTP, las tareas de Windows y los escaneos Nmap deben probarse en una VM con esas
herramientas; pasar las pruebas de Python no verifica esos servicios.

## Tus prácticas originales

Las versiones anteriores, con sus capturas, siguen disponibles en
[el historial conservado](https://github.com/AVillegas118/AVillegas118/tree/55e8b876bf56a7b32867dcc3c15dfa89e807564d).
Los nombres de los diez apuntes se conservaron para que sus enlaces sigan funcionando.

Esta revisión corrige, entre otros, el intérprete mal escrito de Bash, opciones
incorrectas de vsftpd, argumentos de PowerShell, sockets sin cerrar y ejemplos de
correo y HTTP sin manejo adecuado de errores. También conserva cifrado Fernet y
las prácticas de red, explicando su alcance y limitaciones.

## Autoría y aprendizaje

La revisión y las primeras versiones de los proyectos se prepararon con ayuda de
IA. Son una base para estudiar, probar y modificar. Describe en el CV las partes
que comprendes y tus mejoras; no presentes los laboratorios como experiencia laboral
ni como herramientas utilizadas en producción.
