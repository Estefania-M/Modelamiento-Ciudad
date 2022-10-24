# Archivo basado en auxiliares, material de apoyo y del repositorio del curso.
# Contiene todas las luces a mostar en escena, la escena (casas, piso, auto, GPS, sol, luna)
# además las funciones de la trayectoria del auto.
import random
from OpenGL.GL import *
import numpy as np
import sys
import os.path
import libs.transformations as tr
import libs.basic_shapes as bs
import libs.easy_shaders as es
import libs.scene_graph as sg
from libs.assets_path import getAssetPath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


#####################################################################################################
########################## FUNCIONES PARA CREAR LAS LUCES DE LA ESCENA ##############################
#####################################################################################################

# Se crea la clase que contiene los parámetros de la luz a crear.
class Spotlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])
        self.direction = np.array([0,0,0])
        self.cutOff = 0
        self.outerCutOff = 0

# Se crea el pool de luces spotlight (como un diccionario)
spotlightsPool = dict()

# En esta función se crean las luces a mostrar en la escena.
def setLights():
    # Luz de la Luna
    spot1 = Spotlight()
    # añadimos aquí los parametros de luz ambiente por ser una luz general, no añadiremos ninguna point_light
    spot1.ambient = np.array([0.3, 0.3, 0.3])
    spot1.diffuse = np.array([1.0, 1.0, 1.0])
    spot1.specular = np.array([1.0, 1.0, 1.0])
    spot1.constant = 1.0
    spot1.linear = 0.02
    spot1.quadratic = 0.00
    spot1.position = np.array([-1.25, 50, 6.25]) # está ubicada en esta posición
    spot1.direction = np.array([0, -1, 0]) # está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    spot1.cutOff = np.cos(np.radians(180)) # corte del ángulo para la luz
    spot1.outerCutOff = np.cos(np.radians(180)) # no queremos que se difumine la luz, por lo que tiene el mismo angulo que cutoff
    spotlightsPool['spot1'] = spot1 # almacenamos la luz en el diccionario, con una clave única

    # Luz del Sol
    spot2 = Spotlight()
    # añadimos aquí los parametros de luz ambiente por ser una luz general, no añadiremos ninguna point_light
    spot2.ambient = np.array([0.7, 0.7, 0.7])
    spot2.diffuse = np.array([1.0, 1.0, 1.0])
    spot2.specular = np.array([0.2, 0.2, 0.2])
    spot2.constant = 1.0
    spot2.linear = 0.009
    spot2.quadratic = 0.00
    spot2.position = np.array([-1.25, -50, 6.25]) 
    spot2.direction = np.array([0, 1, 0]) 
    spot2.cutOff = np.cos(np.radians(180))
    spot2.outerCutOff = np.cos(np.radians(180)) 
    spotlightsPool['spot2'] = spot2 

    # Luces de los 9 Postes 
    # (los parametros de estas luces son iguales, solo cambia su posición)
    spot3 = Spotlight()
    # Aquí no añadimos los parametros de luz ambiente por ser una luz focalizada en el ángulo de corte, 
    # no queremos más luz que esa.
    spot3.ambient = np.array([0.0, 0.0, 0.0])
    spot3.diffuse = np.array([1.0, 1.0, 1.0])
    spot3.specular = np.array([1.0, 1.0, 1.0])
    spot3.constant = 1.0
    spot3.linear = 0.009
    spot3.quadratic = 0.00
    spot3.position = np.array([13.3, 1.8, -5]) 
    spot3.direction = np.array([0, -1, 0]) 
    spot3.cutOff = np.cos(np.radians(45))
    spot3.outerCutOff = np.cos(np.radians(60)) 
    spotlightsPool['spot3'] = spot3

    spot4 = Spotlight()
    spot4.ambient = np.array([0.0, 0.0, 0.0])
    spot4.diffuse = np.array([1.0, 1.0, 1.0])
    spot4.specular = np.array([1.0, 1.0, 1.0])
    spot4.constant = 1.0
    spot4.linear = 0.009
    spot4.quadratic = 0.00
    spot4.position = np.array([7.3, 1.8, 12.4]) 
    spot4.direction = np.array([0, -1, 0]) 
    spot4.cutOff = np.cos(np.radians(45))
    spot4.outerCutOff = np.cos(np.radians(60)) 
    spotlightsPool['spot4'] = spot4

    spot5 = Spotlight()
    spot5.ambient = np.array([0.0, 0.0, 0.0])
    spot5.diffuse = np.array([1.0, 1.0, 1.0])
    spot5.specular = np.array([1.0, 1.0, 1.0])
    spot5.constant = 1.0
    spot5.linear = 0.009
    spot5.quadratic = 0.00
    spot5.position = np.array([6.2, 1.8, 0]) 
    spot5.direction = np.array([0, -1, 0]) 
    spot5.cutOff = np.cos(np.radians(45))
    spot5.outerCutOff = np.cos(np.radians(60)) 
    spotlightsPool['spot5'] = spot5

    spot6 = Spotlight()
    spot6.ambient = np.array([0.0, 0.0, 0.0])
    spot6.diffuse = np.array([1.0, 1.0, 1.0])
    spot6.specular = np.array([1.0, 1.0, 1.0])
    spot6.constant = 1.0
    spot6.linear = 0.009
    spot6.quadratic = 0.00
    spot6.position = np.array([2.3, 1.8, 19]) 
    spot6.direction = np.array([0, -1, 0]) 
    spot6.cutOff = np.cos(np.radians(45))
    spot6.outerCutOff = np.cos(np.radians(60)) 
    spotlightsPool['spot6'] = spot6

    spot7 = Spotlight()
    spot7.ambient = np.array([0.0, 0.0, 0.0])
    spot7.diffuse = np.array([1.0, 1.0, 1.0])
    spot7.specular = np.array([1.0, 1.0, 1.0])
    spot7.constant = 1.0
    spot7.linear = 0.009
    spot7.quadratic = 0.00
    spot7.position = np.array([-1.25, 1.8, -9.8]) 
    spot7.direction = np.array([0, -1, 0]) 
    spot7.cutOff = np.cos(np.radians(45))
    spot7.outerCutOff = np.cos(np.radians(60)) 
    spotlightsPool['spot7'] = spot7

    spot8 = Spotlight()
    spot8.ambient = np.array([0.0, 0.0, 0.0])
    spot8.diffuse = np.array([1.0, 1.0, 1.0])
    spot8.specular = np.array([1.0, 1.0, 1.0])
    spot8.constant = 1.0
    spot8.linear = 0.009
    spot8.quadratic = 0.00
    spot8.position = np.array([-4.8, 1.8, 0]) 
    spot8.direction = np.array([0, -1, 0]) 
    spot8.cutOff = np.cos(np.radians(45))
    spot8.outerCutOff = np.cos(np.radians(60)) 
    spotlightsPool['spot8'] = spot8

    spot9 = Spotlight()
    spot9.ambient = np.array([0.0, 0.0, 0.0])
    spot9.diffuse = np.array([1.0, 1.0, 1.0])
    spot9.specular = np.array([1.0, 1.0, 1.0])
    spot9.constant = 1.0
    spot9.linear = 0.009
    spot9.quadratic = 0.00
    spot9.position = np.array([-8.7, 1.8, 19]) 
    spot9.direction = np.array([0, -1, 0]) 
    spot9.cutOff = np.cos(np.radians(45))
    spot9.outerCutOff = np.cos(np.radians(60)) 
    spotlightsPool['spot9'] = spot9

    spot10 = Spotlight()
    spot10.ambient = np.array([0.0, 0.0, 0.0])
    spot10.diffuse = np.array([1.0, 1.0, 1.0])
    spot10.specular = np.array([1.0, 1.0, 1.0])
    spot10.constant = 1.0
    spot10.linear = 0.009
    spot10.quadratic = 0.00
    spot10.position = np.array([-15.8, 1.8, 13]) 
    spot10.direction = np.array([0, -1, 0]) 
    spot10.cutOff = np.cos(np.radians(45))
    spot10.outerCutOff = np.cos(np.radians(60)) 
    spotlightsPool['spot10'] = spot10

    spot11 = Spotlight()
    spot11.ambient = np.array([0.0, 0.0, 0.0])
    spot11.diffuse = np.array([1.0, 1.0, 1.0])
    spot11.specular = np.array([1.0, 1.0, 1.0])
    spot11.constant = 1.0
    spot11.linear = 0.009
    spot11.quadratic = 0.00
    spot11.position = np.array([-15.8, 1.8, -6]) 
    spot11.direction = np.array([0, -1, 0]) 
    spot11.cutOff = np.cos(np.radians(45))
    spot11.outerCutOff = np.cos(np.radians(60)) 
    spotlightsPool['spot11'] = spot11

    # A CONTINUACIÓN SE CREARÁN SOLO LUCES PARA EL AUTO
    # 2 Luces delanteras que iluminan el camino del auto.
    spot12 = Spotlight()
    spot12.ambient = np.array([0, 0, 0])
    spot12.diffuse = np.array([1.0, 1.0, 1.0])
    spot12.specular = np.array([1.0, 1.0, 1.0])
    spot12.constant = 1.0
    spot12.linear = 0.0
    spot12.quadratic = 0.0
    spot12.position = np.array([-0.25, 0.2, 1]) 
    spot12.direction = np.array([0, -2, 3]) 
    spot12.cutOff = np.cos(np.radians(35)) 
    spot12.outerCutOff = np.cos(np.radians(45)) 
    spotlightsPool['spot12'] = spot12 

    spot13 = Spotlight()
    spot13.ambient = np.array([0, 0, 0])
    spot13.diffuse = np.array([1.0, 1.0, 1.0])
    spot13.specular = np.array([1.0, 1.0, 1.0])
    spot13.constant = 1.0
    spot13.linear = 0.0
    spot13.quadratic = 0.0
    spot13.position = np.array([0.25, 0.2, 1])
    spot13.direction = np.array([0, -2, 3])
    spot13.cutOff = np.cos(np.radians(35))
    spot13.outerCutOff = np.cos(np.radians(45)) 
    spotlightsPool['spot13'] = spot13

    # 2 Luces Rojas Traseras del Auto, que indican cuando llega a una curva ("frena")
    spot14 = Spotlight()
    spot14.ambient = np.array([0, 0, 0])
    spot14.diffuse = np.array([1.0, 0.0, 0.0])
    spot14.specular = np.array([1.0, 1.0, 1.0])
    spot14.constant = 1.0
    spot14.linear = 0.0
    spot14.quadratic = 0.0
    spot14.position = np.array([0.265, 0.335, -1.8])
    spot14.direction = np.array([0, 0, 1])
    spot14.cutOff = np.cos(np.radians(1.5))
    spot14.outerCutOff = np.cos(np.radians(2)) 
    spotlightsPool['spot14'] = spot14

    spot15 = Spotlight()
    spot15.ambient = np.array([0, 0, 0])
    spot15.diffuse = np.array([1.0, 0.0, 0.0])
    spot15.specular = np.array([1.0, 1.0, 1.0])
    spot15.constant = 1.0
    spot15.linear = 0.0
    spot15.quadratic = 0.0
    spot15.position = np.array([-0.265, 0.335, -1.8])
    spot15.direction = np.array([0, 0, 1])
    spot15.cutOff = np.cos(np.radians(1.5))
    spot15.outerCutOff = np.cos(np.radians(2)) 
    spotlightsPool['spot15'] = spot15

    # 2 Luces Direccionales (amarillas) Traseras, que indican hacia donde doblará.
    spot16 = Spotlight()
    spot16.ambient = np.array([0, 0, 0])
    spot16.diffuse = np.array([1.0, 1.0, 0.0])
    spot16.specular = np.array([1.0, 1.0, 1.0])
    spot16.constant = 1.0
    spot16.linear = 0.0
    spot16.quadratic = 0.0
    spot16.position = np.array([0.278, 0.335, -1.6])
    spot16.direction = np.array([0, 0, 1])
    spot16.cutOff = np.cos(np.radians(1.5))
    spot16.outerCutOff = np.cos(np.radians(2)) 
    spotlightsPool['spot16'] = spot16

    spot17 = Spotlight()
    spot17.ambient = np.array([0, 0, 0])
    spot17.diffuse = np.array([1.0, 1.0, 0.0])
    spot17.specular = np.array([1.0, 1.0, 1.0])
    spot17.constant = 1.0
    spot17.linear = 0.0
    spot17.quadratic = 0.0
    spot17.position = np.array([-0.278, 0.335, -1.6])
    spot17.direction = np.array([0, 0, 1])
    spot17.cutOff = np.cos(np.radians(1.5))
    spot17.outerCutOff = np.cos(np.radians(2)) 
    spotlightsPool['spot17'] = spot17

    # 2 Luces Delanteras del Auto, hace la ilusión de que se prenden los focos delanteros.
    spot18 = Spotlight()
    spot18.ambient = np.array([0, 0, 0])
    spot18.diffuse = np.array([1.0, 1.0, 1.0])
    spot18.specular = np.array([1.0, 1.0, 1.0])
    spot18.constant = 1.0
    spot18.linear = 0.0
    spot18.quadratic = 0.0
    spot18.position = np.array([0.14, 0.29, 2])
    spot18.direction = np.array([0.1, 0, -1])
    spot18.cutOff = np.cos(np.radians(2))
    spot18.outerCutOff = np.cos(np.radians(3)) 
    spotlightsPool['spot18'] = spot18

    spot19 = Spotlight()
    spot19.ambient = np.array([0, 0, 0])
    spot19.diffuse = np.array([1.0, 1.0, 1.0])
    spot19.specular = np.array([1.0, 1.0, 1.0])
    spot19.constant = 1.0
    spot19.linear = 0.0
    spot19.quadratic = 0.0
    spot19.position = np.array([-0.14, 0.29, 2])
    spot19.direction = np.array([-0.1, 0, -1])
    spot19.cutOff = np.cos(np.radians(2))
    spot19.outerCutOff = np.cos(np.radians(3)) 
    spotlightsPool['spot19'] = spot19

    # 2 Luces Direccionales (amarillas) Delanteras, indica hacia donde doblará el auto
    spot20 = Spotlight()
    spot20.ambient = np.array([0, 0, 0])
    spot20.diffuse = np.array([1.0, 1.0, 0.0])
    spot20.specular = np.array([1.0, 1.0, 1.0])
    spot20.constant = 1.0
    spot20.linear = 0.0
    spot20.quadratic = 0.0
    spot20.position = np.array([0.22, 0.27, 1.5])
    spot20.direction = np.array([0, 0, -1])
    spot20.cutOff = np.cos(np.radians(2))
    spot20.outerCutOff = np.cos(np.radians(3)) 
    spotlightsPool['spot20'] = spot20

    spot21 = Spotlight()
    spot21.ambient = np.array([0, 0, 0])
    spot21.diffuse = np.array([1.0, 1.0, 0.0])
    spot21.specular = np.array([1.0, 1.0, 1.0])
    spot21.constant = 1.0
    spot21.linear = 0.0
    spot21.quadratic = 0.0
    spot21.position = np.array([-0.22, 0.27, 1.5])
    spot21.direction = np.array([0, 0, -1])
    spot21.cutOff = np.cos(np.radians(2))
    spot21.outerCutOff = np.cos(np.radians(3)) 
    spotlightsPool['spot21'] = spot21


