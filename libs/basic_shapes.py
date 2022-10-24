# Archivo extraído y modificado de los auxiliares, del material de apoyo y del repositorio de ejemplos del curso.
import libs.transformations as tr
from OpenGL.GL import glUseProgram, glUniformMatrix4fv, glGetUniformLocation,\
    GL_TRUE, glUniform3f, glUniform1ui, glUniform1f
import sys
import os.path
import numpy as np
from libs.assets_path import getAssetPath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#####################################################################################################
################################# FUNCIONES PARA CREAR SHAPES DE OBJETOS ############################
#####################################################################################################

# Clase que crea el Shape (forma) de la figura a partir del orden de los vertices e indices recibidos.
class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices
        
# Función para crear el shape (forma) de los ejes. Recibe un parámetro opcional del largo del eje.
def createAxis(length=1.0):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -length,  0.0,  0.0, 0.0, 0.0, 0.0,
        length,  0.0,  0.0, 1.0, 0.0, 0.0,

        0.0, -length,  0.0, 0.0, 0.0, 0.0,
        0.0,  length,  0.0, 0.0, 1.0, 0.0,

        0.0,  0.0, -length, 0.0, 0.0, 0.0,
        0.0,  0.0,  length, 0.0, 0.0, 1.0]
    # This shape is meant to be drawn with GL_LINES,
    # i.e. every 2 indices, we have 1 line.
    indices = [
        0, 1,
        2, 3,
        4, 5]

    return Shape(vertices, indices)

# Se define la funcion que crea un prisma que se ocupará para el suelo de las casas, y otros objetos más. 
# Recibe como parametros el largo, el alto y ancho del prisma a crear. Además ahora se le añaden los valores 
# de las normales de cada vertice para iluminar el objeto, por lo que recibe un parametro de luz, si es "L" 
# la cara inferior tiene la normal hacia arriba(recibe la luz de manera inversa, esto sirve para iluminar
# el prisma blanco de los postes de luz). Si el parametro luz es diferente a "L", tiene la normal hacia abajo 
# y recibe la luz de manera correcta.
def createPrismas(largo, alto, ancho,luz):
    if(luz =="L"):
        n = 1
    else:
        n = -1
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top lateral1
        largo,  alto,  ancho, 1, 1,      0,0,1,
        largo, -alto,  ancho, 0, 1,      0,0,1,
        -largo, -alto,  ancho, 0, 0,     0,0,1,
        -largo,  alto,  ancho, 1, 0,     0,0,1,

        # Z-: block bottom lateral2
        -largo, -alto, -ancho, 1, 0,     0,0,-1,
        largo, -alto, -ancho, 1, 1,      0,0,-1,
        largo,  alto, -ancho, 0, 1,      0,0,-1,
        -largo,  alto, -ancho, 0, 0,     0,0,-1,

        # X+: block left puerta frontal
        largo, -alto, -ancho, 1, 1,      1,0,0,
        largo,  alto, -ancho, 1, 0,      1,0,0,
        largo,  alto,  ancho, 0, 0,      1,0,0,
        largo, -alto,  ancho, 0, 1,      1,0,0,

        # X-: block right  casa fondo
        -largo, -alto, -ancho, 1, 1,    -1,0,0,
        -largo,  alto, -ancho, 1, 0,    -1,0,0,
        -largo,  alto,  ancho, 0, 0,    -1,0,0,
        -largo, -alto,  ancho, 0, 1,    -1,0,0,

        # Y+: white face
        -largo,  alto, -ancho, 1, 0,    0,1,0,
        largo,  alto, -ancho, 1, 1,     0,1,0,
        largo,  alto,  ancho, 0, 1,     0,1,0,
        -largo,  alto,  ancho, 0, 0,    0,1,0,

        # Y-: yellow face
        -largo, -alto, -ancho, 1, 0,    0,n,0,
        largo, -alto, -ancho, 1, 1,     0,n,0,
        largo, -alto,  ancho, 0, 1,     0,n,0,
        -largo, -alto,  ancho, 0, 0,    0,n,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

