import os,transmisor,canal,receptor
import numpy as np

TP_MENSAJE = "---- TP Grupo 3: Simulación y Análisis de un Sistema de Comunicaciones ----"

def seleccionar_archivo():
    while True:
        ruta = input("Ingrese la ruta del archivo de texto a transmitir: ")

        if os.path.isfile(ruta):
            return ruta
        else:
            print("Error: el archivo no existe. Intente nuevamente.")


def parametros(usar_huffman, esquema_modulacion ,  M , etiquetado,ruido_awgn,  respuesta_impulsiva , atenuacion,mostrar_tablas,mostrar_resultados,mostrar_constelaciones):

    param_fuente = {
        "usar_huffman": usar_huffman
    }

    param_canal = {
        "ruido_awgn": ruido_awgn,
        "respuesta_impulsiva": respuesta_impulsiva,
        "atenuacion": atenuacion
    }

    param_control = {
        "mostrar_tablas": mostrar_tablas,
        "mostrar_resultados": mostrar_resultados,
        "mostrar_constelaciones": mostrar_constelaciones
    }

    param_transmisor = {
        "M": M,
        "esquema_modulacion": esquema_modulacion
    }

    parametros = {
        "fuente": param_fuente,
        "transmisor": param_transmisor,
        "canal": param_canal,
        "control": param_control
    }


    return  parametros


def mostrar(vector_probabilidades,entropia,vector_codigos, diccionario,Long_cod,vector_codificado,trama_binaria ,long_min,mostrar_tablas_flag,mostrar_constelaciones):

    print("\n" + "="*50)
    print("📊 RESULTADOS")
    print("="*50)
    
    if(mostrar_tablas_flag):
        print("\n🔹 Vector de probabilidades:")
        print(vector_probabilidades)

    print("\n🔹 Entropía:")
    print(f"{entropia:.4f} bits")


    if(mostrar_tablas_flag):
        print("\n🔹 Vector de códigos:")
        print(vector_codigos)

    print("\n🔹 Diccionario (símbolo -> código):")
    for simbolo, codigo in diccionario.items():
        print(f"  {simbolo} -> {codigo}")

    print("\n🔹 Longitud promedio del código:")
    print(f"{Long_cod:.4f} bits")

    print("\n🔹 Longitud minima del código:")
    print(f"{long_min:.4f} bits")

    if(mostrar_tablas_flag):
        print("\n🔹 Vector codificado:")
        print(vector_codificado)

    if(mostrar_tablas_flag):
        print("\n🔹 Trama binaria:")
        print(trama_binaria)

    print("\n" + "="*50)
    return


def transmitir_archivo(archivo, parametros):

    usar_huffman = parametros["fuente"]["usar_huffman"]
    ruido = parametros["canal"]["ruido_awgn"]
    mostrar_resultados_flag = parametros["control"]["mostrar_resultados"]
    mostrar_tablas_flag = parametros["control"]["mostrar_tablas"]
    mostrar_constelaciones = parametros["control"]["mostrar_constelaciones"]
    M = parametros["transmisor"]["M"]
    esquema_modulacion = parametros["transmisor"]["esquema_modulacion"]

    print("\n" + "="*60)
    print("📡 TRANSMISOR")
    print("="*60)
    

    vector_probabilidades = transmisor.obtener_vector_probabilidades(archivo)
    probabilidades = vector_probabilidades[:, 1].astype(float)
    entropia = transmisor.Calcular_entropia(probabilidades)

    vector_codigos, diccionario = transmisor.vector_codigo_huffman(vector_probabilidades)

    long_min,Long_cod = transmisor.longitudes_codigo(vector_probabilidades, diccionario)

    vector_codificado, trama_binaria = transmisor.codificar_texto_huffman(archivo,diccionario)

    if mostrar_resultados_flag: 
        mostrar(vector_probabilidades, entropia, vector_codigos, diccionario,Long_cod, vector_codificado, trama_binaria,long_min,mostrar_tablas_flag,mostrar_constelaciones)

    # item C

    if mostrar_resultados_flag: 
        print(f"\n🔹 Modulación: {M} - {esquema_modulacion}\n")
        
    simbolos, puntos, mapa, bps, n_bits_original, n_padding = transmisor.modulador(trama_binaria, esquema_modulacion , M, 'gray', 1,True)

    if mostrar_constelaciones:
        transmisor.graficar_constelacion(puntos, mapa, bps, 'Constelacion', None, None)


    return trama_binaria, diccionario, simbolos, puntos,mapa ,bps


def recibir_archivo(trama_binaria_recibida, diccionario,simbolos,puntos,parametros,mapa,bps):

    esquema = parametros["transmisor"]["esquema_modulacion"]
    print("\n" + "="*60)
    print("📥 RECEPTOR")
    print("="*60)

    indices = receptor._detectar_indices(simbolos, puntos, esquema)

    trama_binaria_recibida = receptor.demodulador(simbolos,puntos,mapa,bps,esquema)

    texto_decodificado = receptor.decodificador(trama_binaria_recibida, diccionario)
    print("\n🔹Texto decodificado en el receptor:")
    print(texto_decodificado)

    receptor.generar_txt(texto_decodificado,"archivos/recibidos/salida_receptor")
    return 


# item C 

def _gray(n):
    # genera array con los n codigos de Gray: indice -> valor Gray
    return np.array([i ^ (i >> 1) for i in range(n)])

def _constelacion_qam(M, Eb=1.0):
    # constelacion cuadrada M-QAM normalizada a Eb dado
    # retorna: puntos (complex, shape M), mapa_gray, mapa_bin, bps
    raiz = int(np.sqrt(M))
    bps = int(np.log2(M))
    bps_dim = bps // 2
    niveles = np.arange(-(raiz - 1), raiz, 2, dtype=float)  # paso 2, simetricos
    gc = _gray(raiz)

    puntos, mapa_gray, mapa_bin = [], [], []
    for qi in range(raiz):      # fila -> eje Q
        for ii in range(raiz):  # columna -> eje I
            puntos.append(niveles[ii] + 1j * niveles[qi])
            mapa_gray.append((gc[qi] << bps_dim) | gc[ii])
            mapa_bin.append(qi * raiz + ii)

    puntos = np.array(puntos)
    mapa_gray = np.array(mapa_gray)
    mapa_bin = np.array(mapa_bin)

    # normalizar: Es = Eb * bps  (Eb = 1 -> Es = bps)
    Es_actual = np.mean(np.abs(puntos) ** 2)
    puntos *= np.sqrt(Eb * bps / Es_actual)

    return puntos, mapa_gray, mapa_bin, bps

def _constelacion_fsk(M, Eb=1.0):
    # M simbolos ortogonales en espacio M-dimensional, normalizados a Eb=1
    # retorna: puntos (shape M x M), mapa (orden natural), mapa, bps
    bps = int(np.log2(M))
    Es = Eb * bps            # Eb=1 -> Es = log2(M)
    puntos = np.sqrt(Es) * np.eye(M)
    mapa = np.arange(M)      # orden natural siempre para FSK
    return puntos, mapa, mapa, bps