#####################################################################################################
############## FUNCIONES PARA CREAR LA ESCENA 3D (SE MANTIENE IGUAL A LA PARTE 1) ###################
#####################################################################################################

# Se crea una función auxiliar que crea el shape de los objetos en la memoria GPU con su respectivo pipeline.
def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

# Función que crea el grafo de los nodos de un prisma, recibe el pipeline, el nombre de la textura a utilizar
# el largo, alto y ancho de este.
def createPrisma(pipeline,nombre,largo,alto,ancho,luz):
    piso = sg.SceneGraphNode('Piso')
    shapePiso = bs.createPrismas(largo,alto,ancho,luz)
    gpuPiso = createGPUShape(pipeline, shapePiso)
    gpuPiso.texture = es.textureSimpleSetup(getAssetPath(nombre), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    piso.childs += [gpuPiso]
    return piso

# Función que crea el grafo de los nodos de las puertas de las casas, recibe el pipeline, el nombre de la textura a utilizar.
def createPuertaModel1(pipeline,nombre):
    puerta = sg.SceneGraphNode('Puerta')
    shapePuerta = bs.createPuerta1()
    gpuPuerta = createGPUShape(pipeline, shapePuerta)
    gpuPuerta.texture = es.textureSimpleSetup(getAssetPath(nombre), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    puerta.childs += [gpuPuerta]
    return puerta

# Función que crea el grafo de los nodos de las ventanas de las casas, recibe el pipeline, el nombre de la textura a utilizar
# el alto y ancho de esta.
def createVentanaModel1(pipeline,nombre,ancho,alto):
    ventana = sg.SceneGraphNode('Ventana')
    shapeVentana = bs.createVentana1(alto,ancho)
    gpuVentana = createGPUShape(pipeline, shapeVentana)
    gpuVentana.texture = es.textureSimpleSetup(getAssetPath(nombre), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    ventana.childs += [gpuVentana]
    return ventana

# Función que crea el grafo de los nodos de los techos de las casas, recibe el pipeline, el nombre de la textura a utilizar
# la inclinacion y largo del techo.
def createTecho(pipeline,nombre,inclinacion,largo,ancho):
    techo = sg.SceneGraphNode('Techo')
    shapeTecho = bs.createModelTecho(inclinacion,largo,ancho)
    gpuTecho = createGPUShape(pipeline, shapeTecho)
    gpuTecho.texture = es.textureSimpleSetup(getAssetPath(nombre), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    techo.childs += [gpuTecho]
    return techo

# Función que crea el grafo del primer modelo de casa, utiliza los nodos previamente definidos, 
# y recibe solo el pipeline.
def createCasa1(pipeline):
    # Definimos el nodo escena
    casa1 = sg.SceneGraphNode('Modelo Casa 1')

    modelPiso = createPrisma(pipeline,"cesped.jpg",2.5,0.1,2.5,"N")
    piso = sg.SceneGraphNode('Piso 1')
    piso.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0, -0.11, 0)])
    piso.childs += [modelPiso]
    casa1.childs += [piso]

    # Puertas
    modelDoor1 = createPuertaModel1(pipeline,"puerta1.webp")
    puerta1 = sg.SceneGraphNode('Puerta 1')
    puerta1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(1.5, 0.4, 0)])
    puerta1.childs += [modelDoor1]
    casa1.childs += [puerta1]

    modelDoor2 = createPuertaModel1(pipeline,"puerta1.webp")
    puerta2 = sg.SceneGraphNode('Puerta 1')
    puerta2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(-0.5, 0.4, 1),tr.rotationY(-np.pi/2)])
    puerta2.childs += [modelDoor2]
    casa1.childs += [puerta2]

    # Ventanas
    modelWindow1 = createVentanaModel1(pipeline,"ventana1.png",0.2,0.3)
    for i in range(2):
        ventana1 = sg.SceneGraphNode('Ventana '+str(i))
        ventana1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(1.5, 1.5, 0.2-0.4*i)])
        ventana1.childs += [modelWindow1]
        casa1.childs += [ventana1]

    ventana3 = sg.SceneGraphNode('Ventana 3')
    ventana3.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.6, 0.5, 1),tr.rotationY(-np.pi/2)])
    ventana3.childs += [modelWindow1]
    casa1.childs += [ventana3]

    for i in range(3):
        ventana4 = sg.SceneGraphNode('Ventana '+str(i+3))
        ventana4.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.4-0.4*i, 0.5, -1),tr.rotationY(np.pi/2)])
        ventana4.childs += [modelWindow1]
        casa1.childs += [ventana4]

    # Piso 1 y 2
    shape1 = bs.createModelPiso1("l1")
    gpu1 = createGPUShape(pipeline, shape1)
    gpu1.texture = es.textureSimpleSetup(getAssetPath("ladrillos.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    for i in range(2):
        piso1 = sg.SceneGraphNode('piso'+str(i))
        piso1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.0, 0.5*(2*i+1), 0.0)])
        piso1.childs += [gpu1]
        casa1.childs += [piso1]

    # Entre entretecho
    shapeETecho = bs.createPiramideC()
    gpuETecho = createGPUShape(pipeline, shapeETecho)
    gpuETecho.texture = es.textureSimpleSetup(getAssetPath("techo.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    etecho = sg.SceneGraphNode('entretecho')
    etecho.transform = tr.matmul([tr.translate(0.0, 1, 0.0),tr.uniformScale(0.5), tr.translate(0.0, 0.5, 0.0)])
    etecho.childs += [gpuETecho]
    casa1.childs += [etecho]

    # Techo
    modelTecho = createTecho(pipeline,"tejas.webp",0,0,1.5)
    techo1 = sg.SceneGraphNode('Techo 1')
    techo1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0, 2.5, 0),tr.uniformScale(1.2)])
    techo1.childs += [modelTecho]
    casa1.childs += [techo1]

    techo2 = sg.SceneGraphNode('Techo 2')
    techo2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0, 2.5, 0),tr.uniformScale(1.2),tr.rotationY(np.pi)])
    techo2.childs += [modelTecho]
    casa1.childs += [techo2]

    return casa1