# Se define la funcion que crea un prisma que se ocupará para los pisos de las casas, 
# recibe como parametro un condicional del ancho del piso, es decir, si es "l1" el 
# primer piso es pequeño, si es "l2" el primer piso es grande, ambos parametros definen 
# el sector de textura a ocupar. Se le añaden las normales a cada vértice correspondiente.
def createModelPiso1(level):
    if(level == "l1"):
        x = 0
    if(level == "l2"):
        x = 2/6

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top lateral1
        1.5,  0.5,  1, 1/6, 4/5,        0,0,1,
        1.5, -0.5,  1, 0, 4/5,          0,0,1,
        -1.5, -0.5,  1, 0, 1/5,         0,0,1,
        -1.5,  0.5,  1, 1/6, 1/5,       0,0,1,

        # Z-: block bottom lateral2
        -1.5, -0.5, -1, 4/6, 1/5,       0,0,-1,
        1.5, -0.5, -1, 4/6, 4/5,        0,0,-1,
        1.5,  0.5, -1, 3/6, 4/5,        0,0,-1,
        -1.5,  0.5, -1, 3/6, 1/5,       0,0,-1,

        # X+: block left puerta frontal
        1.5, -0.5, -1, 3/6+x, 1,        1,0,0,
        1.5,  0.5, -1, 3/6+x, 4/5,      1,0,0,
        1.5,  0.5,  1, 1/6, 4/5,        1,0,0,
        1.5, -0.5,  1, 1/6, 1,          1,0,0,

        # X-: block right  casa fondo
        -1.5, -0.5, -1, 3/6+x, 1/5,     -1,0,0,
        -1.5,  0.5, -1, 3/6+x, 0,       -1,0,0,
        -1.5,  0.5,  1, 1/6, 0,         -1,0,0,
        -1.5, -0.5,  1, 1/6, 1/5,       -1,0,0,

        # Y+: white face
        -1.5,  0.5, -1, 3/6, 1/5,       0,1,0,
        1.5,  0.5, -1, 3/6, 4/5,        0,1,0,
        1.5,  0.5,  1, 1/6, 4/5,        0,1,0,
        -1.5,  0.5,  1, 1/6, 1/5,       0,1,0,

        # Y-: yellow face
        -1.5, -0.5, -1, 1, 1/5,         0,-1,0,
        1.5, -0.5, -1, 1, 4/5,          0,-1,0,
        1.5, -0.5,  1, 4/6, 4/5,        0,-1,0,
        -1.5, -0.5,  1, 4/6, 1/5,       0,-1,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

# Se define la funcion que crea una prisma de base triangular que se ocupará para el 
# entretecho de las casas. Se le añaden las normales a cada vértice correspondiente.
def createPiramideC():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top lateral1
        1.5,  0.5,  0, 1/6, 4/5,        0,1,1,
        1.5, -0.5,  1, 0, 4/5,          0,1,1,
        -1.5, -0.5,  1, 0, 1/5,         0,1,1,
        -1.5,  0.5,  0, 1/6, 1/5,       0,1,1,

        # Z-: block bottom lateral2
        -1.5, -0.5, -1, 4/6, 1/5,       0,1,-1,
        1.5, -0.5, -1, 4/6, 4/5,        0,1,-1,
        1.5,  0.5, 0, 3/6, 4/5,         0,1,-1,
        -1.5,  0.5, 0, 3/6, 1/5,        0,1,-1,

        # X+: block left puerta frontal
        1.5, -0.5, -1, 3/6, 1,          1,0,0,
        1.5,  0.5, 0, 2/6, 4/5,         1,0,0,
        1.5, -0.5,  1, 1/6, 1,          1,0,0,

        # X-: block right  casa fondo
        -1.5, -0.5, -1, 3/6, 1,         -1,0,0,
        -1.5,  0.5, 0, 2/6, 4/5,        -1,0,0,
        -1.5, -0.5,  1, 1/6, 1,         -1,0,0,

        # Y-: yellow face
        -1.5, -0.5, -1, 1, 1/5,         0,-1,0,
        1.5, -0.5, -1, 1, 4/5,          0,-1,0,
        1.5, -0.5,  1, 4/6, 4/5,        0,-1,0,
        -1.5, -0.5,  1, 4/6, 1/5,       0,-1,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10,  # X+
        11,12,13,
        17, 16, 15, 15, 14, 17]

    return Shape(vertices, indices)

