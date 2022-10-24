# Nombre: Estefanía Muñoz Miranda
# Rut: 20281223-6
# Sección: 1

import glfw
from OpenGL.GL import *
import numpy as np
import datetime
import sys
import os.path
import libs.transformations as tr
import libs.basic_shapes as bs
import libs.easy_shaders as es
import libs.scene_graph as sg
import libs.text_renderer as tx
from libs.my_scene import *
from libs.assets_path import getAssetPath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Se crea la clase controlador que determina algunos condicionales de los cuerpos, 
# es decir, controla a la escena.
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.orthographic = False

# Se usa la clase controlador, la cual será llamada más adelante para transformar los objetos
controller = Controller()

# Modificamos esta función para poder configurar todas las luces del pool
def setPlot(texPipeline, lightPipeline, projection):
    # Como tenemos 2 shaders con múltiples luces, tenemos que enviar toda esa información a cada shader
    # Primero al shader de color
    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    # Enviamos la información de la luz puntual y del material
    # La luz puntual está desactivada (su componente ambiente es 0.0, 0.0, 0.0), porque utilizaremos la componente 
    # ambiente en las 2 spotlights de Sol y Luna.
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].ambient"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.ambient"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.diffuse"), 0.8, 0.8, 0.8)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "material.shininess"), 32)

    # Aprovechamos que las luces spotlight están almacenadas en el diccionario para mandarlas al shader
    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)
    
    # Ahora repetimos todo el proceso para el shader de texturas con múltiples luces
    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    # La luz puntual está desactivada (su componente ambiente es 0.0, 0.0, 0.0), porque utilizaremos la componente 
    # ambiente en las 2 spotlights de Sol y Luna.
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].ambient"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.ambient"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "material.shininess"), 32)

    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

# Controla las acciones de las teclas pulsadas mientras el programa corre
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_O:
        controller.orthographic = not controller.orthographic

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


