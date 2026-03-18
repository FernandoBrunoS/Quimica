import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc,rcParams

rc('animation',html='jshtml')
rcParams['animation.embed_limit'] = 2**128

m = 1
N = 10 # no de partículas
L = 20 # lado
pos = np.random.uniform(0,L,size=(N,2))
q = np.random.choice([-1,1],size=N)
vels = np.random.rand(N,2)-0.5

##################################
# Obtener un color para cada partícula
cmap = plt.get_cmap('Spectral',N)

################################1000
# Función que hace que reboten con las paredes

''' Propiedades periódicas a la frontera
'''

def pperiod(pos,N,L):
  for i in range(N):
     if pos[i][0]>L:
       pos[i][0]-=L
     elif pos[i][0]<0:
       pos[i][0]+=L

     if pos[i][1]>L:
       pos[i][1]-=L
     elif pos[i][1]<0:
       pos[i][1]+=L
  return pos


''' Representación de las partículas '''
def circulos(ax,pos,r):
   for i in range(N):
      if q[i]==1:
          circ = plt.Circle((pos[i][0],pos[i][1]),r,color='blue',ec='k')
          ax.add_patch(circ)
      else:
          circ = plt.Circle((pos[i][0],pos[i][1]),r,color='red',ec='k')
          ax.add_patch(circ)

''' Cálculo de la fuerza electrostatica'''

def fuerza_elec(pos,q,N):
    fuerza = np.zeros((N,2))
    for i in range(N):
       sumaf = np.zeros((2))
       for j in range(N):
          if i!=j:
             vecr = pos[i]-pos[j]
             r = np.linalg.norm(vecr)
             unir = vecr/r
             Coul = (q[i]*q[j]/r**2)*unir
             sumaf += Coul
       fuerza[i] = sumaf
    return fuerza

#################################
fig,ax = plt.subplots(figsize=(3,3))


npasos = 10000

t = 0
dt = 0.001 # muy pequeño
G = []
conteo = 0
R = 0.5
for i in range(npasos):
   t += dt # t = t + dt
   f = fuerza_elec(pos,q,N) # Calcula la fuerza
   acel = f/m
   vels = vels + acel*dt # La velocidad no es constante
   pos = pos + vels*dt # Este paso es la integración numérica

   pperiod(pos,N,L)
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
    circulos(ax,G[i],R)
    #plt.scatter(G[i][:,0],G[i][:,1],s=100,c=range(N),cmap='rainbow',ec='k')

anim = FuncAnimation(fig,pelicula,frames=range(len(G)))
anim.save('fuerza_elec.gif', writer='pillow', fps=50)
