import tkinter as tk
import threading
import time
import sqlite3
import json

colores={"0":"White","1":"Black","2":"Green","3":"Blue","4":"gray","5":"Red","6":"Pink","7":"DarkBlue","8":"yellow","9":"gold"}
presed=None


# Para usar la paleta de colores se usan los numeros del teclado 1 al 9 
# El numero 4 es el Color que tiene activo Akura en ese momento


class animador():
    def __init__(self):
        self.ventana = tk.Tk()
        self.frame=tk.Frame(self.ventana)
        self.frame.pack()
        self.dir_anim={}
        self.fotograma=0
        self.botones=[]
        self.nombre=None
        self.proyect_name="Unnamed"
        self.radios=[]
        self.dimencion=None #Pixel de ancho y alto
        self.tupla=[]         #Futura tupla que contiene cada ventana y su color
        self.iniciar()
    def iniciar(self):
        def INICIAR(event=None):
            self.dimencion = (int (entrada_ancho.get()),int (entrada_alto.get()))
            frame.destroy()
            cont=[]
            for celda in range(0,self.dimencion[0]*self.dimencion[1]):
                cont.append([celda,0])
            self.dir_anim.update({0:cont})
            self.mapeo()
        frame = tk.Frame(self.frame)
        frame.pack()
        etiqueta=tk.Label(frame,text="Pixeles ancho X alto")
        etiqueta.pack()
        a= tk.Frame(frame)
        a.pack()
        entrada_ancho=tk.Entry(a,width=5)
        entrada_ancho.pack(side="left",padx=10)
        entrada_ancho.focus_set()
        eti=tk.Label(a,text="X")
        eti.pack(side="left",padx=10)
        entrada_alto=tk.Entry(a,width=5)
        entrada_alto.pack(side="right",padx=10)
        confirmar=tk.Button(frame,text="Confirmar",command=INICIAR)
        confirmar.pack()
        confirmar.bind('<Return>',INICIAR)
    def mapeo(self):
        def verificar_tecla(event):
            global presed
            if event.char in colores:
                presed=event.char
                baner.config(bg=colores[presed])   
        frame_baner = tk.Frame(self.frame)
        frame_baner.pack()
        baner = tk.Label(frame_baner,text=f"ancho= {self.dimencion[0]}--- alto= {self.dimencion[1]}",bg="white",fg="black")
        baner.pack()
        self.ventana.bind("<Key>",verificar_tecla)

        frame = tk.Frame(self.frame,highlightthickness=3,highlightbackground="DarkBlue",highlightcolor="DarkBlue")
        frame.pack(pady=10)
        class boto():
            def __init__(self , roww, columnn,master,num_ventana):
                self.roww= roww
                self.columnn=columnn
                self.master=master
                self.bot1=None
                self.color=None
                self.num_ventana=num_ventana
                self.crear()
            def crear(self):
                self.bot1=tk.Button(self.master,width=2,command=self.propiedad)
                self.bot1.grid(row=self.roww,column=self.columnn)
                self.bot1.bind("<Button-3>",self.reset)
            def propiedad(self):
                self.bot1.config(bg=colores[presed])
                self.color=int(presed)
            def obtener(self):
                return (self.num_ventana,self.color)
            def reset(self,e=None):
                self.bot1.config(bg="systemButtonFace")
                self.color=None
            def update(self,color):
                if color==None:
                    self.bot1.config(bg="systemButtonFace")
                else:
                    self.bot1.config(bg=str(colores[str(color)]))
                self.color=color
                
        i=1
        for roww in range(0,self.dimencion[1]):
            for columnn in range(0,self.dimencion[0]):
                c=boto(roww,columnn,frame,i)
                self.botones.append(c)
                i+=1
        frame_final=tk.Frame(self.frame,highlightthickness=3,highlightbackground="Black",highlightcolor="White")
        frame_final.pack(pady=10)

        class radbut():
            def __init__(self,master,fotograma):
                self.fotogram=fotograma
                self.rad1=tk.Radiobutton(master,text=f"{self.fotogram}",variable=self.fotogram,command=lambda:actualizar(self.fotogram))
                self.rad1.grid(row=1,column=self.fotogram)

                
        def anadir():
            for boton in self.botones:
                self.tupla.append(boton.obtener())
            #self.tupla=tuple(self.tupla)
            self.dir_anim.update({self.fotograma:self.tupla})
            self.tupla=[]
            radio2=radbut(frame_final,self.fotograma)
            self.fotograma+=1
            print(self.dir_anim)
        def resets():
            for boton in self.botones:
                boton.reset()
                del self.dir_anim[self.fotograma]
                self.tupla=[]
        def actualizar(e=None):
            p=0
            for boton in self.botones:
                boton.update(self.dir_anim[e][p][1])
                p+=1
            del p
            self.fotograma=e
        def sampler():
            for i in range(0,self.fotograma):
                actualizar(i)
                time.sleep(0.5)
        def SAVE():
            frame_final.destroy()
            frame.destroy()
            for fotograma,lista in self.dir_anim.items():
                for tupla in range(len(lista)-1,-1,-1):
                    if self.dir_anim[fotograma][tupla][1]== None:
                        lista.pop(self.dir_anim[fotograma][tupla][0]-1)
            ventanas =[[0 for _ in range(self.dimencion[0])]for _ in range(self.dimencion[1])]
            def recursiva(num):
                col=0
                while num>self.dimencion[0]:
                    num-=self.dimencion[0]
                    col+=1
                return (col,num-1)
            for fotograma,lista in self.dir_anim.items():
                for valor in lista:
                    d=recursiva(valor[0])
                    ventanas[d[0]][d[1]]=1
            self.dir_anim.update({"ventanas":ventanas})
            print (self.dir_anim)
            baner.config(text="Dale Nombre al Proyecto!!!")
            self.nombre=tk.Entry(frame_baner)
            self.nombre.pack()
            self.nombre.bind("<Return>",self.exxportar)
                
                
        anadir_buton=tk.Button(frame_final,text="Añadir",command=anadir)
        anadir_buton.grid(row=0,column=0)
        reset=tk.Button(frame_final,text="reset",command=resets)
        reset.grid(row=0,column=1)
        sample=tk.Button(frame_final,text="sample",command=lambda:threading.Thread(target=sampler).start())
        sample.grid(row=0,column=2)
        save=tk.Button(frame_final,text="SAVE",command=SAVE)
        save.grid(row=0,column=3)
    def exxportar(self,event=None):
        a = self.nombre.get()
        self.nombre.destroy()
        if a!=None or a !="":
            self.proyect_name = a
        conn = sqlite3.connect("Animaciones.db")
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS {self.proyect_name} (clave TEXT PRIMARY KEY, valores TEXT)')
        for clave, valores in self.dir_anim.items():
            # Convertir la lista a una cadena JSON
            c.execute(f'INSERT OR REPLACE INTO {self.proyect_name} (clave, valores) VALUES (?, ?)', 
                        (clave, json.dumps(valores)))
        print("----------------------Listo------------------")

        conn.commit()
    




if __name__ == "__main__":
    a = animador()
    a.ventana.mainloop()