# Función que crea el grafo del segundo modelo de casa, utiliza los nodos previamente definidos, 
# y recibe solo el pipeline.
def createCasa2(pipeline):
    # Definimos el nodo escena
    casa2 = sg.SceneGraphNode('Modelo Casa 2')

    modelPiso = createPrisma(pipeline,"piso_2.jpg",2.5,0.1,2.5,"N")
    piso = sg.SceneGraphNode('Piso 1')
    piso.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0, -0.11, 0)])
    piso.childs += [modelPiso]
    casa2.childs += [piso]

    # Puertas
    modelDoor1 = createPuertaModel1(pipeline,"puerta_2.png")
    puerta1 = sg.SceneGraphNode('Puerta 1')
    puerta1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(1.5, 0.4, 1)])
    puerta1.childs += [modelDoor1]
    casa2.childs += [puerta1]

    modelDoor2 = createPuertaModel1(pipeline,"puerta_2.png")
    puerta2 = sg.SceneGraphNode('Puerta 2')
    puerta2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(-0.7, 0.4, -2),tr.rotationY(np.pi/2)])
    puerta2.childs += [modelDoor2]
    casa2.childs += [puerta2]

    #ventanas
    modelWindow1 = createVentanaModel1(pipeline,"ventana2.png",0.5,0.3)
    ventana1 = sg.SceneGraphNode('Ventana 1')
    ventana1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(1.5, 1.5, -1)])
    ventana1.childs += [modelWindow1]
    casa2.childs += [ventana1]

    ventana2 = sg.SceneGraphNode('Ventana 2')
    ventana2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0, 0.5, 2),tr.rotationY(-np.pi/2)])
    ventana2.childs += [modelWindow1]
    casa2.childs += [ventana2]

    ventana3 = sg.SceneGraphNode('Ventana 3')
    ventana3.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.5, 0.5, -2),tr.rotationY(np.pi/2)])
    ventana3.childs += [modelWindow1]
    casa2.childs += [ventana3]

    ventana4 = sg.SceneGraphNode('Ventana 4')
    ventana4.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(-1.5, 1.5, -1),tr.rotationY(np.pi)])
    ventana4.childs += [modelWindow1]
    casa2.childs += [ventana4]

    # Piso 1 y 2, lateral
    shape1 = bs.createModelPiso1("l2")
    gpu1 = createGPUShape(pipeline, shape1)
    gpu1.texture = es.textureSimpleSetup(getAssetPath("marmol_casa.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    piso1 = sg.SceneGraphNode('piso1')
    piso1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.0, 0.5, 0.0),tr.scale(1,1,2)])
    piso1.childs += [gpu1]
    casa2.childs += [piso1]

    piso2 = sg.SceneGraphNode('piso2')
    piso2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.0, 1.5, -1)])
    piso2.childs += [gpu1]
    casa2.childs += [piso2]

    # Entre entretecho
    shapeETecho = bs.createPiramideCL()
    gpuETecho = createGPUShape(pipeline, shapeETecho)
    gpuETecho.texture = es.textureSimpleSetup(getAssetPath("marmol_casa.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    etecho1 = sg.SceneGraphNode('entretecho')
    etecho1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.0, 2.2, -1)])
    etecho1.childs += [gpuETecho]
    casa2.childs += [etecho1]

    etecho2 = sg.SceneGraphNode('entretecho')
    etecho2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.0, 1.2, 1)])
    etecho2.childs += [gpuETecho]
    casa2.childs += [etecho2]

    # Techo
    modelTecho = createTecho(pipeline,"tejas.webp",0.6,1,1.5)
    techo1 = sg.SceneGraphNode('Techo 1')
    techo1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0, 2.62, -2),tr.uniformScale(1.2)])
    techo1.childs += [modelTecho]
    casa2.childs += [techo1]

    techo2 = sg.SceneGraphNode('Techo 2')
    techo2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0, 1.6, 0),tr.uniformScale(1.2)])
    techo2.childs += [modelTecho]
    casa2.childs += [techo2]

    return casa2

