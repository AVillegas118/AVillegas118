# Redes desde cero

[Volver al perfil](../README.md) · [Siguiente: puertos y seguridad](PUERTOS-Y-SEGURIDAD.md)

**Nivel:** principiante. **Lectura orientativa:** 10 minutos.

Objetivo: entender qué hacen una IP, un router, DNS y un puerto antes de usar
herramientas de seguridad. No necesitas instalar nada para leer esta guía.

## 1. Una red no es lo mismo que Internet

Una red conecta dispositivos para intercambiar información. Tu computadora y una
impresora pueden comunicarse dentro de una red local, o **LAN**, aunque no haya
salida a Internet. Internet conecta muchas redes entre sí.

Un **switch** conecta equipos dentro de una red Ethernet. Un **router** comunica
redes y decide por dónde enviar los paquetes. Un **punto de acceso** conecta
dispositivos por Wi-Fi. La caja que llamamos «router de casa» suele reunir varias
de estas funciones. Un **paquete** es una porción de datos con información para
su transporte. [Lectura: la capa de red](https://www.cloudflare.com/learning/network-layer/what-is-the-network-layer/).

## 2. IP, subred y puerta de enlace

Una **dirección IP** identifica una interfaz de red dentro de su contexto. No es
una identidad permanente de una persona: un equipo puede tener varias IP y su
dirección puede cambiar.

Ejemplo ficticio de una LAN:

- Computadora: `192.168.1.10`.
- Impresora: `192.168.1.20`.
- Puerta de enlace: `192.168.1.1`.
- Subred: `192.168.1.0/24`.

Una **subred** agrupa direcciones. En este ejemplo, `/24` indica que los primeros
24 bits forman el prefijo de red: equivale a la máscara `255.255.255.0`. Este
bloque contiene 256 direcciones; en una LAN IPv4 convencional, `.0` representa
la red y `.255` su difusión, dejando `.1` a `.254` para interfaces.

La **puerta de enlace predeterminada** suele ser el router al que se envía tráfico
sin una ruta más específica. No supongas que toda red usa `/24` o que el router
siempre acaba en `.1`. [Lectura: qué es una subred](https://www.cloudflare.com/es-es/learning/network-layer/what-is-a-subnet/).

### Direcciones privadas y públicas

Estos bloques IPv4 están reservados para redes privadas:

- `10.0.0.0/8`: de `10.0.0.0` a `10.255.255.255`.
- `172.16.0.0/12`: de `172.16.0.0` a `172.31.255.255`.
- `192.168.0.0/16`: de `192.168.0.0` a `192.168.255.255`.

Pueden repetirse en redes distintas y no se enrutan directamente por Internet
público. No toda dirección `172.x.x.x` es privada. Y «no privada» tampoco significa
automáticamente «pública»: existen otros rangos especiales.
[Referencia: RFC 1918, sección 3](https://www.rfc-editor.org/rfc/rfc1918.html#section-3).

IPv6 es otra versión de IP, con direcciones más largas. No se le aplican los
rangos privados ni las máscaras de este ejemplo IPv4.

## 3. DNS y DHCP: nombres y configuración

**DNS** permite consultar información asociada a un nombre. Por ejemplo, los
registros A y AAAA relacionan nombres con direcciones IPv4 e IPv6. Un nombre puede
tener varias direcciones; DNS no garantiza que el sitio sea confiable.
[Lectura: cómo funciona DNS](https://www.cloudflare.com/es-es/learning/dns/what-is-dns/).

**DHCP** puede entregar automáticamente una IP y otros parámetros, como la puerta
de enlace y los servidores DNS. No es lo mismo que DNS: uno ayuda a configurar
la conexión; el otro resuelve nombres. [Referencia: DHCP, RFC 2131](https://www.rfc-editor.org/rfc/rfc2131.html).

## 4. TCP y UDP: dos formas de transportar datos

**TCP** establece una conexión y proporciona un flujo de bytes ordenado con
retransmisiones si faltan datos. Eso no garantiza que una aplicación complete su
trabajo ni cifra su contenido. [Lectura: TCP/IP](https://www.cloudflare.com/es-es/learning/ddos/glossary/tcp-ip/).

**UDP** envía datagramas sin establecer una conexión como TCP. Por sí solo no
garantiza entrega, orden ni retransmisión; una aplicación puede implementar esas
funciones encima. Tampoco cifra por sí solo. No significa «siempre más rápido»
ni «siempre inseguro». [Lectura: UDP](https://www.cloudflare.com/es-es/learning/ddos/glossary/user-datagram-protocol-udp/).

El **puerto** ayuda a dirigir los datos al servicio correcto dentro del equipo.
`53/TCP` y `53/UDP` son puntos de comunicación diferentes aunque compartan número.
La siguiente guía explica estos números con ejemplos.

## 5. Qué ocurre al abrir una web HTTPS

Simplificando una conexión nueva, sin cachés:

1. El navegador obtiene mediante DNS una dirección para el nombre.
2. Se comunica con el servicio web del destino. Un caso habitual usa TCP y el puerto 443.
3. TLS establece protección criptográfica y el navegador verifica el certificado.
4. Se intercambian peticiones y respuestas HTTP dentro de esa conexión protegida.

No toda web usa TCP: HTTP/3 emplea QUIC sobre UDP. **HTTPS protege el transporte,
pero no demuestra que el propietario del sitio sea honesto.** No ignores avisos
de certificados para continuar. [Lectura: HTTPS](https://www.cloudflare.com/es-es/learning/ssl/what-is-https/)
y [referencia HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html).

## Glosario de bolsillo

- **Interfaz:** conexión de un equipo a una red; puede ser física o virtual.
- **Protocolo:** reglas que permiten a los participantes comunicarse.
- **Cliente:** programa que solicita un servicio.
- **Servidor:** programa que ofrece un servicio; un equipo puede cumplir ambos papeles.
- **Servicio:** función disponible para otros programas, como una web o un servidor DNS.
- **TLS:** protocolo que protege comunicaciones mediante criptografía.

## Repaso rápido

1. ¿Puede una LAN funcionar sin Internet?
2. ¿DHCP y DNS hacen lo mismo?
3. ¿TCP significa que los datos están cifrados?

<details>
<summary>Ver respuestas</summary>

1. Sí; los equipos pueden intercambiar datos localmente.
2. No. DHCP entrega configuración; DNS responde consultas sobre nombres.
3. No. La fiabilidad del transporte y el cifrado son propiedades distintas.

</details>

Continúa con [puertos y seguridad básica](PUERTOS-Y-SEGURIDAD.md).
