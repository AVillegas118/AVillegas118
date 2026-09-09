# Introducción al web scraping con Python

Web scraping significa extraer información de páginas web de manera automática.
Este apunte usa sitios creados para practicar y limita la cantidad de solicitudes.

## Antes de comenzar

Tener acceso a una página no significa que tengamos permiso para recopilarla.
Antes de automatizar un sitio real:

1. Revisa sus términos de uso y `robots.txt`.
2. Evita datos personales, páginas privadas y contenido con derechos restringidos.
3. Envía pocas solicitudes y añade pausas cuando corresponda.
4. Identifica tu programa con un `User-Agent` claro.
5. Detente ante errores en lugar de reintentar sin límite.

Nunca intentes saltar autenticación, CAPTCHA, límites o controles de acceso.

## Preparación

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install requests beautifulsoup4
```

## 1. Extraer citas de un sitio de práctica

Guarda lo siguiente como `scrape_quotes.py`:

```python
import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup


URL = "https://quotes.toscrape.com/"
HEADERS = {"User-Agent": "AVillegas118-learning-project/1.0"}


def fetch_quotes() -> list[tuple[str, str]]:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    rows = []
    for card in soup.select("div.quote"):
        quote = card.select_one("span.text")
        author = card.select_one("small.author")
        if quote is None or author is None:
            raise ValueError("Una tarjeta no tiene cita o autor; revisa el HTML")
        rows.append((quote.get_text(strip=True), author.get_text(strip=True)))
    if not rows:
        raise ValueError("No se encontraron citas; revisa el HTML")
    return rows


def csv_text(value: str) -> str:
    # Reduce el riesgo de que una hoja de cálculo interprete el texto como fórmula.
    if value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r")):
        return "'" + value
    return value


def save_csv(rows: list[tuple[str, str]], path: Path) -> None:
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["cita", "autor"])
        writer.writerows((csv_text(quote), csv_text(author)) for quote, author in rows)


def main() -> None:
    try:
        rows = fetch_quotes()
        save_csv(rows, Path("citas.csv"))
    except (requests.RequestException, ValueError, OSError) as error:
        print(f"No se pudo completar la práctica: {error}")
        return

    print(f"Se guardaron {len(rows)} citas en citas.csv")


if __name__ == "__main__":
    main()
```

### ¿Qué hace cada parte?

- `requests.get` descarga una página con espera de conexión/lectura de diez segundos;
  el tiempo total puede ser mayor.
- `raise_for_status` detiene el flujo si el servidor devuelve un error.
- `BeautifulSoup` convierte HTML en una estructura que se puede consultar.
- `select("span.text")` busca elementos que coinciden con un selector CSS.
- `get_text(strip=True)` extrae texto y elimina espacios exteriores.
- Buscar la cita y su autor dentro de la misma tarjeta evita emparejarlos mal.
- `csv.writer` crea un archivo que puede abrirse en una hoja de cálculo.
- El modo `x` evita reemplazar un CSV anterior: renómbralo antes de repetir.

## 2. Filtrar empleos ficticios

El sitio `https://realpython.github.io/fake-jobs/` contiene datos inventados para
practicar. Este fragmento localiza tarjetas cuyo título contiene “python”:

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


response = requests.get(
    "https://realpython.github.io/fake-jobs/",
    headers={"User-Agent": "AVillegas118-learning-project/1.0"},
    timeout=10,
)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

for card in soup.select("div.card-content"):
    title = card.select_one("h2.title")
    company = card.select_one("h3.company")
    location = card.select_one("p.location")

    if not all((title, company, location)):
        continue
    if "python" not in title.get_text(strip=True).lower():
        continue

    print(title.get_text(strip=True))
    print(company.get_text(strip=True))
    print(location.get_text(strip=True))
    for link in card.select("a[href]"):
        if link.get_text(strip=True).casefold() == "apply":
            print(urljoin(response.url, link["href"]))
    print()
```

Buscar desde cada tarjeta es más resistente que depender de varios `.parent` o de
la posición exacta de un enlace. Aun así, cualquier cambio en el HTML puede romper
el programa; es una limitación normal del scraping.

## Riesgos y limitaciones

- El contenido remoto no es confiable: nunca lo ejecutes como código.
- Una hoja de cálculo puede interpretar celdas que comienzan con `=`, `+`, `-` o
  `@` como fórmulas; si el origen no es confiable, deben neutralizarse antes.
- Una página dinámica puede requerir una API o JavaScript y no aparecer en el HTML.
- Los selectores dejan de funcionar cuando cambia el diseño.
- Recolectar datos personales puede tener consecuencias legales y de privacidad.

## Siguientes pasos

1. Añadir una pausa entre páginas y un máximo de páginas.
2. Escribir pruebas usando HTML local para no consultar Internet.
3. Probar `csv_text` con entradas que comiencen con espacios y `=`.
4. Comparar scraping con el uso de una API oficial.

## Referencias

Consulta los selectores y la extracción de texto en la
[documentación de Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
