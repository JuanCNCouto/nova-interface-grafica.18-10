import tkinter as tk

temperatura_dat= [1,2,3,4] #lista para salvar os dados medidos enquanto o programa esta, rodando
 
volume_graf = [5,6,7,8] #lista para salvar os dados medidos enquanto o programa esta rodando 

pressao_graf = [9,10,11,15] #lista para salvar os dados medidos enquanto o programa esta rodando 

tab=[temperatura_dat,volume_graf,pressao_graf]

janela= tk.Tk()
janela.geometry(f"{800}x{800}")
frame3= tk.Frame(janela,height=700,width=600)
frame3.pack()


tit= tk.LabelFrame(frame3,text='tabela de valores P-V-T')
tit.pack(side='top')
e = tk.Entry(frame3, width=20, fg='blue',font=('Arial',16,'bold')) 
a=len(volume_graf)
for i in range(a):
	for j in range(3):
		e.insert(END,tab[j][i])
		e.grid(row=i,column=j)
