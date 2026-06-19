import numpy as np 
import utilidades

def enviar_por_canal(datos_tx, parametros):
    datos_rx ={}

    
    utilidades.mostrar_datos_canal(parametros)

    datos_rx["simbolos_rx"] =  canal_awgn(datos_tx["Simbolos"], parametros["canal"]["atenuacion"], parametros["transmisor"]["esquema_modulacion"])

            
    return datos_rx
#D) EFECTOS DEL CANAL
# En este apartado, los alumnos simularán diferentes efectos del canal, tales como ruido térmico, atenuación de
# la señal, desvanecimiento selectivo en frecuencia, etc.



# 1) Elabore una función que genere una muestra aleatoria de ruido térmico (Additive White Gaussian Noise,
# AWGN), con función de distribución Gaussiana de media nula, varianza σ2 = N0/2 y dimensión N.


# 3) Elabore una función que aplique, a los símbolos modulados, los efectos de la atenuación del canal y del
# ruido aditivo AWGN, en base a los valores obtenidos de las funciones anteriores.


def canal_awgn(simbolos, EbN0_dB, esquema):
    # agrega ruido AWGN gaussiano con sigma^2 = N0/2 por dimension
    # Eb = 1 constante -> N0 = 1 / SNR_lineal
    N0 = 1.0 / (10 ** (EbN0_dB / 10))

    sigma = np.sqrt(N0 / 2)
    
    if esquema == 'QAM':
        # ruido complejo: componente real e imaginaria independientes N(0, N0/2)
        ruido = sigma * (np.random.randn(len(simbolos)) + 1j * np.random.randn(len(simbolos)))
    else:  # FSK: ruido real en cada una de las M dimensiones
        ruido = sigma * np.random.randn(*simbolos.shape)
    return simbolos + ruido

# 2) Elabore una función que genere una atenuación aleatoria del canal, con distribución uniforme entre 0,5
# y 0,9.


#Nota: el ejercicio 2 (atenuación aleatoria) no se implementa en este TP.


# 4) Desde el programa principal, grafique la constelación correspondiente a la modulación seleccionada una
# vez que se han aplicado los efectos del canal, indicando las regiones de decisión y el etiquetamiento de
# los símbolos.

#se re utiliza la funcion iii_graficar_constelacion()