import os.path
# Archivo extraído de los auxiliares, material de apoyo, y del repositorio de ejemplos del curso.

# Función de conveniencia para acceder a los archivos de activos independientemente de dónde ejecute el script de ejemplo.
def getAssetPath(filename):
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    parentFolderPath = os.path.dirname(thisFolderPath)
    assetsDirectory = os.path.join(parentFolderPath, "assets")
    requestedPath = os.path.join(assetsDirectory, filename)
    return requestedPath
