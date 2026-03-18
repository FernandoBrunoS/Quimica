import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc,rcParams

rc('animation',html='jshtml')
rcParams['animation.embed_limit'] = 2**128

kb=3.16E-6

N = 5 # no de partículas
L = 10 # lado

pos = np.random.uniform(0,L,size=(N,2))

vels = np.random.rand(N,2)-0.5

################################
# Cálculo de la Temperatura

magv = np.linalg.norm(vels,axis=1)

magv2 = magv**2

sumav2 = magv2.sum()

Tini = sumav2/(2*kb*N)

T = 298
#### Ajuste de Temperaturas
f = np.sqrt(T/Tini)  # factor de ajuste

nvels = f*vels # Velocidades ajustadas

################################
# Función que hace que reboten con las paredes

def pared(pos,nvels,N,L):
   for i in range(N): # Para cada partícula
      if pos[i][0]>L: # si se pasa a la derecha
         pos[i][0] = 2*L-pos[i][0]
         nvels[i][0] *= -1
      # Si se pasa a la izquierda
      elif pos[i][0]<0:
         pos[i][0] *= -1
         nvels[i][0] *= -1

      if pos[i][1]>L: # si se pasa hacia arriba
         pos[i][1] = 2*L-pos[i][1]
         nvels[i][1] *= -1
      # Si se pasa para abajo
      elif pos[i][1]<0:
         pos[i][1] *= -1
         nvels[i][1] *= -1
   return pos,nvels


#################################
fig,ax = plt.subplots(figsize=(3,3))

def circulos(ax,pos,r):
   for i in range(N):
       circ = plt.Circle((pos[i][0],pos[i][1]),r,color=cmap(i),ec='k')
       ax.add_patch(circ)


npasos = 10000

t = 0
dt = 0.1 # muy pequeño
G = []
conteo = 0
for i in range(npasos):
   t += dt # t = t + dt
   pos = pos + nvels*dt # Este paso es la integración numérica
   pared(pos,nvels,N,L)
   if i%(npasos/100)==0:
      G.append(pos)
   if i%(npasos/10)==0:
      conteo += 1
      print('>'*conteo+'-'*(10-conteo))

def pelicula(i):
    ax.clear()
    ax.set_aspect(1)
    ax.axis('off')
    plt.xlim(0,L) # ax.set_xlim(0,L)
    plt.ylim(0,L) # ax.set_ylim(0,L)
    plt.scatter(G[i][:,0],G[i][:,1],s=100,c=range(N),cmap='rainbow',ec='k')

anim = FuncAnimation(fig,pelicula,frames=range(len(G)))
anim.save('pared.gif', writer='pillow', fps=50)
