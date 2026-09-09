# Introducción al consumo de APIs con Python

Una API permite que dos programas intercambien información mediante reglas
conocidas. Este apunte utiliza servicios públicos de práctica y datos ficticios.

## Conceptos básicos

- **Endpoint:** dirección concreta de una operación de la API.
- **GET:** solicita información sin modificarla.
- **POST:** envía información para que el servidor la procese.
- **JSON:** formato de texto común para representar datos.
- **Código de estado:** número que resume el resultado; por ejemplo, `200` indica
  una respuesta correcta y `404` que el recurso no se encontró.
- **Timeout:** límite de espera al conectar o durante una pausa en la recepción;
  no es un límite total para toda la descarga.

## Preparación

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install requests
```

En Windows PowerShell, la activación es `.venv\Scripts\Activate.ps1`.

## 1. Una petición GET

Este ejemplo solicita cinco Pokémon y muestra sus nombres:

```python
import requests


URL = "https://pokeapi.co/api/v2/pokemon"


def main() -> None:
    try:
        response = requests.get(URL, params={"limit": 5}, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as error:
        print(f"No se pudo consultar la API: {error}")
        return

    for pokemon in payload.get("results", []):
        print(pokemon["name"])


if __name__ == "__main__":
    main()
```

Puntos importantes:

- `params` construye los parámetros de la URL correctamente.
- `timeout=10` limita la espera de conexión y las pausas de lectura.
- `raise_for_status()` convierte respuestas HTTP de error en una excepción.
- `get("results", [])` ofrece una lista vacía si falta ese campo.

## 2. Paginación sin recursión

Muchas APIs dividen resultados en páginas:

```python
import requests


URL = "https://pokeapi.co/api/v2/pokemon"


def list_page(offset: int, limit: int = 5) -> bool:
    response = requests.get(
        URL,
        params={"offset": offset, "limit": limit},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    for pokemon in payload.get("results", []):
        print(f"- {pokemon['name']}")
    return bool(payload.get("next"))


def main() -> None:
    offset = 0
    while True:
        try:
            has_next = list_page(offset)
        except (requests.RequestException, ValueError) as error:
            print(f"Error al obtener la página: {error}")
            break

        if not has_next:
            print("No hay más páginas.")
            break
        answer = input("¿Mostrar otra página? [s/N]: ").strip().lower()
        if answer != "s":
            break
        offset += 5


if __name__ == "__main__":
    main()
```

El bucle es más fácil de controlar que llamar repetidamente a la misma función.

## 3. Una petición POST con datos ficticios

`httpbin.org` devuelve los datos de prueba que recibe:

```python
import requests


payload = {
    "nombre": "Persona de ejemplo",
    "curso": "Introducción a APIs",
}

try:
    response = requests.post(
        "https://httpbin.org/post",
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    print(response.json()["json"])
except (requests.RequestException, ValueError, KeyError) as error:
    print(f"La petición falló: {error}")
```

Usar `json=payload` indica el tipo de contenido y serializa el diccionario. No
envíes matrículas, contraseñas, tokens ni información personal a un servicio de
pruebas.

## Seguridad al consumir APIs

- Lee la documentación y las condiciones de uso.
- Usa HTTPS y valida los certificados; `requests` lo hace de forma predeterminada.
- Nunca desactives la validación con `verify=False` para resolver un error.
- Guarda los secretos fuera del código y del repositorio.
- Define timeouts y limita el tamaño/cantidad de respuestas.
- No registres tokens ni respuestas con datos privados.
- Respeta límites de peticiones y maneja códigos `429` sin insistir agresivamente.

## Siguientes pasos

1. Añadir pruebas simulando respuestas, sin depender de Internet.
2. Validar que los campos recibidos tengan el tipo esperado.
3. Leer un token desde una variable de entorno ficticia.
4. Implementar una pausa segura al recibir `429 Too Many Requests`.

## Referencias

El uso de `params`, `json`, excepciones y timeouts se explica en la
[guía oficial de Requests](https://requests.readthedocs.io/en/latest/user/quickstart/).
