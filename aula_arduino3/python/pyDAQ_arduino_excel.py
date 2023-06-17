import serial
import time
from time import sleep
import xlwings as xw


#Abre a porta serial para comunicação com o Arduino
#ArduinoSerial = serial.Serial('/dev/cu.usbserial-110', 9600,timeout=1) #MacOS
ArduinoSerial = serial.Serial('COM4:', 9600,timeout=1) #Windows

sentrada=ArduinoSerial.readline().strip()
while sentrada!=b'OK' :
    sentrada=ArduinoSerial.readline().strip()
ArduinoSerial.write(str.encode('OK\n'))

time.sleep(5)
wb=xw.books.active
sheet=wb.sheets.active
colunas=['A','B','C','D','E','F','G','H','I','J','K']
#inicializa contador de linhas lidas
linhasLidas=0
linhasdeDadosLidas=0
sentrada=ArduinoSerial.readline().decode("utf-8").strip()
concluir=0
while sentrada!='FIM' :
    sentradaSplitted=sentrada.split(',')
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
        case "ROW":
            concluir=1
    if concluir==0 :
        sentrada=ArduinoSerial.readline().decode("utf-8").strip()
    else :
        sentrada="FIM"