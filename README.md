# BASE DE DATOS 2 
## Proyecto 3

## Integrantes ✒️

- Juan Pablo Lozada [IWeseI] Participación: 100%
- Alexandra Shulca [Alexandra-SR] Participación: 100%
- Alex Loja Zumaeta [aljozu] Participación: 100%

## Profesor 🦾

- Heider Sanchez Enriquez


## Introducción :dart:

**_Objetivo:_**  Entender y aplicar los algoritmos de búsqueda y recuperación de la información basado en el contenido.   
 
Este proyecto está enfocado al uso una estructura multidimensional para dar soporte a las búsqueda y 
recuperación eficiente de imágenes en un servicio web de reconocimiento facial. 

**_Descripción del dominio:_** Se  usará  una  colección con  más  de  13  mil  imágenes  de  [rostros  de  personas](http://vis-www.cs.umass.edu/lfw/). Algunas  personas  tienen  más  de  una  imagen  asociada, se consideran todas.  


- **Ejemplo**:



**_Resultados esperados:_** 
Probar  el  desempeño  del  índice  invertido,  mediante una plataforma web (frontend y backend)  que permita interactuar con las principales operaciones del índice invertido:  
- Carga e indexación de documentos en tiempo real. 
- Búsqueda textual relacionado a ciertos temas de interés. 
- Presentación de resultados de búsqueda de forma amigable e intuitiva.  

## Comenzando 🚀

### Pre-requisitos 📋
* [Python](https://www.python.org/downloads/) 
#### Librerías
* [Face Recognition](https://github.com/ageitgey/face_recognition)
* [R Tree](https://rtree.readthedocs.io/en/latest/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)


### Despliegue 📦

**1.** Clonar el repositorio del proyecto.

**2.** Realizar el Build del proyecto en su IDE de preferencia.

**3.** Ejecutar el programa


## Descripción de las técnicas 

Implementación de una plataforma web  para  la  identificación  automática  de  personas  a  partir  de  una colección grande de imágenes de rostros. 
El procedimiento general consiste en lo siguiente: 

- **Extracción de características**

Para la extracción de características se usará la librería Face_Recognition. En dicha librería ya se encuentra implementado las técnicas necesarias para obtener de cada imagen una representación  compacta  del  rostro  (enconding).  El  tamaño  del  vector característico es de 128 . La efectividad del reconocimiento ha sido probada 
con modelos de búsqueda basados en deep learning (99.38% de precisión).

Se usa face embedding en el que cada cara es convertida en un vector, esta técnica es llamada deep metric learning.
Primero se detecta la cara en la imagen, una vez que se sabe la ubicación exacta de la cara, usaremos esa parte de la imagen para extraer los features (características).  Para lo cual, se usa face embeddings.  Una red neuronal toma una imagen como input y da como output un vector que representa las características del rostro.
En el caso de la librería face_recognition, se usa la función face_encodings, la cual dada una imagen, retorna un face encoding de 128 dimensiones para cada cara en la imagen. 

```

def face_encodings(face_image, known_face_locations=None, num_jitters=1, model="small"):
    """
    Given an image, return the 128-dimension face encoding for each face in the image.

    :param face_image: The image that contains one or more faces
    :param known_face_locations: Optional - the bounding boxes of each face if you already know them.
    :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
    :param model: Optional - which model to use. "large" or "small" (default) which only returns 5 points but is faster.
    :return: A list of 128-dimensional face encodings (one for each face in the image)
    """
```



- **Indexación de vectores característicos para búsquedas eficientes**
- **Algoritmo de búsqueda**

- **Construcción del Índice**
  - Estructurar el índice invertido para guardar los pesos TF-IDF.  
  - Calcular  una  sola  vez  la  longitud  de  cada  documento  (norma)  y  guardarlo  para  ser 
  utilizado al momento de aplicar la similitud de coseno. 
  - Construcción del índice en memoria secundaria para grandes colecciones de datos.   
- **Consulta** 
  - La consulta es una frase en lenguaje natural.  
  - El scoring se obtiene aplicando la similitud de coseno sobre el índice invertido en 
  memoria secundaria. 
  - La función de recuperación debe retornar una lista ordenada de documentos que se 
  aproximen a la consulta. 


###  ÍNDICE INVERTIDO  💯

**_Índice Invertido_**: En este método organizamos los registros de acuerdo a un valor de sus campos, para este caso usaremos el campo **Id** como key.

- **Construcción del índice invertido:**

  1.  Recorremos los archivos con la data y los leemos como diccionarios.
  2.  Para cada tweet sacamos las palabras y las llevamos a su forma raíz, pero antes se eliminan los signos de puntuación y emojis. Después, devolvemos una lista que contiene a cada palabra con el número de veces que aparece(tf-term frequency).
  3.  Posteriormente, calculamos el score tfidf para cada palabra, 
  4.  Finalmente escribimos un índice invertido en memoria secundaria cada 5 documentos. 
  ```
  def json_tweets_to_dic():
    tf = []
    for filename in archivos:
        lista = []
        if filename.endswith(".json") :
            with open(input_directory + '\\' + filename, 'r', encoding='utf-8') as all_tweets:
                all_tweets_dictionary = json.load(all_tweets)
                for tweet in all_tweets_dictionary:
                    temp = readFile(all_tweets_dictionary[tweet])
                    lista.append(temp)
                tf.append(merge(lista))
    tfidf(tf)
    ```
- **Manejo de memoria secundaria**
  1. Para leer los archivos con tweets, necesitamos leer todos los documentos que los contengan.
  2. Al haber gran cantidad de información necesitamos almacenar esta en distintos bloques por lo que escribimos un índice invertido para 5 documentos como máximo.
  3. Al momento de buscar, necesitamos leer la infomración que tenemos en los índices por lo que toca ir añadiendolos a memoria principal.
  ```
  def tfidf(tf):
    lista = {}
    it = 0
    for i in tf:
        for k in i:
            wtfidf = math.log(1 + i[k]) * math.log(len(tf)/df(k, tf))
            if k in lista:
                lista[k] = str(lista[k]) + ";" + str(archivos[it]) + "," + str(wtfidf)             
            else:
                lista[k] = str(archivos[it]) + "," + str(wtfidf)
        it += 1            
        if(it % 5 == 0):
            writeblock(lista, it/5)
            lista = {}
    
    writeblock(lista, math.ceil(it/5))

  def writeblock(lista, c):
    nombre = "index" + str(int(c)) + ".txt"
    with open(nombre, 'a', encoding='utf-8') as data:
        for k in lista:
            data.write(k + ':'+ lista[k] + '\n')
    ```
  
- **Consultas**
  1. Para realizar una consulta lo primero que hacemos es tokenizar la query.
  2. Calculamos los scores para cada palabra.
  3. Después de procesar la query, vamos sacando la similitud de coseno entre esta y la información que vamos leyendo de los índices invertidos guardados en memoria secundaria.
  4. Ordenamos los resultados de acuerdo al score obtenido por cada documento.
  5. Devolvemos los k resultados más relevantes a la consulta.
  ```
  def search(query, k):
    tf = readFile(query)
    dic = {}
    inverted = readInverted()
    scores = {}
    lenght1 = {}
    for i in archivos:
        scores[i] = 0
        lenght1[i] = 0
    lenght2 = 0
    for i in tf:
        wtfidf = math.log(1 + tf[i]) * math.log(len(archivos)/df_ind(i, inverted))
        dic[i] = wtfidf
        lenght2 = lenght2 + wtfidf**2
        values = inverted[i].split(';')
        for j in values:
            j = j.split(',')
            lenght1[j[0]] = lenght1[j[0]] + float(j[1])**2
            scores[j[0]] = scores[j[0]] + float(j[1])*wtfidf
    lenght2 = lenght2**0.5
    for i in lenght1:
        if lenght1[i] != 0:
            lenght1[i] = lenght1[i]**0.5
    for i in scores:
        if lenght1[i] != 0:
            scores[i] = scores[i]/(lenght1[i]*lenght2)
    orderedDic = sorted(scores.items(), key=lambda it: it[1], reverse=True)
    return orderedDic[:k]
    ```

###  Vistas de plataforma web 
**Buscador**
<figure class="image" align="center">
  <img src="images/buscador .png" width="70%" height="60%" style="text-align:center;">
</figure>

**Resultados**
<figure class="image" align="center">
  <img src="images/resultados.png" width="70%" height="60%" style="text-align:center;">
</figure>

## Anaálisis de resultados 🚀
**Tabla de resultados*
<figure class="image" align="center">
  <img src="images/tabla.png" width="70%" height="60%" style="text-align:center;">
</figure>

**Gráfico de resultados**
<figure class="image" align="center">
  <img src="images/grafico.png" width="70%" height="60%" style="text-align:center;">
</figure>



## Licencia 📄
Universidad de Ingenieria y Tecnología - UTEC
  
