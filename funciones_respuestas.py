import json
import random

# Función para leer un archivo .json
def leer_archivo_json(ruta:str) -> list[dict]:
    """
    Esta función se encarga de leer un archivo .json() y devuelve su contenido.

    Recibe:
        - ruta (str): ruta del archivo que se va a leer.

    Devuelve:
        - lista_contenido (list[dict]): contenido del archivo.
    """
    # Abrimos el archivo, indicando la ruta y el modo de apertura, en este caso es "r" (read / lectura).
    with open(ruta, "r") as archivo:
        lista_contenido = json.load(archivo) 

    return lista_contenido

def crear_lista_indices_random(cantidad_indices:int, minimo:int, maximo:int) -> list:
    """
    Crea una lista de índices de manera aleatoria.

    Recibe:
        - cantidad_indices (int): cantidad de índices que va a contener la lista.
        - minimo (int): número mínimo límite que puede ser el índice.
        - maximo (int): número máximo límite que puede ser el índice.

    Devuelve:
        - lista_indices (list): lista de índices aleatorios.
    """

    lista_indices = []
    for i in range(cantidad_indices):
        indice = random.randint(minimo, maximo)

        if i == 0:
            lista_indices.append(indice)

        else:
            while verificar_repeticion(lista_indices, indice) == True:
                indice = random.randint(minimo, maximo)
            lista_indices.append(indice)

    return lista_indices

def verificar_repeticion(lista:list, numero:int) -> bool:
    """
    Verifica si se repite el número ingresado por parámetro dentro de la lista.

    Recibe:
        - lista (list): lista a verificar.
        - numero (int): número a verificar dentro de la lista.

    Devuelve:
        - repetido (bool): True en caso de que el número ya exista dentro de la lista, False caso contrario.
    """
    repetido = False
    for i in range(len(lista)):
        if numero == lista[i]:
            repetido = True
            break

    return repetido

def mostrar_pregunta(diccionario:dict, clave:str) -> None:
    """ 
    Muestra las preguntas de cada diccionario dentro de la lista, de manera aleatoria.

    Recibe:
        - diccionario (dict): lista de diccionarios, donde se encuentran las preguntas a mostrar.
        - clave (str): clave a utilizar en cada diccionario.
    """
    print(diccionario[clave])

def mostrar_respuestas_aleatorias(diccionario:dict) -> None:
    """
    Muestra las respuestas de cada diccionario.

    Recibe:
        - diccionario (dict): diccionario de donde se van a mostrar las respuestas.
    """
    indices = crear_lista_indices_random(4, 1, 4)

    for i in range(len(indices)):
        print(f"{chr(97 + i)}) {diccionario[f'r_{indices[i]}']}")


def comprobar_respuesta(diccionario:dict, respuesta:str, clave:str) -> bool:
    """
    Compara si la respuesta es igual a la respuesta correcta, buscando dentro del diccionario.

    Recibe:
        - diccionario (dict): diccionario para sacar la respuesta correcta.
        - respuesta (str): respuesta a comparar.
        - clave (str): clave del diccionario donde se encuentra la respuesta correcta.

    Devuelve:
        - respuesta_correcta (bool): True en caso de que la respuesta sea la correcta, False caso contrario.
    """
    respuesta_correcta = False # Bandera
    correcta_lower = f"{diccionario[clave]}".strip().lower() 

    if respuesta.strip().lower() == correcta_lower:
        respuesta_correcta = True

    return respuesta_correcta

# ------------------------------------------- COMODINES -------------------------------------------
# COMODÍN DE OCULTAR RESPUESTAS
def ocultar_respuestas(diccionario:dict, clave:str) -> list:
    """
    Comodín de ocultar dos respuestas incorrectas aleatoriamente.
    """
    lista_indices = crear_lista_indices_random(4, 1, 4)
    respuestas_incorrectas = None

    for i in range(len(lista_indices)):
        if diccionario[f"r_{lista_indices[i]}"] == diccionario[clave]:
            print(diccionario[f"r_{lista_indices[i]}"])

        else:
            if respuestas_incorrectas == None:
                print(diccionario[f"r_{lista_indices[i]}"])
                respuestas_incorrectas = True

# COMODÍN DE CAMBIAR PREGUNTA
def cambiar_pregunta(lista_diccionarios:list[dict], lista_indices:list, minimo:int, maximo:int) -> dict:
    """
    Comodín de cambio de pregunta.
    """
    nuevo_indice = random.randint(minimo, maximo)
    while verificar_repeticion(lista_indices, nuevo_indice) == True:
        nuevo_indice = random.randint(minimo, maximo)

    nueva_pregunta = lista_diccionarios[nuevo_indice]
    return nueva_pregunta                