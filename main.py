# importar librerias
import numpy as np
import pandas as pd
import ast

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# cargar datos
df = pd.read_csv('datasetB.zip', sep=',', encoding='utf-8', decimal='.')

# cambiar tipo de datos
df.id = df.id.astype('object')
df.releaseDate = pd.to_datetime(df['releaseDate'], format='%Y-%m-%d')

# eliminar duplicados
df.drop_duplicates(subset='id', inplace=True)
df.reset_index(drop=True, inplace=True) # reset index

# funcion obtener lista
def GetData(x):
    if pd.isnull(x):
        return np.nan
    else: 
        return ast.literal_eval(x)   
    
# invocar funcion genreList tipo lista
df['genreList'] = df['genreList'].apply(GetData)
df['languageList'] = df['languageList'].apply(GetData)

from fastapi import FastAPI

#http://127.0.0.1:8000
#.\venv\Scripts\activate
#uvicorn main:app --reload

app = FastAPI(title='PI1_MLOPS Harlan Tonguino PT01',
              description='API: 7 endpoints')

@app.get('/')        
def welcome():
    return {'¡Hola!': 'por favor dirigete a /docs'}

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):

    dict_mes={'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
    
    if dict_mes.get(mes.lower(), 0) > 0:
        nmes=dict_mes.get(mes.lower())
        respuesta=(df['releaseDate'].dt.month==nmes).sum().item()
        return {'mes':mes.capitalize(), 'cantidad':respuesta}
    else:
        return {'¡mes no valido!':'ingresa un mes valido, ejemplo: enero'}

@app.get('/cantidad_filmaciones_dia{dia}')
def cantidad_filmaciones_dia(dia:str):

    dict_dia={'lunes':0, 'martes':1, 'miercoles':2, 'jueves':3, 'vierne':4, 'sabado':5, 'domingo':6}

    if dict_dia.get(dia.lower(), -1) >= 0:
        ndia=dict_dia.get(dia.lower())
        respuesta=(df['releaseDate'].dt.dayofweek==ndia).sum().item()
        return {'dia':dia.capitalize(), 'cantidad':respuesta}
    else:
        return {'¡dia no valido!':'ingresa un dia valido, ejemplo: lunes'}

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):

   if len(df[df['title']==titulo.title()]) > 0:
         
         funcion_3 = df[df['title']==titulo.title()][['releaseYear', 'score']]
         funcion_3.reset_index(drop=True, inplace=True)
         respuesta_1 = funcion_3['releaseYear'][0].item()
         respuesta_2 = funcion_3['score'][0].item()
                 
         return {'titulo':titulo.title(), 'anio':respuesta_1, 'popularidad':respuesta_2}
   else:
         return {'¡titulo no valido!':'ingresa un titulo valido, ejemplo: Toy Story'}

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    
    if len(df[df['title']==titulo.title()]) > 0:
        funcion_4 = df[df['title']==titulo.title()][['releaseYear', 'votes', 'rating']]
        funcion_4.reset_index(drop=True, inplace=True)
        respuesta_1 = funcion_4['releaseYear'][0].item()
        respuesta_2 = funcion_4['votes'][0].item()
        respuesta_3 = funcion_4['rating'][0].item()

        if funcion_4['votes'][0] >= 2000:
            return {'titulo':titulo.title(), 'anio':respuesta_1, 'voto_total':respuesta_2, 'voto_promedio':respuesta_3}
        else:
            return {'mensaje':'No cumple con votacion igual o mayor a 2000 votos'}
    else:
        return {'¡titulo no valido!':'ingresa un titulo valido, ejemplo: Toy Story'}   
    
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):

    funcion_5 = df[df['cast'].str.contains(nombre_actor.title())][['id', 'return']]
    funcion_5.reset_index(drop=True, inplace=True)    
    respuesta_1 = funcion_5['id'].count().item()
    respuesta_2 = round(funcion_5['return'].sum(), 2).item()
    respuesta_3 = round(funcion_5['return'].mean(), 2).item()
    
    return {'actor':nombre_actor.title(), 'cantidad_filmaciones':respuesta_1, 'retorno_total':respuesta_2, 'retorno_promedio':respuesta_3}

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):

    funcion_6 = df[df['director'].str.contains(nombre_director.title())][['id', 'title', 'releaseYear', 'budget', 'revenue', 'return']]
    funcion_6.reset_index(drop=True, inplace=True) 
    respuesta_1 = round(funcion_6['return'].sum(), 2).item()
    respuesta_2 = funcion_6['title'].tolist()
    respuesta_3 = funcion_6['releaseYear'].tolist()
    respuesta_4 = funcion_6['return'].tolist()
    respuesta_5 = funcion_6['budget'].tolist()
    respuesta_6 = funcion_6['revenue'].tolist()

    indice = funcion_6['id'].tolist()
    pelis=[]
    data={}

    for i in indice:
        j=indice.index(i)
        pelis.append({'titulo': respuesta_2[j], 'anio':respuesta_3[j], 'retorno_pelicula':respuesta_4[j], 'budget_pelicula':respuesta_5[j], 'revenue_pelicula':respuesta_6[j]})

    return {'director':nombre_director.title(), 'retorno_total_director':respuesta_1, 'peliculas': pelis}

