from cgitb import text
from datetime import date
from pickle import FALSE, TRUE
import tkinter as tk
from tkinter import ttk
from turtle import width
import tk_tools
import serial
import time
import matplotlib.pyplot as plt
import pandas 
#width= largura
largura = 1000 
#height altura

tab={'P(Pa)': [],'T(C)':[],'V(ml)':[]}

tab_df=pandas.DataFrame(tab)

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

tab={'P(Pa)': temperatura_dat,'T(C)':volume_graf,'V(ml)': pressao_graf} #tabela 

tab_df=pandas.DataFrame(tab)

cont=0

altura = 600
janela= tk.Tk()
janela.title("Projeto todos nas ciências")
janela.geometry(f'{largura}x{altura}')
frame1= tk.Frame(janela,height=30)
frame2= tk.Frame(janela,height=570,width=80)
frame3= tk.Frame(janela,height=570,width=80)
frame4= tk.Frame(janela,height=570,width=80)
frame1.place(relx=0,rely=0,relwidth=1)
frame2.place(relx=0,rely=0.05,relwidth=0.2,relheight=1)
frame3.place(relx=0.30,rely=0.05,relwidth=0.3,relheight=1)
frame4.place(relx=0.60,rely=0.05,relwidth=0.5,relheight=1)


ttk.Separator(frame1,orient='horizontal').place(relwidth=1,rely=0.999)


######################################### FRAME 1 - BOTOES DE CONECTAR ARDUINO- ############################################
btn_conectar= tk.Button(frame1,text="conectar",command= conectar)
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
temp_txt.place( rely= 0.15, relx=0.2)

pressao_var = tk.StringVar()
pressao_var.set("Pressão (HPa): None")
pressao_txt = tk.Label(frame2,textvariable=pressao_var,pady=30)
pressao_txt.place(rely=0.30, relx=0.2)

btn_medir= tk.Button(frame2,text='medir',command= medir,pady=15,padx=30)
btn_medir.place( rely=0.45, relx=0.2)

btn_salvar= tk.Button(frame2,text='salvar medidas',command=salvar ,pady=15,padx=30)
btn_salvar.place( rely=0.60, relx=0.2)

btn_plotar= tk.Button(frame2,text='plotar',command= plotar,pady=15,padx=30)
btn_plotar.place( rely=0.75, relx=0.2)

##########################################- FRAME 3- TABELA -##################################
tit= tk.LabelFrame(frame3,text='tabela de valores P-V-T')
tit.pack(side='top')
e = tk.Entry(frame3, width=20, fg='blue',font=('Arial',16,'bold')) 
for j in range(3):
    e.tk.Entry.insert(cont, tab[j][cont]) 
    e.grid(row=cont, column=j)


##########################################- FRAME 4- GRAFICOS -##################################


graficoVP = tk.Label(frame4)
graficoVP.place(relx=0,rely=0,relheight=0.4,relwidth=0.5)
graficoPT = tk.Label(frame4)
graficoPT.place(relx=0,rely=0.5,relheight=0.4,relwidth=0.5)

janela.mainloop()
