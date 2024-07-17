import os
import cv2
import face_recognition as fr
import numpy as np
from datetime import datetime
from Instrucciones import Instrucciones
from Menu import Menus

class Login:

    def facial(self):
        ruta = "C:\\Users\\Jhair\\PycharmProjects\\ControladorAsistenciaFace\\.venv\\Espejo\\Clases\\Empleados"  # Carpeta donde se encuentran las fotos de los empleados

        # Muestra las instrucciones de inicio de sesión
        # Instrucciones.ins_facial()

        # Limpia la pantalla
        print("\n" * 20)

        mis_imagenes = []
        nombres_empleados = []
        lista_empleados = os.listdir(ruta)

        for empleado in lista_empleados:
            imagen_actual = cv2.imread(f"{ruta}/{empleado}")
            mis_imagenes.append(imagen_actual)
            nombres_empleados.append(os.path.splitext(empleado)[0])

        def codificar(imagenes):
            lista_codificada = []  # lista vacia

            for imagen in imagenes:
                imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)  # convertir de bgr a rgb
                codificado = fr.face_encodings(imagen)[0]  # donde está la cara en la imagen
                lista_codificada.append(codificado)  # agregar a la lista codificada

            return lista_codificada

        lista_empleados_codificada = codificar(mis_imagenes)

        captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        exito, imagen = captura.read()

        if not exito:
            print("No se pudo tomar la foto")
            captura.release()
            exit()
        else:
            cara_captura = fr.face_locations(imagen)
            cara_captura_codificada = fr.face_encodings(imagen, known_face_locations=cara_captura)

            if len(cara_captura_codificada) > 0:
                caracodif = cara_captura_codificada[0]
                coincidencias = fr.compare_faces(lista_empleados_codificada, caracodif, 0.6)
                distancia = fr.face_distance(lista_empleados_codificada, caracodif)
                indice_coincidencia = np.argmin(distancia)

                if coincidencias[indice_coincidencia]:
                    caraubic = cara_captura[0]
                    nombre_empleado = nombres_empleados[indice_coincidencia]

                    # Dibujar un rectángulo alrededor de la cara en la imagen capturada
                    top, right, bottom, left = caraubic
                    cv2.rectangle(imagen, (left, top), (right, bottom), (0, 255, 0), 2)

                    # Dibujar un rectángulo alrededor de la cara en la imagen del empleado
                    imagen_reconocida = mis_imagenes[indice_coincidencia]
                    caraubic_reconocida = fr.face_locations(imagen_reconocida)[0]
                    top_r, right_r, bottom_r, left_r = caraubic_reconocida
                    cv2.rectangle(imagen_reconocida, (left_r, top_r), (right_r, bottom_r), (0, 255, 0), 2)

                    # Agregar texto con el nombre y la fecha/hora en la imagen capturada
                    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cv2.putText(imagen, f"Bienvenido {nombre_empleado}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(imagen, fecha_hora_actual, (left, top - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Redimensionar ambas imágenes a la misma dimensión
                    height, width, _ = imagen.shape
                    imagen_reconocida = cv2.resize(imagen_reconocida, (width, height))

                    # Asegurar que ambas imágenes sean del mismo tipo
                    if imagen.dtype != imagen_reconocida.dtype:
                        imagen_reconocida = imagen_reconocida.astype(imagen.dtype)

                    combinada = cv2.hconcat([imagen, imagen_reconocida])
                    cv2.imshow("Empleado Reconocido", combinada)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                    print(f"Bienvenido {nombre_empleado}")
                    input("\nPresione Enter para continuar.")
                    return True
                else:
                    #self.retry(captura)
                    return False
            else:
                #self.retry(captura)
                return False

    def retry(self, captura):
        pregunta = input("No se encontraron coincidencias. \nPresione Enter para intentar de nuevo, o X para cerrar el sistema: ").lower()
        captura.release()
        if pregunta != "x":
            self.facial()  # Llama recursivamente a la función para reintentar
        else:
            exit()  # Cierra el sistema si el usuario ingresa 'x'

    def contrasenia(self):
        # Muestra las instrucciones de inicio de sesión
        Instrucciones.ins_login()

        # Limpia la pantalla
        print("\n" * 20)

        # Credenciales de acceso predeterminadas
        usuario = "admin"
        contrasenia = "admin123"
        contraseniaInversa = contrasenia[::-1]  # Invierte la contraseña
        acceso = False

        print("---INICIO DE SESION---\n")
        # Solicita al usuario ingresar sus credenciales
        usu = input("Ingrese el usuario: ")
        intento = input("Ingresa tu contraseña: ")
        intentoInverso = intento[::-1]  # Invierte la contraseña ingresada

        # Verifica si las credenciales ingresadas coinciden con las predeterminadas
        if usu == usuario and intento == contrasenia and intentoInverso == contraseniaInversa and contraseniaInversa[2::2] == intentoInverso[2::2]:
            acceso = True
            return acceso  # Retorna True si el acceso es exitoso

        else:
            # Informa al usuario que las credenciales son incorrectas
            print("\nUsuario o contraseña incorrectos.")

            # Opción para reintentar o cerrar el sistema
            pregunta = input("Presione Enter para intentar de nuevo, o X para cerrar el sistema: ").lower()

            if pregunta != "x":
                var = self.contrasenia()  # Llama recursivamente a la función para reintentar
                return var
            else:
                return exit()  # Cierra el sistema si el usuario ingresa 'x'

    def elegir_metodo(self, opcion):
        var = False
        menus = Menus()

        if opcion == "1":
            var = self.facial()
            return var
        elif opcion == "2":
            var = self.contrasenia()
            return var
        elif opcion == "3":
            return exit()
        elif opcion != "1" and opcion != "2" and opcion != "3":
            input("\nOpcion no valida, presione Enter para intentar de nuevo.")
            m = menus.login_menu()
            self.elegir_metodo(m)