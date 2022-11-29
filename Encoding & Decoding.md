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




