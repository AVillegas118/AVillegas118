# Introducción a Nmap en un laboratorio

Nmap ayuda a descubrir equipos, puertos y servicios de una red. Esa información es
útil para inventarios y revisiones defensivas, pero también puede ser sensible.

> Ejecuta estos comandos únicamente contra `localhost`, máquinas virtuales propias
> o sistemas para los que tengas autorización explícita. No escanees Internet ni
> redes ajenas como práctica.

## Conceptos básicos

- **Host:** equipo conectado a una red.
- **Puerto:** número que identifica un servicio de red.
- **Servicio:** programa que escucha conexiones, como SSH o un servidor web.
- **TCP:** protocolo usado por muchos servicios para establecer conexiones.
- **Estado abierto:** un programa aceptó la conexión en ese puerto.
- **Estado cerrado:** el equipo respondió, pero no hay un servicio escuchando.
- **Filtrado:** un firewall u otro control impidió determinar el estado.

Un puerto abierto no es automáticamente una vulnerabilidad. Primero hay que saber
qué servicio lo usa, si es necesario y cómo está protegido.

## Preparar un laboratorio seguro

En Debian puedes instalarlo con `sudo apt install nmap` y consultar la versión con
`nmap --version`.

La opción más sencilla es analizar el propio equipo:

```bash
nmap -sT -p 22,80,443 127.0.0.1
```

- `-sT` realiza una conexión TCP normal.
- `-p` limita la prueba a tres puertos.
- `127.0.0.1` siempre representa el equipo local.

Para abrir temporalmente un servidor de práctica en el puerto `8000`:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

En otra terminal:

```bash
nmap -sT -p 7999-8001 127.0.0.1
```

Deberías observar `8000/tcp open`. Detén el servidor con `Ctrl+C` al terminar.

## Identificar servicios

En una máquina virtual propia puedes solicitar una identificación básica:

```bash
nmap -sV -p 22,80 IP_DE_TU_VM
```

Reemplaza `IP_DE_TU_VM` por la IP de tu máquina virtual. `-sV` envía solicitudes
adicionales para estimar el servicio y su versión. No
garantiza que la identificación sea exacta y genera más tráfico que una conexión
sencilla.

## Descubrimiento en una red aislada

Primero consulta la red de la máquina virtual:

```bash
ip -brief address
ip route
```

Si tu laboratorio usa, por ejemplo, `192.168.56.0/24`, puedes buscar equipos activos:

```bash
nmap -sn 192.168.56.0/24
```

`-sn` realiza descubrimiento de hosts sin un escaneo de puertos. Sustituye la red
del ejemplo sólo por el segmento aislado que realmente te pertenece.

## Guardar resultados

```bash
nmap -sT -p 22,80,443 127.0.0.1 -oN resultado-local.txt
```

`-oN` crea un archivo de texto. Revísalo antes de publicarlo: un resultado real
puede revelar IPs, nombres de equipos, servicios y versiones internas.

## Ampliación: reconocer una VM y revisar su servicio TLS

El apunte original usaba una VM Kioptrix. Puedes conservar esa práctica en una red
virtual aislada y con una instantánea. Confirma la IP desde la consola de la VM;
un resultado de descubrimiento por sí solo no demuestra qué máquina es.

Sustituye `IP_DE_TU_VM` en los ejemplos por la dirección de esa VM:

```bash
sudo nmap -v -A -p 22,80,443 IP_DE_TU_VM
```

`-v` muestra más detalle. `-A` combina detección de sistema operativo, versiones,
scripts predeterminados y trazado de ruta. No significa «todos los puertos» ni
«encontrar todas las vulnerabilidades». Genera más comprobaciones que el ejemplo
básico; sus funciones de sistema operativo y ruta necesitan privilegios.
Referencia: [opciones adicionales de Nmap](https://nmap.org/book/man-misc-options.html).

Si la VM tiene un servicio TLS en `443`, conserva estas dos comprobaciones
históricas del apunte:

```bash
nmap -sV --script ssl-poodle -p 443 IP_DE_TU_VM
nmap -sV --script ssl-ccs-injection -p 443 IP_DE_TU_VM -oN resultado-tls.txt
```

- [`ssl-poodle`](https://nmap.org/nsedoc/scripts/ssl-poodle.html) comprueba si se
  aceptan ciertos cifrados CBC de SSLv3, asociados a CVE-2014-3566.
- [`ssl-ccs-injection`](https://nmap.org/nsedoc/scripts/ssl-ccs-injection.html)
  comprueba una respuesta del protocolo relacionada con CVE-2014-0224.

Son comprobaciones concretas, no una auditoría TLS completa. Guarda el comando,
la versión de Nmap y la salida; explica qué detecta cada script. Que no aparezca
una alerta no prueba que todo sea seguro: puede no existir un servicio TLS, no
responder o requerir otra prueba. No esperes que toda VM antigua tenga ambos fallos.

## Siguientes pasos

1. Comparar el resultado con los servicios que esperabas tener activos.
2. Cerrar el servidor de práctica y comprobar que el puerto cambia a `closed`.
3. Documentar un falso positivo o una identificación incorrecta.
4. Crear un inventario sólo de tus máquinas virtuales.

## Referencia para seguir aprendiendo

Consulta la [guía oficial de Nmap](https://nmap.org/book/man.html) para los estados
de puertos, las técnicas de escaneo y los formatos de salida.
