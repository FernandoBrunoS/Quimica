import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc,rcParams

rc('animation',html='jshtml')
rcParams['animation.embed_limit'] = 2**128

# Parámetros del sistema
m = 1
N = 5 # no de partículas
L = 20 # lado

pos = np.array([[9,9],[11,11],[9,11],[11,9],[10,10]])

vels = np.zeros((N,2))

q = np.array([-1,-1,-1,-1,1])

##################################
# Obtener un color para cada partícula
cmap = plt.get_cmap('Spectral',N)

################################

'''
Función para aplicar condiciones periódicas de frontera
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


def circulos(ax,pos,r):
   for i in range(N):
       circ = plt.Circle((pos[i][0],pos[i][1]),r,color=cmap(i),ec='k')
       ax.add_patch(circ)


'''
Fuerza eléctrica
'''

def fuerza_elec(pos, q, N):
    fuerza = np.zeros((N,2))
    for i in range(N):
       sumaf = np.zeros((2))
       for j in range(N):
          if i!=j:
             vecr = pos[i]-pos[j]
             r = np.linalg.norm(vecr)
             unir = vecr/r
             elec = (q[i]*q[j]/r**2)*unir
             sumaf += elec
       fuerza[i] = sumaf
    return fuerza


#################################
fig,ax = plt.subplots(figsize=(3,3))


npasos = 10000

t = 0
dt = 0.001 # muy pequeño
G = []
conteo = 0
r = 0.5

for i in range(npasos):
    f = fuerza_elec(pos,q,N)
    acel = f/m
    vels = vels + acel*dt
    pos = pos + vels*dt
    pperiod(pos,N,L)
    if i%(npasos/100)==0:
        G.append(pos)

G = np.array(G)



def pelicula(i):
    ax.clear()
    ax.set_aspect(1)
    ax.axis('off')
    plt.xlim(0,L) # ax.set_xlim(0,L)
    plt.ylim(0,L) # ax.set_ylim(0,L)
    circulos(ax,G[i],r=0.5)
    #plt.scatter(G[i][:,0],G[i][:,1],s=100,c=range(N),cmap='rainbow',ec='k')

anim = FuncAnimation(fig,pelicula,frames=range(len(G)))
anim.save('elec_5q.gif', writer='pillow', fps=50)
