import transmisor,canal,receptor,utilidades



print(utilidades.TP_MENSAJE)


#Modulo A

#Ingreso de archivo de entrada, salida y parametros


archivo_entrada = "archivos/enviados/texto_ejemplo.txt" #utilidades.seleccionar_archivo()
#para pruebas archivo_entrada = "archivos/texto_ejemplo.txt"

#def parametros(huffman_ctrl, esquema_modulacion_ctrl , orden_ctrl , etiquetado_ctrl,ruido_awgn_ctrl,  respuesta_impulsiva_ctrl , atenuacion_ctrl,mostrar_tablas_ctrl,mostrar_resultados_ctrl,mostrar_constelaciones_ctrl):
parametros = utilidades.parametros(True,None,None,None,None,None,None,True,True,False)

trama_binaria, diccionario = utilidades.transmitir_archivo(archivo_entrada, parametros)

trama_binaria_recibida = canal.efectos_del_canal(trama_binaria,parametros)

utilidades.recibir_archivo(trama_binaria_recibida, diccionario)