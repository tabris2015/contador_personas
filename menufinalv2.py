import os
import tkinter as tk
import tkinter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

def estimado_de_la_galeria():
    multiplicacion=float(entrada2.get())*int(entrada3.get())*float(var.get())*float(var1.get())*float(var2.get())*float(var3.get())*float(var4.get())*float(var5.get())*float(var6.get())
    return datos.set(multiplicacion)

def estimado_construccion():
    multi=float(entradaa.get())*float(entradaa.get())*float(var7.get())*float(var8.get())*float(var9.get())*float(var10.get())
    return datos2.set(multi)

def valor_total():
    ventana.withdraw()
    win=tk.Toplevel()
    win.title("monitoreo")
    win.geometry('800x410')
    win.configure(background='dark blue')
    
    ima=tk.PhotoImage(file="logocopi.png")
    ima=ima.subsample(1,1)
    label=tk.Label(ima=ima)
    label.place()
    
    ent12=tk.Label(win, text="superficie en metros cuadrados de la construcion:", bg="yellow", fg="black")
    ent12.pack(padx=5, pady=5, ipadx=5, ipady=0)
    ent12.place(x=10, y=50)
    resultadoa=tk.Label(win, bg='white', textvariable=entradaa.get(), padx=5, pady=5, width=20)
    resultadoa.pack()
    resultadoa.place(x=10, y=75)
    
    ent13=tk.Label(win, text="coeficente para valor de la construccion:", bg="yellow", fg="black")
    ent13.pack(padx=5, pady=5, ipadx=5, ipady=0)
    ent13.place(x=10, y=110)
    var7.set(0)
    opciones7=['0.65','0.7','0.8','1','1.2','1.4']
    opcion7=tk.OptionMenu(win, var7, *opciones7)
    opcion7.config(width=20)
    opcion7.pack()
    opcion7.place(x=10, y=140)
    
    ent14=tk.Label(win, text="coeficente de deprecaicion:", bg="yellow", fg="black")
    ent14.pack(padx=5, pady=5, ipadx=5, ipady=0)
    ent14.place(x=10, y=180)
    var8.set(0)
    opciones8=['0.55', '0.6', '0.65','0.7', '0.75', '0.8', '0.85', '0.9', '0.93', '0.97', '1']
    opcion8=tk.OptionMenu(win, var8, *opciones8)
    opcion8.config(width=20)
    opcion8.pack()
    opcion8.place(x=10, y=210)
    
    ent15=tk.Label(win, text="coeficente de conservacion:", bg="yellow", fg="black")
    ent15.pack(padx=5, pady=5, ipadx=5, ipady=0)
    ent15.place(x=540, y=50)
    var9.set(0)
    opciones9=['0.2','0.6','0.9','1','1.05','1.1']
    opcion9=tk.OptionMenu(win, var9, *opciones9)
    opcion9.config(width=20)
    opcion9.pack()
    opcion9.place(x=540, y=80)
    
    ent16=tk.Label(win, text="coeficente de uso:", bg="yellow", fg="black")
    ent16.pack(padx=5, pady=5, ipadx=5, ipady=0)
    ent16.place(x=540, y=170)
    var10.set(0)
    opciones10=['0.8','1','1.2','1.4']
    opcion10=tk.OptionMenu(win, var10, *opciones10)
    opcion10.config(width=20)
    opcion10.pack()
    opcion10.place(x=540, y=200)
    
    ent17=tk.Label(win, text="resultado valor del terreno:", bg="yellow", fg="black")
    ent17.pack(padx=5, pady=5, ipadx=5, ipady=0)
    ent17.place(x=20, y=250)
    resultado=tk.Label(win, bg='white', textvariable=datos, padx=5, pady=5, width=20)
    resultado.pack()
    resultado.place(x=20, y=280)
    
    ent18=tk.Label(win, text="resultado valor de la construccion:", bg="yellow", fg="black")
    ent18.pack(padx=5, pady=5, ipadx=5, ipady=0)
    ent18.place(x=250, y=250)
    resultado2=tk.Label(win, bg='white', textvariable=datos2, padx=5, pady=5, width=20)
    resultado2.pack()
    resultado2.place(x=250, y=280)
    
    ent19=tk.Label(win, text="resultado total aproximado:", bg="yellow", fg="black")
    ent19.pack(padx=5, pady=5, ipadx=5, ipady=0)
    ent19.place(x=490, y=250)
    resultado3=tk.Label(win, bg='white', textvariable=datosf, padx=5, pady=5, width=20)
    resultado3.pack()
    resultado3.place(x=490, y=280)
    
    bot1 = tk.Button(master=win, text="salir", highlightbackground='red', fg='red', command=salir)
    bot1.pack(side=tkinter.BOTTOM)
    bot1.place(x=10, y=370)
    
    bot2 = tk.Button(master=win, text="valor de total", highlightbackground='green', fg='green', command=estimado_construccion)
    bot2.pack(side=tkinter.BOTTOM)
    bot2.place(x=600, y=330)
    
    bot3 = tk.Button(master=win, text="monitorear", highlightbackground='green', fg='green', command=monitoreo)
    bot3.pack(side=tkinter.BOTTOM)
    bot3.place(x=600, y=370) 
    
