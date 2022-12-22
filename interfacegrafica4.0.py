from cgitb import text
from datetime import date
import pickle 
import tkinter as tk
from tkinter import ttk
from turtle import width
import tk_tools
import serial
import time
import matplotlib.pyplot as plt
import pandas 
import numpy as np





start = 0
#variavel de controle para o modo de manipulação de arquivos
#(0=nao foi começado a medir, modo de leitura 'w'), (1 = foi começado a medir, modo de leitura 'a')

dat= list(time.localtime())
#função que pega as informações da ano,mes,dia,hoa,minuto,segundo do local, transformei em lista
#por que é mais facil de manipular

#a variavel nome é uma string q sempre vai ter a informação da data e da hora que começaram a rodar o programa
#isso vai servir para evitar o problema de sobreposição, pois para começar a fazer um grafico do 0 tem que
#fechar o progrma e abrir ele denovo

nome= str(dat[2])+'-' + str(dat[1])+'-'+str(dat[0])+'-'+str(dat[3])+'-'+str(dat[4])

#ordem:
#time.struct_time(tm_year=2022(0), tm_mon=10(1), tm_mday=7(2), tm_hour=1(3), tm_min=57(4), tm_sec=45(5), 
# tm_wday=4(6), tm_yday=280(7), tm_isdst=0(8))

ser=0 # variavel global para conectar o arduino

temperatura_dat= [] #lista para salvar os dados medidos enquanto o programa esta rodando
 
volume_graf = [] #lista para salvar os dados medidos enquanto o programa esta rodando 

pressao_graf = [] #lista para salvar os dados medidos enquanto o programa esta rodando 
tab=[]
cont=0

def desconectar():
    global ser

    if(ser != 0):
        time.sleep(1.8)
        ser.write('d'.encode('utf-8'))
        time.sleep(1.8)
        resposta = ser.readline()
        resposta = int(resposta.decode("utf-8"))
        if(resposta):
            texto_arduino.set("Arduino Desconectado")
            led.to_red(on=True)
            ser.write('n'.encode('utf-8'))
            ser.close()
    return

def conectar():

    global ser

    ser = serial.Serial("COM9",9600,timeout=10)
    time.sleep(1.8)
    ser.write('c'.encode('utf-8'))
    time.sleep(1.8)
    resposta = ser.readline()
    resposta = int(resposta.decode("utf-8"))
    if(resposta):
        texto_arduino.set("Arduino conectado")
        led.to_green(on=True)
        ser.write('n'.encode('utf-8'))
    return


#função para salvar os dados em um arquivo

def salvar():

  global nome #usa a variavel global nome para abrir o arquivo
  global cont #contador das listas
  global pressao_graf,temperatura_dat,volume_graf #listas dos dados
  aux= 'C:\\Users\\JuanC\\Desktop\\medidas\\DES-'+nome+'.txt' # nome do arquivo com os dados salvos em float
  print(aux)
  #abri o arquivo no modo 'w' e escreve todos os dados nos arquivos
  tab=[pressao_graf,temperatura_dat,volume_graf]
  a= len(pressao_graf)
  arq=open(aux,'w')
  for i in range(0,a):
      arq.write(f"{volume_graf[i]} {pressao_graf[i]} {temperatura_dat[i]}\n")
      #arq.write('\n')
  arq.close()
  #v=np.array(tab).shape(a,3)
  #np.savetxt(aux,v)
#  v2=np.array(pressao_graf,volume_graf)
#  np.savetxt(r"C:\\User\\JuanC\\desktop\\dadospv.txt",v2)
#  arq = open(aux,'wb')
#  pickle.dump(tab,arq)
#  arq.close()

def Peltier():
    global ser,Pelt_var
    ser.write('a'.encode())
    co = ser.readline()
    co= int(co.decode('utf-8'))
    print(co)
    if co == 1:
        print("Peltier ligado")
        Pelt_var.set("Desligar")
    if co==0 :
        print("Peltier Desligado")
        Pelt_var.set("Ligar")


def plotar():
    global nome,pressao_graf,temperatura_dat,volume_graf
    
    plt.clf()
    fig,ax=plt.subplots(2,1,figsize=(6,6),constrained_layout=True)
    ax[0].scatter(y=pressao_graf,x=temperatura_dat)
    ax[0].set_title('Grafico PxT')
    aux="C:\\Users\\JuanC\\Desktop\\medidas\\"+nome+".png"
    ax[1].scatter(volume_graf,pressao_graf)
    ax[1].set_title('Grafico PxV')
    fig.savefig(aux)
    img = tk.PhotoImage(file=aux)
    grafico.configure(image=img)
    grafico.imagem= img

