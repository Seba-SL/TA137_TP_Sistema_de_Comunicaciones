import transmisor,canal,receptor,utilidades

print(utilidades.TP_MENSAJE)


#Modulo A

#Ingreso de archivo de entrada, salida y parametros


archivo_entrada = "archivos/enviados/texto_largo_quijote.txt" #utilidades.seleccionar_archivo()
#para pruebas archivo_entrada = "archivos/texto_largo_quijote.txt"

#def parametros(huffman_ctrl, esquema_modulacion_ctrl , orden_ctrl , etiquetado_ctrl,ruido_awgn_ctrl,  respuesta_impulsiva_ctrl , atenuacion_ctrl,mostrar_tablas_ctrl,mostrar_resultados_ctrl,mostrar_constelaciones_ctrl):
parametros = utilidades.parametros(True,'FSK',4,None,None,None,None,False,True,True)

trama_binaria, diccionario, simbolos, puntos,mapa,bps,bits_originales = utilidades.transmitir_archivo(archivo_entrada, parametros)




trama_binaria_recibida = canal.efectos_del_canal(trama_binaria,parametros)

utilidades.recibir_archivo(trama_binaria_recibida, diccionario,simbolos,puntos,parametros,mapa,bps,bits_originales)