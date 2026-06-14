

import numpy as np
import matplotlib.pyplot as plt 

def efectos_del_canal(simbolos,parametros):

    esquema = parametros["transmisor"]["esquema_modulacion"]
    EbN0_dB = parametros ["canal"]["atenuacion"]

    print("\n" + "="*60)
    print("🌪️ CANAL")
    print("="*60)

    simbolos_con_ruido = canal_awgn(simbolos, EbN0_dB, esquema)

    return simbolos_con_ruido



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