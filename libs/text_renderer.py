# Archivo extraído del repositorio del curso del ejemplo ex_text_renderer.py

from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import libs.basic_shapes as bs
import libs.font8x8_basic as f88

# Funcion que identifica bits del mapa
def toBit(number, bit):
    return int((number & bit) != 0)

# Función que crea la "textura" de todos los caracteres, en el mapa de bits 8x8,
# utiliza la funcion toBit.
def generateTextBitsTexture():
    assert f88.font8x8_basic.shape == (128,8)
    bits = np.zeros(shape=(8,8,128), dtype=np.uint8)
    for k in range(128):
        for i in range(8):
            row = f88.font8x8_basic[k, i]
            bits[0, i, k] = toBit(row, 1)
            bits[1, i, k] = toBit(row, 2)
            bits[2, i, k] = toBit(row, 4)
            bits[3, i, k] = toBit(row, 8)
            bits[4, i, k] = toBit(row, 16)
            bits[5, i, k] = toBit(row, 32)
            bits[6, i, k] = toBit(row, 64)
            bits[7, i, k] = toBit(row, 128)

    return bits

# Manda a la textura previamente creada con la función 
# generateTextBitsTexture() a la memoria GPU.
def toOpenGLTexture(textBitsTexture):
    assert textBitsTexture.shape == (8, 8, 128)
    data = np.copy(textBitsTexture)
    data.reshape((8*8*128,1), order='C')
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_3D, texture)
    # texture wrapping params
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    # texture filtering params
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage3D(GL_TEXTURE_3D, 0, GL_RED, 128, 8, 8, 0, GL_RED, GL_UNSIGNED_BYTE, data)

    return texture

# Se obtiene el shape (forma) del caracter char recibido.
def getCharacterShape(char):
    # Obtiene el valor del código ASCII de un caracter.
    k = ord(char)
    # Se crean los vértices entre 0 y 1 en (x,y,0)
    vertices = [
        # space, texture
        0, 0, 0, k, 8, 0, \
        1, 0, 0, k, 8, 8, \
        1, 1, 0, k, 0, 8, \
        0, 1, 0, k, 0, 0
    ]
    indices = [
        0,1,2,\
        2,3,0
    ]
    return bs.Shape(vertices, indices)

# Crea el shape (forma) del texto "text" recibido, utiliza la función getCharacterShape()
# para obtener el shape de cada caracter. También recibe los parametros, charWidth, charHeight
# que son el tamaño de ancho y alto que tendrá cada caracter.
def textToShape(text, charWidth, charHeight):
    shape = bs.Shape([],[])

    for i in range(len(text)):
        char = text[i]
        charShape = getCharacterShape(char)
        bs.applyOffset(charShape, 6, [i, 0, 0])
        bs.scaleVertices(charShape, 6, [charWidth, charHeight, 1])
        bs.merge(shape, 6, charShape)

    return shape


