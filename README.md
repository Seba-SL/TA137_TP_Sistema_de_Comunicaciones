
# TA137_TP_Sistema_de_Comunicaciones



<img width="641" height="391" alt="readme_diagrama" src="https://github.com/user-attachments/assets/538e9502-5360-4da7-ab93-b8c2e4d500df" />


<img width="536" height="222" alt="image" src="https://github.com/user-attachments/assets/dd7f91e2-1f68-4bb1-b1e2-ab80c04e5aac" />


#Algoritmo de Huffman
<img width="1327" height="862" alt="arbol_huffman" src="https://github.com/user-attachments/assets/5b9d6ba8-e0f0-44ff-a804-68630e0fdb3e" />



```bash
---- TP Grupo 3: Simulación y Análisis de un Sistema de Comunicaciones ----
===================================
 Configuración del sistema
===================================
¿Usar parámetros del Grupo 03? (s/n): s

=== PARÁMETROS GRUPO 03 ===
Fuente de información:

Archivo a transmitir:  archivos/enviados/texto_largo_quijote.txt

Codificación de fuente:

Aplicar Huffman = True

Codificación de canal:

Matriz generadora: G = [[1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0], [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1]]
k = 5
n = 15

Modulación:

Catiddad de simbolos: M = 16
Esquema de modulación = QAM
Codigo etiquetado: gray

Canal:

Ruido AWGN = True
Respuesta impulsiva = False
Eb/N0 = 6 dB

============================================================
📡 TRANSMISOR
============================================================

Entropia:
  4.3787

longitud minima :
  4.3787

longitud promedio :
  4.4158

Eficiencia:
  0.9915983513746094

Energia media :
  (22.405358, 5.60134)

============================================================
🌪️ CANAL:
============================================================

Ruido AWGN

Respuesta impulsiva

============================================================
📥 RECEPTOR
============================================================

Probabilidad de error de simbolo: 2.0293469475167702e-05

Probabilidad de error de bit: 5.0733684640711605e-06
```
