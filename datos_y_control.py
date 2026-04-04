import transmisor,canal,receptor,utilidades



print(utilidades.TP_MENSAJE)


#Modulo A

#Ingreso de archivo de entrada, para pruebas archivo_entrada = "archivos/texto_ejemplo.txt"
archivo_entrada = utilidades.seleccionar_archivo()
archivo_salida = "texto_recibido.txt"


# Parametros de la fuente
usar_huffman = True

# parametros del transmisor/receptor
# (los completamos otro dia cuando cuando hagamos modulacion y canal)
esquema_modulacion = None      # puede ser 2-PAM, 4-PSK, 8-QAM, etc.
M = None                       # orden de mod
etiquetado = None              # gray o binario

# params del canal
ruido_awgn = None              # potencia de ruido, varianza, Eb/N0, etc.
respuesta_impulsiva = None     # mas adelante
atenuacion = None              # mas adelante

# params de control
mostrar_tablas = True
mostrar_resultados = True
mostrar_constelaciones = False   # en el A y B todavia no lo usamos

print("Parametros inicializados correctamente.")
print(f"Archivo de entrada: {archivo_entrada}")
print(f"Archivo de salida: {archivo_salida}")


#Modulo B

# 1) Probabilidades
vector_prob = transmisor.obtener_vector_probabilidades(archivo_entrada)

print("Vector de probabilidades:")
print(vector_prob)

# 2) Entropía
probabilidades = vector_prob[:,1].astype(float)

H = transmisor.Calcular_entropia(probabilidades)

print("Entropia de la fuente:", H)