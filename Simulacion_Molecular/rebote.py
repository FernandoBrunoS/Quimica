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
s=10
magv2 = magv**2

sumav2 = magv2.sum()

Tini = sumav2/(2*kb*N)

T = 298
#### Ajuste de Temperaturas
f = np.sqrt(T/Tini)  # factor de ajuste

nvels = f*vels # Velocidades ajustadas

##################################
# Obtener un color para cada partícula
cmap = plt.get_cmap('Spectral',N)

################################1000
# Función que hace que reboten con las paredes

'''
La función pared_r es la función pared consideran el radio
'''
def pared_r(pos,nvels,N,L,r):
   for i in range(N): # Para cada partícula
      if (pos[i][0]+r)>L: # si se pasa a la derecha
         pos[i][0] = 2*L-pos[i][0]
         nvels[i][0] *= -1
      # Si se pasa a la izquierda
      elif (pos[i][0]-r)<0:
         pos[i][0] *= -1
         nvels[i][0] *= -1

      if (pos[i][1]+r)>L: # si se pasa hacia arriba
         pos[i][1] = 2*L-pos[i][1]
         nvels[i][1] *= -1
      # Si se pasa para abajo
      elif (pos[i][1]-r)<0:
         pos[i][1] *= -1
         nvels[i][1] *= -1
   return pos,nvels

def circulos(ax,pos,r):
   for i in range(N):
       circ = plt.Circle((pos[i][0],pos[i][1]),r,color=cmap(i),ec='k')
       ax.add_patch(circ)

'''
Vamos a crear una función que identifique cuándo chocan las pelotas y
'''
def choque(pos,nvels,r,N):
    for i in range(N):
        for j in range(i+1,N):
           d = np.sqrt((pos[j][0]-pos[i][0])**2+(pos[j][1]-pos[i][1])**2)
           if d<=2*r:
              tempvix = nvels[i][0]
              tempviy = nvels[i][1]

              nvels[i][0]=nvels[j][0]
              nvels[i][1]=nvels[j][1]

              nvels[j][0]=tempvix
              nvels[j][1]=tempviy

              del tempvix
              del tempviy

    return nvels



#################################
fig,ax = plt.subplots(figsize=(3,3))


npasos = 10000

t = 0
dt = 0.1 # muy pequeño
G = []
conteo = 0
r = 0.5
for i in range(npasos):
   t += dt # t = t + dt
   pos = pos + nvels*dt # Este paso es la integración numérica
   choque(pos,nvels,r,N) # Para ver si chocan entrimport numpy as np
   pared_r(pos,nvels,N,L,r)
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
    circulos(ax,G[i],r=0.5)
    #plt.scatter(G[i][:,0],G[i][:,1],s=100,c=range(N),cmap='rainbow',ec='k')

anim = FuncAnimation(fig,pelicula,frames=range(len(G)))
anim.save('rebote.gif', writer='pillow', fps=50)