# Se define la funcion que crea una prisma rectangular que se ocupará para la puerta de las casas.
# Se le añaden las normales a cada vértice correspondiente.
def createPuerta1():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top lateral1
        0.05,  0.4,  0.2, 3/6, 1/5,     0,0,1,
        0.05, -0.4,  0.2, 3/6, 4/5,     0,0,1,
        -0.05, -0.4,  0.2, 4/6, 4/5,    0,0,1,
        -0.05,  0.4,  0.2, 4/6, 1/5,    0,0,1,

        # Z-: block bottom lateral2
        -0.05, -0.4, -0.2, 4/6, 1/5,    0,0,-1,
        0.05, -0.4, -0.2, 4/6, 4/5,     0,0,-1,
        0.05,  0.4, -0.2, 3/6, 4/5,     0,0,-1,
        -0.05,  0.4, -0.2, 3/6, 1/5,    0,0,-1,

        # X+: block left puerta frontal
        0.05, -0.4, -0.2, 1, 1,         1,0,0,
        0.05,  0.4, -0.2, 1, 0,         1,0,0,
        0.05,  0.4,  0.2, 0, 0,         1,0,0,
        0.05, -0.4,  0.2, 0, 1,         1,0,0,

        # X-: block right  casa fondo
        -0.05, -0.4, -0.2, 1, 1,        -1,0,0,
        -0.05,  0.4, -0.2, 1, 0,        -1,0,0,
        -0.05,  0.4,  0.2, 0, 0,        -1,0,0,
        -0.05, -0.4,  0.2, 0, 1,        -1,0,0,

        # Y+: white face
        -0.05,  0.4, -0.2, 3/6, 1/5,    0,1,0,
        0.05,  0.4, -0.2, 3/6, 4/5,     0,1,0,
        0.05,  0.4,  0.2, 1/6, 4/5,     0,1,0,
        -0.05,  0.4,  0.2, 1/6, 1/5,    0,1,0,

        # Y-: yellow face
        -0.05, -0.4, -0.2, 1, 1/5,      0,-1,0,
        0.05, -0.4, -0.2, 1, 4/5,       0,-1,0,
        0.05, -0.4,  0.2, 4/6, 4/5,     0,-1,0,
        -0.05, -0.4,  0.2, 4/6, 1/5,    0,-1,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

# Se define la funcion que crea una prisma rectangular que se ocupará para las ventanas de las casas.
# recibe el alto y largo de la ventana. Se le añaden las normales a cada vértice correspondiente.
def createVentana1(alto, ancho):
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top lateral1
        0.05,  alto,  ancho, 3/6, 1/5,      0,0,1,
        0.05, -alto,  ancho, 3/6, 4/5,      0,0,1,
        -0.05, -alto,  ancho, 4/6, 4/5,     0,0,1,
        -0.05,  alto,  ancho, 4/6, 1/5,     0,0,1,

        # Z-: block bottom lateral2
        -0.05, -alto, -ancho, 4/6, 1/5,     0,0,-1,
        0.05, -alto, -ancho, 4/6, 4/5,      0,0,-1,
        0.05,  alto, -ancho, 3/6, 4/5,      0,0,-1,
        -0.05,  alto, -ancho, 3/6, 1/5,     0,0,-1,

        # X+: block left puerta frontal
        0.05, -alto, -ancho, 1, 1,          1,0,0,
        0.05,  alto, -ancho, 1, 0,          1,0,0,
        0.05,  alto,  ancho, 0, 0,          1,0,0,
        0.05, -alto,  ancho, 0, 1,          1,0,0,

        # X-: block right  casa fondo
        -0.05, -alto, -ancho, 1, 1,         -1,0,0,
        -0.05,  alto, -ancho, 1, 0,         -1,0,0,
        -0.05,  alto,  ancho, 0, 0,         -1,0,0,
        -0.05, -alto,  ancho, 0, 1,         -1,0,0,

        # Y+: white face
        -0.05,  alto, -ancho, 3/6, 1/5,     0,1,0,
        0.05,  alto, -ancho, 3/6, 4/5,      0,1,0,
        0.05,  alto,  ancho, 1/6, 4/5,      0,1,0,
        -0.05,  alto,  ancho, 1/6, 1/5,     0,1,0,

        # Y-: yellow face
        -0.05, -alto, -ancho, 1, 1/5,       0,-1,0,
        0.05, -alto, -ancho, 1, 4/5,        0,-1,0,
        0.05, -alto,  ancho, 4/6, 4/5,      0,-1,0,
        -0.05, -alto,  ancho, 4/6, 1/5,     0,-1,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

