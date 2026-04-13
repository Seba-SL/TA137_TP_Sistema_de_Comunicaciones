
import numpy as np

# Para el Receptor:
# 6) Elabore una función que decodifique las palabras de código recibidas a su entrada, devolviendo en un
# vector los caracteres del texto.
# 7) Elabore una función que reciba un vector de caracteres y genere un archivo de texto como salida del
# receptor.



def decodificador(vector_codificado, diccionario_huffman):
  #el diccionario que me da la función vector_codigo_huffman es del tipo {np.str_('h'): '00'}...
  diccionario_inverso = {v: k for k, v in diccionario_huffman.items()}

  texto_decodificado = []
  bits = ""
  for codigo in vector_codificado:
    bits += codigo
    if bits in diccionario_inverso:
      texto_decodificado.append(diccionario_inverso[bits])
      bits = ""
  return texto_decodificado



def generar_txt(vector_decodificado, archivo_salida):
    # Convertimos la lista a un array de numpy para poder usar .astype
    texto_decodificado = "".join(np.array(vector_decodificado).astype(str))

    with open(archivo_salida, 'w', encoding='utf-8') as archivo:
        archivo.write(texto_decodificado)