# Función que crea el grafo del tercer modelo de casa, utiliza los nodos previamente definidos, 
# y recibe solo el pipeline.
def createCasa3(pipeline):
    # Definimos el nodo escena
    casa3 = sg.SceneGraphNode('Modelo Casa 3')
        
    modelPiso = createPrisma(pipeline,"piso_3.png",2.5,0.1,2.5,"N")
    piso = sg.SceneGraphNode('Piso 1')
    piso.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0, -0.11, 0)])
    piso.childs += [modelPiso]
    casa3.childs += [piso]

    #Puertas
    modelDoor1 = createPuertaModel1(pipeline,"puerta3.png")
    puerta1 = sg.SceneGraphNode('Puerta 1')
    puerta1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(-0.5, 0.4, 2),tr.rotationY(-np.pi/2)])
    puerta1.childs += [modelDoor1]
    casa3.childs += [puerta1]

    modelDoor2 = createPuertaModel1(pipeline,"puerta3.png")
    puerta2 = sg.SceneGraphNode('Puerta 2')
    puerta2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(-0.5, 0.4, -2),tr.rotationY(np.pi/2)])
    puerta2.childs += [modelDoor2]
    casa3.childs += [puerta2]

    # Ventanas
    modelWindow1 = createVentanaModel1(pipeline,"ventana3.png",0.6,0.45)
    ventana1 = sg.SceneGraphNode('Ventana 1')
    ventana1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(1.4, 0.6, 0)])
    ventana1.childs += [modelWindow1]
    casa3.childs += [ventana1]

    modelWindow2 = createVentanaModel1(pipeline,"ventana3.1.png",0.2,0.3)
    for i in range(2):
        ventana2 = sg.SceneGraphNode('Ventana '+str(i+2))
        ventana2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.6, 0.5, 1.5-(3*i))])
        ventana2.childs += [modelWindow2]
        casa3.childs += [ventana2]

    # Piso 1 y 2, latera
    shape1 = bs.createModelPiso1("l2")
    gpu1 = createGPUShape(pipeline, shape1)
    gpu1.texture = es.textureSimpleSetup(getAssetPath("madera_casa3.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    piso1 = sg.SceneGraphNode('piso1')
    piso1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(-0.5, 0.5, 0.0),tr.scale(0.75,1,2)])
    piso1.childs += [gpu1]
    casa3.childs += [piso1]

    piso2 = sg.SceneGraphNode('piso2')
    piso2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.5, 0.5, 0),tr.scale(0.6,1,1)])
    piso2.childs += [gpu1]
    casa3.childs += [piso2]

    # Entre entretecho
    shapeETecho = bs.createPiramideC()
    gpuETecho = createGPUShape(pipeline, shapeETecho)
    gpuETecho.texture = es.textureSimpleSetup(getAssetPath("madera_casa3.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    etecho1 = sg.SceneGraphNode('entretecho 1')
    etecho1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.5, 1.5, 0.0),tr.scale(0.6,1,1)])
    etecho1.childs += [gpuETecho]
    casa3.childs += [etecho1]

    etecho2 = sg.SceneGraphNode('entretecho 1')
    etecho2.transform = tr.matmul([tr.uniformScale(0.5),tr.translate(-0.5, 1.5, 0.0),tr.rotationY(np.pi/2),tr.scale(1.33,1,1.125)])
    etecho2.childs += [gpuETecho]
    casa3.childs += [etecho2]

    # Techo
    modelTecho = createTecho(pipeline,"tejas.webp",0,0,1.5)
    techo1 = sg.SceneGraphNode('Techo 1')
    techo1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.5, 1.5, 0),tr.scale(0.66,1.2,1.2)])
    techo1.childs += [modelTecho]
    casa3.childs += [techo1]

    techo2 = sg.SceneGraphNode('Techo 2')
    techo2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.5, 1.5, 0),tr.scale(0.66,1.2,1.2),tr.rotationY(np.pi)])
    techo2.childs += [modelTecho]
    casa3.childs += [techo2]

    techo3 = sg.SceneGraphNode('Techo 3')
    techo3.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(-0.5, 1.5, 0.0),tr.rotationY(np.pi/2),tr.scale(1.33*1.1,1.2,1.125*1.2)])
    techo3.childs += [modelTecho]
    casa3.childs += [techo3]

    techo4 = sg.SceneGraphNode('Techo 4')
    techo4.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(-0.5, 1.5, 0.0),tr.rotationY(3*np.pi/2),tr.scale(1.33*1.1,1.2,1.125*1.2)])
    techo4.childs += [modelTecho]
    casa3.childs += [techo4]

    return casa3