# Se define la funcion que crea un prisma que se ocupará en los techos de las casas, 
# recibe como parametro la inclinación que tendrá y el largo de este. Se le añaden las normales a cada 
# vértice correspondiente.
def createModelTecho(inclinacion, largo, ancho): 

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top lateral1
        ancho,  0.5-inclinacion,  0, 1/6, 4/5,                0,1,1,
        ancho, -0.5, 1+largo, 0, 4/5,                         0,1,1,
        -ancho, -0.5, 1+largo, 0, 1/5,                        0,1,1,
        -ancho,  0.5-inclinacion,  0, 1/6, 1/5,               0,1,1,

        # Z-: block bottom lateral2
        -ancho, -0.5, 0.9+largo-(inclinacion/3), 4/6, 1/5,    0,-1,-1,
        ancho, -0.5, 0.9+largo-(inclinacion/3), 4/6, 4/5,     0,-1,-1,
        ancho,  0.4-inclinacion, 0, 3/6, 4/5,                 0,-1,-1,
        -ancho,  0.4-inclinacion, 0, 3/6, 1/5,                0,-1,-1,

        # X+: block left puerta frontal
        ancho, -0.5, 0.9+largo-(inclinacion/3), 0, 0,         1,0,0,
        ancho,  0.4-inclinacion, 0, 1/6, 0,                   1,0,0,
        ancho,  0.5-inclinacion, 0, 1/6, 1,                   1,0,0,
        ancho, -0.5, 1+largo, 0, 1,                           1,0,0,

        # X-: block right  casa fondo (vista desde atras)
        -ancho, -0.5, 0.9+largo-(inclinacion/3), 0, 1,        -1,0,0,
        -ancho,  0.4-inclinacion, 0, 1/6, 1,                  -1,0,0,
        -ancho,  0.5-inclinacion, 0, 1/6, 0,                  -1,0,0,
        -ancho, -0.5, 1+largo, 0, 0,                          -1,0,0,

        # Y+: white face
        -ancho,  0.4-inclinacion, 0, 3/6, 1/5,                0,0,-1,
        ancho,  0.4-inclinacion, 0, 3/6, 4/5,                 0,0,-1,
        ancho,  0.5-inclinacion,  0, 1/6, 4/5,                0,0,-1,
        -ancho,  0.5-inclinacion,  0, 1/6, 1/5,               0,0,-1,

        # Y-: yellow face
        -ancho, -0.5, 0.9+largo, 1, 1/5,                      0,-1,0,
        ancho, -0.5, 0.9+largo, 1, 4/5,                       0,-1,0,
        ancho, -0.5,  1+largo, 4/6, 4/5,                      0,-1,0,
        -ancho, -0.5,  1+largo, 4/6, 1/5,                     0,-1,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

# Se define la funcion que crea un prisma de base triangular que se ocupará para algunas formas del entretecho
# de las casas. Se le añaden las normales a cada vértice correspondiente.
def createPiramideCL():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top lateral1
        1.5,  0.2,  -1, 1/6, 4/5,       0,1,1,
        1.5, -0.2,  1, 0, 4/5,          0,1,1,
        -1.5, -0.2,  1, 0, 1/5,         0,1,1,
        -1.5,  0.2,  -1, 1/6, 1/5,      0,1,1,

        # Z-: block bottom lateral2
        -1.5, -0.2, -1, 4/6, 1/5,       0,0,-1,
        1.5, -0.2, -1, 4/6, 4/5,        0,0,-1,
        1.5,  0.2, -1, 3/6, 4/5,        0,0,-1,
        -1.5,  0.2, -1, 3/6, 1/5,       0,0,-1,

        # X+: block left puerta frontal
        1.5, -0.2, -1, 3/6, 1,          1,0,0,
        1.5,  0.2, -1, 3/6, 9/10,       1,0,0,
        1.5, -0.2,  1, 1/6, 1,          1,0,0,

        # X-: block right  casa fondo
        -1.5, -0.2, -1, 3/6, 2/10,      -1,0,0,
        -1.5,  0.2, -1, 3/6, 1/10,      -1,0,0,
        -1.5, -0.2,  1, 1/6, 2/10,      -1,0,0,

        # Y-: yellow face
        -1.5, -0.2, -1, 1, 1/5,         0,-1,0,
        1.5, -0.2, -1, 1, 4/5,          0,-1,0,
        1.5, -0.2,  1, 4/6, 4/5,        0,-1,0,
        -1.5, -0.2,  1, 4/6, 1/5,       0,-1,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10,  # X+
        11,12,13,
        17, 16, 15, 15, 14, 17]

    return Shape(vertices, indices)

