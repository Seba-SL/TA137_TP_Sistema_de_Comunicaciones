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
import matplotlib.pyplot as plt 
import utilidades as util

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

    # armamos la lista de nodos con probavilidad y simbolo
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


# item C)

def modulador(bits, esquema, M, etiquetado='gray', Eb=1.0, devolver_info=False):
    # convierte vector de bits en simbolos modulados
    # esquema: 'QAM' o 'FSK' | etiquetado: 'gray' o 'binario' (solo QAM)
    # si devolver_info=True, tambien devuelve la longitud original y el padding agregado
    bps = int(np.log2(M))

    # convertir bits a lista de enteros si viene como string (tipo 010101)
    if isinstance(bits, str):
        bits = [int(bit) for bit in bits]

    bits = np.asarray(bits, dtype=int)

    bits_originales = bits
    # guardamos longitud original antes del padding
    n_bits_original = len(bits)

    # padding al multiplo de bps mas cercano
    n_padding =(-n_bits_original) % bps

    if n_padding > 0:
        bits = np.append(bits, np.zeros(n_padding, dtype=int))

    grupos = bits.reshape(-1, bps)

    if esquema == 'QAM':
        puntos, mapa_gray, mapa_bin, _ = util._constelacion_qam(M, Eb)
        mapa = mapa_gray if etiquetado == 'gray' else mapa_bin
    else:
        puntos, mapa, _, _ = util._constelacion_fsk(M, Eb)
    
    # mapa inverso: etiqueta entera -> indice en puntos
    inv = {int(v): i for i, v in enumerate(mapa)}

    simbolos = np.array([
        puntos[inv[int(''.join(map(str, g)), 2)]]
        for g in grupos
    ])

    if devolver_info:
        return simbolos, puntos, mapa, bps,bits_originales, n_bits_original, n_padding

    return simbolos, puntos, mapa, bps



def energia_media(simbolos, bps):
    # estima Es y Eb a partir de los simbolos transmitidos
    if np.iscomplexobj(simbolos):  # QAM
        Es = float(np.mean(np.abs(simbolos) ** 2))
    else:                          # FSK: suma de cuadrados por fila
        Es = float(np.mean(np.sum(simbolos ** 2, axis=1)))
    return round(Es, 6), round(Es / bps, 6)



def graficar_constelacion(puntos, mapa, bps, titulo='Constelacion', recibidos=None, save_path=None):
    # grafica la constelacion ideal (azul) y opcionalmente los simbolos recibidos (rojo)
    # QAM: scatter en plano I-Q  |  FSK M=2: scatter en espacio (phi1, phi2)
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    fig.patch.set_facecolor('#fafafa')
    ax.set_facecolor('#f0f2f5')

    # colores
    _c_ideal = '#1a56db'
    _c_ideal_edge = '#1e3a8a'
    _c_rx = '#e05a4e'
    _c_dec = '#9ca3af'
    _c_axis = '#6b7280'
    _c_lbl = '#374151'

    if np.iscomplexobj(puntos):
        # --- QAM ---
        ax.scatter(puntos.real, puntos.imag,
                   color=_c_ideal, edgecolors=_c_ideal_edge,
                   linewidths=0.6, s=90, zorder=4)
        if recibidos is not None:
            ax.scatter(recibidos.real, recibidos.imag,
                       color=_c_rx, alpha=0.12, s=5, zorder=2)

        # fronteras de decision en los puntos medios entre niveles
        I_uniq = np.sort(np.unique(np.round(puntos.real, 8)))
        Q_uniq = np.sort(np.unique(np.round(puntos.imag, 8)))
        for x in (I_uniq[:-1] + I_uniq[1:]) / 2:
            ax.axvline(x, color=_c_dec, lw=0.7, ls='--', alpha=0.65)
        for y in (Q_uniq[:-1] + Q_uniq[1:]) / 2:
            ax.axhline(y, color=_c_dec, lw=0.7, ls='--', alpha=0.65)

        # etiquetas binarias sobre cada punto
        for pt, lbl in zip(puntos, mapa):
            ax.annotate(format(int(lbl), f'0{bps}b'), (pt.real, pt.imag),
                        textcoords='offset points', xytext=(5, 5),
                        fontsize=8, color=_c_lbl)

        ax.axhline(0, color=_c_axis, lw=0.5)
        ax.axvline(0, color=_c_axis, lw=0.5)
        ax.set_xlabel('I', color=_c_lbl)
        ax.set_ylabel('Q', color=_c_lbl)

    else:
        # --- FSK M=2: espacio 2D (phi1, phi2) ---
        ax.scatter(puntos[:, 0], puntos[:, 1],
                   color=_c_ideal, edgecolors=_c_ideal_edge,
                   linewidths=0.6, s=90, zorder=4)
        if recibidos is not None:
            ax.scatter(recibidos[:, 0], recibidos[:, 1],
                       color=_c_rx, alpha=0.12, s=5, zorder=2)

        # frontera de decision: diagonal phi1 = phi2
        lim = max(float(np.max(np.abs(puntos))) * 1.6, 1.5)
        ax.plot([-lim, lim], [-lim, lim], color=_c_dec, lw=0.7, ls='--', alpha=0.65)

        for pt, lbl in zip(puntos, mapa):
            ax.annotate(format(int(lbl), f'0{bps}b'), (pt[0], pt[1]),
                        textcoords='offset points', xytext=(5, 5),
                        fontsize=9, color=_c_lbl)

        ax.set_xlabel('φ₁', color=_c_lbl)
        ax.set_ylabel('φ₂', color=_c_lbl)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)

    ax.set_title(titulo, fontsize=11, color='#1f2937', pad=10)
    ax.set_aspect('equal')
    ax.grid(True, color='#cbd5e1', lw=0.3, alpha=0.7)
    ax.tick_params(colors=_c_lbl, labelsize=8)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_color('#d1d5db')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.show()