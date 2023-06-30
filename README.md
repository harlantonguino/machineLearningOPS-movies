# MLOPS_Movies

![HENRY](https://techsmart.gr/wp-content/uploads/2020/11/greek-subs-movies-700x337.jpg)



### Proyecto Machine Learning Operations
Desarrollar e implementar un modelo de machine learning con el objeto de realizar una recomendacion de peliculas al ususario solicitando como entrada una pelicula de referencia. Se desarrolla una API y disponibiliza los datos en la web del modelo junto con otras 6 funciones de consulta

##### El proyecto se desarrolla en python, framework fastAPI con deploy en Render

### Archivos disponibles:

[>>> link to datasets originales::](https://drive.google.com/drive/folders/1nvSjC2JWUH48o3pb8xlKofi8SNHuNWeu?usp=drive_link)

### datasets
##### dataset credits luego de ETL
- credits_datasetB

##### dataset movies luego de ETL
- movies_datasetB

##### merge datasets movies credits
- dataset

##### dataset final usado para funciones de consulta y modelo
- datasetB
- datasetB.zip (comprimido)

### notebooks
##### ETL
- ETLCredits
- ETLMovies

##### union datasets 
- mergeDatasets

##### limpieza normalizacion texto 
- clean_overview

##### modelo
- machineLearning

##### desarrollo funciones de consulta
- funciones

### scripts
##### script funciones de consulta-modelo API deploy
- main

### ETL

Es realizado un proceso de extraccion, transformacion y carga de los datos. El proceso de normalizacion y limpieza se realiza considerando los features a usar en un futuro tanto por las funciones de consulta desarrolladas como por el modelo de recomendacion. Se elimina algunos features que no agregan valor al proyecto al igual que algunos registros con valores nulos, se imputa algunos valores nulos con criterio del autor, se identifica la posibilidad de completar valores con datos de otras columnas. Finalmente se dispone de un nuevo archivo csv

### EDA

A lo largo del proyecto se identificaron algunos aspectos relevantes respecto a los datos utiles para tomar decisiones como eliminacion imputacion creacion de algunos datos, valores o columnas. Igualmente con la informacion recopilada se determina las estrategias y tecnicas a juicio del autor mas convenietes para obtener un mejor performance tanto del modelo como de las funciones de consulta. 

### Modelo 

Se desarrolla un model ode machine learning con el objeto de devolver una lista con 5 peliculas similares a la pelicula ingresada. Es considerado que algunas peliculas pertenecen a colecciones de peliculas por lo cual se toma como prioridad en estos casos recomendar las peliculas que pertenecen a la misma coleccion. Es realizado un primer filtro usando el feature genero y un segundo filtro usando el feture idioma al considerar relevante que una pelicula a recomendar pertenesca a un mismo genero y tenga un mismo idioma. Para identificar las peliculas similares e susado el feature titulo mas overview, texto que despues de un procesamiento para su limpieza y vectorizacion es usado para buscar similitud con el texto seleccionado de la pelicula ingresada, finalmente la lista de peliculas es armada usando el score obtenido  ordenando de forma descendente.

### API

[>>> link to API:](https://mlops-movies-4683.onrender.com/docs#/docs)

En primera instancia se crea un entrono virtual para el proyecto, se desarrolla la API usando fastAPI y se realiza el deploy en Render

### Consultas disponibles:

**/cantidad_filmaciones_mes/{mes}** retorna la cantidad de peliculas que se estrenaron en ese mes historicamente, ejemplo: enero

**/cantidad_filmaciones_dia/{dia}** retorna la cantidad de peliculas que se estrenaron en ese día historicamente, ejemplo: lunes

**/score_titulo/{titulo}** ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score, ejemplo: toy story
 
**/votos_titulo/{titulo}** ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones, deberá de contar con al menos 2000 valoraciones para mostrar resultados, ejemplo: toy story

**/get_actor/{nombre_actor}**  ingresa el nombre de un actor para devolver el éxito a través del retorno y cantidad de películas que participó y el promedio de retorno, ejemplo: tom hanks
 
**/get_director/{nombre_director}** ingresa el nombre de un director para devolver el éxito del mismo medido a través del retorno, nombre de sus películas, con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, ejemplo: steven spielberg

**/recomendacion/{titulo}** Ingresa un titulo de pelicula y devuelve una lista con la recomendacion de 5 peliculas, ejemplo: toy story

### Autor
Harlan Tonguino
[>>> link to Linkedin:](https://www.linkedin.com/in/harlan-tonguino-37048a174)
