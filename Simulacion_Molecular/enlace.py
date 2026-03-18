import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc,rcParams

rc('animation',html='jshtml')
rcParams['animation.embed_limit'] = 2**128

m = 1
L = 5 # lado
l = 1

posi = np.random.uniform(0,L,size=(2))
ang = np.random.choice(np.linspace(0,2*np.pi,100))

posj = posi+l*[np.cos(ang),np.sin(ang)]

vels = np.random.rand(2,2)-0.5

pos = np.array([posi,posj])

''' Propiedades periódicas a la frontera
'''

def pperiod(pos,L):
  cmx,cmy = 0.5*(pos[0][0]+pos[1][0]),0.5*(pos[0][1]+pos[1][1])
  #cm = pos.mean(axis=0)
  if cmx>L:
       pos[0][0]-=L
       pos[1][0]-=L
  elif cmx<0:
       pos[0][0]+=L
       pos[1][0]+=L

  if cmy>L:
       pos[0][1]-=L
       pos[1][1]-=L
  elif cmy<0:
       pos[0][1]+=L
       pos[1][1]+=L
  return pos


''' Representación de las partículas '''
def circulos(ax,pos,r):
       circ = plt.Circle((pos[0][0],pos[0][1]),r,color='coral',ec='k')
       ax.add_patch(circ)
       circ = plt.Circle((pos[1][0],pos[1][1]),r,color='indigo',ec='k')
       ax.add_patch(circ)

''' Cálculo de la fuerza'''

def fuerza_enlace(pos,l):
  k=10
  fuerza = np.zeros((2,2))
  vecr = pos[1]-pos[0]
  r = np.linalg.norm(vecr)
  unir = vecr/r
  f1 = k*(r-l)*unir
  f2 = -k*(r-l)*unir
  fuerza[0]=f1
  fuerza[1]=f2
  return fuerza

#################################
fig,ax = plt.subplots(figsize=(3,3))


npasos = 1000000

t = 0
dt = 0.00001 # muy pequeño
G = []
conteo = 0
R = 0.2
for i in range(npasos):
   t += dt # t = t + dt
   f = fuerza_enlace(pos,l) # Calcula la fuerza
   acel = f/m
   vels = vels + acel*dt # La velocidad no es constante
   pos = pos + vels*dt # Este paso es la integración numérica

   pperiod(pos,L)
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
    plt.plot([G[i][0][0],G[i][1][0]],[G[i][0][1],G[i][1][1]],c='gray',zorder=-1)
    circulos(ax,G[i],R)
    #plt.scatter(G[i][:,0],G[i][:,1],s=100,c=range(N),cmap='rainbow',ec='k')

anim = FuncAnimation(fig,pelicula,frames=range(len(G)))
#anim.save('enlace.gif')
anim.save('enlace.gif', writer='pillow', fps=50)
