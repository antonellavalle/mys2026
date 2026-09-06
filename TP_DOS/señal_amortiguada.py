import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox

#definimos el variables del rango del grafico
t_inicio = 0      
t_fin = 5           
paso = 0.001 
#definimos el rango
t = np.arange(t_inicio, t_fin, paso)

#definimos las variables de la señal amortiguada -> A (amplitud), f0 (frecuencia), theta (fase), alpha (amortiguamiento)
# estos son solo los valores INICIALES, porque los va a controlar el slider

A_inicial = 5         #Amplitud: escala el valor de la señal
f0_inicial = 1          #Frecuencia en Hz
theta_inicial = 0       #Fase inicial, en radianes
alpha_inicial = -1      #Tasa de amortiguamiento: si alpha<0 decae, si alpha>0 crece


# convertimos el cálculo de x(t) en una FUNCIÓN, para poder llamarla
# de nuevo cada vez que se mueva un slider
def calcular_amortiguada(t, A, f0, theta, alpha):
    x = np.zeros(len(t))
    for i in range(len(t)):
        tiempo_actual = t[i]
        x[i] = A * np.sin(2 * np.pi * f0 * tiempo_actual + theta) * np.exp(alpha * tiempo_actual)
    return x


# --- cálculo inicial ---
x = calcular_amortiguada(t, A_inicial, f0_inicial, theta_inicial, alpha_inicial)



# Gráfico

fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor('#fff0f7')    # fondo de toda la ventana, rosa muy suave
ax.set_facecolor('#fffafc')           # fondo del área del gráfico, casi blanco rosado
plt.subplots_adjust(bottom=0.45)      # dejo espacio abajo para los 4 sliders

linea, = ax.plot(t, x, linewidth=2.5, color='#e91e8c')

# --- envolventes +A.e^(alpha.t) y -A.e^(alpha.t) (marcan los "límites" de la oscilación) ---
env_sup, = ax.plot(t, A_inicial * np.exp(alpha_inicial * t), '--', color='#f7a8d0', linewidth=1)
env_inf, = ax.plot(t, -A_inicial * np.exp(alpha_inicial * t), '--', color='#f7a8d0', linewidth=1)

ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)

# --- textos y etiquetas ---
titulo = ax.set_title(
    f'Señal amortiguada:  x(t) = {A_inicial}·sen(2π·{f0_inicial}·t + {theta_inicial})·e^({alpha_inicial}t)',
    fontsize=12
)
ax.set_xlabel('t')
ax.set_ylabel('x(t)')
ax.set_ylim(-10.5, 10.5)      # rango fijo en Y
ax.set_xlim(t_inicio, t_fin)
ax.grid(True, alpha=0.3)



# Sliders + cajas de texto

ax_A = plt.axes([0.2, 0.30, 0.5, 0.03])
ax_f0 = plt.axes([0.2, 0.23, 0.5, 0.03])
ax_theta = plt.axes([0.2, 0.16, 0.5, 0.03])
ax_alpha = plt.axes([0.2, 0.09, 0.5, 0.03])

slider_A = Slider(ax_A, 'A', valmin=0, valmax=10, valinit=A_inicial, valstep=0.5, color='#e91e8c')
slider_f0 = Slider(ax_f0, 'f0', valmin=0.1, valmax=10, valinit=f0_inicial, valstep=0.1, color='#e91e8c')
slider_theta = Slider(ax_theta, 'θ', valmin=-np.pi, valmax=np.pi, valinit=theta_inicial, valstep=0.1, color='#e91e8c')
slider_alpha = Slider(ax_alpha, 'α', valmin=-5, valmax=5, valinit=alpha_inicial, valstep=0.1, color='#e91e8c')

ax_texto_A = plt.axes([0.82, 0.30, 0.08, 0.04])
ax_texto_f0 = plt.axes([0.82, 0.23, 0.08, 0.04])
ax_texto_theta = plt.axes([0.82, 0.16, 0.08, 0.04])
ax_texto_alpha = plt.axes([0.82, 0.09, 0.08, 0.04])

texto_A = TextBox(ax_texto_A, '', initial=str(A_inicial))
texto_f0 = TextBox(ax_texto_f0, '', initial=str(f0_inicial))
texto_theta = TextBox(ax_texto_theta, '', initial=str(theta_inicial))
texto_alpha = TextBox(ax_texto_alpha, '', initial=str(alpha_inicial))



# Sincronización slider <-> texto

def actualizar_desde_slider(val):
    A_actual = slider_A.val
    f0_actual = slider_f0.val
    theta_actual = slider_theta.val
    alpha_actual = slider_alpha.val

    nueva_x = calcular_amortiguada(t, A_actual, f0_actual, theta_actual, alpha_actual)

    linea.set_ydata(nueva_x)
    env_sup.set_ydata(A_actual * np.exp(alpha_actual * t))
    env_inf.set_ydata(-A_actual * np.exp(alpha_actual * t))

    titulo.set_text(
        f'Señal amortiguada:  x(t) = {A_actual}·sen(2π·{f0_actual:.1f}·t + {theta_actual:.2f})·e^({alpha_actual:.1f}t)'
    )

    texto_A.set_val(f'{A_actual:g}')
    texto_f0.set_val(f'{f0_actual:g}')
    texto_theta.set_val(f'{theta_actual:g}')
    texto_alpha.set_val(f'{alpha_actual:g}')

    fig.canvas.draw_idle()


def desde_texto_A(texto):
    try:
        valor = np.clip(float(texto), slider_A.valmin, slider_A.valmax)
        slider_A.set_val(valor)
    except ValueError:
        pass


def desde_texto_f0(texto):
    try:
        valor = np.clip(float(texto), slider_f0.valmin, slider_f0.valmax)
        slider_f0.set_val(valor)
    except ValueError:
        pass


def desde_texto_theta(texto):
    try:
        valor = np.clip(float(texto), slider_theta.valmin, slider_theta.valmax)
        slider_theta.set_val(valor)
    except ValueError:
        pass


def desde_texto_alpha(texto):
    try:
        valor = np.clip(float(texto), slider_alpha.valmin, slider_alpha.valmax)
        slider_alpha.set_val(valor)
    except ValueError:
        pass


slider_A.on_changed(actualizar_desde_slider)
slider_f0.on_changed(actualizar_desde_slider)
slider_theta.on_changed(actualizar_desde_slider)
slider_alpha.on_changed(actualizar_desde_slider)

texto_A.on_submit(desde_texto_A)
texto_f0.on_submit(desde_texto_f0)
texto_theta.on_submit(desde_texto_theta)
texto_alpha.on_submit(desde_texto_alpha)


plt.show()