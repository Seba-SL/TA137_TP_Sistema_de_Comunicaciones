import os
TP_MENSAJE = "---- TP Grupo 3: Simulación y Análisis de un Sistema de Comunicaciones ----"

def seleccionar_archivo():
    while True:
        ruta = input("Ingrese la ruta del archivo de texto a transmitir: ")

        if os.path.isfile(ruta):
            return ruta
        else:
            print("Error: el archivo no existe. Intente nuevamente.")