# Se define la funcion que crea un prisma de base triangular que se ocupa para crear el piso del parque.
# recibe el largo y ancho de este. Se le añaden las normales a cada vértice correspondiente.
def createPisoParque(largo, ancho):

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top lateral1
        0.1,  largo,  -ancho, 1/6, 4/5,     0,1,1,   
        0.1, -largo,  ancho, 0, 4/5,        0,1,1,
        -0.1, -largo,  ancho, 0, 1/5,       0,1,1,
        -0.1,  largo,  -ancho, 1/6, 1/5,    0,1,1,

        # Z-: block bottom lateral2
        -0.1, -largo, -ancho, 4/6, 1/5,     0,0,-1,
        0.1, -largo, -ancho, 4/6, 4/5,      0,0,-1,
        0.1,  largo, -ancho, 3/6, 4/5,      0,0,-1,
        -0.1,  largo, -ancho, 3/6, 1/5,     0,0,-1,

        # X+: block left puerta frontal
        0.1, -largo, -ancho, 0, 1,          1,0,0,
        0.1,  largo, -ancho, 1, 1,          1,0,0,
        0.1, -largo,  ancho, 0, 0,          1,0,0,

        # X-: block right  casa fondo
        0.1, -largo, -ancho, 3/6, 2/10,     -1,0,0,
        -0.1,  largo, -ancho, 3/6, 1/10,    -1,0,0,
        -0.1, -largo,  ancho, 1/6, 2/10,    -1,0,0,

        # Y-: yellow face
        -0.1, -largo, -ancho, 1, 1/5,       0,-1,0,
        0.1, -largo, -ancho, 1, 4/5,        0,-1,0,
        0.1, -largo,  ancho, 4/6, 4/5,      0,-1,0,
        -0.1, -largo,  ancho, 4/6, 1/5,     0,-1,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10,  # X+
        11,12,13,
        17, 16, 15, 15, 14, 17]

    return Shape(vertices, indices)

# Se define la funcion que crea un prisma que se ocupa para crear algunos sectores de calles, y parque
# recibe el largo, alto y ancho de este. Además la inclinacion correspondiente a una cara de este.
# Se le añaden las normales a cada vértice correspondiente.
def createEsquina(largo, alto, ancho,inclinacion):
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top lateral1
        largo,  alto,  ancho, 1, 1,                 0,1,1,
        largo, -alto,  ancho, 0, 1,                 0,1,1,
        -largo, -alto,  ancho+inclinacion, 0, 0,    0,1,1,
        -largo,  alto,  ancho+inclinacion, 1, 0,    0,1,1,

        # Z-: block bottom lateral2
        -largo, -alto, -ancho, 1, 0,                0,0,-1,
        largo, -alto, -ancho, 1, 1,                 0,0,-1,
        largo,  alto, -ancho, 0, 1,                 0,0,-1,
        -largo,  alto, -ancho, 0, 0,                0,0,-1,

        # X+: block left puerta frontal
        largo, -alto, -ancho, 1, 1,                 1,0,0,
        largo,  alto, -ancho, 1, 0,                 1,0,0,
        largo,  alto,  ancho, 0, 0,                 1,0,0,
        largo, -alto,  ancho, 0, 1,                 1,0,0,

        # X-: block right  casa fondo
        -largo, -alto, -ancho, 1, 1,                -1,0,0,
        -largo,  alto, -ancho, 1, 0,                -1,0,0,
        -largo,  alto,  ancho+inclinacion, 0, 0,    -1,0,0,
        -largo, -alto,  ancho+inclinacion, 0, 1,    -1,0,0,

        # Y+: white face
        -largo,  alto, -ancho, 1, 0,                0,1,0,
        largo,  alto, -ancho, 1, 1,                 0,1,0,
        largo,  alto,  ancho, 0, 1,                 0,1,0,
        -largo,  alto,  ancho+inclinacion, 0, 0,    0,1,0,

        # Y-: yellow face
        -largo, -alto, -ancho, 1, 0,                0,-1,0,
        largo, -alto, -ancho, 1, 1,                 0,-1,0,
        largo, -alto,  ancho, 0, 1,                 0,-1,0,
        -largo, -alto,  ancho+inclinacion, 0, 0,    0,-1,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)

