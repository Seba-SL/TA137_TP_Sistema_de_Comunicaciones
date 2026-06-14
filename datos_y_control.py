import transmisor,canal,receptor,utilidades

print(utilidades.TP_MENSAJE)


#Modulo A

#Ingreso de archivo de entrada, salida y parametros


archivo_entrada = "archivos/enviados/texto_ejemplo.txt" #utilidades.seleccionar_archivo()
#para pruebas archivo_entrada = "archivos/texto_largo_quijote.txt"

#def parametros(huffman_ctrl, esquema_modulacion_ctrl , orden_ctrl , etiquetado_ctrl,ruido_awgn_ctrl,  respuesta_impulsiva_ctrl , atenuacion_ctrl,mostrar_tablas_ctrl,mostrar_resultados_ctrl,mostrar_constelaciones_ctrl):
parametros = utilidades.parametros(True,'FSK',4,None,None,None,6,False,True,True)

trama_binaria, diccionario, simbolos_tx, puntos,mapa,bps,bits_tx = utilidades.transmitir_archivo(archivo_entrada, parametros)




simbolos_rx = canal.efectos_del_canal(simbolos_tx,parametros)

utilidades.recibir_archivo(trama_binaria, diccionario,simbolos_tx,simbolos_rx,puntos,parametros,mapa,bps,bits_tx)