## Webscraping
### Se veran practicas de Webscraping y analisis de metadata con los siguientes escenarios
- **Scrape Quotes**
- **Python Fake Jobs**
___

#### SCRAPE_QUOTES
___
1. El script de este escenario se basará en el sitio: http://quotes.toscrape.com/ el cual está diseñado para webscraping además de que no se incumplen condiciones de uso.

![image](https://user-images.githubusercontent.com/111693854/204680050-1f9a63b3-fe40-4f64-a7f5-d4fb3f3309ca.png)

___
2. Independiente del navegador que usemos para visualizar el sitio, es posible analizar la
estructura del mismo, en este caso se trata de un sitio estático:

![image](https://user-images.githubusercontent.com/111693854/204680178-adcbfc1e-b61f-433a-bbf0-61e09e5940ff.png)

___
3. El script lleva por nombre “scrape_quote.py” y servirá para hace una petición a la URL del sitio, analizar el contenido HTML y generar listas citas y autores para mostrar en pantalla y guardar en un archivo .csv, el script tiene este código: 
~~~
#Importar modulos 
import requests
import csv 
from bs4 import BeautifulSoup
# Direccion de la pagina web
url = "https://quotes.toscrape.com/"
# Ejecutar Get-Request
response = requests.get(url)
# Analizar sintacticamente el archivo HTML de BeautifulSoup del texto fuente
html = BeautifulSoup(response.text,'html.parser')
# Extraer todas las citas y autores del archivo HTML
quotes_html = html.find_all('span', class_="text")
authors_html = html.find_all('small', class_="author")
# Crear una lista de las citas
quotes = list()
for quote in quotes_html:
    quotes.append(quote.text)
# Crear una lista de los autores
authors = list()
for author in authors_html:
    authors.append(author.text)
# Para hacer el test: combinar y mostrar las entradas de ambas listas
for t in zip(quotes, authors):
    print(t)
# Guardar las citas y los autores en un archivo CSV en el directorio actual
# Abrir el archivo con Excel / LibreOffice, etc.
with open('./citas_matricula.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file, dialect='excel')
    csv_writer.writerows(zip(quotes, authors))
~~~