# Función que crea el grafo de las veredas de la ciudad, utiliza los nodos previamente definidos, 
# y recibe solo el pipeline.
def createVereda(pipeline):
    # Definimos el nodo escena
    vereda = sg.SceneGraphNode('Veredas')
    # Verticales
    for i in range(6):
        for j in range(47):
            if ((i == 0) and (j==23)):
                break
            if((i==1)and(j==34)):
                break
            if((i==1)and(j==33)):
                largo = 0.9
                t = 0.9
            else:
                largo = 1.25
                t = 0
            modelVereda = createPrisma(pipeline,"veredas.png",largo,0.1,0.5,"N")
            vereda1 = sg.SceneGraphNode('Vereda 1')
            vereda1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(25 -11*i, -0.11, (-16.25+(t)+1.25*j)),tr.rotationY(np.pi/2)])
            vereda1.childs += [modelVereda]
            vereda.childs += [vereda1]
    #horizontales
    for i in range(3):
        for j in range(12):
            modelVereda = createPrisma(pipeline,"veredas.png",1,0.1,0.5,"N")
            vereda1 = sg.SceneGraphNode('Vereda 1')
            if ((i ==0) and (j==6)):
                break
            if(j>5):
                a = 43
                b = 36.5
            else:
                a =-18
                b = 24.5
            vereda1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(b -2*j -22*i, -0.11, a)])
            vereda1.childs += [modelVereda]
            vereda.childs += [vereda1]

    for j in range(10):
        if(j==9):
            largo = 0.9
            t = 0.9
        else:
            largo = 1.25
            t = 0
        modelVereda = createPrisma(pipeline,"veredas.png",largo,0.1,0.5,"N")
        vereda1 = sg.SceneGraphNode('Vereda 1')
        vereda1.transform = tr.matmul([tr.uniformScale(0.5),tr.shearing(0, 0, -0.7, 0, 0, 0), tr.translate(33.75, -0.11, -15+(t)+1.25*(j+23)),tr.rotationY(np.pi/2)])
        vereda1.childs += [modelVereda]
        vereda.childs += [vereda1]

    shapeVeredaE = bs.createPisoParque(1.425,0.995)
    gpuVeredaE = createGPUShape(pipeline, shapeVeredaE)
    gpuVeredaE.texture = es.textureSimpleSetup(getAssetPath("veredaEsq.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    veredaE = sg.SceneGraphNode('Vereda E')
    veredaE.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(14.495, -0.11, 28.225), tr.rotationY(np.pi/2),tr.rotationZ(np.pi/2)])
    veredaE.childs += [gpuVeredaE]
    vereda.childs += [veredaE]

    return vereda

# Función que crea el grafo de las calles, utiliza los nodos previamente definidos, 
# y recibe solo el pipeline.
def createCalle(pipeline):
    # Definimos el nodo escena
    calles = sg.SceneGraphNode('Calles')

    for i in range(4):
        for j in range(4):
            a = 7.75
            b = 15.5
            calle1 = sg.SceneGraphNode('Calle 1')
            if ((i == 0)and(j==2)):
                break
            elif (i == 1 and j==2):
                a = 8.65
                b = 15.9
                nombre = "calle.png"
            elif (j==3):
                nombre = "pasoPeatonalS.png"
                if(i==1):
                    break
            elif (j==0):
                nombre = "pasoPeatonalI.png"
            else:
                nombre = "calle.png"
            modelCalle = createPrisma(pipeline,nombre,a,0.02,5,"N")
            calle1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(30.5 -22*i, -0.19, -10.75+b*j),tr.rotationY(np.pi/2)])
            calle1.childs += [modelCalle]
            calles.childs += [calle1]

    for j in range(4):
        modelCalle = createPrisma(pipeline,"calleI.png",9.5,0.02,5,"N")
        calle1 = sg.SceneGraphNode('Calle 1')
        calle1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(26 -19*j, -0.19, -23.5)])
        calle1.childs += [modelCalle]
        calles.childs += [calle1]

    for j in range(2):
        modelCalle = createPrisma(pipeline,"calleS.png",9.45,0.02,5,"N")
        calle1 = sg.SceneGraphNode('Calle 1')
        calle1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(5.75-(9.2*2*(j+1)), -0.19, 48.5)])
        calle1.childs += [modelCalle]
        calles.childs += [calle1]

    for j in range(3):
        if((j==0) or (j==1)):
            nombre = "calleS.png"
        elif(j==2):
            nombre = "calleE.png"
        else:
            nombre = "calle.png"
        modelCalle = createPrisma(pipeline,nombre,7,0.02,5,"N")
        calle1 = sg.SceneGraphNode('Calle 1')
        calle1.transform = tr.matmul([tr.uniformScale(0.5),tr.shearing(0, 0, -0.7, 0, 0, 0), tr.translate(39.25, -0.19, -7.5+13.5*(j+2)),tr.rotationY(np.pi/2)])
        calle1.childs += [modelCalle]
        calles.childs += [calle1]

    shapeCalleT = bs.createPisoParque(5,3.5)
    gpuCalleT = createGPUShape(pipeline, shapeCalleT)
    gpuCalleT.texture = es.textureSimpleSetup(getAssetPath("calleT.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    calleT = sg.SceneGraphNode('Calle T')
    calleT.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.3, -0.19, -10.25+1.25*47), tr.rotationY(np.pi/2),tr.rotationZ(np.pi/2),tr.scale(0.2,1,1)])
    calleT.childs += [gpuCalleT]
    calles.childs += [calleT]

    shapeCalleP = bs.createEsquina(6.9,0.02,5,-9.7)
    gpuCalleP = createGPUShape(pipeline, shapeCalleP)
    gpuCalleP.texture = es.textureSimpleSetup(getAssetPath("calleP.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    calleP = sg.SceneGraphNode('Calle P')
    calleP.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(8.5, -0.19, -22.15+1.25*47),tr.rotationY(np.pi/2)])
    calleP.childs += [gpuCalleP]
    calles.childs += [calleP]


    return calles

