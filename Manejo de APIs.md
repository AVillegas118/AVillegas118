## Manejo de APIs
### Aqui se veran varios ejercicios en el manejo de APIs haciendo uso de los scripts de python 
___
#### Consultando a POKEMON API
1. Se genera un script llamado Pokemon1.py que permite realizar peticiones al api de pokemon en su endpoint pokemon-form:
~~~
import requests
#
if __name__ == '__main__':
    url = 'https://pokeapi.co/api/v2/pokemon-form/'

    response = requests.get(url)
    if response.status_code == 200:
        payload = response.json()
        results = payload.get('results',[])

        if results:
            for pokemon in results:
                name = pokemon['name']
                print(name)
~~~
Al ejecutar el script Pokemon1.py se monstrara algo como lo siguiente 

![EjecucionPokemon1_2013610](https://user-images.githubusercontent.com/111693854/204409535-48339d6c-20f1-4676-b274-389f70360f56.png)

___
2. Tomando como base el script anterior se crea una funcion para traer la lista de distintos pokemon de 20 en 20 hasta que se le confirme que ya no se listen, a este script le llamaremos Pokemon2.py 

~~~
import requests 
#
def get_pokemons (url='https://pokeapi.co/api/v2/pokemon-form/', offset=0):
    args = {'offset':offset} if offset else {}

    response = requests.get(url,params = args)

    if response.status_code == 200:
        payload = response.json()
        results = payload.get('results',[])

        if results:
            for pokemon in results:
                name = pokemon['name']
                print(name)
        next = input ("¿Continuar listando? [Y/N]").lower()
        if next == 'y':
            get_pokemons(offset=offset+20)
if __name__ == '__main__':
    url = 'http://pokeapi.co/api/v2/pokemon-form'
    get_pokemons()
~~~
Al ejecutar el script Pokemon2.py se monstrara algo como lo siguiente 

![EjecucionPokemon2_2013610](https://user-images.githubusercontent.com/111693854/204410252-958473da-0ce5-41ae-9c70-4c502f748c8e.png)

___

## HTTPBIN.ORG
___
#### Posteo.py
1. Vamos a generar un script que genere un peticion post a htttpbin.org , con el siguiente codigo: 

~~~
from ast import If
import requests
import json
#
if __name__ == '__main__':
    url = "https://httpbin.org/post"
    argumentos = {'nombre':'<Nombre>','matricula': '<Matricula>', 'curso':'Programacion para Ciberseguridad'}

    response = requests.post(url, params=argumentos)

    if response.status_code == 200:
        print(response.content)
~~~
**Nota**: En los argumentos se ponen los datos al momento de generar el script.

Al ejecutar el script se monstrara algo como lo siguiente

![EjecucionPosteo_2013610](https://user-images.githubusercontent.com/111693854/204411114-e6f678bc-0366-4d78-8ab5-4668e75606a8.png)
