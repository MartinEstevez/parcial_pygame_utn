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

""" def mostrar_respuestas_aleatorias(diccionario:dict) -> None:
    
    Muestra las respuestas de cada diccionario.

    Recibe:
        - diccionario (dict): diccionario de donde se van a mostrar las respuestas.
    
    indices = crear_lista_indices_random(4, 1, 4)

    for i in range(len(indices)):
        print(f"{chr(97 + i)}) {diccionario[f'r_{indices[i]}']}") """


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
    respuestas_filtradas = []
    respuestas_incorrectas = None

    for i in range(len(lista_indices)):
        respuesta_actual = diccionario[f"r_{lista_indices[i]}"]

        if respuesta_actual == diccionario[clave]:
            respuestas_filtradas.append(respuesta_actual)

        else:
            if respuestas_incorrectas is None:
                respuestas_filtradas.append(respuesta_actual)
                respuestas_incorrectas = True

    return respuestas_filtradas

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

# ------------------------------------------- FUNCIONES NICOLÁS -------------------------------------------

def leer_archivo(ruta:str) -> str | None:
    """
    Lee el archivo si existe , si no existe lo crea vacio 
    """
    try: 
        with open(ruta, "r") as archivo:
            datos = archivo.read()
            
    except:
        archivo = open(ruta, "w")
        archivo.close()
        datos = None
    return datos



def mostrar_lista_diccionarios(lista_diccionarios:list[dict]) -> None:
    """
    """
    espacios_reservados = medir_clave_mas_larga(lista_diccionarios[0].keys()) + 5
    # espacios_reservados = 12

    imprimir_encabezado(lista_diccionarios[0].keys(), espacios_reservados)

    for i in range(len(lista_diccionarios)):
        contador = 0
        for clave in lista_diccionarios[i].keys():
            contador += 1
            if contador < len(lista_diccionarios[i].keys()):
                print(f"{lista_diccionarios[i][clave]:<{espacios_reservados}}", end=" | ")

            else:
                print(f"{lista_diccionarios[i][clave]:<{espacios_reservados}}")

def imprimir_encabezado(claves_diccionario:list, espacios_reservados:int) -> None:
    """

    """
    contador = 0
    for clave in claves_diccionario:
        contador += 1
        clave_capitalize = f"{clave}".capitalize()
        
        if contador < len(claves_diccionario):
            print(f"{clave_capitalize:^{espacios_reservados}}", end=" | ")

        else:
            print(f"{clave_capitalize:^{espacios_reservados}}")


def medir_clave_mas_larga(claves_diccionario:list) -> int:
    """
    """
    clave_mas_larga = None

    for clave in claves_diccionario:
        if clave_mas_larga == None:
            clave_mas_larga = len(clave)

        else:

            if len(clave) > clave_mas_larga:
                clave_mas_larga = len(clave)

    return clave_mas_larga

def cargar_datos(datos:str) -> list[dict]:
    """
    Modifica el texto del CSV en una lista de diccionarios (uno por jugador).
    """
    print(datos)
    lista_retorno = []
    if datos != "":
        lista_strings = datos.strip().split("\n") 
        # strip(): Limpia los espacios vacíos del principio y final del string.
        # split(): Separa un string en una lista de elementos, por el separador ingresado por parámetro.

        for i in range(len(lista_strings)):
            if i == 0:
                lista_claves = lista_strings[i].split(",")

            else:
                lista_valores = lista_strings[i].split(",")
                nombre = {}
                for j in range(len(lista_claves)):
                    nombre.update({lista_claves[j]: lista_valores[j]})

                lista_retorno.append(nombre)
    return lista_retorno

def formatear_alumnos(lista_diccionarios:list[dict]) -> str:
    """
    Modifica la lista de jugadores en un string csv para guardarlo.
    """
    retorno = ""
    
    if len(lista_diccionarios) > 0:
        retorno += ",".join(lista_diccionarios[0].keys()) + "\n"
        for i in range(len(lista_diccionarios)):
            retorno += ",".join(lista_diccionarios[i].values()) + "\n" # Se invoca desde un separador y recibe una lista, la cual une utilizando el separador.
    return retorno


def actualizar_ranking(nombre:str, nuevo_puntaje:int, ruta:str) -> None:
    """
    Actualiza el ranking guardando solo el mejor puntaje de cada jugador.
    """
    datos_csv = leer_archivo(ruta)

    if datos_csv is None or datos_csv.strip() == "":
        lista_ranking = []
    else:
        lista_ranking = cargar_datos(datos_csv)
    
    encontrado = False # busca si existe el jugador 
    for jugador in lista_ranking:
        if jugador["nombre"] == nombre:
            encontrado = True
            if int(jugador["puntaje"]) < nuevo_puntaje:
                jugador["puntaje"] = str(nuevo_puntaje)
            break

    if not encontrado:
        nuevo_jugador = {"nombre": nombre, "puntaje": str(nuevo_puntaje)}
        lista_ranking.append(nuevo_jugador)

    datos_actualizados = formatear_alumnos(lista_ranking)
    guardar_archivo(ruta, "w", datos_actualizados)


def guardar_archivo(ruta:str, modo:str, datos:str) -> None:
    """
    Guarda el archivo
    """
    with open(ruta, modo) as archivo:
        archivo.write(datos)

def ordenar_diccionarios(lista_diccionarios:list[dict], clave:str, descendente:str = False):
    """
    Ordena una lista de diccionarios, por la clave y criterio.
    """
    for i in range(len(lista_diccionarios) - 1):
        for j in range(i + 1, len(lista_diccionarios)):
            if (descendente == False and lista_diccionarios[i][clave] > lista_diccionarios[j][clave]) or (descendente == True and lista_diccionarios[i][clave] < lista_diccionarios[j][clave]):
                aux = lista_diccionarios[i]
                lista_diccionarios[i] = lista_diccionarios[j]
                lista_diccionarios[j] = aux

#def calcular_puntaje(contador: int, tiempo_respuesta: float) -> int:

def obtener_respuestas(pregunta: dict) -> list:
    indices = crear_lista_indices_random(4, 1, 4)
    respuestas = []
    for i in range(len(indices)):
        respuestas.append(pregunta[f"r_{indices[i]}"])
    return respuestas







