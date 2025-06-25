from funciones_respuestas import *
ruta = "clase_17/datos.json"

lista_diccionarios = leer_archivo_json(ruta)
lista_indices_random = crear_lista_indices_random(10, 0, len(lista_diccionarios) - 1)
print(lista_indices_random)
variable_respuesta = "correcta"
variable_pregunta = "pregunta"
contador = 0
menu_comodines = """
[1] Llamar a un amigo
[2] Ocultar dos respuestas
[3] Cambiar pregunta

Ingrese el comodín que quiere utilizar: """

for i in range(len(lista_indices_random)):
    mostrar_pregunta(lista_diccionarios[lista_indices_random[i]], variable_pregunta)
    mostrar_respuestas_aleatorias(lista_diccionarios[lista_indices_random[i]])

    respuesta = input("Ingrese su respuesta ('0' para utilizar un comodín): ")

    if respuesta == "0":
        while True:
            opcion = input(menu_comodines)

            match opcion:
                case "1":
                    pass

                case "2":
                    print("Comodín seleccionado: Ocultar dos respuestas\n")
                    mostrar_pregunta(lista_diccionarios[lista_indices_random[i]], variable_pregunta)
                    ocultar_respuestas(lista_diccionarios[lista_indices_random[i]], "correcta")
                    respuesta = input("Ingrese su respuesta: ")
                    if comprobar_respuesta(lista_diccionarios[lista_indices_random[i]], respuesta, variable_respuesta) == True:
                        print("Respuesta correcta.")
                        contador += 1

                    else:
                        print("Respuesta incorrecta.")

                    break

                case "3":
                    nueva_pregunta = cambiar_pregunta(lista_diccionarios, lista_indices_random, 0, len(lista_diccionarios) - 1)
                    mostrar_pregunta(nueva_pregunta, variable_pregunta)
                    respuesta = input("Ingrese su respuesta: ")

                    if comprobar_respuesta(nueva_pregunta, respuesta, variable_respuesta) == True:
                        print("Respuesta correcta.")
                        contador += 1

                    else:
                        print("Respuesta incorrecta.")

                    break

                case _:
                    print("Opción inválida.")

    else:
        if comprobar_respuesta(lista_diccionarios[lista_indices_random[i]], respuesta, variable_respuesta) == True:
            print("Respuesta correcta.")
            contador += 1

        else:
            print("Respuesta incorrecta.")

    print()

print(f"Respuestas correctas: {contador}")