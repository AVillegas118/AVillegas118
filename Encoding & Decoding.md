## Encoding & Decoding
### Se veran practicas en las que se emplearan herramientas:
- Python
- Powershell
___

#### PYTHON
___

#### Encode_Text
___
1. Se desarrollara el primer script basico para codificar el texto en Base64,el script lleva por nombre encode_text.py:
~~~
import base64
#
# Obtenemos una frase desde el input principal.
#
print ("Bienvenido a codificadorBase64 en Python")
frase = input("Proporciona una frase para codificar: ")
#
# Obtenemos los bytes de la frase
#
frase_bytes = frase.encode('ascii')
#
# Se calculan los bytes en base64
#
base64_bytes = base64.b64encode(frase_bytes)
#
# Se genera mensaje en base64
#
base64_message = base64_bytes.decode('ascii')
print("La frase codificada en Base 64 en: ")
print(base64_message)
~~~
___

#### Encode_Imgur
___
2. Se visita el sitio de imagenes : https://imgur.com/

3. Usando el link de la imagen obtenido implementar el script que descargara la imagen y la codificara en Base64:
~~~
import requests
import base64
from requests import Response
#
## Para descargar la imagen del sitio
#
if __name__ == '__main__':
    url = 'https://i.pinimg.com/originals/04/56/32/045632827cc644fdb8a7962a5f2fcb81.jpg' # Por alguna razon no se descargaban las imagenes de imgur 

    Response: Response = requests.get(url, stream=True)
    with open('Megaman.jpg','wb') as file_down:
        for chunk in Response.iter_content():
            file_down.write(chunk)
    Response.close()

# Para codificar la imagen

with open('stones.jpg','rb') as binary_file:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf8')

    print (base64_message)
~~~
**Nota**: En este ejemplo se utilizo una imagen de Megaman de ahi el nombre de el archivo creado 
___

#### Decoding_uanl
___
4. El siguiente script (decoding_uanl.py) es para decodificar una imagen que se encuentra en Base64 pasarla a formato png. Para facilitar la implementación del script se proporciona la codificación en el archivo “uanlencode.txt” que se encuentra en los recursos de la plataforma, el script inicia así: 

[decoding_uanl.zip](https://github.com/AVillegas118/AVillegas118/files/10117764/decoding_uanl.zip)
**Nota**: El script es grande por la imagen codificada 

![image](https://user-images.githubusercontent.com/111693854/204660040-b0a7b677-7b6a-4727-aac9-6b235d10650d.png)

y termina asi 
 
![image](https://user-images.githubusercontent.com/111693854/204660275-3f3c3785-4730-48c7-9cda-bdae7b8618df.png)

___

#### Cypher
___
5. El siguiente script de Python utiliza el módulo “cryptography” y lo iremos armando por bloques: 

![image](https://user-images.githubusercontent.com/111693854/204674393-18a2118b-b8ed-43ce-8c31-1e8852251d42.png)

6. Definimos una función genwrite para guardar la llave con que cifraremos:
 
![image](https://user-images.githubusercontent.com/111693854/204674453-c8b209cb-e559-4c15-ab7d-acf254c342ca.png)

7. Llamaremos a la función genwrite para que genere el archivo con la llave:

![image](https://user-images.githubusercontent.com/111693854/204674579-0226aaa6-c99b-4fd4-9145-9a521f48cc71.png)

8. Definimos la función call_key para leer desde el archivo “pass.key” la llave para cifrar:

![image](https://user-images.githubusercontent.com/111693854/204674678-e0049e63-23c5-4461-81f7-9b3df54fdf99.png)

9. Cifraremos un mensaje almacenado en una variable:

![image](https://user-images.githubusercontent.com/111693854/204674719-6bf3e69f-5e84-4ffb-8f1f-576897c210f2.png)

10. Y agregamos el proceso para descifrar el mismo mensaje:

![image](https://user-images.githubusercontent.com/111693854/204674792-1c8677f9-1e04-49bb-901f-62e5007ace13.png)

11. Guardamos el archivo como “cypher.py” y dependiendo de donde lo hayamos guardado lo
podemos ejecutar con “python cypher.py” : 

![image](https://user-images.githubusercontent.com/111693854/204674886-b42a6900-859d-4a64-9e26-2463fc308ff2.png)

___

#### POWERSHELL
___

Code_posh
___
12. Ahora veremos varios ejemplos de codificación/decodificación usando PowerShell, el primer ejemplo es para codificar en Base64 (coder_posh.ps1):
~~~
# Limpiando pantalla
# 
Clear-Host
# Mensaje de bienvenida
Write-Host "Ejemplo de codificador Base64 en Powershell" -ForegroundColor Yellow
Write-Host "Escribe una frase a codificar: "-ForegroundColor Yellow
# Solicitando la entrada de una cabina de texto.
$frase = Read-Host
# Codificando en Base64 y guardando resultado en una cadena.
$encod = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes(($frase)))
# Imprimiendo la salida
Write-Host "La frase escrita en base64 es: " -ForegroundColor Green
Write-Output $encod 
~~~
El resultado al ejecutarlo deberia de verse asi 

![image](https://user-images.githubusercontent.com/111693854/204675088-ca8ce449-c586-4783-95d6-97f0bdc44126.png)

___

#### Decoder_posh
___
13. el siguiente script (decoder_posh.ps1) sirve para decodificar una cadena en Base64. Para facilitar la implementación de este script usaremos “texto_decoder_posh.txt” el cual contiene la cadena de la variable $texto: 

"texto_decoder_posh.txt"
~~~
TABhAGIAbwByAGEAdABvAHIAaQBvACAAZABlACAAUAByAG8AZwByAGEAbQBhAGMAaQDzAG4AIABwAGEAcgBhACAAQwBpAGIAZQByAFMAZQBnAHUAcgBpAGQAYQBkACAAUwBlAHMAaQDzAG4AIAAxADAA
~~~

"decoder_posh.ps1"
~~~
# Limpiando Pantalla 
Clear-Host
# Mensaje de bienvenida 
write-host " Ejemplo de Decodificador Base64 en Powershell"-ForegroundColor Yellow
# Mensaje codificando Base64
$texto = 'TABhAGIAbwByAGEAdABvAHIAaQBvACAAZABlACAAUAByAG8AZwByAGEAbQBhAGMAaQDzAG4AIABwAGEAcgBhACAAQwBpAGIAZQByAFMAZQBnAHUAcgBpAGQAYQBkACAAUwBlAHMAaQDzAG4AIAAxADAA'
Write-Host "La cadena a decodificar es:"
Write-Host $texto
# Decodificamos el mensaje
$decod =[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($texto))
Write-Host "La cadena ya decodificada es:" -ForegroundColor Green
Write-Host $decod
~~~