def medir():
    global cont,volume_entry_var #contador que acompanha o indice do ultimo elemento nas listas( sempre começa em 0, isso significa q vai ser adicionado a primeira medida no arquivo)
    
    time.sleep(1.8)#delay
    
    ser.write('m'.encode('utf-8'))# transmissao da sinal q é o caracter 'm' para o arduino
    
    volume = float(volume_entry.get().replace(',','.'))+0.00 #leitura do volume escrito via teclado na interface
    
    volume_entry_var.set(f"{volume}")#altera a o numero do volume que mostra na interface grafica
    
    time.sleep(1.8) #delay
    
    temperatura = ser.readline() #le a informação que o arduino enviou para a porta USB e q foi mostrada no monitor serial
    
    temperatura = temperatura.decode('utf-8') #decodifica ela 
    
    temperatura_dat.append(float(temperatura)) # adiciona a medida na lista temperatura_dat
    
    temp_var.set(f"Temperatura (°C): {temperatura}")#altera a o numero do temperatura que mostra na interface grafica
    
    time.sleep(1.8) #delay
    
    pressao = ser.readline() #le a informação que o arduino enviou para a porta USB e q foi mostrada no monitor serial
    
    pressao = pressao.decode('utf-8') #decodifica ela de utf-8 para float
    
    #UTF-8 (UCS Transformation Format 8) é a codificação de caracteres mais comum da World Wide Web.
    
    pressao_var.set(f"Pressão (HPa): {pressao}") #altera a o numero do pressao que mostra na interface grafica
    
    volume_graf.append(volume) #add a medida na lista volume_graf
    
    pressao_graf.append(float(pressao)) #add a medida na lista pressao_graf
    
    #essas listas com o '_graf' serve para plotar os pontos no grafico
    tree.insert('',tk.END,values=[str(pressao),str(volume),str(temperatura)])
    
    cont +=1 #aumenta o contador pq a quantidade de elementos nas listas aumentaram 

    return


#width= largura
largura = 1049
#height altura
altura = 677
janela= tk.Tk()
janela.title("Projeto todos nas ciências")
janela.geometry(f'{largura}x{altura}')
frame1= tk.Frame(janela,height=30)
frame2= tk.Frame(janela)
frame3= tk.Frame(janela)
frame4= tk.Frame(janela)
frame1.place(relx=0,rely=0,relwidth=1)
frame2.place(relx=0,rely=0.05,relwidth=0.2,relheight=1)
frame3.place(relx=0.2,rely=0.05,relwidth=0.25,relheight=1)
frame4.place(relx=0.41,rely=0.05,relwidth=1,relheight=1)


ttk.Separator(frame1,orient='horizontal').place(relwidth=1,rely=0.999)


######################################### FRAME 1 - BOTOES DE CONECTAR ARDUINO- ############################################
btn_conectar= tk.Button(frame1,text= 'conectar',command= conectar)
btn_conectar.place(relx=0.62)

btn_desconectar= tk.Button(frame1,text='desconectar arduino',command= desconectar)
btn_desconectar.place(relx=0.80)
led= tk_tools.Led(janela,size=25)
led.place(relx=0)
led.to_red(on=True)

texto_arduino= tk.StringVar()
texto_arduino.set("Arduino desconectado")
ard_label= tk.Label(frame1,textvariable = texto_arduino,pady=7)
ard_label.place(relx=0.05)

ttk.Separator(frame2, orient='vertical').place(relheight=1,relx=0.9974)


##############################- FRAME 2- ENTRADA DE VOLUME, BOTOES DE MEDIR,PLOTAR GRAFICO E SALVAR - ##########################

volume_txt=tk.Label(frame2,text="volume indicado em mL :") 
volume_entry_var=tk.StringVar()
volume_entry= tk.Entry(frame2,textvariable= volume_entry_var,width=20)
volume_txt.place(rely=0.05, relx=0.2)
volume_entry.place( rely=0.10,relx=0.2)

temp_var = tk.StringVar()
temp_var.set("Temperatura (°C): None")
temp_txt = tk.Label(frame2,textvariable=temp_var,pady=30)
temp_txt.place( rely= 0.20, relx=0.2)

pressao_var = tk.StringVar()
pressao_var.set("Pressão (HPa): None")
pressao_txt = tk.Label(frame2,textvariable=pressao_var,pady=30)
pressao_txt.place(rely=0.30, relx=0.2)

btn_medir= tk.Button(frame2,text='medir',command= medir,pady=15,padx=30)
btn_medir.place( rely=0.40, relx=0.2)

btn_salvar= tk.Button(frame2,text='salvar medidas',command=salvar ,pady=15,padx=30)
btn_salvar.place( rely=0.50, relx=0.2)

btn_plotar= tk.Button(frame2,text='plotar',command= plotar,pady=15,padx=30)
btn_plotar.place( rely=0.60, relx=0.2)

Pelt_txt= tk.Label(frame2,text= "Peltier")
Pelt_txt.place(rely= 0.75,relx=0.2)
Pelt_var= tk.StringVar()
Pelt_var.set("Ligar")
btn_Peltier= tk.Button(frame2,textvariable= Pelt_var ,command=Peltier,pady=15,padx=30)
btn_Peltier.place(rely= 0.80, relx=0.2)


##########################################- FRAME 3- TABELA -##################################
colunas=('p','v','t')
tree= ttk.Treeview(frame3,columns=colunas,show='headings',height=100)
tree.heading('p', text='P(hPa)')
tree.heading('v', text='V(ml)')
tree.heading('t', text='T(ºC)')
tree.column('p',width=70)
tree.column('v',width=70)
tree.column('t',width=70)
tree.grid(row=0,column=0,sticky='nsew')

##########################################- FRAME 4- GRAFICOS -##################################


grafico = tk.Label(frame4)
grafico.place(relx=0,rely=0)

janela.mainloop()