import numpy as np
import matplotlib.pyplot as plt 
import transmisor,utilidades

def recibir_datos(datos_tx, datos_rx , parametros):
    datos_salida = {}

   
    #C)

    if(parametros["utilidades"]["ver_constelaciones"]):
        transmisor.iii_graficar_constelacion( datos_tx["Puntos"],  datos_tx["Mapa"],  datos_tx["BPS"], titulo='Constelacion despues del canal (con ruido AWGN): ' + str(parametros["transmisor"]["M"]) + "-"+ str(parametros["transmisor"]["esquema_modulacion"]), recibidos=datos_rx["simbolos_rx"], save_path=None)

  
    bits_rx = iV_demodulador(datos_rx["simbolos_rx"] , datos_tx["Puntos"], datos_tx["Mapa"],   datos_tx["BPS"], parametros["transmisor"]["esquema_modulacion"])
    
    #B)
    texto_decodificado_canal = vi_decodificador_canal(bits_rx, datos_tx["Diccionario Huffman"])

    vii_generar_txt(texto_decodificado_canal, "archivos/recibidos/salida_receptor")

    Pe_simbolo = v_estimar_Pe_simbolo(datos_tx["Simbolos"] , datos_rx["simbolos_rx"],  datos_tx["Puntos"], parametros["transmisor"]["esquema_modulacion"])

    Pe_bit = vi_estimar_Pe_bit(datos_tx["Trama binaria"], bits_rx)




    # Guardar resultados
    datos_salida["Bits RX"] = bits_rx

    datos_salida["Texto decodificado"] = texto_decodificado_canal

    datos_salida["Probabilidad error simbolo"] = Pe_simbolo

    datos_salida["Probabilidad error bit"] = Pe_bit

    datos_salida["Simbolos RX"] = datos_rx["simbolos_rx"]

    # Mostrar resultados
    utilidades.mostrar_datos_rx(datos_salida, parametros)


    return datos_salida


#B)
# 6) Elabore una función que decodifique las palabras de código recibidas a su entrada, devolviendo en un
# vector los caracteres del texto.

def vi_decodificador_canal(vector_codificado, diccionario_huffman):
  #el diccionario que me da la función vector_codigo_huffman es del tipo {np.str_('h'): '00'}...
  diccionario_inverso = {v: k for k, v in diccionario_huffman.items()}

  texto_decodificado = []
  bits = ""
  for codigo in vector_codificado:
    bits += str(codigo)
    if bits in diccionario_inverso:
      texto_decodificado.append(diccionario_inverso[bits])
      bits = ""
  return texto_decodificado




# 7) Elabore una función que reciba un vector de caracteres y genere un archivo de texto como salida del
# receptor.

def vii_generar_txt(vector_decodificado, archivo_salida):
  # Convertimos la lista a un array de numpy para poder usar .astype
    texto_decodificado = "".join(np.array(vector_decodificado).astype(str))

    with open(archivo_salida, 'w', encoding='utf-8') as archivo:
        archivo.write(texto_decodificado)


#C)



# 4) Elabore una función que reciba a su entrada, desde el programa principal, un vector de símbolos
# modulados, el esquema y orden de la modulación, y el código seleccionado para el etiquetamiento de
# los símbolos, efectúe la demodulación de los símbolos y obtenga la información binaria “0” ó “1”.


def iV_demodulador(simbolos_rx, puntos, mapa, bps, esquema):
    # demodulacion ML: minima distancia euclidea (QAM) o maximo componente (FSK)
    indices = _detectar_indices(simbolos_rx, puntos, esquema)
    bits_rx = []
    for idx in indices:
        bits_rx.extend([int(b) for b in format(int(mapa[idx]), f'0{bps}b')])
    return np.array(bits_rx)



def _detectar_indices(simbolos, puntos, esquema):
    # retorna indices ML de los simbolos detectados
    if esquema == 'QAM':
        return np.array([np.argmin(np.abs(puntos - s)) for s in simbolos])
    else:  # FSK: maximo componente
        return np.argmax(simbolos, axis=1)
    

# 5) Elabore una función que reciba y compare sendos vectores de símbolos modulados y demodulados, y
# estime la probabilidad de error de símbolo del sistema.




def v_estimar_Pe_simbolo(simbolos_tx, simbolos_rx, puntos, esquema):
    # Compara simbolos transmitidos y recibidos.
    # Devuelve la probabilidad de error de simbolo sin redondear.
    idx_tx = _detectar_indices(simbolos_tx, puntos, esquema)
    idx_rx = _detectar_indices(simbolos_rx, puntos, esquema)
    return float(np.mean(idx_tx != idx_rx))



# 6) Elabore una función que reciba y compare sendos vectores de dígitos binarios transmitidos y recibidos,
# y estime la probabilidad de error de bit del sistema.



def vi_estimar_Pe_bit(bits_tx, bits_rx):
    
    bits_tx = np.array([int(b) for b in bits_tx], dtype=int)
    bits_rx = np.array([int(b) for b in bits_rx], dtype=int)


    # Compara bits transmitidos y recibidos.
    # Devuelve la probabilidad de error de bit sin redondear.
    bits_rx = np.array([int(b) for b in bits_rx], dtype=int)
    # print("Tipo de dato bits_tx =", type(bits_tx))
    # print("bits_tx =", bits_tx)

    # print("Tipo de dato bits_rx =", type(bits_rx))
    # print("bits_rx =", bits_rx)
  
    bits_tx = np.asarray(bits_tx)
    bits_rx = np.asarray(bits_rx)

    n = min(len(bits_tx), len(bits_rx))
    return float(np.mean(bits_tx[:n] != bits_rx[:n]))



