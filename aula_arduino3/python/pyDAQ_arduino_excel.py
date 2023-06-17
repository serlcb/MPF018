import serial
import time
import pytz
import datetime
#import math
import tkinter as ttk
#import tk_tools
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep
#import scipy
#from scipy import optimize
#import numpy as np
#import pandas as pd
import xlwings as xw


#Cria interface gráfica
myfont=("Times New Roman",14)
#Cria a janela principal do app
root=ttk.Tk()
#Ajusta o tamanho da janela principal para 900x600
root.geometry('240x225')
root.resizable(False,False)
root.title('pyPLX-DAQ') #titulo da janela

#configura o layout da janela
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.rowconfigure(7, weight=1)
root.rowconfigure(8, weight=1)
root.rowconfigure(9, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

myfont=("Times New Roman",18)
style = ttk.Style()
style.configure("BW.TLabel", foreground="black", background="white")

labeltitulo = ttk.Label(root, text = "pyPLX-DAQ",font=myfont,style="BW.TLabel")

labeltitulo.grid(row=0,column=0,rowspan=2)

#Abre a porta serial para comunicação com o Arduino
ArduinoSerial = serial.Serial('/dev/cu.usbserial-110', 9600,timeout=1)
time.sleep(5)
#app = xw.apps.active
wb=xw.books.active
sheet=wb.sheets.active
colunas=['A','B','C','D','E','F','G','H','I','J','K']
#inicializa contador de linhas lidas
linhasLidas=0
linhasdeDadosLidas=0
sentrada=ArduinoSerial.readline().decode("utf-8").strip()
while sentrada!='FIM' :
    sentradaSplitted=sentrada.split(',')
    #for i in range(len(sentradaSplitted)) :
    #    sentradaSplitted[i]=sentradaSplitted[i].decode('utf-8')
    #sentradaSplitted[len(sentradaSplitted)-1]=sentradaSplitted[len(sentradaSplitted)-1][:len(sentradaSplitted)-2]
    match sentradaSplitted[0]:
        case 'DATA':
            linhasdeDadosLidas+=1
            contacoluna=0
            for dado in sentradaSplitted :
                if dado != 'DATA' :
                    sheet["%s%d" % (colunas[contacoluna],linhasdeDadosLidas+1)].value = dado
                    contacoluna=+1
        case 'CLEARDATA':
            sheet.range("A:F").clear_contents()
            linhasdeDadosLidas=0
        case 'LABEL':
            contacoluna=0
            for dado in sentradaSplitted :
                if dado != 'LABEL' :
                    sheet["%s%d" % (colunas[contacoluna],1)].value = str(dado)
                    contacoluna+=1
#        case "ROW":
    sentrada=ArduinoSerial.readline().decode("utf-8").strip()