
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



# item C)
def _detectar_indices(simbolos, puntos, esquema):
    # retorna indices ML de los simbolos detectados
    if esquema == 'QAM':
        return np.array([np.argmin(np.abs(puntos - s)) for s in simbolos])
    else:  # FSK: maximo componente
        return np.argmax(simbolos, axis=1)

def demodulador(simbolos_rx, puntos, mapa, bps, esquema):
    # demodulacion ML: minima distancia euclidea (QAM) o maximo componente (FSK)
    indices = _detectar_indices(simbolos_rx, puntos, esquema)
    bits_rx = []
    for idx in indices:
        bits_rx.extend([int(b) for b in format(int(mapa[idx]), f'0{bps}b')])
    return np.array(bits_rx)


def estimar_Pe_simbolo(simbolos_tx, simbolos_rx, puntos, esquema):
    # Compara simbolos transmitidos y recibidos.
    # Devuelve la probabilidad de error de simbolo sin redondear.
    idx_tx = _detectar_indices(simbolos_tx, puntos, esquema)
    idx_rx = _detectar_indices(simbolos_rx, puntos, esquema)
    return float(np.mean(idx_tx != idx_rx))

def estimar_Pe_bit(bits_tx, bits_rx):
    # Compara bits transmitidos y recibidos.
    # Devuelve la probabilidad de error de bit sin redondear.
    bits_rx = np.array([int(b) for b in bits_rx], dtype=int)
    print("bits_tx =", type(bits_tx))
    print("bits_tx =", bits_tx)

    print("bits_rx =", type(bits_rx))
    print("bits_rx =", bits_rx)
  
    bits_tx = np.asarray(bits_tx)
    bits_rx = np.asarray(bits_rx)

    n = min(len(bits_tx), len(bits_rx))
    return float(np.mean(bits_tx[:n] != bits_rx[:n]))


def imprimir_tabla_cd(resultados_cd):
    # imprime una tabla resumen de las pruebas de modulacion o canal
    print("\nTabla resumen C y D:")
    print("Modulacion | M | Etiq | Eb/N0[dB] | bps | N_bits | N_simbolos | Es | Eb | Pe_sim | Pe_bit")
    print("-" * 105)

    for fila in resultados_cd:
        print(
            f"{fila['modulacion']:<10} | "
            f"{fila['M']:<2} | "
            f"{fila['etiquetado']:<7} | "
            f"{fila['EbN0_dB']:<9} | "
            f"{fila['bps']:<3} | "
            f"{fila['N_bits']:<6} | "
            f"{fila['N_simbolos']:<10} | "
            f"{fila['Es']:<6} | "
            f"{fila['Eb']:<6} | "
            f"{fila['Pe_sim']:<8} | "
            f"{fila['Pe_bit']:<8}"
        )


def guardar_tabla_cd(resultados_cd, nombre_archivo="tabla_resultados_CD.csv"):
    # guarda la tabla en un archivo csv para poder usarla en el informe
    columnas = [
        "modulacion",
        "M",
        "etiquetado",
        "EbN0_dB",
        "bps",
        "N_bits",
        "N_simbolos",
        "Es",
        "Eb",
        "Pe_sim",
        "Pe_bit"
    ]

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(";".join(columnas) + "\n")

        for fila in resultados_cd:
            valores = []
            for col in columnas:
                valores.append(str(fila[col]))

            archivo.write(";".join(valores) + "\n")

    print(f"\nTabla guardada en: {nombre_archivo}")