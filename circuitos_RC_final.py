#Circuito RC
#Habilidades EF08CI01 EF08CI02 EM13CNT106 EM13CNT107 da BNCC
#Prof. Sérgio Barroso, UESB. Disciplina MPF018 do POLO UESB/MNPEF.
#Arquivo livre para uso, mas favor citar a fonte ao utilizá-lo

import serial
import time
import pytz
import datetime
import math
import tkinter as ttk
import tk_tools
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep
import scipy
from scipy import optimize
import numpy as np
import pandas as pd

def carga(x, rc):
    return (5.*(1. - np.exp(-x/rc)))

def presbotaoSAIR() :
    root.quit()
    
def presbotaoOK() :
    labelstatus["text"]="Iniciando porta serial."
    root.after(1,root.update())
    #Abre a porta serial para comunicação com o Arduino
    ArduinoSerial = serial.Serial('COM7', 9600,timeout=1)
    #Espera 5 segundos
    time.sleep(5)
    #inicializa a variável para guardar os dados lidos do Arduino
    dados=[]
    #inicializa contador de linhas lidas
    i=0
    #Atualiza o status
    labelstatus["text"]="Lendo dados."
    root.after(1,root.update())
    #Lê a hora do sistema para usar no nome do arquivo de saída
    currentime = datetime.datetime.now(pytz.timezone('America/Bahia'))
    #Gera o nome do arquivo de saída a partir da data/hora do sistema
    file_name = "%4d%02d%02d%02d%02d.csv" % (currentime.year, 
        currentime.month, currentime.day, 
        currentime.hour, currentime.minute)
    #Comanda o Arduino a começar a carregar o capacitor
    ArduinoSerial.write(str.encode('OK\n'))
    sentrada=ArduinoSerial.readline()
    #Lê os dados do Arduino, pela porta serial, até que este informe que o processo
    #de carga e descarga terminou
    while sentrada!=b'FIM\r\n' :
        sentrada=ArduinoSerial.readline()
        tmps=str(sentrada,'UTF-8')
        #Algumas mensagens do Arduino não tem informação de tempo e voltagem
        if (tmps.find("t=")>-1) :
            #Lê a voltagem
            tmpvoltagem = float(tmps[tmps.find("v=")+2:tmps.find("#")])
            #Lê o tempo
            tmptempo = float(tmps[tmps.find("t=")+2:tmps.find(";")])
            #Armazena o tempo e a voltagem
            dados.append((tmptempo,tmpvoltagem))
            #A cada cinco leituras, atualiza o voltímetro
            if ((i % 5) == 0) :
                tensaoV_gauge.set_value(dados[i][1]);
                root.update()
            #incrementa o contador de linhas lidas
            i=i+1
    #Fecha a porta serial
    ArduinoSerial.close()
    #Converte os dados lidos num DataFrame Pandas, que
    #suporta automaticamente o uso de vírgula no separador decimal
    dadosDF = pd.DataFrame(dados,columns=['tempo (ms)','Vc (V)'])
    #Grava arquivo CSV com os dados lidos utilizando o suporte CSV do
    #DataFrame Pandas
    dadosDF.to_csv(file_name, decimal = ',', sep = ';', index = False)
    
    #Ajuste de curva
  
    #Acha o índice do valor máximo de Vc, para
    #identificar o fim do intervalo de carga do capacitor
    maxpos = np.argmax(dadosDF.to_numpy()[:,1])
    #Faz o ajuste de curva, não esquecendo de converter o tempo de milisegundos para segundos
    popt, _ = scipy.optimize.curve_fit(carga, dadosDF.to_numpy()[0:maxpos,0]/1e3,
        dadosDF.to_numpy()[0:maxpos,1])
    #Inicia a plotagem
    labelstatus["text"]="Plotando"
    #Atualiza a janela
    root.after(1,root.update())
    #Truques para que o gráfico aparece no janela raiz Tkinter
    figure = plt.figure(figsize=(5,4), dpi=100)
    chart_type = FigureCanvasTkAgg(figure, root)
    chart_type.get_tk_widget().grid(row=1,column=1, columnspan=2)
    #Plota (dispersão/scatter) os dados lidos pelo Arduino
    plt.scatter(dadosDF.to_numpy()[:,0],dadosDF.to_numpy()[:,1],label='Dados Arduino', marker='o',s=1)
    #Plota a função ajustada pela scipy.optimize.curve_fit
    plt.plot(dadosDF.to_numpy()[0:maxpos,0],carga(dadosDF.to_numpy()[0:maxpos,0]/1e3,popt[0]),
        label='constante RC ajustada = %4.2f 1/s' % (popt[0]),
        color='red', linestyle='solid', linewidth = 1)
    #Ajusta os títulos dos eixos
    plt.xlabel('t (ms)')
    plt.ylabel('Tensão (V)')
    #Ajusta o título do gráfico
    plt.title('Carga x Descarga circuito RC Arduino/Python')
    #Adiciona legenda ao gráfico
    plt.legend()
    labelstatus["text"]="Pressione OK para começar."
    root.after(1,root.update())
    #Limpar memória. Precisa?
    del [[dadosDF]]
    
#Porção "main" do código
myfont=("Times New Roman",14)
#Cria a janela principal do app
root=ttk.Tk()
#Ajusta o tamanho da janela principal para 900x600
root.geometry('900x600')
#Bloqueio a mudança de tamano da janela
root.resizable(False,False)
#Ajusta o título da janela principal
root.title('Exemplo EF08CI01 EF08CI02 EM13CNT106 EM13CNT107 MPF018 UESB')
#Configura o número de linhas e colunas da janela principal
#para facilitar a disposição dos 'widgets' na janela com a função grid() do 
#Tkinter. 3 linhas e 3 colunas, sendo que a linha 1
#tem o dobro da altura das demais
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=2)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
#Adiciona um widget com uma "foto" do circuito (obtida do TinkerCad)
photo = ttk.PhotoImage(file='./circuito_266x300.png')
image_label = ttk.Label(root,image=photo)
image_label.grid(row=1,column=0,sticky='N')
#Adiciona Label no alto da janela
labeltitulo = ttk.Label(root, text = "EXEMPLO APLICAÇÃO ARDUÍNO MPF018 - CIRCUITO RC",font=myfont)
labeltitulo.grid(row=0,column=0,columnspan=3)
#Adiciona Label de status
labelstatus = ttk.Label(root, text = "Pressione OK para começar.",font=myfont)
labelstatus.grid(row=2,column=0,columnspan=2)
#Adiciona o botão OK
botaoOK = ttk.Button(root,text='OK',command=presbotaoOK).grid(row=2,column=2, ipadx=10,sticky='W')
#Adiciona o botão sair
botaoSAIR = ttk.Button(root,text='SAIR',command=presbotaoSAIR).grid(row=2,column=2, ipadx=10)
#Adiciona o voltímetro do pacote tktools
tensaoV_gauge = tk_tools.Gauge(root, height=150, width=200,
                            max_value=5, min_value=0,
                            label='Vc(A0)',
                            unit='V',
                            divisions=5,
                            yellow=100,
                            bg='white'
                            )
tensaoV_gauge.grid(row=1, column=0, sticky='S')
#Adiciona uma figura em branco para ajustar os widogets na janela
photo1 = ttk.PhotoImage(file='./tela_branco_500x400.png')
image_label1 = ttk.Label(root,image=photo1)
image_label1.grid(row=1,column=1,columnspan=2)
#Inicia o app
root.mainloop()



