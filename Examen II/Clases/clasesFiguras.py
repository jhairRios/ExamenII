import os

class figuras:

    def areas(self):
        r = float(input("Ingrese el radio:"))
        circ= 2*3.1416*r
        esf=  (4*3.1416)*(r*r)
        print("El area del circulo es: ",circ,"El area de la esfera es: ",esf)
        return 0

    def volumen(self):
        r = float(input("Ingrese el radio:"))
        esf = (4 * (3.1416)*(r*r*r))/3
        print("El volumen de la esfera es: ",esf)
        return 0
