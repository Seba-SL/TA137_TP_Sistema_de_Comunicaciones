import os,transmisor,canal,receptor


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

    parametros = {
        "fuente": param_fuente,
        "canal": param_canal,
        "control": param_control
    }


    return  parametros


def mostrar(vector_probabilidades,entropia,vector_codigos, diccionario,Long_cod,vector_codificado,trama_binaria ):

    print("\n" + "="*50)
    print("📊 RESULTADOS")
    print("="*50)
    
    print("\n🔹 Vector de probabilidades:")
    print(vector_probabilidades)

    print("\n🔹 Entropía:")
    print(f"{entropia:.4f} bits")

    print("\n🔹 Vector de códigos:")
    print(vector_codigos)

    print("\n🔹 Diccionario (símbolo -> código):")
    for simbolo, codigo in diccionario.items():
        print(f"  {simbolo} -> {codigo}")

    print("\n🔹 Longitud promedio del código:")
    print(f"{Long_cod[0]:.4f} bits")

    print("\n🔹 Vector codificado:")
    print(vector_codificado)

    print("\n🔹 Trama binaria:")
    print(trama_binaria)

    print("\n" + "="*50)
    return


def transmitir_archivo(archivo, parametros):

    usar_huffman = parametros["fuente"]["usar_huffman"]
    ruido = parametros["canal"]["ruido_awgn"]
    mostrar_flag = parametros["control"]["mostrar_resultados"]

    print("\n" + "="*60)
    print("📡 TRANSMISOR")
    print("="*60)
    

    vector_probabilidades = transmisor.obtener_vector_probabilidades(archivo)
    probabilidades = vector_probabilidades[:, 1].astype(float)
    entropia = transmisor.Calcular_entropia(probabilidades)

    vector_codigos, diccionario = transmisor.vector_codigo_huffman(vector_probabilidades)

    Long_cod = transmisor.longitudes_codigo(vector_probabilidades, diccionario)

    vector_codificado, trama_binaria = transmisor.codificar_texto_huffman(archivo,diccionario)

    

    if mostrar_flag: 
        mostrar(vector_probabilidades, entropia, vector_codigos, diccionario,Long_cod, vector_codificado, trama_binaria)

    return trama_binaria, diccionario


def recibir_archivo(trama_binaria_recibida, diccionario):


    print("\n" + "="*60)
    print("📥 RECEPTOR")
    print("="*60)

    texto_decodificado = receptor.decodificador(trama_binaria_recibida, diccionario)
    print("\n🔹Texto decodificado en el receptor:")
    print(texto_decodificado)

    receptor.generar_txt(texto_decodificado,"archivos/recibidos/salida_receptor")
    return 