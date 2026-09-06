import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider   # NUEVO: para los deslizadores
 
#definimos el variables del rango del grafico
t_inicio = -5      
t_fin = 5           
paso = 0.001 
#definimos el rango
t = np.arange(t_inicio, t_fin, paso)
 
#definimos las variables del escalon -> t0 (tiempo donde se evalua la función) y A (amplitud)
# ahora estos son solo los valores INICIALES, porque los va a controlar el slider
 
A_inicial = 2   #Ampitud: variable que valor salta la señal
t0_inicial = 3  #Instante de tiempo en el que ocurre el salto
 
 
# convertimos el cálculo de x(t) en una FUNCIÓN, para poder llamarla
# de nuevo cada vez que se mueva un slider
def calcular_escalon(t, A, t0):
    x = np.zeros(len(t))
    for i in range(len(t)):
        tiempo_actual = t[i]
        if tiempo_actual < t0:
            x[i] = 0
        else:
            x[i] = A
    return x
 
 
# --- cálculo inicial (con los valores iniciales de A y t0) ---
x = calcular_escalon(t, A_inicial, t0_inicial)
 
 

# Gráfico

fig, ax = plt.subplots(figsize=(8, 5.5))
fig.patch.set_facecolor('#fff0f7')    # fondo de toda la ventana, rosa muy suave
ax.set_facecolor('#fffafc')           # fondo del área del gráfico, casi blanco rosado
plt.subplots_adjust(bottom=0.32)   # NUEVO: dejo espacio abajo para los sliders
 
linea, = ax.plot(t, x, linewidth=2.5, color='#e91e8c')   # dibujo t (eje x) vs x (eje y) -- rosa/fucsia
# NOTA: guardo la curva en "linea" para poder actualizarla después
 
# --- líneas de referencia ---
ax.axhline(0, color='black', linewidth=0.8)     # eje horizontal (x(t)=0)
ax.axvline(0, color='black', linewidth=0.8)     # eje vertical (t=0)
linea_t0 = ax.axvline(t0_inicial, color='#f7a8d0', linestyle='--', linewidth=1)  # marca el salto
 
# --- puntos que marcan el salto ---
punto_lleno, = ax.plot(t0_inicial, A_inicial, 'o', color='#e91e8c', markersize=7)
punto_vacio, = ax.plot(t0_inicial, 0, 'o', color='white', markeredgecolor='#e91e8c', markersize=7)
 
# --- textos y etiquetas ---
titulo = ax.set_title(f'Función escalón:  x(t) = {A_inicial}·μ(t − {t0_inicial})', fontsize=13)
ax.set_xlabel('t')
ax.set_ylabel('x(t)')
ax.set_ylim(-0.5, 10.5)      # NUEVO: rango fijo en Y para que no "salte" al mover A
ax.set_xlim(t_inicio, t_fin)
ax.grid(True, alpha=0.3)
 
 

# Sliders

ax_A = plt.axes([0.2, 0.15, 0.6, 0.03])     # [izquierda, abajo, ancho, alto]
ax_t0 = plt.axes([0.2, 0.08, 0.6, 0.03])
 
slider_A = Slider(ax_A, 'A', valmin=0, valmax=10, valinit=A_inicial, valstep=0.5, color='#e91e8c')
slider_t0 = Slider(ax_t0, 't0', valmin=t_inicio, valmax=t_fin, valinit=t0_inicial, valstep=0.1, color='#e91e8c')
 
 

# Función que se ejecuta cada vez que se mueve un slider

def actualizar(val):
    A_actual = slider_A.val
    t0_actual = slider_t0.val
 
    nueva_x = calcular_escalon(t, A_actual, t0_actual)   # recalculo la señal completa
 
    linea.set_ydata(nueva_x)                  # actualizo la curva
    linea_t0.set_xdata([t0_actual, t0_actual]) # muevo la línea punteada del salto
    punto_lleno.set_data([t0_actual], [A_actual])  # muevo el punto lleno
    punto_vacio.set_data([t0_actual], [0])         # muevo el punto vacío
 
    titulo.set_text(f'Función escalón:  x(t) = {A_actual}·μ(t − {t0_actual:.1f})')
    fig.canvas.draw_idle()   # le aviso a matplotlib que redibuje
 
 
slider_A.on_changed(actualizar)
slider_t0.on_changed(actualizar)
 
 
plt.show()   # abre la ventana interactiva