@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):

    if len(df[df['title'].str.lower()==titulo.lower()]) > 0:

        # indice pelicula input
        movieIndex=df[df['title'].str.lower()==titulo.lower()].index
        movieIndex[0]

        # genero pelicula input
        movieGenre=df['genreList'][movieIndex[0]]

        # lenguaje pelicula input
        movieLanguage=df['languageList'][movieIndex[0]]

        # filtro genero
        if movieGenre == 'No Data':
            pass
        else:
            dfFilter=df[df['genreList'].apply(lambda x: True if set(x)==set(movieGenre) else False)]
            if dfFilter.shape[0] < 6: # si cantidad de peliculas muy pequeña no filtrar 
                dfFilter=df

        # filtro lenguaje
        dfFilter['check'] = dfFilter['language'].apply(lambda x: [True for i in movieLanguage if i in x])

        # crear columna auxiliar check para filtrar el dataset 
        dfFilter = dfFilter[dfFilter['check'].apply(lambda x: False if x==[] else True)]

        #-------
        # tfidfVectorizer
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer() # (ngram_range=(1.2))

        tfidf_matrix = vectorizer.fit_transform(dfFilter['inputML'])
        tfidf_vector = vectorizer.transform([dfFilter['inputML'][movieIndex[0]]])

        # similitud textos
        from sklearn.metrics.pairwise import cosine_similarity

        score = cosine_similarity(tfidf_vector, tfidf_matrix).flatten()

        # indices 
        indices=np.argpartition(score, -6)[-6:]
        
        # ordenar
        dfResultado = dfFilter.iloc[indices][::-1]

        # lista peliculas 
        resultadoList=dfResultado['title'].str.lower().tolist()
        resultadoList.remove(titulo.lower())

        # verificar coleccion
        if dfResultado['collection'][movieIndex[0]] == 'Not in a Collection':
            resultadoFinal=[]
        else: 
            resultadoFinal = df[df['collection']==dfResultado['collection'][movieIndex[0]]]['title'].str.lower().tolist()
            resultadoFinal.remove(titulo.lower())
    
        # agregar peliculas coleccion
        if len(resultadoFinal)!=0:
            for i in resultadoList:
                if i not in resultadoFinal and len(resultadoFinal) < 5:
                    resultadoFinal.append(i)
            respuesta=resultadoFinal
        else:
            respuesta=resultadoList   

        return {'lista recomendada': respuesta}

    else:
        return {'¡titulo no valido!':'ingresa un titulo valido, ejemplo: Toy Story'} 