# Se define la funcion que crea una piramide de base rectangular que se ocupará para el GPS, el "triangulo"
# que se ve desde la vista ortográfica. No se le añaden las normales, ya que no queremos que este sea reflejado
# con luz.
def createGPS():
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top 
        1,  0.5,  0, 1/6, 4/5,       
        1, -0.5,  1, 0, 4/5,         
        -1, -0.5,  1, 0, 1/5,         
        -1,  0.5,  0, 1/6, 1/5,      

        # Z-: block bottom 
        -1, -0.5, -1, 4/6, 1/5,      
        1, -0.5, -1, 4/6, 4/5,        
        1,  0.5, 0, 3/6, 4/5,         
        -1,  0.5, 0, 3/6, 1/5,      

        # X+: block left 
        1, -0.5, -1, 3/6, 1,          
        1,  0.5, 0, 2/6, 4/5,        
        1, -0.5,  1, 1/6, 1,         

        # X-: block right  
        -1, -0.5, -1, 3/6, 1,        
        -1,  0.5, 0, 2/6, 4/5,       
        -1, -0.5,  1, 1/6, 1,         

        # Y-: yellow face
        -1, -0.5, -1, 1, 1/5,       
        1, -0.5, -1, 1, 4/5,          
        1, -0.5,  1, 4/6, 4/5,    
        -1, -0.5,  1, 4/6, 1/5,
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10,  # X+
        11,12,13,
        17, 16, 15, 15, 14, 17]

    return Shape(vertices, indices)

# Esta es la función encargada de definir los vertices e indices en que se dibujaran los triangulos 
# para crear una esfera. Recibe los parametros radio que será el radio de la esfera, N_vertical que 
# son cuantas divisiones se hará de manera vertical y N_horizontal cuantas divisones en horizontal
# como los meridianos y paralelos de la Tierra. Además, r,g,b que son los colores que tendrá esta 
# esfera con valores de 0 a 1. 
# No se le añaden las normales, ya que no queremos que la esfera del sol o de la luna sean reflejadas 
# por la luz.
def createSphere(radio, N_vertical, N_horizontal, r, g, b):
    # Tamaño de los ángulos para cada sección
    d_vertical = np.pi / (N_vertical-1)
    d_horizontal = 2* np.pi / (N_horizontal)
    puntos = []                          #puntos de la esfera
    theta = 0                            #angulo vertical
    for j in range(N_vertical):
        phi = 0                          #angulo horizontal
        for i in range(N_horizontal):    #se obtienen los valores de x, y, z con coordenadas esféricas
            x = radio * np.sin(theta) * np.cos(phi)
            y = radio * np.sin(theta) * np.sin(phi)
            z = radio * np.cos(theta)
            puntos.append((x,y,z))
            phi += d_horizontal
        theta += d_vertical

    # Se crean los arreglos que contendrán los vertices e índices de la esfera
    vertices = []
    indices = []
    # Se recorren todas las secciones verticales y horizontales
    for j in range(N_vertical-1):
        for i in range(N_horizontal):
            next_i = (i+ 1+ j * N_horizontal) % N_horizontal
            # Se extraen los 3 vertices del arreglo puntos los que formarán un triángulo
            v1 = puntos[i + (j+1) * N_horizontal]
            v2 = puntos[next_i + j * N_horizontal]
            v3 = puntos[i + j *N_horizontal]
            tl = len(indices)
            for tr in (v1,v2,v3):
                triangle = [*tr, r,g,b]
                vertices += triangle
            indices += [tl,tl+1,tl+2]
            # Une los otros 2 vertices con uno nuevo, algo así
            #v1  _____ v3
            #   |\   |
            #   | \  |
            #v4 |__\ | v2
            v4 = puntos[next_i + (j+1) * N_horizontal]
            tl = len(indices)
            for tr in (v2,v1,v4):
                triangle = [*tr, r,g,b]
                vertices += triangle
            indices += [tl,tl+1,tl+2]

    return Shape(vertices,indices)


