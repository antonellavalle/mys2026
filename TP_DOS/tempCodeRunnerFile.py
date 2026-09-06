import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox

#definimos el variables del rango del grafico
t_inicio = -5      
t_fin = 5           
paso = 0.001 
#definimos el rango
t = np.arange(t_inicio, t_fin, paso)

#definimos las variables del pulso -> A (amplitud), t0 (instante de inicio), D (duración del pulso)
# estos son solo los valores INICIALES, porque los va a controlar el slider

A_inicial = 3      #Amplitud: altura del pulso
t0_inicial = -1     #Instante en que empieza el pulso
D_inicial = 2       #Duración del pulso (ancho): termina en t0 + D


# la función mu es el escalón unitario, la reutilizamos para construir el pulso
def mu(t, t0=0):
    return np.where(t >= t0, 1.0, 0.0)


# convertimos el cálculo de p(t) en una FUNCIÓN, para poder llamarla
# de nuevo cada vez que se mueva un slider
# p(t) = A . [ mu(t - t0)  -  mu(t - t0 - D) ]
def calcular_pulso(t, A, t0, D):
    p = np.zeros(len(t))
    for i in range(len(t)):
        tiempo_actual = t[i]
        p[i] = A * (mu(np.array([tiempo_actual]), t0)[0] - mu(np.array([tiempo_actual]), t0 + D)[0])
    return p


# --- cálculo inicial ---
p = calcular_pulso(t, A_inicial, t0_inicial, D_inicial)



# Gráfico

fig, ax = plt.subplots(figsize=(8, 5.5))
fig.patch.set_facecolor('#fff0f7')    # fondo de toda la ventana, rosa muy suave
ax.set_facecolor('#fffafc')           # fondo del área del gráfico, casi blanco rosado
plt.subplots_adjust(bottom=0.38)      # dejo espacio abajo para los 3 sliders

linea, = ax.plot(t, p, linewidth=2.5, color='#e91e8c')

ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)
linea_t0 = ax.axvline(t0_inicial, color='#f7a8d0', linestyle='--', linewidth=1)          # inicio del pulso
linea_fin = ax.axvline(t0_inicial + D_inicial, color='#f7a8d0', linestyle='--', linewidth=1)  # fin del pulso

# --- puntos que marcan los saltos ---
p_sube_lleno, = ax.plot(t0_inicial, A_inicial, 'o', color='#e91e8c', markersize=7)
p_sube_vacio, = ax.plot(t0_inicial, 0, 'o', color='white', markeredgecolor='#e91e8c', markersize=7)
p_baja_lleno, = ax.plot(t0_inicial + D_inicial, 0, 'o', color='#e91e8c', markersize=7)
p_baja_vacio, = ax.plot(t0_inicial + D_inicial, A_inicial, 'o', color='white', markeredgecolor='#e91e8c', markersize=7)

# --- textos y etiquetas ---
titulo = ax.set_title(
    f'Pulso:  p(t) = {A_inicial}·[μ(t − {t0_inicial}) − μ(t − {t0_inicial} − {D_inicial})]',
    fontsize=12
)
ax.set_xlabel('t')
ax.set_ylabel('p(t)')
ax.set_ylim(-0.5, 10.5)      # rango fijo en Y
ax.set_xlim(t_inicio, t_fin)
ax.grid(True, alpha=0.3)



# Sliders + cajas de texto

ax_A = plt.axes([0.2, 0.22, 0.5, 0.03])
ax_t0 = plt.axes([0.2, 0.15, 0.5, 0.03])
ax_D = plt.axes([0.2, 0.08, 0.5, 0.03])

slider_A = Slider(ax_A, 'A', valmin=0, valmax=10, valinit=A_inicial, valstep=0.5, color='#e91e8c')
slider_t0 = Slider(ax_t0, 't0', valmin=t_inicio, valmax=t_fin, valinit=t0_inicial, valstep=0.1, color='#e91e8c')
slider_D = Slider(ax_D, 'D', valmin=0.1, valmax=10, valinit=D_inicial, valstep=0.1, color='#e91e8c')

ax_texto_A = plt.axes([0.82, 0.22, 0.08, 0.04])
ax_texto_t0 = plt.axes([0.82, 0.15, 0.08, 0.04])
ax_texto_D = plt.axes([0.82, 0.08, 0.08, 0.04])

texto_A = TextBox(ax_texto_A, '', initial=str(A_inicial))
texto_t0 = TextBox(ax_texto_t0, '', initial=str(t0_inicial))
texto_D = TextBox(ax_texto_D, '', initial=str(D_inicial))



# Sincronización slider <-> texto
def actualizar_desde_slider(val):
    A_actual = slider_A.val
    t0_actual = slider_t0.val
    D_actual = slider_D.val

    nueva_p = calcular_pulso(t, A_actual, t0_actual, D_actual)

    linea.set_ydata(nueva_p)
    linea_t0.set_xdata([t0_actual, t0_actual])
    linea_fin.set_xdata([t0_actual + D_actual, t0_actual + D_actual])

    p_sube_lleno.set_data([t0_actual], [A_actual])
    p_sube_vacio.set_data([t0_actual], [0])
    p_baja_lleno.set_data([t0_actual + D_actual], [0])
    p_baja_vacio.set_data([t0_actual + D_actual], [A_actual])

    titulo.set_text(f'Pulso:  p(t) = {A_actual}·[μ(t − {t0_actual:.1f}) − μ(t − {t0_actual:.1f} − {D_actual:.1f})]')

    texto_A.set_val(f'{A_actual:g}')
    texto_t0.set_val(f'{t0_actual:g}')
    texto_D.set_val(f'{D_actual:g}')

    fig.canvas.draw_idle()


def desde_texto_A(texto):
    try:
        valor = np.clip(float(texto), slider_A.valmin, slider_A.valmax)
        slider_A.set_val(valor)
    except ValueError:
        pass


def desde_texto_t0(texto):
    try:
        valor = np.clip(float(texto), slider_t0.valmin, slider_t0.valmax)
        slider_t0.set_val(valor)
    except ValueError:
        pass


def desde_texto_D(texto):
    try:
        valor = np.clip(float(texto), slider_D.valmin, slider_D.valmax)
        slider_D.set_val(valor)
    except ValueError:
        pass


slider_A.on_changed(actualizar_desde_slider)
slider_t0.on_changed(actualizar_desde_slider)
slider_D.on_changed(actualizar_desde_slider)

texto_A.on_submit(desde_texto_A)
texto_t0.on_submit(desde_texto_t0)
texto_D.on_submit(desde_texto_D)


plt.show()