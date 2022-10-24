import numpy as np
# Archivo extraído de los auxiliares, material de apoyo, y del repositorio de ejemplos del curso.

# Función que retorna la matriz identidad con 4 filas
def identity():
    return np.identity(4, dtype=np.float32)

# Se define la funcion que cambia el tamaño de la figura en cada dimensión x, 
# y, z de manera uniforme. Recibe el valor de escala s que es mayor a 0. Si está entre
# 0 y 1 la dimensión correspondiente se achica, y si el valor es mayor 
# a 1 se agranda. Retorna la matriz de escalación.
def uniformScale(s):
    return np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1]], dtype=np.float32)

# Se define la funcion que cambia el tamaño de la figura en cada dimensión x, 
# y, z. Recibe los valores de sx, sy, sz que son mayores a 0, si está entre
# 0 y 1 la dimensión correspondiente se achica, y si el valor es mayor 
# a 1 se agranda. Retorna la matriz de escalación.
def scale(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]], dtype=np.float32)

# Se define la función que rota la figura con respecto al eje X. Recibe un 
# ángulo theta, el cual si es mayor a 0 la figura rota en sentido antihorario
# Si es menor a 0 rota en sentido horario. Retorna la matriz de rotación en X.
def rotationX(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [1, 0, 0, 0],
        [0, cos_theta, -sin_theta, 0],
        [0, sin_theta, cos_theta, 0],
        [0, 0, 0, 1]], dtype=np.float32)

# Se define la función que rota la figura con respecto al eje Y. Recibe un 
# ángulo theta, el cual si es mayor a 0 la figura rota en sentido antihorario
# Si es menor a 0 rota en sentido horario. Retorna la matriz de rotación en Y.
def rotationY(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta, 0, sin_theta, 0],
        [0, 1, 0, 0],
        [-sin_theta, 0, cos_theta, 0],
        [0, 0, 0, 1]], dtype=np.float32)

# Se define la función que rota la figura con respecto al eje Z. Recibe un 
# ángulo theta, el cual si es mayor a 0 la figura rota en sentido antihorario
# Si es menor a 0 rota en sentido horario. Retorna la matriz de rotación en Z.
def rotationZ(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta, -sin_theta, 0, 0],
        [sin_theta, cos_theta, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]], dtype=np.float32)

# Se define la funcion que traslada la figura hasta el punto (tx, ty, tz),
# la cual recibe los valores de tx, ty, tz, y retorna en la matriz 
# de traslación.
def translate(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]], dtype=np.float32)

# Se define la funcion que distorsiona el tamaño de la figura cada 2 dimensiones, 
# recibiendo los valores de xy, yx, xz, zx, yz, zy. Retorna la matriz de shearing.
def shearing(xy, yx, xz, zx, yz, zy):
    return np.array([
        [1, xy, xz, 0],
        [yx,  1, yz, 0],
        [zx, zy,  1, 0],
        [0,  0,  0, 1]], dtype=np.float32)

# Se define la función que reordena los valores que se le entregan en un arreglo.
# Recibe un parámetro mats que es un arreglo con valores/matrices, luego es en donde 
# pone los valores en orden opuesto, el primer valor, es el último. Retornando el
# mismo arreglo pero en orden opuesto.
def matmul(mats):
    out = mats[0]
    for i in range(1, len(mats)):
        out = np.matmul(out, mats[i])

    return out

# Función que ocupa la proyeccion de perspectiva, recibe como parametros 
# los rangos de izquierda, derecha, arriba, abajo, el valor más cercano y 
# más lejano de la proyección que serán usada en la cámara.
def frustum(left, right, bottom, top, near, far):
    r_l = right - left
    t_b = top - bottom
    f_n = far - near
    return np.array([
        [2 * near / r_l,
         0,
         (right + left) / r_l,
            0],
        [0,
         2 * near / t_b,
         (top + bottom) / t_b,
            0],
        [0,
         0,
         -(far + near) / f_n,
         -2 * near * far / f_n],
        [0,
         0,
         -1,
         0]], dtype=np.float32)

# Función que determina la transformación de proyeccion de perspectiva, que recibe los parametros
# del campo de visión, el aspecto de la camara, el valor más cercano y más lejano
# de la proyección que serán usada en la cámara.
def perspective(fovy, aspect, near, far):
    halfHeight = np.tan(np.pi * fovy / 360) * near
    halfWidth = halfHeight * aspect
    return frustum(-halfWidth, halfWidth, -halfHeight, halfHeight, near, far)

# Función que determina la transformación de proyeccion ortográfica, recibe como parametros 
# los rangos de izquierda, derecha, arriba, abajo, el valor más cercano y más lejano
# de la proyección que serán usada en la cámara.
def ortho(left, right, bottom, top, near, far):
    r_l = right - left
    t_b = top - bottom
    f_n = far - near
    return np.array([
        [2 / r_l,
         0,
         0,
         -(right + left) / r_l],
        [0,
         2 / t_b,
         0,
         -(top + bottom) / t_b],
        [0,
         0,
         -2 / f_n,
         -(far + near) / f_n],
        [0,
         0,
         0,
         1]], dtype=np.float32)

# Define la matriz de visualización del programa, que recibe el arreglo de la ubicación de la cámara
# o el ojo de vista, el punto at en donde estará dirigida la vista, y up el eje que apuntará hacia arriba.
def lookAt(eye, at, up):

    forward = (at - eye)
    forward = forward / np.linalg.norm(forward)

    side = np.cross(forward, up)
    side = side / np.linalg.norm(side)

    newUp = np.cross(side, forward)
    newUp = newUp / np.linalg.norm(newUp)

    return np.array([
        [side[0],       side[1],    side[2], -np.dot(side, eye)],
        [newUp[0],     newUp[1],   newUp[2], -np.dot(newUp, eye)],
        [-forward[0], -forward[1], -forward[2], np.dot(forward, eye)],
        [0, 0, 0, 1]
    ], dtype=np.float32)
