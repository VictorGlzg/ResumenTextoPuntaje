import re
import pandas as pd
from nltk.corpus import stopwords
stopwordsES = stopwords.words("spanish")

#TAM
N = 5

# opening the file in read mode
my_file = open("ej1.txt", "r", encoding="utf-8")
# reading the file
data = my_file.read()
my_file.close()

palabras = data.split(" ")

def eliminarStopWords(text):
    text = ' '.join([word for word in text.split() if word not in stopwordsES])
    return text

#Elimina simbolos y quita las stopwords de nltk
palabrasLimpias = re.sub(r'[^\w]', ' ', eliminarStopWords(data))
#Las convierte en minusculas y las divide
todasPalabras = palabrasLimpias.lower().split()
#print(todasPalabras)

def countFreq(arr,f):
   n = len(arr)
   # Marcar todas las visitas en falso
   visited = [False for i in range(n)]

   # Recorrer todos los valores
   # y contar las frecuencias
   for i in range(n):

     # Ignorar el elemento si ya fue visitado
     if (visited[i] == True):
        continue

     count = 1
     for j in range(i + 1, n, 1):
        if (arr[i] == arr[j]):
          visited[j] = True
          count += 1

     f.append((arr[i], count))

frecuencias = []
countFreq(todasPalabras,frecuencias)
dfPalabras = pd.DataFrame(frecuencias, columns=['Palabra','Puntaje'])

parrafos=data.split("\n\n")
#print("Cantidad de parrafos: "+str(len(parrafos)))

#Separar por punto y seguido [. ]
frases = []
for i in range(len(parrafos)):
    parrafo = parrafos[i].split(". ")
    for j in range(len(parrafo)):
        frases.append((parrafo[j],0))
    #print("Cantidad de frases en el parrafo "+str(i+1)+": " + str(len(frases[i])))

dfFrases = pd.DataFrame(frases, columns=['Frase','ValorTotal'])
#print(dfFrases)

def evaluarFrase(frase):
    frase = re.sub(r'[^\w]', ' ', eliminarStopWords(frase)).lower()
    puntaje = 0
    pal = frase.split(" ")
    for i in pal:
        if(i != ''):
            search = dfPalabras.loc[dfPalabras["Palabra"]== i]["Puntaje"].squeeze()
            puntaje+=search
    return puntaje

evaluacion = []
for i in range(len(dfFrases)):
    evaluacion.append(evaluarFrase(dfFrases["Frase"][i]))

dfFrases["ValorTotal"] = evaluacion
dfFrasesMAX = dfFrases.sort_values(by="ValorTotal", ascending=False)
#print(dfFrasesMAX["Frase"])

def getNindex():
    listIndex = []
    if (N <= len(dfFrasesMAX)):
        for i in range(N):
            listIndex.append(dfFrasesMAX.index[i])
    else:
        print("No hay suficientes frases")
    return(listIndex)

N_items = getNindex()

for n in N_items:
    print(dfFrasesMAX["Frase"][n])

#print(dfFrasesMAX)

#pd.set_option('display.max_rows', None)
#print(dfPalabras.sort_values(by="Puntaje", ascending=False))