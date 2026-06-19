import numpy as np
import matplotlib.pyplot as plt 
import transmisor,utilidades

def recibir_datos(datos_tx, datos_rx , parametros):
    datos_salida = {}

   
    #C)

    if(parametros["utilidades"]["ver_constelaciones"]):
        transmisor.iii_graficar_constelacion( datos_tx["Puntos"],  datos_tx["Mapa"],  datos_tx["BPS"], titulo='Constelacion despues del canal (con ruido AWGN): ' + str(parametros["transmisor"]["M"]) + "-"+ str(parametros["transmisor"]["esquema_modulacion"]), recibidos=datos_rx["simbolos_rx"], save_path=None)

  
    bits_rx = iV_demodulador(datos_rx["simbolos_rx"] , datos_tx["Puntos"], datos_tx["Mapa"],   datos_tx["BPS"], parametros["transmisor"]["esquema_modulacion"])
    

    #E
    H = i_calcular_H(parametros["transmisor"]["G"], parametros["transmisor"]["k"], parametros["transmisor"]["n"])


    tabla_s = ii_tabla_sindromes(H, parametros["transmisor"]["n"])

    bits_rx = iv_decodificador_canal(bits_rx, parametros["transmisor"]["k"], parametros["transmisor"]["n"], H, tabla_s, datos_tx["n_bits_original"])

    #B)
    texto_decodificado_fuente = vi_decodificador_fuente(bits_rx, datos_tx["Diccionario Huffman"])

    vii_generar_txt(texto_decodificado_fuente, "archivos/recibidos/salida_receptor")

    Pe_simbolo = v_estimar_Pe_simbolo(datos_tx["Simbolos"] , datos_rx["simbolos_rx"],  datos_tx["Puntos"], parametros["transmisor"]["esquema_modulacion"])

    Pe_bit = vi_estimar_Pe_bit(datos_tx["Trama binaria"], bits_rx)




    # Guardar resultados
    datos_salida["Bits RX"] = bits_rx

    datos_salida["Texto decodificado"] = texto_decodificado_fuente

    datos_salida["Probabilidad error simbolo"] = Pe_simbolo

    datos_salida["Probabilidad error bit"] = Pe_bit

    datos_salida["Simbolos RX"] = datos_rx["simbolos_rx"]

    # Mostrar resultados
    utilidades.mostrar_datos_rx(datos_salida, parametros)


    return datos_salida


#B)
# 6) Elabore una función que decodifique las palabras de código recibidas a su entrada, devolviendo en un
# vector los caracteres del texto.

def vi_decodificador_fuente(vector_codificado, diccionario_huffman):
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



# E) CODIFICACIÓN DE CANAL
# En este apartado se intercalará, entre el Codificador de fuente y el Modulador, un bloque Codificador de canal.
# Similarmente, entre el Demodulador y el Decodificador de fuente se intercalará un Decodificador de canal. La
# acción de estos bloques permitirá la detección y corrección de errores de bits.


# Para el Receptor:


# 1) Elabore una función que reciba a su entrada los valores adoptados de k, n y la Matriz Generadora, G, y
# devuelva su matriz de Chequeo de Paridad asociada, H.

def i_calcular_H(G, k, n):
    # G = [P | I_k]  =>  H = [I_{n-k} | P^T]

    G = np.asarray(G, dtype=int)

    # cantidad de bits de paridad
    r = n - k

    # Verificamos dimensiones de G
    if G.shape != (k, n):
        raise ValueError(f"La matriz G debe tener dimension ({k}, {n}), pero tiene {G.shape}")

    # Verificamos que las ultimas k columnas sean la identidad I_k
    I_k = np.eye(k, dtype=int)
    if not np.array_equal(G[:, r:], I_k):
        raise ValueError("La matriz G no esta en forma [P | I_k]. Revisar el orden de las columnas.")

    # P esta en las primeras n-k columnas
    P = G[:, :r]

    # H = [I_{n-k} | P^T]
    H = np.hstack((np.eye(r, dtype=int), P.T))

    # Verificacion fundamental: H @ G.T = 0 mod 2
    verificacion = np.mod(H @ G.T, 2)

    if not np.all(verificacion == 0):
        raise ValueError("La matriz H calculada no cumple H @ G.T = 0 mod 2.")

    return H

# 2) Elabore una función que reciba a su entrada la matriz de Chequeo de Paridad, H, y calcule y devuelva la
# tabla de síndromes, S.

