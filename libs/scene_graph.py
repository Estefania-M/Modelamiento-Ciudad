from OpenGL.GL import *
import numpy as np
import libs.transformations as tr
import libs.easy_shaders as gs
# Archivo extraído del aux 5, 6 y del repositorio de ejemplos del curso.

# Se crea la clase para manejar un escenario gráfico. Cada nodo representa un grupo de objetos.
# Cada hoja representa una figura básica (GPUShape)
# Para identificar cada nodo correctamente, debe tener un nombre único
class SceneGraphNode:
    def __init__(self, name):
        self.name = name
        self.transform = tr.identity()
        self.childs = []
    # Se libera la memoria GPU
    def clear(self):
        for child in self.childs:
            child.clear()

# Se define la función para dibujar los nodos de la escena
def drawSceneGraphNode(node, pipeline, transformName, parentTransform=tr.identity()):
    assert(isinstance(node, SceneGraphNode))

    # Componer las transformaciones a través de este camino
    newTransform = np.matmul(parentTransform, node.transform)

    # Si el nodo secundario es una hoja, debe ser GPUShape.
    # Por lo tanto, se puede dibujar con drawCall
    if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
        leaf = node.childs[0]
        glUniformMatrix4fv(glGetUniformLocation(
            pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
        pipeline.drawCall(leaf)

    # Si el nodo secundario no es una hoja, DEBE ser un SceneGraphNode,
    # por lo que esta función de dibujo se llama recursivamente
    else:
        for child in node.childs:
            drawSceneGraphNode(child, pipeline, transformName, newTransform)

def findNode(node, name):

    # The name was not found in this path
    if isinstance(node, gs.GPUShape):
        return None

    # This is the requested node
    if node.name == name:
        return node
    
    # All childs are checked for the requested name
    for child in node.childs:
        foundNode = findNode(child, name)
        if foundNode != None:
            return foundNode

    # No child of this node had the requested name
    return None