# Función que crea el grafo del parque en la ciudad, utiliza los nodos previamente definidos, 
# y recibe solo el pipeline.
def createParque(pipeline):
    parque = sg.SceneGraphNode('Parque')
    # Piso Parque
    shapeParque = bs.createPisoParque(7.15,5)
    gpuParque = createGPUShape(pipeline, shapeParque)
    gpuParque.texture = es.textureSimpleSetup(getAssetPath("pisoParque.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    parque1 = sg.SceneGraphNode('parque')
    parque1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(19.5, -0.11, 19.65),tr.rotationY(np.pi/2),tr.rotationZ(np.pi/2)])
    parque1.childs += [gpuParque]
    parque.childs += [parque1]

    # Bordes de pasto 1
    Bordes = createPrisma(pipeline,"bordes_Parque.png",2,0.02,0.05,"N")
    borde1 = sg.SceneGraphNode('Borde 1')
    borde1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(14.55, 0.01, 14.5),tr.rotationY(np.pi/2)])
    borde1.childs += [Bordes]
    parque.childs += [borde1]

    borde2 = sg.SceneGraphNode('Borde 2')
    borde2.transform = tr.matmul([tr.uniformScale(0.5), tr.shearing(0, 0, -0.7, 0, 0, 0),tr.translate(33.2, 0.01, 14.5),tr.rotationY(np.pi/2)])
    borde2.childs += [Bordes]
    parque.childs += [borde2]

    Bordes3 = createPrisma(pipeline,"bordes_Parque.png",4.9,0.02,0.05,"N")
    borde3 = sg.SceneGraphNode('Borde 3')
    borde3.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(19.5, 0.01, 12.55)])
    borde3.childs += [Bordes3]
    parque.childs += [borde3]

    Bordes4 = createPrisma(pipeline,"bordes_Parque.png",3.55,0.02,0.05,"N")
    borde4 = sg.SceneGraphNode('Borde 4')
    borde4.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(18.15, 0.01, 16.45)])
    borde4.childs += [Bordes4]
    parque.childs += [borde4]

    # Bordes Pasto 2 Verticales
    Bordes5 = createPrisma(pipeline,"bordes_Parque.png",3,0.02,0.05,"N")
    borde5 = sg.SceneGraphNode('Borde 5')
    borde5.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(14.55, 0.01, 21),tr.rotationY(np.pi/2)])
    borde5.childs += [Bordes5]
    parque.childs += [borde5]

    borde6 = sg.SceneGraphNode('Borde 6')
    borde6.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(15.3, 0.01, 21),tr.rotationY(np.pi/2)])
    borde6.childs += [Bordes5]
    parque.childs += [borde6]

    borde7 = sg.SceneGraphNode('Borde 7')
    borde7.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(15.8, 0.01, 21),tr.rotationY(np.pi/2)])
    borde7.childs += [Bordes5]
    parque.childs += [borde7]

    borde8 = sg.SceneGraphNode('Borde 8')
    borde8.transform = tr.matmul([tr.uniformScale(0.5), tr.shearing(0, 0, -0.7, 0, 0, 0),tr.translate(33.2, 0.01, 21),tr.rotationY(np.pi/2)])
    borde8.childs += [Bordes5]
    parque.childs += [borde8]

    # Bordes Pasto 2 Horizontales
    Bordes9 = createPrisma(pipeline,"bordes_Parque.png",0.345,0.02,0.05,"N")
    borde9 = sg.SceneGraphNode('Borde 9')
    borde9.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(14.925, 0.01, 18.05)])
    borde9.childs += [Bordes9]
    parque.childs += [borde9]

    borde10 = sg.SceneGraphNode('Borde 10')
    borde10.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(14.925, 0.01, 23.95)])
    borde10.childs += [Bordes9]
    parque.childs += [borde10]

    Bordes11 = createPrisma(pipeline,"bordes_Parque.png",0.3,0.02,0.05,"N")
    borde11 = sg.SceneGraphNode('Borde 11')
    borde11.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(16.15, 0.01, 23.95)])
    borde11.childs += [Bordes11]
    parque.childs += [borde11]

    Bordes12 = createPrisma(pipeline,"bordes_Parque.png",2.35,0.02,0.05,"N")
    borde12 = sg.SceneGraphNode('Borde 11')
    borde12.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(18.2, 0.01, 18.05)])
    borde12.childs += [Bordes12]
    parque.childs += [borde12]

    # Pasto
    Pasto1 = createPrisma(pipeline,"pastoParque.png",0.325,0.005,2.9,"N")
    pasto1 = sg.SceneGraphNode('Pasto 1')
    pasto1.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(14.925, 0.0025, 21)])
    pasto1.childs += [Pasto1]
    parque.childs += [pasto1]

    shapePasto2 = bs.createEsquina(2.9,0.005,2.305,-4)
    gpuPasto2 = createGPUShape(pipeline, shapePasto2)
    gpuPasto2.texture = es.textureSimpleSetup(getAssetPath("pastoParque.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    pasto2 = sg.SceneGraphNode('Pasto 2')
    pasto2.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(18.155, 0.0025, 21),tr.rotationY(np.pi/2)])
    pasto2.childs += [gpuPasto2]
    parque.childs += [pasto2]

    shapePasto3 = bs.createEsquina(1.9,0.005,4.875,-2.6)
    gpuPasto3 = createGPUShape(pipeline, shapePasto3)
    gpuPasto3.texture = es.textureSimpleSetup(getAssetPath("pastoParque.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    pasto3 = sg.SceneGraphNode('Pasto 3')
    pasto3.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(19.45, 0.0025, 14.5),tr.rotationY(np.pi/2)])
    pasto3.childs += [gpuPasto3]
    parque.childs += [pasto3]

    return parque

# Función que crea el grafo de las casas centrales y laterales derecha de la ciudad, poniendo las casas de manera aleatoria, 
# utiliza los grafos previamente definidos, y recibe solo el pipeline.
def createSceneCentral(pipeline):
    modelHouses1 = createCasa1(pipeline)
    modelHouses2 = createCasa2(pipeline)
    modelHouses3 = createCasa3(pipeline)
    sceneCentral = sg.SceneGraphNode('Scene Central')

    for i in range(24):
        houses = sg.SceneGraphNode('Houses '+str(i))
        if (i==0):
            houses.transform = tr.matmul([tr.translate(0, 0, -7.5),tr.rotationY(np.pi/2)])
        elif (i == 11):
            houses.transform = tr.matmul([tr.translate(0, 0, 5+7.5*2),tr.rotationY(-np.pi/2)])
        elif (i == 12):
            houses.transform = tr.matmul([tr.translate(-2.5, 0, -7.5),tr.rotationY(np.pi/2)])
        elif (i == 23):
            houses.transform = tr.matmul([tr.translate(-2.5, 0, 5+7.5*2),tr.rotationY(-np.pi/2)])
        elif (i<12):
            houses.transform = tr.translate(0, 0, -7.5+2.5*(i))
        else:
            houses.transform = tr.matmul([tr.translate(-2.5, 0, -7.5+2.5*(i-12)),tr.rotationY(np.pi)])
        numeroDiseño = random.randint(1,3)
        if (numeroDiseño == 1):
            houses.childs += [modelHouses1]
        elif(numeroDiseño == 2):
            houses.childs += [modelHouses2]
        else:
            houses.childs += [modelHouses3]
        sceneCentral.childs += [houses]

    return sceneCentral

# Función que crea el grafo de las casas laterales izquierda de la ciudad, poniendo las casas de manera aleatoria, 
# utiliza los grafos previamente definidos, y recibe solo el pipeline.
def createSceneLateral(pipeline):
    modelHouses1 = createCasa1(pipeline)
    modelHouses2 = createCasa2(pipeline)
    modelHouses3 = createCasa3(pipeline)
    sceneLateral = sg.SceneGraphNode('Scene Lateral')

    for i in range(12):
        houses = sg.SceneGraphNode('Houses '+str(i+24))
        if (i==0):
            houses.transform = tr.matmul([tr.translate(11, 0, -7.5),tr.rotationY(np.pi/2)])
        elif (i == 6):
            houses.transform = tr.matmul([tr.translate(11-2.5, 0, -7.5),tr.rotationY(np.pi/2)])
        elif (i<=5):
            houses.transform = tr.translate(11, 0, -7.5+2.5*(i))
        else:
            houses.transform = tr.matmul([tr.translate(11-2.5, 0, -7.5+2.5*(i-6)),tr.rotationY(np.pi)])
        numeroDiseño = random.randint(1,3)
        if (numeroDiseño == 1):
            houses.childs += [modelHouses1]
        elif(numeroDiseño == 2):
            houses.childs += [modelHouses2]
        else:
            houses.childs += [modelHouses3]
        sceneLateral.childs += [houses]

    return sceneLateral

# (NUEVO) Función que crea la estructura de un poste, con sus texturas correspondientes. 
# Solo se recibe el pipeline como parámetro.
def createPostes(pipeline):
    basePoste = createPrisma(pipeline,"posteC.jpg",0.1,1.5,0.1,"N")
    diagonalPoste = createTecho(pipeline,"posteC.jpg",0.3,0.1,0.1)
    bordePoste = createPrisma(pipeline,"posteC.jpg",0.2,0.05,0.1,"N")
    luzPoste = createPrisma(pipeline,"posteLuz.png",0.15,0.015,0.07,"L")

    base = sg.SceneGraphNode('Base Poste')
    base.transform = tr.matmul([tr.uniformScale(0.5),tr.translate(0, 1.5, 0)])
    base.childs += [basePoste]

    diagonal = sg.SceneGraphNode('Diagonal Poste')
    diagonal.transform = tr.matmul([tr.uniformScale(0.5),tr.translate(1, 3.5, 0),tr.rotationY(-np.pi/2)])
    diagonal.childs += [diagonalPoste]

    borde = sg.SceneGraphNode('Borde Poste')
    borde.transform = tr.matmul([tr.uniformScale(0.5),tr.translate(1.2, 3.65, 0)])
    borde.childs += [bordePoste]

    luz = sg.SceneGraphNode('Luz Poste')
    luz.transform = tr.matmul([tr.uniformScale(0.5),tr.translate(1.2, 3.585, 0)])
    luz.childs += [luzPoste]

    modelPoste = sg.SceneGraphNode('Model Poste')
    modelPoste.childs += [base]
    modelPoste.childs += [diagonal]
    modelPoste.childs += [borde]
    modelPoste.childs += [luz]

    return modelPoste

