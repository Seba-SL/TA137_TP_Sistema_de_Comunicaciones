import os,transmisor,canal,receptor
import numpy as np

def datos_control(datos_del_grupo=None):

    archivo_tx = seleccionar_archivo(datos_del_grupo)
   
    parametros =  seleccionar_parametros(datos_del_grupo)   
#parametros_del_grupo_03()
    return archivo_tx , parametros


def seleccionar_archivo(datos_del_grupo = None):

   if(os.path.isfile(datos_del_grupo["archivo_entrada"])):
        return datos_del_grupo["archivo_entrada"]
   else:
     
    while True:
                ruta = input("Ingrese la ruta del archivo de texto a transmitir: ")

                if os.path.isfile(ruta):
                    return ruta
                else:
                    print("Error: el archivo no existe. Intente nuevamente.")
            


def seleccionar_parametros(datos_del_grupo=None):

    print("===================================")
    print(" Configuración del sistema")
    print("===================================")
    grupo03 = input("¿Usar parámetros del Grupo 03? (s/n): ").lower()

    if grupo03 == 's':

        G = datos_del_grupo["G"]
        n = datos_del_grupo["n"]
        k = datos_del_grupo["k"]
        M = datos_del_grupo["M"]
        esquema_modulacion = datos_del_grupo["esquema_modulacion"]
        aplicar_huffman = datos_del_grupo["aplicar_huffman"]

        ruido_awgn = datos_del_grupo["ruido_awgn"]
        respuesta_impulsiva = datos_del_grupo["respuesta_impulsiva"]
        atenuacion = datos_del_grupo["atenuacion"]

        etiquetado = datos_del_grupo["etiquetado"]

        ver_datos = datos_del_grupo["ver_datos"]
        ver_estadisticas = datos_del_grupo["ver_estadisticas"]
        ver_constelaciones = datos_del_grupo["ver_constelaciones"]

        archivo_tx = datos_del_grupo["archivo_entrada"]

        print("\n=== PARÁMETROS GRUPO 03 ===")

        print("Fuente de información:\n")
        print("Archivo a transmitir: ", archivo_tx)

        print("\nCodificación de fuente:\n")
        print(f"Aplicar Huffman = {aplicar_huffman}")

        print("\nCodificación de canal:\n")

        print(f"Matriz generadora: G = {G}")
        print(f"k = {k}")
        print(f"n = {n}")

        print("\nModulación:\n")
        print(f"Catiddad de simbolos: M = {M}")
        print(f"Esquema de modulación = {esquema_modulacion}")
        print(f"Codigo etiquetado: " + str(etiquetado))

        print("\nCanal:\n")
        print(f"Ruido AWGN = {ruido_awgn}")
        print(f"Respuesta impulsiva = {respuesta_impulsiva}")
        print(f"Eb/N0 = {atenuacion} dB")
       
    else:

        print("\n=== CONFIGURACIÓN DEL TRANSMISOR ===")

        M = int(input("M (2,4,8,16,...): "))
        G = eval(input("Ingrese la matriz: "))
        n = int(input("Segmentacion de trama binaria  n: "))
        k = int(input("Palabras de código de n bits  k: "))
        esquema_modulacion = input("Esquema de modulación (PSK/QAM/FSK): ")
        aplicar_huffman = input("¿Aplicar Huffman? (s/n): ").lower() == 's'

        print("\n=== CONFIGURACIÓN DEL CANAL ===")

        ruido_awgn = input("¿Agregar ruido AWGN? (s/n): ").lower() == 's'
        respuesta_impulsiva = input("¿Aplicar respuesta impulsiva? (s/n): ").lower() == 's'
        atenuacion = float(input("Eb/N0 [dB]: "))

        print("\n=== VISUALIZACIÓN ===")

        ver_datos = input("¿Mostrar datos? (s/n): ").lower() == 's'
        ver_estadisticas = input("¿Mostrar estadísticas? (s/n): ").lower() == 's'
        ver_constelaciones = input("¿Mostrar constelaciones? (s/n): ").lower() == 's'

    parametros = {
        "transmisor": {
            "M": M,
            "esquema_modulacion": esquema_modulacion,
            "aplicar_huffman": aplicar_huffman,
            "etiquetado":etiquetado,
            "G":G,
            "k":k
        },

        "canal": {
            "ruido_awgn": ruido_awgn,
            "respuesta_impulsiva": respuesta_impulsiva,
            "atenuacion": atenuacion
        },

        "receptor": {
            "ruido_awgn": ruido_awgn,
            "respuesta_impulsiva": respuesta_impulsiva,
            "atenuacion": atenuacion
        },

        "utilidades": {
            "ver_datos": ver_datos,
            "ver_estadisticas": ver_estadisticas,
            "ver_constelaciones": ver_constelaciones
        }
    }

    return parametros



def mostrar_datos_tx(datos_tx, parametros):

    print("\n" + "="*60)
    print("📡 TRANSMISOR")
    print("="*60)
     
    if(parametros["utilidades"]["ver_datos"]):
        print("\nVector de probabilidades:\n " , datos_tx["Vector probabilidades"])
        print("\nDiccionario de Huffman:\n " , datos_tx["Diccionario Huffman"])
        print("\nVector codificado :\n " , datos_tx["Vector codificado"])
        print("\ntrama_binaria :\n " , datos_tx["Trama binaria"])
    

    if(parametros["utilidades"]["ver_estadisticas"]):
        print("\nEntropia:\n " , datos_tx["Entropia"])
        print("\nlongitud minima :\n " , datos_tx["Longitud minima"])
        print("\nlongitud promedio :\n " , datos_tx["Longitud promedio"])
        print("\nEficiencia:\n " , datos_tx["Longitud minima"]/datos_tx["Longitud promedio"])
        print("\nEnergia media :\n " ,datos_tx["Energia media"])
    



    return



def mostrar_datos_rx(datos_salida, parametros):
    

    print("\n" + "="*60)
    print("📥 RECEPTOR")
    print("="*60)
    


    if(parametros["utilidades"]["ver_datos"]):
            print("\nTexto decodificado:")
            print(datos_salida["Texto decodificado"])
            print("\nBits RX:")
            print(datos_salida["Bits RX"])



    if(parametros["utilidades"]["ver_estadisticas"]):
        print(
            "\nProbabilidad de error de simbolo:",
            datos_salida["Probabilidad error simbolo"]
        )

        print(
            "\nProbabilidad de error de bit:",
            datos_salida["Probabilidad error bit"]
        )

   


    return


def mostrar_datos_canal(parametros):

    print("\n" + "="*60)
    print("🌪️ CANAL:")
    print("="*60)
    
    if(parametros["utilidades"]["ver_datos"]):
        if(parametros["canal"]["ruido_awgn"]):
            print("\nRuido AWGN")

        if(parametros["canal"]["respuesta_impulsiva"]):
            print("\nRespuesta impulsiva")

        if(parametros["canal"]["atenuacion"]):
            print("\nRespuesta impulsiva")

    return



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


def _gray(n):
    # genera array con los n codigos de Gray: indice -> valor Gray
    return np.array([i ^ (i >> 1) for i in range(n)])
