import transmisor,canal,receptor,utilidades

#Datos codificador de canal
G =[[1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1]]

k = 5  # Segmentacion de trama binaria
n=15   # Palabras de código de n bits


datos_del_grupo = {
    "archivo_entrada":"archivos/enviados/texto_ejemplo.txt", # si queres entrar archivo por teclado colcocar: False 
    "M": 16, #tamaño de la constelación, M
    "esquema_modulacion": "QAM",  #esquemas de banda base y banda pasante
    "aplicar_huffman": True,
    "ruido_awgn": True,
    "respuesta_impulsiva": False,
    "atenuacion": 6,
    "etiquetado":'gray',  # o binario
    "G":G,
    "n":n,
    "k":k,
    "ver_datos": True,
    "ver_estadisticas": True,
    "ver_constelaciones": True
}

print("---- TP Grupo 3: Simulación y Análisis de un Sistema de Comunicaciones ----")

archivo_tx , parametros  = utilidades.datos_control(datos_del_grupo)

datos_tx = transmisor.transmitir_archivo(archivo_tx , parametros )

datos_rx = canal.enviar_por_canal(datos_tx, parametros)

datos_salida = receptor.recibir_datos(datos_tx, datos_rx , parametros)




# 3) Código BCH (15, 5)
#El código BCH(15,5) es un código cíclico corrector de errores binario 
# muy utilizado en telecomunicaciones y almacenamiento digital. Pertenece a la familia de códigos Bose-Chaudhuri-Hocquenghem (BCH) 