def monitoreo():    
    os.system('python people_counter.py -p MobileNetSSD_deploy.prototxt -m MobileNetSSD_deploy.caffemodel -i example_02.mp4')
    ventana.withdraw()
    win1=tk.Toplevel()
    win1.title("monitoreo")
    win1.geometry('800x410')
    win1.configure(background='dark blue')
    
    bot1 = tk.Button(master=win1, text="salir", highlightbackground='red', fg='red', command=salir)
    bot1.pack(side=tkinter.BOTTOM)
    bot1.place(x=10, y=370)

def obtener_datos():
    ventana.withdraw()
    win=tk.Toplevel()
    fig = Figure(figsize=(7, 5), dpi=50)
    df = pd.read_csv('datoseloy.csv', delimiter=',', nrows=1700, skiprows=[2])
    y=df['position_x'];
    x=df['object_id'];
    plt.xlabel('x'); plt.ylabel('y')
    a=fig.add_subplot(121)
    a.bar(x,y)
    b=df['position_x'];
    c=df['position_y'];
    plt.xlabel('b'); plt.ylabel('c')
    a=fig.add_subplot(122)
    a.scatter(b,c)

    canvas = FigureCanvasTkAgg(fig, master=win)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    #toolbar = NavigationToolbar2Tk(canvas, win)
    #toolbar.update()
    #canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    boton3 = tk.Button(master=win, text="salir", command=salir)
    boton3.pack(side=tkinter.BOTTOM)

def salir():
    ventana.quit()     
    ventana.destroy()
#configuracion ventana principal
ventana=tk.Tk()#ventana principal    
ventana.title("sistema de monitoreo")
ventana.geometry('800x410')
ventana.configure(background='dark blue')
#variables del codigo
datos=tk.StringVar()
datos2=tk.StringVar()
datosf=tk.StringVar()
var=tk.StringVar()
var1=tk.StringVar()
var2=tk.StringVar()
var3=tk.StringVar()
var4=tk.StringVar()
var5=tk.StringVar()
var6=tk.StringVar()
var7=tk.StringVar()
var8=tk.StringVar()
var9=tk.StringVar()
var10=tk.StringVar()
#introduccion imagen izquierda
ima=tk.PhotoImage(file="logo.png")
ima=ima.subsample(2,2)
label=tk.Label(ima=ima)
label.place(x=10,y=10)
#introduccion imagen derecha
im=tk.PhotoImage(file="logoemi.png")
im=im.subsample(2,2)
label1=tk.Label(im=im)
label1.place(x=635,y=10)

ent1=tk.Label(ventana, text="Nombre de la galeria:", bg="yellow", fg="black")
ent1.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent1.place(x=250, y= 10)
entrada1=tk.Entry(ventana)
entrada1.pack(padx=5, pady=5, ipadx=5, ipady=5)
entrada1.place(x=230, y=40)

enta=tk.Label(ventana, text="superficie construida:", bg="yellow", fg="black")
enta.pack(padx=5, pady=5, ipadx=5, ipady=0)
enta.place(x=230, y=70)
entradaa=tk.Entry(ventana)
entradaa.pack(padx=5, pady=5, ipadx=5, ipady=5)
entradaa.place(x=230, y= 100)

