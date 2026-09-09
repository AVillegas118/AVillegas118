# Lecturas y ejercicios: seguridad de redes

[Volver al perfil](../README.md)

No necesitas leer todo de una vez. Empieza por las dos guías del repositorio y usa
las referencias para resolver dudas. Son explicaciones propias con enlaces a las
fuentes, no copias de libros ni certificaciones.

## Orden de lectura

1. [Redes desde cero](REDES-DESDE-CERO.md): LAN, IP, subredes, DNS, DHCP, TCP y UDP.
2. [Puertos y seguridad](PUERTOS-Y-SEGURIDAD.md): servicios comunes, estados y exposición.
3. [Conexiones seguras — INCIBE](https://www.incibe.es/ciudadania/tematicas/conexiones):
   consejos en español para proteger conexiones y el router de casa.
4. [Puertos de red — Cloudflare](https://www.cloudflare.com/es-es/learning/network-layer/what-is-a-computer-port/):
   lectura introductoria en español; recuerda que un servicio puede usar otro puerto.
5. [Estados de puertos — Nmap](https://nmap.org/book/man-port-scanning-basics.html):
   referencia en inglés para interpretar resultados sin sacar conclusiones precipitadas.
6. [Registro de servicios — IANA](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml):
   úsalo como consulta, no como una lista para memorizar entera.

Los enlaces fueron revisados el 8 de septiembre de 2026. Las guías externas pueden
cambiar y algunas describen funciones de productos concretos.

## Lista básica de protección de una red doméstica

- Mantén actualizado el router y comprueba que todavía recibe soporte.
- Usa una contraseña de administración única; no la confundas con la del Wi-Fi.
- Prefiere WPA3 si tus dispositivos lo admiten; si no, WPA2 con AES. Evita WEP y
  WPA antiguo, y utiliza una clave Wi-Fi larga y única.
- Revisa si necesitas administración remota, WPS o redirecciones de puertos; no
  dejes funciones activas sin conocer su propósito.
- Considera una red de invitados aislada de tus equipos principales, si el router
  ofrece esa función. Comprueba qué aislamiento proporciona realmente.

Consulta las opciones exactas en el manual del fabricante o con tu proveedor
antes de cambiarlas: podrías desconectar dispositivos. Estas medidas complementan
las actualizaciones y el firewall; no garantizan por sí solas que una red sea segura.
[Orientación de INCIBE](https://www.incibe.es/ciudadania/tematicas/conexiones).

## Ejercicio 1: mirar sin cambiar nada

Opcional: en tu propio equipo, observa qué servicios TCP están escuchando.
Estos comandos no abren puertos ni escanean otros equipos.

En Linux con `ss` instalado:

```bash
ss -lnt
```

`-l` muestra sockets en escucha, `-n` evita traducir números a nombres y `-t`
selecciona TCP. [Manual de ss](https://man7.org/linux/man-pages/man8/ss.8.html).

En PowerShell de Windows, con el módulo NetTCPIP:

```powershell
Get-NetTCPConnection -State Listen |
    Select-Object LocalAddress, LocalPort, OwningProcess
```

Las columnas indican dirección local, puerto y PID del proceso. Los resultados
dependen del equipo y de los permisos de consulta. No borres reglas ni detengas
procesos porque no reconozcas un nombre. [Referencia de Microsoft](https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-nettcpconnection?view=windowsserver2025-ps).

Ambos ejemplos muestran TCP, no todos los servicios UDP. Ver una escucha local
no confirma acceso desde Internet. La consulta de Windows está revisada contra
su documentación, no ejecutada en este entorno Linux.

## Ejercicio 2: razonar con un caso ficticio

Una herramienta muestra `127.0.0.1:8000` y otra `0.0.0.0:8001` en escucha.

1. ¿Cuál está limitada a loopback IPv4?
2. ¿Puedes afirmar que el segundo servicio es accesible desde Internet?
3. ¿Sabes qué programa atiende sólo por ver `8001`?

<details>
<summary>Ver respuestas</summary>

1. La primera, en `127.0.0.1`.
2. No: faltan rutas, reglas de firewall y posibles mecanismos de publicación.
3. No: el número no identifica de forma fiable a la aplicación.

</details>

## Ejercicio 3: escribir una nota de aprendizaje

Completa esto usando ejemplos ficticios, sin publicar tu IP pública, contraseñas,
capturas del router ni información de redes de tu escuela o trabajo:

```text
Concepto que aprendí:
Mi explicación con palabras sencillas:
Ejemplo ficticio:
Qué puedo concluir:
Qué no puedo concluir todavía:
Fuente que consulté:
```

Después sigue el [laboratorio de Nmap](../Nmap.md), sólo en equipos propios o con
autorización. La meta es interpretar lo que observas, no ejecutar más comandos.
