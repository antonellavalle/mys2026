import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
 
#definimos el variables del rango del grafico
t_inicio = -2      
t_fin = 2           
paso = 0.001 
#definimos el rango
t = np.arange(t_inicio, t_fin, paso)
 
#definimos las variables de la exponencial -> A (amplitud), alpha (tasa de crecimiento/decaimiento), t0 (desplazamiento)
# estos son solo los valores INICIALES, porque los va a controlar el slider
 
A_inicial = 2        #Amplitud: escala el valor de la señal
alpha_inicial = 2    #Tasa: si alpha>0 crece, si alpha<0 decae
t0_inicial = 0        #Instante de referencia (desplaza la curva en el tiempo)
 
 
# convertimos el cálculo de x(t) en una FUNCIÓN, para poder llamarla
# de nuevo cada vez que se mueva un slider
def calcular_exponencial(t, A, alpha, t0):
    x = np.zeros(len(t))
    for i in range(len(t)):
        tiempo_actual = t[i]
        x[i] = A * np.exp(alpha * (tiempo_actual - t0))
    return x
 
 
# --- cálculo inicial ---
x = calcular_exponencial(t, A_inicial, alpha_inicial, t0_inicial)
 
 

# Gráfico

fig, ax = plt.subplots(figsize=(8, 5.5))
fig.patch.set_facecolor('#fff0f7')    # fondo de toda la ventana, rosa muy suave
ax.set_facecolor('#fffafc')           # fondo del área del gráfico, casi blanco rosado
plt.subplots_adjust(bottom=0.38)      # dejo espacio abajo para los 3 sliders
 
linea, = ax.plot(t, x, linewidth=2.5, color='#e91e8c')
 
# --- líneas de referencia ---
ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)
linea_t0 = ax.axvline(t0_inicial, color='#f7a8d0', linestyle='--', linewidth=1)  # marca t0
 
# --- textos y etiquetas ---
titulo = ax.set_title(
    f'Función exponencial:  x(t) = {A_inicial}·e^({alpha_inicial}(t − {t0_inicial}))',
    fontsize=13
)
ax.set_xlabel('t')
ax.set_ylabel('x(t)')
ax.set_ylim(-1, 20)      # rango fijo en Y
ax.set_xlim(t_inicio, t_fin)
ax.grid(True, alpha=0.3)
 
 

# Sliders + cajas de texto

ax_A = plt.axes([0.2, 0.22, 0.5, 0.03])
ax_alpha = plt.axes([0.2, 0.15, 0.5, 0.03])
ax_t0 = plt.axes([0.2, 0.08, 0.5, 0.03])
 
slider_A = Slider(ax_A, 'A', valmin=0, valmax=10, valinit=A_inicial, valstep=0.5, color='#e91e8c')
slider_alpha = Slider(ax_alpha, 'α', valmin=-5, valmax=5, valinit=alpha_inicial, valstep=0.1, color='#e91e8c')
slider_t0 = Slider(ax_t0, 't0', valmin=t_inicio, valmax=t_fin, valinit=t0_inicial, valstep=0.1, color='#e91e8c')
 
ax_texto_A = plt.axes([0.82, 0.22, 0.08, 0.04])
ax_texto_alpha = plt.axes([0.82, 0.15, 0.08, 0.04])
ax_texto_t0 = plt.axes([0.82, 0.08, 0.08, 0.04])
 
texto_A = TextBox(ax_texto_A, '', initial=str(A_inicial))
texto_alpha = TextBox(ax_texto_alpha, '', initial=str(alpha_inicial))
texto_t0 = TextBox(ax_texto_t0, '', initial=str(t0_inicial))
 
 

# Sincronización slider <-> texto

def actualizar_desde_slider(val):
    A_actual = slider_A.val
    alpha_actual = slider_alpha.val
    t0_actual = slider_t0.val
 
    nueva_x = calcular_exponencial(t, A_actual, alpha_actual, t0_actual)
 
    linea.set_ydata(nueva_x)
    linea_t0.set_xdata([t0_actual, t0_actual])
 
    titulo.set_text(f'Función exponencial:  x(t) = {A_actual}·e^({alpha_actual:.1f}(t − {t0_actual:.1f}))')
 
    texto_A.set_val(f'{A_actual:g}')
    texto_alpha.set_val(f'{alpha_actual:g}')
    texto_t0.set_val(f'{t0_actual:g}')
 
    fig.canvas.draw_idle()
 
 
def desde_texto_A(texto):
    try:
        valor = np.clip(float(texto), slider_A.valmin, slider_A.valmax)
        slider_A.set_val(valor)
    except ValueError:
        pass
 
 
def desde_texto_alpha(texto):
    try:
        valor = np.clip(float(texto), slider_alpha.valmin, slider_alpha.valmax)
        slider_alpha.set_val(valor)
    except ValueError:
        pass
 
 
def desde_texto_t0(texto):
    try:
        valor = np.clip(float(texto), slider_t0.valmin, slider_t0.valmax)
        slider_t0.set_val(valor)
    except ValueError:
        pass
 
 
slider_A.on_changed(actualizar_desde_slider)
slider_alpha.on_changed(actualizar_desde_slider)
slider_t0.on_changed(actualizar_desde_slider)
 
texto_A.on_submit(desde_texto_A)
texto_alpha.on_submit(desde_texto_alpha)
texto_t0.on_submit(desde_texto_t0)
 
 
plt.show()