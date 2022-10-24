# Modelamiento-Ciudad
Este repositorio corresponde a los archivos necesarios para modelar una ciudad típica en OpenGL.

El archivo t2p2.py es el archivo inicial en donde se corre la tarea, allí se definen las variables de inicio, la configuración de las luces, las camaras,etc. con sus transformaciones. Todo se encuentra detallado en el archivo.

El documento se realizó en 2 partes, sin embargo, acá se muestra la versión final del proyecto (incluye ambas partes).

## Parte 1

Se crea además el grafo de ubicación (es mi detalle creativo) el cual es un prisma triagular que se va trasladando y rotando según la posición de la camara de perspectiva. Por lo que al alternar entre la camara ortografica se puede ver en qué posición estamos ubicados (en donde está la cámara ortografica).

Por otro lado, en el archivo main se encuentra la función on_key que determina las acciones de las teclas en el programa. Al pulsar SPACE todas las figuras rellenas de textura se ven en lineas y viceversa. LEFT_CONTROL muestra/oculta los ejes x, y, z. Al pulsar O se activa o desactiva la vista ortografica. Además, con las teclas W, S la cámara avanza o retrocede, con A y D la cámara rota en un angulo theta, y finalmente con las flechas UP y DOWN la camara se eleva o desciende, todo esto dentro de los limites de la escena.

El archivo transformaciones muestra las matrices de traslacion, de escalación, shearing, rotación con respecto a cada eje, matmul reorganiza las marices de transformaciones, ortho de la proyección ortografica, y perspective la proyeccion de la camara en perspectiva, etc.

Los otros archivos scene_graph.py, y assets_path.py son necesario para que acceder y leer otros archivos y crear grafos de escena.

## Parte 2

Al correr la Tarea, se inicia con la vista nocturna a las 00:00 hrs cuando el auto dobla en una esquina con las luces encendidas, y se muestra en ventana la hora cada 30 minutos. El periodo de la Luna y del Sol son de 48 segundos. El auto posee un periodo diferente que el Sol y la Luna, da la vuelta en aproximadamente 68 segundos (esto varía dependiendo del valor del N, el cual debe ser un valor par, ya que algunas curvas utilizan un paso de N/2 para que la "velocidad" en las esquinas curvas no se vea tan afectada y no vaya tan lento).

Mi detalle creativo involucra a las luces del auto, cuando se encuentra en alguna esquina donde debe doblar, este "enciende" las luces rojas traseras, y se prenden ademas las luces direccionales (delanteras y traseras) para el lado que va a doblar (derecha o izquierda). Cuando es de noche y se prenden las luces delanteras que iluminan el camino, también se prenden las luces que simulan que los focos del auto se encienden. Para hacer esto, todas estas luces apuntan hacia adentro del auto (excepto por las que iluminan el camino), y solo lo afectan a este. Es por esto que para los archivos multiple_lights_textures.fs se señalan solo 13 Spotlights y en multiple_lights_color.fs se señalan 21 Spotlights que incluyen las luces del detalle creativo del auto.

Cabe destacar que estos archivos multiple_lights_textures.fs, multiple_lights_textures.vs, multiple_lights_color.fs y multiple_lights_color.vs son necesarios para crear los shader de multiples luces para objetos con texturas o con colores.

Las funciones que creaban los grafos de los objetos de las casas, del piso, etc, que antes estaban en el archivo principal ahora se trasladaron a un nuevo archivo llamado my_scene.py, allí se encuentran todas esas funciones. Además, se encuentran los postes creados, el grafo del auto, las spotlights para el auto, los postes, el sol-luna. Asimismo, se crea ahí la trayectoria del auto, con las curvas bezier. Todo se encuentra detallado en cada bloque de código.

Para definir todo lo que se encuentra en my_scene.py se necesitan otros archivos, como el de basic_shapes.py en donde se encuentran las funciones para crear las figuras de los pisos, techos, casas, postes, etc.. Ahora, se les añadieron los parametros de las normales para que estos pudieran reflejar la luz.

Otro archivo es el easy_shaders,py en donde se encuentran 5 tipos de shader: para los objetos de color o textura sin luz, para los objetos de color o textura con multiples luces, y el shader para renderizar texto y mostrarlo en pantalla.

Para mostar el texto en pantalla, en este caso la hora del día, se necesitaron de otros 2 archivos más, el text_renderer.py que crea y renderiza los shader de los caracteres y que los une en el texto requerido, y el segundo archivo que necesita text_renderer.py para funcionar es el archivo font8x8_basic.py. que crea una grilla de bits 8x8 para generar el texto.

Finalmente, cabe destacar que mi código se basó en todos los auxiliares vistos, en el material de apoyo (tarea del auto con luces, entre otros) y en los ejemplos del repositorio del curso. Además, dentro de la carpeta se incluyen imagenes del barrio que cuentan con el barrio visto en la parte 1 y en la parte 2.

PD: Todo lo demás se explica con más detalle en cada código. Sin embargo, el programa se demora en correr, y a veces se crashea haciendo que la camara de perspectiva baje más allá del límite del piso.
