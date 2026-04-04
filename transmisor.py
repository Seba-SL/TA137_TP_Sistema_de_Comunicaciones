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
    print("La suma de probabilidades es 1")
    return vector_probabilidades

  else:
    print("Error: no suma 1")
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