# Se define la función main, la cual es la que se ejecuta al momento de correr el archivo en la terminal.
def main():
    # Se inicializa glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Alto y ancho de la ventana
    width = 600
    height = 600

    # Se crea la ventana con las dimesiones en pixeles previamente definidas
    window = glfw.create_window(width, height, "Tarea 2 Parte 2: Opción 2 Barrio Genérico", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Conecta la función con las acciones del teclado
    glfw.set_key_callback(window, on_key)

    # Creación de los shader para texturas y colores sin luces, texturas y colores con multiples luces,
    # y para el renderizado de texto en ventana.
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    colorLightingProgram = es.MultipleLightPhongShaderProgram()
    lightingPipeline = es.MultipleLightTexturePhongShaderProgram()
    textPipeline = es.TextureTextRendererShaderProgram()

    # Se le asigna un color rgb al fondo de la ventana
    glClearColor(0.46, 0.65, 0.79, 1.0)

    # Al trabajar en 3D, se debe verificar qué parte está al frente y cuál está en la parte de atrás
    glEnable(GL_DEPTH_TEST)

    # Se crean los ejes en la memoria GPU
    cpuAxis = bs.createAxis(30)
    gpuAxis = es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    # Acá se configuran las luces llamando a la función en donde las definimos, y creamos el grafo de las 
    # escenas 3D del barrio, el grafo de la ubicación, el grafo de Sol y Luna, y finalmente el del auto, 
    # todo esto en la memoria GPU.
    setLights()
    dibujo = createScene(lightingPipeline)
    ubicacion = createUbicacion(textureShaderProgram)
    solyluna = createSol_Luna(colorShaderProgram)
    car = createCarScene(colorLightingProgram)

    # Se define el N como parametro de la curva (mientras más bajo el valor más rapido va el auto, debe ser 
    # un valor par, ya que algunas curvas utilizan un paso de N//2), se crea la trayectoria C del auto, y 
    # se añade un contador step que indica cuanto tramo ha avanzado el auto.
    N = 80
    C = generateCurveT5(N)
    step = 0

    # Se crea la textura de todos los caracteres y se mueve a la memoria GPU
    textBitsTexture = tx.generateTextBitsTexture()
    gpuText3DTexture = tx.toOpenGLTexture(textBitsTexture)

    # Se definen los parametros del texto que se mostrará en pantalla, en este caso son las horas del día
    # cada 30 minutos, (cada 30 minutos de la escena hay 1 segundo de tiempo normal, por lo que el periodo 
    # del sol o de la luna es de 48 segundos.)
    timeCharSize = 0.05
    timeCharSize2 = 0.04
    contador_horas = 0
    periodo_segundos = 48
    horas = ["00:00","00:30","01:00","01:30","02:00","02:30","03:00","03:30","04:00","04:30",
            "05:00","05:30","06:00","06:30","07:00","07:30","08:00","08:30","09:00","09:30",
            "10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30",
            "15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30",
            "20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"]
    timeShape = tx.textToShape(horas[contador_horas], timeCharSize2, timeCharSize)
    gpuTime = es.GPUShape().initBuffers()
    textPipeline.setupVAO(gpuTime)
    gpuTime.fillBuffers(timeShape.vertices, timeShape.indices, GL_STATIC_DRAW)
    gpuTime.texture = gpuText3DTexture

    # Se obtiene un segundo
    now = datetime.datetime.now()
    second = now.second

    # Se obtiene el tiempo de inicio del programa
    t0 = glfw.get_time()

    # Parametros iniciales de posición y ángulos de la cámara, del sol y de la luna
    camera_pos = np.array([6, 0.5, -13])
    camera_radius = 2
    camera_theta = np.pi/2
    sol_theta = -np.pi/2
    luna_theta = np.pi/2
    # Variables auxiliares que nos ayudarán a definir cuando se prenden o se apagan ciertas luces.
    luz1 = 1
    luz2 = 0
    luzP = 1
    luzf = 0
    angle = np.arctan2(C[step+1,0]-C[step,0], C[step+1,2]-C[step,2])

    # Se obtienen las posiciones y las direcciones de todas las luces del auto (delanteras, traseras, 
    # direccionales, etc.) y se guardan en 2 arreglos light_pos y dir_Iniciales para manipularlas en 
    # el bucle.
    light1pos = np.append(spotlightsPool['spot12'].position, 1)
    light2pos = np.append(spotlightsPool['spot13'].position, 1)
    dir_inicial = np.append(spotlightsPool['spot12'].direction, 1)

    lightT1pos = np.append(spotlightsPool['spot14'].position, 1)
    lightT2pos = np.append(spotlightsPool['spot15'].position, 1)
    lightDT1pos = np.append(spotlightsPool['spot16'].position, 1)
    lightDT2pos = np.append(spotlightsPool['spot17'].position, 1)
    dir_inicialT = np.append(spotlightsPool['spot14'].direction, 1)

    lightD1pos = np.append(spotlightsPool['spot18'].position, 1)
    lightD2pos = np.append(spotlightsPool['spot19'].position, 1)
    dir_inicialD1 = np.append(spotlightsPool['spot18'].direction, 1)
    dir_inicialD2 = np.append(spotlightsPool['spot19'].direction, 1)
    lightDD1pos = np.append(spotlightsPool['spot20'].position, 1)
    lightDD2pos = np.append(spotlightsPool['spot21'].position, 1)
    dir_inicialDD = np.append(spotlightsPool['spot20'].direction, 1)

    light_Pos = [light1pos,light2pos,lightT1pos,lightT2pos,lightDT1pos,lightDT2pos,
                lightD1pos,lightD2pos,lightDD1pos,lightDD2pos]
    dir_Iniciales = [dir_inicial,dir_inicial,dir_inicialT,dir_inicialT,dir_inicialT,
                dir_inicialT,dir_inicialD1,dir_inicialD2,dir_inicialDD,dir_inicialDD]

    # Mientras no se cierre la ventana esto sigue iterando
    while not glfw.window_should_close(window):
        # Uso de glfw para verificar eventos de entrada
        glfw.poll_events()

        # Se obtiene la diferencia de tiempo en segundos de cada iteración
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Se verifica si está activado el comando para utilizar la camara es ortografica
        if (controller.orthographic):
            camera_theta_1 = 20*np.pi/10
            camera_phi = 2*np.pi/5
            projection = tr.ortho(-25, 30, -25, 30, 0.1, 100) #limites de vista
            a = 30*np.sin(camera_theta_1)*np.cos(camera_phi)
            b = 30*np.cos(camera_theta_1)
            c = 30*np.sin(camera_theta_1)*np.sin(camera_phi)
            viewPos = np.array([a, b, c]) #(posicion camara)
            at = np.array([0,0,0])        #hacia a donde mira
        # Si no está activado, se utiliza la camara de perspectiva
        else:
            projection = tr.perspective(60, float(width)/float(height), 0.1, 150)
            # Si se presiona la tecla A o D la camara rota en un angulo theta
            if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
                camera_theta -= 2 * dt
            if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
                camera_theta += 2* dt
            # Si se presiona W o S la camara avanza o retrocede segun el caso dentro de los limites de la escena
            if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
                a = camera_pos[0]
                b = camera_pos[2]
                if((-20.25< a+np.cos(camera_theta)*dt*3 <3.25) and (-14.1< b+np.sin(camera_theta)*dt*3 <6.25)):
                    camera_pos[0] += np.cos(camera_theta) * dt * 3
                    camera_pos[2] += np.sin(camera_theta) * dt * 3
                elif((6.25<b+np.sin(camera_theta)*dt*3 <26.75) and (a + np.cos(camera_theta)*dt*3< (-0.7*(b-6.25)+17.6))and(-20.25< a + np.cos(camera_theta) * dt * 3)):
                    camera_pos[0] += np.cos(camera_theta) * dt * 3
                    camera_pos[2] += np.sin(camera_theta) * dt * 3
                elif((-14.1< b+np.sin(camera_theta)*dt*3 <6.25) and (-20.25< a+np.cos(camera_theta)*dt*3 <17.6)):
                    camera_pos[0] += np.cos(camera_theta) * dt * 3
                    camera_pos[2] += np.sin(camera_theta) * dt * 3
                    
            if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
                a = camera_pos[0]
                b = camera_pos[2]
                if((-20.25< a-np.cos(camera_theta)*dt*3 <3.25) and (-14.1< b-np.sin(camera_theta)*dt*3 <6.25)):
                    camera_pos[0] -= np.cos(camera_theta) * dt * 3
                    camera_pos[2] -= np.sin(camera_theta) * dt * 3
                elif((6.25<b-np.sin(camera_theta)*dt*3 <26.75) and (a-np.cos(camera_theta)*dt*3< (-0.7*(b-6.25)+17.6))and(-20.25< a-np.cos(camera_theta) * dt * 3)):
                    camera_pos[0] -= np.cos(camera_theta) * dt * 3
                    camera_pos[2] -= np.sin(camera_theta) * dt * 3
                elif((-14.1< b-np.sin(camera_theta)*dt*3 <6.25) and (-20.25<a-np.cos(camera_theta)*dt*3 <17.6)):
                    camera_pos[0] -= np.cos(camera_theta) * dt * 3
                    camera_pos[2] -= np.sin(camera_theta) * dt * 3

            # Si se presiona arriba o abajo la camara se eleva o desciende dependiendo del caso sin traspasar el piso
            if ((glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS) and (10 > camera_pos[1])):
                camera_pos[1] +=  dt * 2

            if ((glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS) and (0.1 < camera_pos[1])):
                camera_pos[1] -=  dt * 2
            a = camera_pos[0] + np.cos(camera_theta) * camera_radius
            b = camera_pos[1] 
            c = camera_pos[2] + np.sin(camera_theta) * camera_radius
            viewPos = camera_pos # tambien llamado eye
            at = np.array([a,b,c])

        # Parametros de la matriz de vista
        up = np.array([0,1,0])

        # Actualizar la matriz de vista
        view = tr.lookAt(
            viewPos,
            at,
            up
        )
        ## Ahora modificaremos los parametros de posicion, dirección, y encendido o apagado de la luz del sol y de la luna.
        # Luna
        luna_theta -= (np.pi/24)*dt
        if(13<=contador_horas<=30):
            if(luz1-(1/10)*dt>0):
                luz1 -= (1/10)*dt
            else:
                luz1 = 0
        else:
            if(luz1+(1/10)*dt<1):
                luz1 += (1/10)*dt
            else:
                luz1 = 1
        spotlightsPool['spot1'].position = np.array([-1.25+50*np.cos(luna_theta), 50*np.sin(luna_theta), 6.25])
        spotlightsPool['spot1'].direction = np.array([-1*np.cos(luna_theta), -1*np.sin(luna_theta), 0])
        spotlightsPool['spot1'].ambient = np.array([luz1*0.3, luz1*0.3, luz1*0.3])
        spotlightsPool['spot1'].diffuse = np.array([luz1, luz1, luz1])
        spotlightsPool['spot1'].specular = np.array([luz1, luz1, luz1])

        # Sol
        sol_theta -= (np.pi/24)*dt
        if(13<=contador_horas<=30):
            if(luz2+(1/10)*dt<1):
                luz2 += (1/10)*dt
            else:
                luz2 = 1
        else:
            if(luz2-(1/10)*dt>0):
                luz2 -= (1/10)*dt
            else:
                luz2 = 0
        spotlightsPool['spot2'].position = np.array([-1.25+50*np.cos(sol_theta), 50*np.sin(sol_theta), 6.25])
        spotlightsPool['spot2'].direction = np.array([-1*np.cos(sol_theta), -1*np.sin(sol_theta), 0])
        spotlightsPool['spot2'].ambient = np.array([luz2*0.7, luz2*0.7, luz2*0.7])     
        spotlightsPool['spot2'].diffuse = np.array([luz2, luz2, luz2])
        spotlightsPool['spot2'].specular = np.array([luz2*0.2, luz2*0.2, luz2*0.2])
        
        # Ahora configuraremos las luces de los postes para que de manera gradual se apaguen antes de
        # las 8 de la mañana y se enciendan despues de las 6 de la tarde. Se utiliza el contador de horas.
        if(11<=contador_horas<=36):
            if(luzP-(1/4)*dt>0):
                luzP -= (1/4)*dt
            else:
                luzP = 0
        else:
            if(luzP+(1/4)*dt<1):
                luzP += (1/4)*dt
            else:
                luzP = 1
        for i in range(13):
            if (i <11):
                spotlightsPool['spot'+str(i+3)].diffuse = np.array([luzP, luzP, luzP])
                spotlightsPool['spot'+str(i+3)].specular = np.array([luzP, luzP, luzP])
            else:
                # Acá se configuran las luces delanteras del auto, para que se apaguen y se enciendan en el 
                # mismo momento de manera gradual al igual que los postes de luz.
                spotlightsPool['spot'+str(i+7)].diffuse = np.array([luzP, luzP, luzP])
                spotlightsPool['spot'+str(i+7)].specular = np.array([luzP, luzP, luzP])
        
        # Acá se configuras las otras luces de los autos, las luces traseras rojas, y direccionales delanteras y traseras.
        # Se verifica que esten en alguna esquina o curva de doblada. Si es así se prenden las luces rojas, y las luces 
        # amarillas se encienden y se apagan en algún intervalo de pasos.
        if (not(((N//2)*2<step<(N//2)*3) or ((N//2)*4<step<(N//2)*4+N) or ((N//2)*5+N<step<(N//2)*5+N*2) 
            or ((N//2)*6+N*2<step<(N//2)*6+N*3) or ((N//2)*7+N*4<step<(N//2)*7+N*5) or ((N//2)*8+N*6<step<(N//2)*8+N*7))):
            luzT = 1
            if (step%(N//10) <= 5):
                luzDD = 0
                luzDI = 0
            else:
                if(step>(N//2)*7+N*5):
                    luzDI = 1
                    luzDD = 0
                else:
                    luzDI = 0
                    luzDD = 1
        else:
            luzT = 0
            luzDD = 0
        for i in range(2):
                spotlightsPool['spot'+str(i+14)].diffuse = np.array([luzT, 0, 0])
                spotlightsPool['spot'+str(i+14)].specular = np.array([luzT, luzT, luzT])
        spotlightsPool['spot16'].diffuse = np.array([luzDI, luzDI, 0])
        spotlightsPool['spot16'].specular = np.array([luzDI, luzDI, luzDI])
        spotlightsPool['spot17'].diffuse = np.array([luzDD, luzDD, 0])
        spotlightsPool['spot17'].specular = np.array([luzDD, luzDD, luzDD])

        spotlightsPool['spot20'].diffuse = np.array([luzDI, luzDI, 0])
        spotlightsPool['spot20'].specular = np.array([luzDI, luzDI, luzDD])
        spotlightsPool['spot21'].diffuse = np.array([luzDD, luzDD, 0])
        spotlightsPool['spot21'].specular = np.array([luzDD, luzDD, luzDD])

        # Se configura el color del fondo, para que se oscurezca cuando llegue la noche, y se aclare cuando
        # llegue el día.
        if(10<=contador_horas<=33):
            if(luzf+(1/10)*dt<1):
                luzf += (1/10)*dt
            else:
                luzf = 1
        else:
            if(luzf-(1/10)*dt>0.2):
                luzf -= (1/10)*dt
            else:
                luzf = 0.2
        glClearColor(luzf*0.46,luzf*0.65, luzf*0.79, 1.0)

        # Se limpia la pantalla en color y en profundidad.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Evalúa si se rellenan las figuras con su textura dependiendo del valor del controlador
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Si el controlador lo indica se dibujan los ejes, sino, no lo hace.
        if (controller.showAxis):
            # Drawing axes (no texture)
            glUseProgram(colorShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            colorShaderProgram.drawCall(gpuAxis, GL_LINES)

        # Acá se verifica si ha pasado un segundo, si es así se actualiza la hora y la muestra en pantalla
        now = datetime.datetime.now()
        timeShape = tx.textToShape(horas[contador_horas], timeCharSize2, timeCharSize)
        gpuTime.fillBuffers(timeShape.vertices, timeShape.indices, GL_STREAM_DRAW)
        if now.second != second:
            if (contador_horas == (periodo_segundos-1)):
                contador_horas = 0
            else:
                contador_horas += 1
            second = now.second
        glUseProgram(textPipeline.shaderProgram)
        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "fontColor"), 0,0,0,1)
        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "backColor"), 0.85,0.85,0.65,1)
        glUniformMatrix4fv(glGetUniformLocation(textPipeline.shaderProgram, "transform"), 1, GL_TRUE,tr.translate(-0.9, -0.9, 0))
        textPipeline.drawCall(gpuTime)

        #  Acá se dibuja el GPS, con la escena 3D de las casas y se configuran las luces del pool
        setPlot(lightingPipeline,colorLightingProgram, projection)
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        ubicacion.transform = tr.matmul([tr.translate(camera_pos[0],15,camera_pos[2]),tr.rotationY(-camera_theta),tr.rotationZ(-np.pi/2)])
        sg.drawSceneGraphNode(ubicacion, textureShaderProgram, "model")
        glUseProgram(lightingPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        sg.drawSceneGraphNode(dibujo, lightingPipeline, "model")

        # Se actualiza la posición del sol y la luna y se dibujan en pantalla
        lightLuna = sg.findNode(solyluna, "Luna")
        lightSol = sg.findNode(solyluna, "Sol")
        lightLuna.transform = tr.translate(spotlightsPool['spot1'].position[0],spotlightsPool['spot1'].position[1],spotlightsPool['spot1'].position[2])
        lightSol.transform = tr.translate(spotlightsPool['spot2'].position[0],spotlightsPool['spot2'].position[1],spotlightsPool['spot2'].position[2])
        glUseProgram(colorShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(solyluna, colorShaderProgram, "model")

        # Se configura la posicón del auto para que avance según se describe en la trayectoria C, y además se configuran las
        # luces del auto para que se mantengan en la posición dada del auto. 
        for i in range(10):
            spotlightsPool['spot'+str(i+12)].direction = tr.matmul([tr.rotationY(angle), dir_Iniciales[i]])
            spotlightsPool['spot'+str(i+12)].position = tr.matmul([tr.translate(C[step,0], C[step,1], C[step,2]),tr.rotationY(angle), light_Pos[i]])
        
        carNode = sg.findNode(car, "system-car")
        carNode.transform = tr.matmul([tr.translate(C[step,0], C[step,1], C[step,2]), tr.rotationY(angle)])
        glUseProgram(colorLightingProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(colorLightingProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(colorLightingProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(car, colorLightingProgram, "model")
        # Cantidad de curvas que tienen un paso de N 
        CurvasN = 15
        # Cantidad de curvas que tienen un paso de N//2
        CurvasN_2 = 8
        # Se aumenta el paso, para que el auto avance en la siguente iteración
        step = step + 1
        # Si el auto llegó al final de la curva el paso vuelve a ser 0 para que parte desde el inicio
        if step > N*(CurvasN-CurvasN_2)+(N//2)*(CurvasN_2)-2:
            step = 0
        # Caso especial: cuando cada curva termina su step N-1, el angulo se repite con el step anterior
        elif ((step%N==(N-1)) or (step%(N//2)==(N//2 - 1))):
            angle = np.arctan2(C[step,0]-C[step-1,0],C[step,2]-C[step-1,2])
        # En otro caso se calcula el angulo correspondiente
        elif step < N*(CurvasN-CurvasN_2)+(N//2)*(CurvasN_2)-1:
            angle = np.arctan2(C[step+1,0]-C[step,0], C[step+1,2]-C[step,2])

        # Con el renderizado listo de las figuras, se muestra la escena completa en la ventana
        glfw.swap_buffers(window)

    # Se limpian las figuras creadas en la memoria GPU (se libera la memoria).
    gpuAxis.clear()
    dibujo.clear()
    ubicacion.clear()
    gpuTime.clear()
    solyluna.clear()
    car.clear()

    glfw.terminate()
    return 0


if __name__ == "__main__":
    main()
