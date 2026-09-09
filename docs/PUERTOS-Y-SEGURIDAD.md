# Puertos y seguridad básica

[Anterior: redes desde cero](REDES-DESDE-CERO.md) · [Lecturas y ejercicios](LECTURAS-DE-SEGURIDAD.md)

**Nivel:** principiante. **Lectura orientativa:** 10 minutos.

Objetivo: reconocer puertos frecuentes y distinguir entre un servicio que escucha,
uno accesible desde una red y uno que realmente tiene una vulnerabilidad.

## 1. Qué es un puerto

Un puerto de red es un identificador lógico, no el conector físico del cable.
Una dirección como `127.0.0.1:8000` indica una IP y un puerto. También hace falta
saber el protocolo: TCP y UDP tienen espacios de puertos separados.

Una analogía útil: la IP es la dirección de un edificio y el puerto, una recepción
concreta. Es una simplificación, no una descripción exacta del sistema operativo.
[Lectura: puertos de red](https://www.cloudflare.com/es-es/learning/network-layer/what-is-a-computer-port/).

Los números van de `0` a `65535`; el `0` está reservado. IANA distingue puertos de
sistema (`0–1023`), de usuario (`1024–49151`) y dinámicos/privados (`49152–65535`).
El sistema operativo puede elegir otro intervalo para sus puertos temporales.

## 2. Puertos que conviene reconocer

Son usos habituales, no pruebas de qué programa está detrás:

| Puerto habitual | Servicio | Para qué se utiliza |
| --- | --- | --- |
| 21/TCP | FTP | Control de transferencias; los datos usan otras conexiones. |
| 22/TCP | SSH | Administración remota; también suele transportar SFTP. |
| 23/TCP | Telnet | Terminal remota tradicional sin cifrado. |
| 53/UDP y TCP | DNS | Consultas y otras operaciones DNS tradicionales. |
| 80/TCP | HTTP | Tráfico web sin TLS. |
| 443/TCP | HTTPS | Tráfico web protegido con TLS. |
| 443/UDP | HTTP/3 | Tráfico web mediante QUIC. |
| 445/TCP | SMB | Compartir archivos y otros recursos. |
| 3389/TCP y UDP | RDP | Escritorio remoto. |

Consulta el [registro de IANA](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
para las asignaciones. Un programa puede usar otro puerto; cambiar SSH a un número
distinto no sustituye actualizarlo ni proteger el acceso. DNS cifrado también puede
usar otros transportes y puertos.

## 3. Escuchando, abierto, cerrado y filtrado

**Escuchando (`LISTEN`)** es un estado local de TCP: un proceso espera conexiones.
No demuestra que alguien desde Internet pueda alcanzarlo.

Cuando una herramienta como Nmap observa un destino:

- **Abierto (`open`):** encuentra un servicio que acepta conexiones TCP o tráfico UDP.
- **Cerrado (`closed`):** el destino responde, pero no hay un servicio escuchando allí.
- **Filtrado (`filtered`):** el filtrado impide determinar si está abierto o cerrado.
- **Abierto o filtrado (`open|filtered`):** las respuestas no permiten distinguir
  ambos estados; es frecuente en ciertos escaneos UDP.

Son observaciones desde un lugar y momento concretos, no etiquetas permanentes.
No interpretes silencio como «cerrado». [Referencia: estados de Nmap](https://nmap.org/book/man-port-scanning-basics.html).

## 4. Puerto abierto no significa vulnerabilidad

Un servidor necesita recibir conexiones para prestar un servicio. El riesgo depende
de **qué programa** atiende, su versión, configuración, autenticación, permisos y
quién puede llegar hasta él.

Ejemplo ficticio: el puerto 22 puede corresponder a un SSH actualizado y limitado a
la red de administración, o a un servicio antiguo expuesto a cualquiera. El número
es el mismo; las condiciones son diferentes. Un escaneo de puertos no basta para
concluir que existe una vulnerabilidad ni para certificar seguridad.

Preguntas útiles al revisar un servicio propio:

1. ¿Sé qué aplicación lo necesita y quién la administra?
2. ¿Está actualizada y tiene autenticación apropiada?
3. ¿Debe ser accesible sólo en este equipo, en la LAN o desde otra red?
4. ¿Puede desactivarse si ya no se utiliza?
5. ¿Hay registros que permitan revisar accesos y errores?

## 5. Firewall y NAT no son lo mismo

Un **firewall** permite o bloquea tráfico según reglas. Una regla debería considerar
protocolo, origen, destino, puerto y sentido; «permitir 443» es una descripción
incompleta. Hay firewalls en equipos y en redes. No sustituyen los parches ni la
autenticación. [Lectura: firewall](https://www.cloudflare.com/es-es/learning/security/what-is-a-firewall/).

**NAT** traduce direcciones; **NAPT**, habitual en routers domésticos, también
traduce puertos. Esa traducción no equivale a una política de seguridad. Una
redirección de puertos puede dar acceso a un servicio interior. La ausencia de
NAT en una conexión IPv6 tampoco obliga a dejar pasar todo: siguen siendo
importantes las reglas del firewall. [Referencia: NAT y NAPT, RFC 3022](https://datatracker.ietf.org/doc/html/rfc3022).

No abras puertos del router ni desactives el firewall para seguir esta lectura.
Si una aplicación falla, primero identifica qué comunicación necesita.

## 6. Leer direcciones de escucha

- `127.0.0.1:8000`: loopback IPv4; el servicio escucha localmente.
- `0.0.0.0:8000`: todas las interfaces IPv4 locales.
- `[::1]:8000`: loopback IPv6.
- `[::]:8000`: todas las interfaces IPv6; aceptar además IPv4 depende del sistema
  y de la configuración del socket.

Escuchar en todas las interfaces no demuestra exposición pública: también influyen
rutas, reglas y otros componentes de red. Un proxy o túnel puede publicar un
servicio inicialmente local. [Referencias: direcciones IPv4](https://man7.org/linux/man-pages/man7/ip.7.html)
y [IPv6 en Linux](https://man7.org/linux/man-pages/man7/ipv6.7.html).

## Repaso rápido

¿Qué falta para evaluar un resultado `445/tcp open`? Identificar el servicio real,
su necesidad, versión, configuración y alcance. No basta con memorizar que ese
número suele asociarse a SMB.

Para practicar después: [apunte de Nmap](../Nmap.md) y
[escáner local de puertos](../Esc%C3%A1ner%20de%20Puertos.md).
