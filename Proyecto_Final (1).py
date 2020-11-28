#!/usr/bin/env python
# coding: utf-8

# $$\textbf  {Estudiante: Jesús David Cárdenas Barreto}\\
#   \textbf {Simulación}\\
#   \textbf {Grupo 51}$$

# La forma de aplicarlo es creando un conjunto de propuestas como solución al problema, cada solución será un individuo de la población. 

# In[1]:


import numpy as np
from math import pi, pow
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle
import pandas
import openpyxl


# Primero se migrarán los datos de la BVC (Bolsa de Valores de Colombia)

# In[36]:


df = pandas.read_excel('datosInv.xlsx', sheet_name='Hoja1', header=None, skiprows=[0,3000])
df


# Se mostrará la cadena de datos para el historico del BVC

# De 8 opciones de inversión supongamos que el inversionista tomará la opción 0

# In[37]:


plt.plot(df[0])
print(df[0].size)


# In[4]:


portafolio1=df[0].tolist()


# In[38]:


portafolio1[3000]


# Una generación en un algoritmo genético es una población diferente, donde en cada generación se realiza una evaluación para determinar cuál es la solución que más se acerca a lo óptimo.

# Al crear una nueva generación los individuos sufren de mutación, que realmente es lo que aporta nuevas soluciones posibles al problema y a lo largo del tiempo se encontrará la mejor.

# In[39]:


modelo = [1,1,1,1,1,1,1,1,1,1] #Objetivo a alcanzar
#La longitud del material genetico de cada individuo
largo = 10
#La cantidad de individuos que habra en la poblacion
num = 3
#Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
pressure = 3 
 #La probabilidad de que un individuo mute
mutation_chance = 1

minimo = min(portafolio1)
maximo = max(portafolio1)
print("\n\nMinimo: %s\n"%(minimo))
print("\n\nMaximo: %s\n"%(maximo))
  
    
def individual(min, max):
     return[random.randint(minimo, maximo) for i in range(largo)]
  
def crearPoblacion():
    return [individual(1,9) for i in range(num)]
  
def calcularFitness(individual):
    fitness = 0
    for i in range(len(individual)):
        if individual[i] == modelo[i]:
            fitness += 1
  
    return fitness


# In[12]:


fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))


axes[0, 0].set_title("Valor BVC")
axes[0, 0].plot(individual(minimo, maximo) , color='blue')


axes[0, 1].set_title("Inversion 1")
axes[0, 1].plot(crearPoblacion()[0],'r')

axes[1, 0].set_title("Inversion 2")
axes[1, 0].plot(crearPoblacion()[1],'g')

axes[1, 1].set_title("Inversion 3")
axes[1, 1].plot(crearPoblacion()[2],'y')

#axes[0, 1].remove()  # don't display empty ax

 

fig.tight_layout()
plt.show()


# In[13]:



  
def selection_and_reproduction(population):
    #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (i , [1,2,1,1,4,1,8,9,4,1])
    puntuados = [ (calcularFitness(i), i) for i in population]
    #Ordena los pares ordenados y se queda solo con el array de valores
    puntuados = [i[1] for i in sorted(puntuados)] 
    population = puntuados
  
  
  #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
    selected =  puntuados[(len(puntuados)-pressure):] 
  
  
  
    #Se mezcla el material genetico para crear nuevos individuos
    for i in range(len(population)-pressure):
        #Se elige un punto para hacer el intercambio
        punto = random.randint(1,largo-1) 
        #Se eligen dos padres
        padre = random.sample(selected, 2) 
          
            #Se mezcla el material genetico de los padres en cada nuevo individuo
        population[i][:punto] = padre[0][:punto] 
        population[i][punto:] = padre[1][punto:]
  
 #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven
    return population 
  
def mutation(population):
    """
        Se mutan los individuos al azar. Sin la mutacion de nuevos genes nunca podria
        alcanzarse la solucion.
    """
    contador = 0
    for i in range(len(population)-pressure):
        if random.random() <= mutation_chance: #Cada individuo de la poblacion (menos los padres) tienen una probabilidad de mutar
            punto = random.randint(0,largo-1) #Se elgie un punto al azar
            nuevo_valor = random.randint(1,9) #y un nuevo valor para este punto
            #Es importante mirar que el nuevo valor no sea igual al viejo
            while nuevo_valor == population[i][punto]:
                nuevo_valor = random.randint(1,9)
  
            #Se aplica la mutacion
            population[i][punto] = nuevo_valor
            if nuevo_valor == population[i][punto]:
                contador = contador +1

  
    return population, contador
      
  
  
population = crearPoblacion()#Inicializar una poblacion
print("Poblacion Inicial:\n%s"%(population)) 
base=population
  
#Se evoluciona la poblacion
for i in range(100):
    population = selection_and_reproduction(population)
    population = mutation(population)[0]
  
print('arr\n', mutation(population)[1])
print("\nPoblacion Final:\n%s"%(population))
print("\n\n")
pivot=population

uno=base[0]
dos=base[1]
tres=base[2]

unoa=pivot[0]
dosa=pivot[1]
tresa=pivot[2]

valoresF = []
for i in range(10):
    x = uno[i]-unoa[i]
    y = dos[i]-dosa[i]
    z = tres[i]-tresa[i]
    valoresF.append(x)
    valoresF.append(y)
    valoresF.append(z)
Dp1=[]
for i in range(0,9):
    Dp1.append(valoresF[i])
print('Distancia entre valores para los protafolios: \n', Dp1)


# In[35]:



fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 10))


axes[0, 0].set_title("Portafolio 1")
axes[0, 0].plot(population[0] , color='blue')
axes[0, 0].plot(crearPoblacion()[0],'ro--')

axes[1, 0].remove()  # don't display empty ax
axes[1, 1].remove()  # don't display empty ax
axes[1, 2].remove()  # don't display empty ax

axes[2, 0].remove()  # don't display empty ax
axes[2, 1].remove()  # don't display empty ax
axes[2, 2].remove()  # don't display empty ax

axes[0, 1].set_title("Portafolio 2")
axes[0, 1].plot(population[1],color='green')
axes[0, 1].plot(crearPoblacion()[1],'ro--')

axes[0, 2].set_title("Portafolio 3")
axes[0, 2].plot(population[2],'y')
axes[0, 2].plot(crearPoblacion()[2],'ro--')



 

fig.tight_layout()
plt.show()