ent2=tk.Label(ventana, text="superficie en metros cuadrados:", bg="yellow", fg="black")
ent2.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent2.place(x=10, y=150)
entrada2=tk.Entry(ventana)
entrada2.pack(padx=5, pady=5, ipadx=5, ipady=5)
entrada2.place(x=20, y= 180)

ent3=tk.Label(ventana, text="valor unitario por zona:", bg="yellow", fg="black")
ent3.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent3.place(x=10, y=210) 
entrada3=tk.Entry(ventana)
entrada3.pack(padx=5, pady=5, ipadx=5, ipady=5)
entrada3.place(x=20, y=240)

ent4=tk.Label(ventana, text="coeficente de via:", bg="yellow", fg="black")
ent4.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent4.place(x=10, y=270)
var.set(0)
opciones=['0.7','0.8','0.9','1','1.1','1.2','1.3','1.5']
opcion=tk.OptionMenu(ventana, var, *opciones)
opcion.config(width=20)
opcion.pack()
opcion.place(x=20, y=300)

ent5=tk.Label(ventana, text="coeficente de la pendiente:", bg="yellow", fg="black")
ent5.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent5.place(x=290, y=130)
var1.set(0)
opciones1=['0.5','0.6','0.9','1','1.1']
opcion1=tk.OptionMenu(ventana, var1, *opciones1)
opcion1.config(width=20)
opcion1.pack()
opcion1.place(x=280, y=160)

ent6=tk.Label(ventana, text="coeficente de nivel:", bg="yellow", fg="black")
ent6.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent6.place(x=290, y=200)
var2.set(0)
opciones2=['0.5','0.8','1']
opcion2=tk.OptionMenu(ventana, var2, *opciones2)
opcion2.config(width=20)
opcion2.pack()
opcion2.place(x=280, y=230)

ent7=tk.Label(ventana, text="coeficente de la forma:", bg="yellow", fg="black")
ent7.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent7.place(x=290, y=270)
var3.set(0)
opciones3=['0.5','0.8','1']
opcion3=tk.OptionMenu(ventana, var3, *opciones3)
opcion3.config(width=20)
opcion3.pack()
opcion3.place(x=280, y=300)

ent8=tk.Label(ventana, text="coeficente de la ubicacion:", bg="yellow", fg="black")
ent8.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent8.place(x=540, y=130)
var4.set(0)
opciones4=['1','1.2']
opcion4=tk.OptionMenu(ventana, var4, *opciones4)
opcion4.config(width=20)
opcion4.pack()
opcion4.place(x=540, y=160)

ent9=tk.Label(ventana, text="servicios", bg="yellow", fg="black")
ent9.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent9.place(x=540, y=200)
var5.set(0)
opciones5=['0.5','0.8','1']
opcion5=tk.OptionMenu(ventana, var5, *opciones5)
opcion5.config(width=20)
opcion5.pack()
opcion5.place(x=540, y=230)

ent10=tk.Label(ventana, text="coeficente de frente/fondo:", bg="yellow", fg="black")
ent10.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent10.place(x=540, y=270)
var6.set(0)
opciones6=['0.5','0.8','1']
opcion6=tk.OptionMenu(ventana, var6, *opciones6)
opcion6.config(width=20)
opcion6.pack()
opcion6.place(x=540, y=300)

ent11=tk.Label(ventana, text="resultado valor del terreno:", bg="yellow", fg="black")
ent11.pack(padx=5, pady=5, ipadx=5, ipady=0)
ent11.place(x=300, y=340)
resultado=tk.Label(ventana, bg='white', textvariable=datos, padx=5, pady=5, width=20)
resultado.pack()
resultado.place(x=300, y=370)


boton1 = tk.Button(master=ventana, text="salir", highlightbackground='red', fg='red', command=salir)
boton1.pack(side=tkinter.BOTTOM)
boton1.place(x=10, y=370)

boton2 = tk.Button(master=ventana, text="valor de la construccion", highlightbackground='green', fg='green', command=valor_total)
boton2.pack(side=tkinter.BOTTOM)
boton2.place(x=600, y=370)

boton4=tk.Button(ventana, text='valor del terreno', fg='black', command=estimado_de_la_galeria)
boton4.place(x=120, y=370)

ventana.mainloop()
