# Para el Transmisor:
# 1) Implemente una función de lectura y análisis estadístico del archivo de texto, que reciba un archivo en
# formato .txt, lea uno por uno sus caracteres y devuelva un vector con la probabilidad de aparición de
# cada uno de los caracteres. Debe tener en cuenta letras (mayúsculas y minúsculas), números, caracteres
# especiales y caracteres de control.
# 2) Elabore una función que calcule la entropía del texto ingresado a partir de las probabilidades de
# ocurrencia de cada caracter.
# 3) Con las probabilidades de ocurrencia obtenidas, implemente una función para codificar cada uno de los
# caracteres según el algoritmo de Huffman, devolviendo un vector que relacione cada caracter con su
# palabra de código.
# 4) Calcule la longitud mínima y la longitud promedio del código obtenido. Compare ambos resultados.
# 5) Elabore una función que codifique el texto ingresado en el punto (1), utilizando el código obtenido en el
# punto (3). La función debe devolver un vector con la palabra binaria correspondiente a cada caracter
# del texto.


# Implementación

import numpy as np

# 1) Implemente una función de lectura y análisis estadístico del archivo de texto, que reciba un archivo en
# formato .txt, lea uno por uno sus caracteres y devuelva un vector con la probabilidad de aparición de
# cada uno de los caracteres. Debe tener en cuenta letras (mayúsculas y minúsculas), números, caracteres
# especiales y caracteres de control.





def obtener_vector_probabilidades(archivo):
  texto = open(archivo, 'r')
  caracteres = texto.read()
  texto.close()

  lista_caracter = []
  lista_apariciones = []

  caracteres = np.array(list(caracteres))
  lista_caracter, lista_apariciones = np.unique(caracteres, return_counts=True)
  tot = np.sum(lista_apariciones)

  vector_probabilidades = []  # (caracter, proba)
  vector_probabilidades = np.column_stack((lista_caracter, lista_apariciones / tot)) # aca es mejor si no redondeamos todavia, nos sirve para calcular entropia y huffman, despues para mostrar resultados si
  
  suma = np.sum(vector_probabilidades[:,1].astype(float))

  if np.isclose(suma, 1):
    #print("La suma de probabilidades es 1")
    return vector_probabilidades

  else:
    print("Error: La suma de probabiliadades no da 1")
    return -1

  return vector_probabilidades



# 2) Elabore una función que calcule la entropía del texto ingresado a partir de las probabilidades de
# ocurrencia de cada caracter.


def Calcular_entropia(probabilidades):
  H = np.sum(probabilidades * np.log2(1 / probabilidades))
  return round(H,4)



# 3) Con las probabilidades de ocurrencia obtenidas, implemente una función para codificar cada uno de los
# caracteres según el algoritmo de Huffman, devolviendo un vector que relacione cada caracter con su
# palabra de código.

# funcion auxiliar que sirve para recorrer el arbol y asignar los codigos
def asignar_codigos_huffman(nodo, prefijo="", diccionario=None):
    if diccionario is None:
       diccionario = {}

    # si el nodo es una tupla, entonces es un caracter
    if not isinstance(nodo, tuple):
        if prefijo == "":
            diccionario[nodo] = "0"
        else:
            diccionario[nodo] = prefijo
    else:
        izquierda, derecha = nodo
        asignar_codigos_huffman(izquierda, prefijo + "0", diccionario)
        asignar_codigos_huffman(derecha, prefijo + "1", diccionario)

    return diccionario


# funcion principal para que podamos armar el codigo de huffman
def codigo_huffman(vector_probabilidades):
    nodos = []

    # armamos la lista de nodos con provavilidad y simbolo
    for fila in vector_probabilidades:
        caracter = fila[0]
        probabilidad = float(fila[1])
        nodos.append([probabilidad, caracter])

    # si hay un solo simbolo distinto, le damos codigo 0
    if len(nodos) == 1:
        return {nodos[0][1]: "0"}

    # armamos el arbol de huffman
    while len(nodos) > 1:
        # ordenamos por probabilidad de menor a mayor
        nodos = sorted(nodos, key=lambda x: x[0])

        # agarramos los dos nodos mas chicos
        nodo_izq = nodos.pop(0)
        nodo_der = nodos.pop(0)

        # los juntamos en un nodo nuevo
        nuevo_nodo = [nodo_izq[0] + nodo_der[0], (nodo_izq[1], nodo_der[1])]

        # lo metemos de nuevo en la lista
        nodos.append(nuevo_nodo)

    # al final el arbol completo queda aca
    arbol = nodos[0][1]

    #recorremos el arbol para sacar los codigos
    diccionario = asignar_codigos_huffman(arbol)

    return diccionario

# esta funcion es para devolver un vector con caracter y su codigo
def vector_codigo_huffman(vector_probabilidades):
    diccionario = codigo_huffman(vector_probabilidades)

    caracteres = []
    codigos = []

    #mantenemos el orden original del vector
    for fila in vector_probabilidades:
        caracter = fila[0]
        caracteres.append(caracter)
        codigos.append(diccionario[caracter])

    vector_codigos = np.column_stack((caracteres, codigos))
    return vector_codigos, diccionario




def longitudes_codigo(vector_probabilidades, diccionario_huffman):
    probabilidades = vector_probabilidades[:, 1].astype(float)

    longitudes = []
    for fila in vector_probabilidades:
        caracter = fila[0]
        longitud = len(diccionario_huffman[caracter])
        longitudes.append(longitud)

    longitudes = np.array(longitudes)

    longitud_minima = np.min(longitudes)
    longitud_promedio = np.sum(probabilidades * longitudes)

    return longitud_minima, round(longitud_promedio, 4)



def codificar_texto_huffman(archivo, diccionario_huffman):
    texto = open(archivo, 'r').read()

    vector_codificado = []

    # reemplazamos cada caracter por su palabra de codigo
    for caracter in texto:
        vector_codificado.append(diccionario_huffman[caracter])

    # armamos la trama binaria compl
    trama_binaria = "".join(vector_codificado)

    return vector_codificado, trama_binaria


# Pruebas
# # Prueba 1)
# archivo = "texto_ejemplo.txt"

# vector_de_proba = obtener_vector_probabilidades(archivo)

# suma = np.sum(vector_de_proba[:,1].astype(float))

# if np.isclose(suma, 1):
#     print("La suma de probabilidades es 1")
# else:
#     print("Error: no suma 1")


# with open(archivo, "r") as f:
#     contenido = f.read()

# print(contenido)

# print(vector_de_proba)



# #Prueba 2)

# probabilidades = vector_de_proba[:, 1].astype(float)
# entropia = Calcular_entropia(probabilidades)


# print("Entropia :" + str(entropia) )