# Función que utiliza los grafos anteriores para unirlos solo en el grafo de la escena a mostar en la ventana.
# Recibe solo el pipeline.
def createScene(pipeline):
    scene = sg.SceneGraphNode('Scene')

    escenaC = createSceneCentral(pipeline)
    sceneC = sg.SceneGraphNode('SceneC')
    sceneC.childs +=[escenaC]
    scene.childs += [sceneC]

    escenaD = createSceneCentral(pipeline)
    sceneD = sg.SceneGraphNode('SceneD')
    sceneD.transform = tr.translate(-11, 0, 0)
    sceneD.childs +=[escenaD]
    scene.childs += [sceneD]

    escenaI = createSceneLateral(pipeline)
    sceneI = sg.SceneGraphNode('SceneI')
    sceneI.childs +=[escenaI]
    scene.childs += [sceneI]

    escenaV = createVereda(pipeline)
    sceneVI = sg.SceneGraphNode('SceneVI')
    sceneVI.childs +=[escenaV]
    scene.childs += [sceneVI]

    escenaP = createCalle(pipeline)
    sceneP = sg.SceneGraphNode('SceneP')
    sceneP.childs +=[escenaP]
    scene.childs += [sceneP]

    escenaPar = createParque(pipeline)
    scenePar = sg.SceneGraphNode('ScenePar')
    scenePar.childs +=[escenaPar]
    scene.childs += [scenePar]

    # NUEVO: SE AÑADEN LOS GRAFOS DE LOS 9 POSTES.
    # Poste Calle 1
    escenaPostes = createPostes(pipeline)
    scenePoste1 = sg.SceneGraphNode('Poste 1')
    scenePoste1.transform = tr.translate(12.7, 0, -5)
    scenePoste1.childs +=[escenaPostes]
    scene.childs += [scenePoste1]

    # Poste Plaza
    scenePoste2 = sg.SceneGraphNode('Poste 2')
    scenePoste2.transform = tr.matmul([tr.translate(7.3, 0, 13),tr.rotationY(np.pi/2)])
    scenePoste2.childs +=[escenaPostes]
    scene.childs += [scenePoste2]

    # Poste Calle 2
    scenePoste3 = sg.SceneGraphNode('Poste 3')
    scenePoste3.transform = tr.matmul([tr.translate(6.8, 0, 0),tr.rotationY(np.pi)])
    scenePoste3.childs +=[escenaPostes]
    scene.childs += [scenePoste3]

    # Poste Esquina Superior Calle 2
    scenePoste4 = sg.SceneGraphNode('Poste 4')
    scenePoste4.transform = tr.translate(1.7, 0, 19)
    scenePoste4.childs +=[escenaPostes]
    scene.childs += [scenePoste4]

    # Poste Calle Inferior 
    scenePoste5 = sg.SceneGraphNode('Poste 5')
    scenePoste5.transform = tr.matmul([tr.translate(-1.25, 0, -9.2),tr.rotationY(np.pi/2)])
    scenePoste5.childs +=[escenaPostes]
    scene.childs += [scenePoste5]

    # Poste Inferior Calle 3
    scenePoste6 = sg.SceneGraphNode('Poste 6')
    scenePoste6.transform = tr.matmul([tr.translate(-4.2, 0, 0),tr.rotationY(np.pi)])
    scenePoste6.childs +=[escenaPostes]
    scene.childs += [scenePoste6]

    # Poste Superior Calle 3
    scenePoste7 = sg.SceneGraphNode('Poste 7')
    scenePoste7.transform = tr.translate(-9.3, 0, 19)
    scenePoste7.childs +=[escenaPostes]
    scene.childs += [scenePoste7]

    # Poste Superior Calle 4
    scenePoste8 = sg.SceneGraphNode('Poste 8')
    scenePoste8.transform = tr.matmul([tr.translate(-15.2, 0, 13),tr.rotationY(np.pi)])
    scenePoste8.childs +=[escenaPostes]
    scene.childs += [scenePoste8]

    # Poste Inferior Calle 4
    scenePoste9 = sg.SceneGraphNode('Poste 9')
    scenePoste9.transform = tr.matmul([tr.translate(-15.2, 0, -6),tr.rotationY(np.pi)])
    scenePoste9.childs +=[escenaPostes]
    scene.childs += [scenePoste9]

    return scene

# Se crea un grafo adicional (prisma triangular) que mostrará la ubicacion de la cámara en perspectiva, cuando la ciudad es vista 
# de manera satelital (camara ortografica).
def createUbicacion(pipeline):
    shapeUbicacion = bs.createGPS()
    gpuUbicacion = createGPUShape(pipeline, shapeUbicacion)
    gpuUbicacion.texture = es.textureSimpleSetup(getAssetPath("amarilloF.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    ubicacion = sg.SceneGraphNode('Ubicacion')
    ubicacion.childs += [gpuUbicacion]

    return ubicacion

# (NUEVO) Se crea el grafo que contiene a las 2 esferas que serán el sol y la luna. Solo se recibe el pipeline.
def createSol_Luna(pipeline):
    shapeSol = bs.createSphere(2,30,30,0.78, 0.57, 0.08)
    gpuSol = createGPUShape(pipeline, shapeSol)
    sol = sg.SceneGraphNode('Sol')
    sol.transform = tr.translate(-1.25, -50, 6.25)
    sol.childs += [gpuSol]

    shapeLuna = bs.createSphere(1,30,30,0.6, 0.6, 0.6)
    gpuLuna = createGPUShape(pipeline, shapeLuna)
    luna = sg.SceneGraphNode('Luna')
    luna.transform = tr.translate(-1.25, 50, 6.25)
    luna.childs += [gpuLuna]

    sol_luna = sg.SceneGraphNode('Sol y Luna')
    sol_luna.childs += [luna]
    sol_luna.childs += [sol]

    return sol_luna

#####################################################################################################
###################################### FUNCIONES PARA CREAR EL AUTO #################################
#####################################################################################################

# Función que crea el shape de los objetos en los archivos .off en la memoria GPU, para ello necesita 
# leerlos con la función readOFF del archivo basic_shapes.py
def createOFFShape(pipeline, filename, r,g, b):
    shape = bs.readOFF(getAssetPath(filename), (r, g, b))
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

# Función crea un grafo para el auto, se leen los archivos .off de chasis y de las ruedas del auto
# y se unen en un solo grafo.
def createCarScene(pipeline):
    chasis = createOFFShape(pipeline, 'auto.off', 0.2, 0.08, 0.08)
    wheel = createOFFShape(pipeline, 'ruedas.off', 0.1, 0.1, 0.1)

    scale = 2.0
    rotatingWheelNode = sg.SceneGraphNode('rotatingWheel')
    rotatingWheelNode.childs += [wheel]

    chasisNode = sg.SceneGraphNode('chasis')
    chasisNode.transform = tr.uniformScale(scale)
    chasisNode.childs += [chasis]

    wheel1Node = sg.SceneGraphNode('wheel1')
    wheel1Node.transform = tr.matmul([tr.uniformScale(scale),tr.translate(0.056390,0.037409,0.091705)])
    wheel1Node.childs += [rotatingWheelNode]

    wheel2Node = sg.SceneGraphNode('wheel2')
    wheel2Node.transform = tr.matmul([tr.uniformScale(scale),tr.translate(-0.060390,0.037409,-0.099705)])
    wheel2Node.childs += [rotatingWheelNode]

    wheel3Node = sg.SceneGraphNode('wheel3')
    wheel3Node.transform = tr.matmul([tr.uniformScale(scale),tr.translate(-0.056390,0.037409,0.091705)])
    wheel3Node.childs += [rotatingWheelNode]

    wheel4Node = sg.SceneGraphNode('wheel4')
    wheel4Node.transform = tr.matmul([tr.uniformScale(scale),tr.translate(0.060390,0.037409,-0.099705)])
    wheel4Node.childs += [rotatingWheelNode]

    car1 = sg.SceneGraphNode('car1')
    car1.transform = tr.uniformScale(3)
    car1.childs += [chasisNode]
    car1.childs += [wheel1Node]
    car1.childs += [wheel2Node]
    car1.childs += [wheel3Node]
    car1.childs += [wheel4Node]

    scene = sg.SceneGraphNode('system-car')
    scene.childs += [car1]

    return scene

#####################################################################################################
###################### FUNCIONES PARA CREAR LA TRAYECTORIA (CURVAS) DEL AUTO ########################
#####################################################################################################

# Se genera la matriz T(t) de la fórmula de las curvas bezier. Sirve para evaluar la matriz e
# n el tiempo/paso "t".
def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T

# Esta función genera la matriz bezier recibiendo como parametros 4 puntos PO, P1, P2, P3.
# Multiplica la matriz G que contiene los 4 puntos con la matriz constante Mb.
def bezierMatrix(P0, P1, P2, P3):
    # Genera una matriz concatenando los puntos
    G = np.concatenate((P0, P1, P2, P3), axis=1)
    # Se genera la matriz constante de base de Bezier
    Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])
    return np.matmul(G, Mb)

