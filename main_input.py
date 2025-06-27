from funciones_respuestas import *

ruta = "datos.json"
ruta_csv = "archivo.csv"

# VARIABLES
variable_respuesta = "correcta"
variable_pregunta = "pregunta"

# LISTAS
lista_diccionarios = leer_archivo_json(ruta)
datos_csv = leer_archivo(ruta_csv)
# Si el archivo CSV está vacío, inicializar la lista de jugadores
if datos_csv== None:
    lista_jugadores = []
else:   # Si el archivo CSV no está vacío, cargar los datos existentes
    lista_jugadores = cargar_datos(datos_csv)

# MENSAJES
menu_comodines = """
[1] Llamar a un amigo
[2] Ocultar dos respuestas
[3] Cambiar pregunta

Ingrese el comodín que quiere utilizar: """

while True:
    lista_indices_random = crear_lista_indices_random(2, 0, len(lista_diccionarios) - 1)
    contador_correctas = 0
    acumuludador_puntaje_total = 0
    comodines = True
    nombre_jugador = input("Ingrese nombre: ")
    puntaje_base = 60
    

    for i in range(len(lista_indices_random)):
        correcta = False
        mostrar_pregunta(lista_diccionarios[lista_indices_random[i]], variable_pregunta)
        mostrar_respuestas_aleatorias(lista_diccionarios[lista_indices_random[i]])

        if comodines == True:
            respuesta = input("Ingrese su respuesta ('0' para utilizar un comodín): ")

        else:
            respuesta = input("Ingrese su respuesta (no tienes comodines disponibles): ")

        if respuesta == "0" and comodines == True:
            while True:
                comodines = False
                opcion = input(menu_comodines)

                match opcion:
                    case "1":
                        print("Comodín seleccionado: Llamar a un amigo\n")
                        llamar_amigo(lista_diccionarios[lista_indices_random[i]], "correcta")       

                    case "2":
                        print("Comodín seleccionado: Ocultar dos respuestas\n")
                        mostrar_pregunta(lista_diccionarios[lista_indices_random[i]], variable_pregunta)
                        ocultar_respuestas(lista_diccionarios[lista_indices_random[i]], "correcta")
                        respuesta = input("Ingrese su respuesta: ")
                        if comprobar_respuesta(lista_diccionarios[lista_indices_random[i]], respuesta, variable_respuesta) == True:
                            print("Respuesta correcta.")
                            contador_correctas += 1
                            correcta = True
                            
                        else:
                            print("Respuesta incorrecta.")

                        break

                    case "3":
                        nueva_pregunta = cambiar_pregunta(lista_diccionarios, lista_indices_random, 0, len(lista_diccionarios) - 1)
                        mostrar_pregunta(nueva_pregunta, variable_pregunta)
                        mostrar_respuestas_aleatorias(nueva_pregunta)
                        respuesta = input("Ingrese su respuesta: ")

                        if comprobar_respuesta(nueva_pregunta, respuesta, variable_respuesta) == True:
                            print("Respuesta correcta.")
                            contador_correctas += 1
                            correcta = True

                        else:
                            print("Respuesta incorrecta.")

                        break

                    case _:
                        print("Opción inválida.")
                        
        else:
            if comprobar_respuesta(lista_diccionarios[lista_indices_random[i]], respuesta, variable_respuesta) == True:
                print("Respuesta correcta.")
                contador_correctas += 1
                correcta = True

            else:
                print("Respuesta incorrecta.")
        tiempo_respuesta = int(input("Ingrese el tiempo de respuesta: "))
        if correcta == True:
            acumuludador_puntaje_total += (lambda p,t:p//t)(puntaje_base, tiempo_respuesta)#calcula el puntaje base dividido por el tiempo de respuesta
        print()
    procentaje_respuestas_correctas = (lambda c,t:c/t*100)(contador_correctas, len(lista_indices_random))#calcula el porcentaje de respuestas correctas
    procentaje_respuestas_correctas = str(procentaje_respuestas_correctas)
    acumuludador_puntaje_total = str(acumuludador_puntaje_total)
    contador_correctas = str(contador_correctas)
    lista_jugadores.append({"nombre":nombre_jugador,"porcentaje":procentaje_respuestas_correctas,"puntaje":acumuludador_puntaje_total})

    
    seguir_jugando = input("Quiere seguir jugando (si/no):  ") 
    while seguir_jugando != "no" and seguir_jugando != "si":
        print("Lo ingresado no es válido.")
        seguir_jugando = input("Quiere seguir jugando (si/no):  ") 

    if seguir_jugando == "no":
        print("Saliendo del programa..")
        break



print("Fin del juego.")
ordenar_diccionarios(lista_jugadores, "puntaje", descendente=True)
guardar_archivo (ruta_csv,"w",formatear_alumnos(lista_jugadores))
print("Puntajes guardados correctamente.")