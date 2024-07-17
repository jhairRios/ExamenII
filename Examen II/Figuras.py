import os
import sys
sys.path.append('C:\\Users\\Jhair\\PycharmProjects\\ControladorAsistenciaFace\\.venv\\Espejo\\Clases')

from Clases.Login import Login
from Clases.clasesFiguras import figuras

figuras = figuras()
login = Login()

booleana = True
booleana = login.facial()

if booleana == True or booleana == None:
    figuras.areas()
else:
    figuras.volumen()

print(booleana)