# Esta función evalua la matriz de bezier de la curva cúbica M con el N número de 
# muestras/paso que habrá entre 0 y 1. Multiplica M por la matriz T(t).
def evalCurve(M, N):
    # El parámetro t debe moverse entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T
        
    return curve

# Función que genera la trayectoria que seguirá el auto. Une las distintas curvas 
# creadas con bezier, las cuales son 15 tramos en total. Retorna la curva (trayectoria)
# final creada.
def generateCurveT5(N):
    # (Las calles verticales se enumeran de izquierda a derecha)
    # Curva Inferior 2da Calle
    R0 = np.array([[5.5, -0.13, -8]]).T
    R1 = np.array([[ 5.5, -0.13, -9]]).T
    R2 = np.array([[ 5.5, -0.13, -10.5]]).T
    R3 = np.array([[8, -0.13, -10.5]]).T
    
    M1 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve1 = evalCurve(M1, N//2)

    # Curva inferior 1ra Calle
    R0 = np.array([[8, -0.13, -10.5]]).T
    R1 = np.array([[13, -0.13, -10.5]]).T
    R2 = np.array([[14, -0.13, -10.5]]).T
    R3 = np.array([[14, -0.13, -8.5]]).T
    
    M2 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve2 = evalCurve(M2, N//2)

    # Tramo 1ra Calle
    R0 = np.array([[14, -0.13, -8.5]]).T
    R1 = np.array([[14, -0.13, -3]]).T
    R2 = np.array([[14, -0.13, 0]]).T
    R3 = np.array([[14, -0.13, 4]]).T
    
    M3 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve3 = evalCurve(M3, N//2)

    # Curva Diagonal Inferior
    R0 = np.array([[14, -0.13, 4]]).T
    R1 = np.array([[14, -0.13, 5.5]]).T
    R2 = np.array([[14, -0.13, 6.5]]).T
    R3 = np.array([[12, -0.13, 9.3]]).T
    
    M4 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve4 = evalCurve(M4, N//2)

    # Tramo Diagonal
    R0 = np.array([[12, -0.13, 9.3]]).T
    R1 = np.array([[8, -0.13, 14.9]]).T
    R2 = np.array([[5, -0.13, 19.1]]).T
    R3 = np.array([[4, -0.13, 20.5]]).T
    
    M5 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve5 = evalCurve(M5, N)

    # Curva Diagonal Superior
    R0 = np.array([[4, -0.13, 20.5]]).T
    R1 = np.array([[3, -0.13, 21.9]]).T
    R2 = np.array([[2, -0.13, 23]]).T
    R3 = np.array([[0, -0.13, 23]]).T
    
    M6 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve6 = evalCurve(M6, N//2)

    # Tramo Calle Superior
    R0 = np.array([[0, -0.13, 23]]).T
    R1 = np.array([[-3, -0.13, 23]]).T
    R2 = np.array([[-8, -0.13, 23]]).T
    R3 = np.array([[-14, -0.13, 23]]).T
    
    M7 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve7 = evalCurve(M7, N)

    # Curva Superior 4ta Calle
    R0 = np.array([[-14, -0.13, 23]]).T
    R1 = np.array([[-15, -0.13, 23]]).T
    R2 = np.array([[-16.5, -0.13, 23]]).T
    R3 = np.array([[-16.5, -0.13, 20]]).T
    
    M8 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve8 = evalCurve(M8, N//2)

    # Tramo 4ta Calle
    R0 = np.array([[-16.5, -0.13, 20]]).T
    R1 = np.array([[-16.5, -0.13, 10]]).T
    R2 = np.array([[-16.5, -0.13, 0]]).T
    R3 = np.array([[-16.5, -0.13, -8]]).T
    
    M9 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve9 = evalCurve(M9, N)

    # Curva Inferior 4ta Calle
    R0 = np.array([[-16.5, -0.13, -8]]).T
    R1 = np.array([[-16.5, -0.13, -9]]).T
    R2 = np.array([[-16.5, -0.13, -10.5]]).T
    R3 = np.array([[-13.5, -0.13, -10.5]]).T
    
    M10 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve10 = evalCurve(M10, N//2)
        
    # Curva Inferior 3ra Calle
    R0 = np.array([[-13.5, -0.13, -10.5]]).T
    R1 = np.array([[-10.5, -0.13, -10.5]]).T
    R2 = np.array([[-8, -0.13, -10.5]]).T
    R3 = np.array([[-8, -0.13, -8.5]]).T
    
    M11 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve11 = evalCurve(M11, N)

    # Tramo 3ra Calle
    R0 = np.array([[-8, -0.13, -8.5]]).T
    R1 = np.array([[-8, -0.13, 0]]).T
    R2 = np.array([[-8, -0.13, 10]]).T
    R3 = np.array([[-8, -0.13, 20]]).T
    
    M12 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve12 = evalCurve(M12, N)

    # Curva Superior 3ra Calle
    R0 = np.array([[-8, -0.13, 20]]).T
    R1 = np.array([[-8, -0.13, 22]]).T
    R2 = np.array([[-7, -0.13, 25.5]]).T
    R3 = np.array([[-5, -0.13, 25.5]]).T
    
    M13 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve13 = evalCurve(M13, N//2)

    # Curva Superior 2do Calle
    R0 = np.array([[-5, -0.13, 25.5]]).T
    R1 = np.array([[0, -0.13, 25.5]]).T
    R2 = np.array([[5.5, -0.13, 25.5]]).T
    R3 = np.array([[5.5, -0.13, 20]]).T
    
    M14 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve14 = evalCurve(M14, N)

    # Tramo 2do Calle
    R0 = np.array([[5.5, -0.13, 20]]).T
    R1 = np.array([[5.5, -0.13, 15]]).T
    R2 = np.array([[5.5, -0.13, 5]]).T
    R3 = np.array([[5.5, -0.13, -8]]).T
    
    M15 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve15 = evalCurve(M15, N)

    # Concatenamos las curvas
    C = np.concatenate((bezierCurve1,bezierCurve2,bezierCurve3,bezierCurve4,
        bezierCurve5,bezierCurve6,bezierCurve7,bezierCurve8,bezierCurve9,
        bezierCurve10,bezierCurve11,bezierCurve12,bezierCurve13,bezierCurve14,bezierCurve15), axis=0)
    return C