############################################################################################
############################## FUNCION PARA LEER ARCHIVOS .OFF #############################
############################################################################################

# Función destinada a leer archivos .off que importan objetos a la escena. Recibe el nombre del 
# archivo "filename", y el color en (r,g,b) con el que se mostrará el objeto en escena.
def readOFF(filename, color):
    vertices = []
    normals= []
    faces = []

    with open(filename, 'r') as file:
        line = file.readline().strip()
        assert line=="OFF"

        line = file.readline().strip()
        aux = line.split(' ')

        numVertices = int(aux[0])
        numFaces = int(aux[1])

        for i in range(numVertices):
            aux = file.readline().strip().split(' ')
            vertices += [float(coord) for coord in aux[0:]]
        
        vertices = np.asarray(vertices)
        vertices = np.reshape(vertices, (numVertices, 3))
        normals = np.zeros((numVertices,3), dtype=np.float32)

        for i in range(numFaces):
            aux = file.readline().strip().split(' ')
            aux = [int(index) for index in aux[0:]]
            faces += [aux[1:]]
            
            vecA = [vertices[aux[2]][0] - vertices[aux[1]][0], vertices[aux[2]][1] - vertices[aux[1]][1], vertices[aux[2]][2] - vertices[aux[1]][2]]
            vecB = [vertices[aux[3]][0] - vertices[aux[2]][0], vertices[aux[3]][1] - vertices[aux[2]][1], vertices[aux[3]][2] - vertices[aux[2]][2]]

            res = np.cross(vecA, vecB)
            normals[aux[1]][0] += res[0]  
            normals[aux[1]][1] += res[1]  
            normals[aux[1]][2] += res[2]  

            normals[aux[2]][0] += res[0]  
            normals[aux[2]][1] += res[1]  
            normals[aux[2]][2] += res[2]  

            normals[aux[3]][0] += res[0]  
            normals[aux[3]][1] += res[1]  
            normals[aux[3]][2] += res[2]  

        norms = np.linalg.norm(normals,axis=1)
        normals = normals/norms[:,None]

        color = np.asarray(color)
        color = np.tile(color, (numVertices, 1))

        vertexData = np.concatenate((vertices, color), axis=1)
        vertexData = np.concatenate((vertexData, normals), axis=1)

        indices = []
        vertexDataF = []
        index = 0

        for face in faces:
            vertex = vertexData[face[0],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[1],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[2],:]
            vertexDataF += vertex.tolist()
            
            indices += [index, index + 1, index + 2]
            index += 3        

        return Shape(vertexDataF, indices)
        
#####################################################################################################
############################# FUNCIONES PARA MOSTAR TEXTO EN PANTALLA ###############################
#####################################################################################################

# Función que une los shape (forma) de los caracteres recibidos, para convertirlos en el texto requerido.
def merge(destinationShape, strideSize, sourceShape):
    # los vertices se desplazan en sus índices para los vértices del nuevo shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset/strideSize) + index for index in sourceShape.indices]

# Función que modifica/acomoda el shape recibido.
def applyOffset(shape, stride, offset):
    numberOfVertices = len(shape.vertices)//stride
    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     += offset[0]
        shape.vertices[index + 1] += offset[1]
        shape.vertices[index + 2] += offset[2]

# Función que escala los vertices del shape recibido. Además, recibimos el paso en que debemos avanzar,
# y la escala a la cual queremos dejarlos.
def scaleVertices(shape, stride, scaleFactor):
    numberOfVertices = len(shape.vertices) // stride
    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     *= scaleFactor[0]
        shape.vertices[index + 1] *= scaleFactor[1]
        shape.vertices[index + 2] *= scaleFactor[2]