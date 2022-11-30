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
Al ejecutarse se veria algo así

![image](https://user-images.githubusercontent.com/111693854/204680499-48e5842a-647b-44fd-83c5-df65291cf5dc.png)

___

#### PYTHON FAKE JOBS
___
4.  En los siguientes pasos iremos construyendo un script de webscraping usando el sitio Python Fake Jobs (https://realpython.github.io/fake-jobs/) :

![image](https://user-images.githubusercontent.com/111693854/204680718-63cd2d11-f894-4fd1-8c19-bd40e345c4e3.png)

___
5. Igual que en el caso anterior es recomendable inspeccionar la estructura del sitio, analizar los metadatos y cómo podemos obtener la información de ellos: 

![image](https://user-images.githubusercontent.com/111693854/204680842-8f8e5b47-0834-4b7f-9449-2e225958d758.png)

___
6. Comenzamos con lo más sencillo, conectarse y traer la información de la URL (scrap1.py):
~~~
# Importarlos modulos
import requests# Obtener la informacion HTML de la URL
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
# Imprimir el texto de la peticion GET
print(page.text)
~~~
Al ejecutarse se veria algo así

![image](https://user-images.githubusercontent.com/111693854/204681071-76b73f25-2983-407d-b6db-80ef02071e37.png)

___
7. Ahora utilizando BeautifulSoup se analizará el contenido y se comenzará a formatear la información recibida (scrap2.py):
~~~
# Importacion de modulogs
from unittest import result
import requests
from bs4 import BeautifulSoup
# Obtencion de los datos mediante peticion GET
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
# Analizamos el contenido HTML con BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
# Formateamos la salida del objeto results de BeautifulSoup
print(results.prettify())
~~~
Al ejecutarse se veria algo así 

![image](https://user-images.githubusercontent.com/111693854/204681235-c9bf4f66-5961-4092-9188-e1ddde0c94cd.png)

___
8. Ahora comenzamos a buscar información en base a metadatos, por ejemplo, buscamos elementos de class “card-content” (scrap3.py):
~~~
# Importacion de modulos
import requests
from bs4 import BeautifulSoup
# Obtencion de los datos mediante peticion GET 
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
# Analizamos el contenido HTML con BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
# Buscar todos los elementos que el class "card-content"
job_elements = results.find_all("div", class_="card-content")
# Por cada elemento encontrado job_elements imprimimos.
for job_element in job_elements:
    print(job_element,end="\n"*2)
~~~
Y el resultado es algo como esto: 

![image](https://user-images.githubusercontent.com/111693854/204681404-49a54d3a-c227-4518-8f06-abbb7e1f825f.png)

___
9. Nos sigue apareciendo mucho código HTML extra, por lo que ahora buscaremos títulos con información más precisa (scrap4.py):
~~~
# Importacion de modulos 
import requests
from bs4 import BeautifulSoup
# Obtencion de los datos mediante peticion GET
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
# Analizamos el contenido HTML con BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
# Buscar todos los elementos que el class "card-content"
job_elements = results.find_all("div",class_="card-content")
# En el objeto job_elemento buscamos solo aquellos elementos con
# titulo e informacion relevante.
for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element)
    print(company_element)
    print(location_element)
    print()
~~~
La ejecución del script regresa resultados como estos:

![image](https://user-images.githubusercontent.com/111693854/204681649-a8bdd422-c272-476e-a3c4-3d46b3f0c12e.png)

___
10. Sin embargo, seguimos viendo código HTML, si lo queremos la información procederemos solo mostrando el texto del elemento a imprimir del objeto (scrap5.py): 
~~~
import requests
from bs4 import BeautifulSoup
# Importacion de modulos 
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
# Obtencion de los datos mediante peticion GET 
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
# Analizamos el contenido HTML con BeautifulSoup
job_elements = results.find_all("div", class_="card-content")
#En el objeto job_elemento buscamos solo aquellos elementos con
# titulo e informacion relevante.
for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    # Se imprime solo el texto.
    print(title_element.text)
    print(company_element.text)
    print(location_element.text)
    print()
~~~
La salida ahora solo muestra el texto que realmente nos interesa: 

![image](https://user-images.githubusercontent.com/111693854/204682810-9c59de89-0ac4-4b8f-ad43-d2d9c9d50421.png)

___
11. Sin embargo, el resultado del script anterior parece arrojar espacios en blanco extra, los podemos limpiar haciendo un ajuste en esta sección (scrap6.py):
~~~
import requests
from bs4 import BeautifulSoup
# Importacion de modulos 
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
# Obtencion de los datos mediante peticion GET 
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
# Analizamos el contenido HTML con BeautifulSoup
job_elements = results.find_all("div", class_="card-content")
#En el objeto job_elemento buscamos solo aquellos elementos con
# titulo e informacion relevante.
for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    # Se imprime solo el texto.
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
~~~
La salida es más limpia 

![image](https://user-images.githubusercontent.com/111693854/204683136-f01825f9-bb0f-42bd-8406-8a3ccfedbb7a.png)

___
12. Sin embargo, si el interés en particular es buscar empleos que esta relacionados a desarrollo de Python, entonces la forma de la búsqueda cambia (scrap7.py):
~~~
# Importacion de modulos
import requests
from bs4 import BeautifulSoup
# Obtencion de los datos mediante peticion GET
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
# Analizamos el contenido HTML con BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
# Buscar todos los elementos que el class "card-content"
job_elements = results.find_all("div", class_="card-content")
# Buscr todoslos elementos que el h2 contenga en su texto
# la palabra "python"
python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
)
# Mostramos la cantidad de elementos que cumplen la busqueda.
print(len(python_jobs))
~~~
Y su ejecución solo retorna un valor numérico, la cantidad de trabajos que tienen que ver con “Python”:

![image](https://user-images.githubusercontent.com/111693854/204683357-ddfb6c3d-8d7e-42c3-ab46-9737ecd8c1f1.png)

___
13. Si queremos información adicional sobre esos empleos, podrías intentar iterar sobre la
información que previamente estábamos desplegando(scrap8.py): 
~~~
# Importacion de modulos
import requests
from bs4 import BeautifulSoup
# Obtencion de los datos mediante peticion GET
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
# Analizamos el contenido HTML con BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
# Buscar todos los elementos que el class "card-content"
job_elements = results.find_all("div", class_="card-content")
# Buscar todos los elementos que el h2 contenga en su texto
# la palabra "python"
python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
)
# buscamos y mostramos informacion sobre los elementos de 
# python_jobs
for job_element in python_jobs:
    title_element = job_element.find("h2", calss_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
~~~
Sin embargo, el resultado no es el esperado: 

![image](https://user-images.githubusercontent.com/111693854/204683497-c5dd2d0c-3cdd-4926-996a-d1617d896c08.png)

La razón por la que sucede esto es que la búsqueda de “scrap8.py” está haciendo una búsqueda sobre un 3er nivel de divisiones, como se muestra a continuación:

![image](https://user-images.githubusercontent.com/111693854/204683642-3b924028-2392-4b78-8bc2-8af478578109.png)
Para eso tendremos que realizar ajustes para poder encontrar la información que necesitamos (scrap9.py)

 
