import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc, rcParams

rc('animation', html='jshtml')
rcParams['animation.embed_limit'] = 2**128

# Parámetros físicos y geométricos del CO2
m = 1
L = 8 # Lado de la caja
l = 1.16 # Longitud de enlace C=O
l2 = 2.32 # Distancia O-O para molécula lineal (1.16 * 2)

# Posicionamiento inicial
posC = np.random.uniform(0, L, size=(2)) # Átomo central (Carbono)
ang0 = np.radians(180) # Geometría lineal del CO2
ang_orientacion = np.random.choice(np.linspace(0, 2*np.pi, 100)) # Orientación aleatoria

# Posiciones de los Oxígenos basándose en el Carbono central
posO1 = posC + [l * np.cos(ang_orientacion), l * np.sin(ang_orientacion)]
posO2 = posC + [l * np.cos(ang_orientacion + ang0), l * np.sin(ang_orientacion + ang0)]

pos = np.array([posC, posO1, posO2]) # Orden: C, O1, O2
vels = np.random.rand(3, 2) - 0.5 # Velocidades iniciales

def pperiod(pos, L):
    """ Propiedades periódicas basadas en el centro de masa """
    # Masas aproximadas: C=12, O=16. Aquí se usa una aproximación de pesos
    cmx = (12 * pos[0][0] + 16 * pos[1][0] + 16 * pos[2][0]) / 44
    cmy = (12 * pos[0][1] + 16 * pos[1][1] + 16 * pos[2][1]) / 44

    if cmx > L: pos[:, 0] -= L
    elif cmx < 0: pos[:, 0] += L
    if cmy > L: pos[:, 1] -= L
    elif cmy < 0: pos[:, 1] += L
    return pos

def circulos(ax, pos, r):
    """ Representación: C (negro) y O (rojo) """
    # Carbono central
    circC = plt.Circle((pos[0][0], pos[0][1]), r, color='black', ec='k')
    ax.add_patch(circC)
    # Oxígenos
    circO1 = plt.Circle((pos[1][0], pos[1][1]), r * 0.9, color='red', ec='k')
    circO2 = plt.Circle((pos[2][0], pos[2][1]), r * 0.9, color='red', ec='k')
    ax.add_patch(circO1)
    ax.add_patch(circO2)

def fuerza_enlace(pos, l, l2):
    """ Cálculo de fuerzas armónicas """
    k = 10 # Constante de fuerza
    fuerza = np.zeros((3, 2))

    # Enlaces C-O1 y C-O2
    for i in [1, 2]:
        vecr = pos[i] - pos[0]
        r = np.linalg.norm(vecr)
        unir = vecr / r
        f_mag = k * (r - l) * unir
        fuerza[0] += f_mag
        fuerza[i] -= f_mag

    # Restricción angular (distancia O1-O2) para mantener linealidad
    vecr_oo = pos[2] - pos[1]
    r_oo = np.linalg.norm(vecr_oo)
    unir_oo = vecr_oo / r_oo
    f_oo = k * (r_oo - l2) * unir_oo
    fuerza[1] += f_oo
    fuerza[2] -= f_oo

    return fuerza

def espiral(ax, x1, y1, x2, y2, R):
    theta = np.linspace(0, 16 * np.pi, 100)
    dx = np.linspace(x1, x2, 100)
    dy = np.linspace(y1, y2, 100)
    X = 0.5 * R * np.cos(theta) + dx
    Y = 0.5 * R * np.sin(theta) + dy
    ax.plot(X, Y, c='k', zorder=-1, lw=1)

# Simulación
fig, ax = plt.subplots(figsize=(3, 3))
npasos = 1000000
dt = 0.00001
G = []
R = 0.2

for i in range(npasos):
    f = fuerza_enlace(pos, l, l2)
    acel = f / m
    vels += acel * dt
    pos += vels * dt
    pperiod(pos, L)
    if i % (npasos / 100) == 0:
        G.append(pos.copy())

def pelicula(i):
    ax.clear()
    ax.set_aspect(1)
    ax.axis('off')
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    # Dibujar resortes entre C-O1 y C-O2
    espiral(ax, G[i][0][0], G[i][0][1], G[i][1][0], G[i][1][1], R)
    espiral(ax, G[i][0][0], G[i][0][1], G[i][2][0], G[i][2][1], R)
    circulos(ax, G[i], R)

anim = FuncAnimation(fig, pelicula, frames=range(len(G)))
anim.save('enlace_CO2.gif', writer='pillow', fps=50)