def ii_tabla_sindromes(H, n):
    # Genera la tabla completa de sindromes.
    # Para cada sindrome se guarda un patron de error de peso minimo que lo
    # produce. Ese patron se llama lider de coset.

    from itertools import combinations

    H = np.asarray(H, dtype=int)

    # cantidad de bits del sindrome
    r = H.shape[0]

    # cantidad total de sindromes posibles
    total_sindromes = 2 ** r

    tabla = {}

    # Recorremos patrones de error por peso creciente.
    # Asi, cuando aparece por primera vez un sindrome,
    # queda asociado a un patron de error de peso minimo.
    for peso in range(n + 1):

        for posiciones in combinations(range(n), peso):

            e = np.zeros(n, dtype=int)

            for pos in posiciones:
                e[pos] = 1

            # sindrome s = H e^T mod 2
            s = tuple(np.mod(H @ e, 2))

            # si el sindrome todavia no estaba, guardamos este patron
            if s not in tabla:
                tabla[s] = e

            # cuando ya tenemos todos los sindromes posibles, terminamos
            if len(tabla) == total_sindromes:
                return tabla

    return tabla

def resumen_tabla_sindromes(tabla_s):
    # Cuenta cuantos patrones correctores hay de cada peso de Hamming

    resumen = {}

    for patron_error in tabla_s.values():
        peso = int(np.sum(patron_error))

        if peso not in resumen:
            resumen[peso] = 0

        resumen[peso] += 1

    return dict(sorted(resumen.items()))


def mostrar_resumen_tabla_sindromes(tabla_s):
    # Muestra un resumen de la tabla de sindromes

    resumen = resumen_tabla_sindromes(tabla_s)

    print("Resumen de la tabla de sindromes:")
    print("Peso del patron | Cantidad de sindromes")
    print("---------------------------------------")

    for peso, cantidad in resumen.items():
        print(f"{peso:<15} | {cantidad}")


def verificar_errores_de_1_bit(H, tabla_s, n):
    # Verifica que todos los errores de 1 bit se corrijan correctamente

    for i in range(n):
        e = np.zeros(n, dtype=int)
        e[i] = 1

        s = tuple(np.mod(H @ e, 2))

        if s not in tabla_s:
            return False

        if not np.array_equal(tabla_s[s], e):
            return False

    return True


def contar_patrones_corregibles_por_peso(H, tabla_s, n, peso):
    # Cuenta cuantos patrones de error de cierto peso se corrigen exactamente

    from itertools import combinations

    total = 0
    corregibles = 0

    for posiciones in combinations(range(n), peso):
        e = np.zeros(n, dtype=int)

        for pos in posiciones:
            e[pos] = 1

        s = tuple(np.mod(H @ e, 2))
        e_estimado = tabla_s[s]

        if np.array_equal(e_estimado, e):
            corregibles += 1

        total += 1

    return corregibles, total

# 3) Elabore una función que reciba a su entrada la matriz de chequeo de Paridad, H, la tabla de Síndromes,
# S y una palabra de código, de longitud n, calcule su síndrome, detecte y corrija de ser posible los errores
# ocurridos, y devuelva la palabra corregida.


def iii_decodificar_palabra(palabra, H, tabla_s, k):
    # calcula sindrome, busca patron de error, corrige y extrae los k bits del mensaje
    s = tuple(np.mod(H @ palabra, 2))
    e = tabla_s.get(s, np.zeros(len(palabra), dtype=int))
    return np.mod(palabra + e, 2)[-k:]



# 4) Elabore una función que reciba a su entrada la matriz de chequeo de Paridad, H, la tabla de Síndromes,
# S, y un vector de valores binarios, “0” ó “1”, los organice en palabras codificadas de n bits y las
# decodifique, detectando y corrigiendo todos los errores que sean posibles, utilizando la función
# solicitada en (3).


def iv_decodificador_canal(bits, k, n, H, tabla_s, n_bits_original=None):
    # Organiza bits recibidos en palabras de n bits, corrige cada palabra
    # mediante sindrome y recupera los k bits de informacion.
    # Si n_bits_original se pasa como parametro, recorta el padding final.

    if isinstance(bits, str):
        bits = np.array([int(b) for b in bits], dtype=int)
    else:
        bits = np.asarray(bits, dtype=int)

    rem = len(bits) % n

    if rem:
        bits = np.append(bits, np.zeros(n - rem, dtype=int))

    palabras = bits.reshape(-1, n)

    bits_decodificados = np.array([
        iii_decodificar_palabra(p, H, tabla_s, k)
        for p in palabras
    ]).flatten()

    if n_bits_original is not None:
        bits_decodificados = bits_decodificados[:n_bits_original]

    return bits_decodificados


# 5) Elabore una función que calcule la distancia mínima dmin, la cantidad máxima de errores a detectar, e,
# y a corregir, t.


def v_metricas_canal(G, k, n):
    # dmin = minimo peso de Hamming de todas las palabras de codigo no nulas
    dmin = n
    for i in range(1, 2**k):
        m = np.array([(i >> j) & 1 for j in range(k)], dtype=int)
        w = int(np.sum(np.mod(m @ G, 2)))
        if w < dmin:
            dmin = w
    return dmin, dmin - 1, (dmin - 1) // 2