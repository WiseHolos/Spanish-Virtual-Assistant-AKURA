import tkinter as tk
from tkinter import Button,Canvas,Label
import time
import threading
import psutil
import ismart
import pyautogui


temperatura = 40.00
class Akura:
    def __init__(self):
        self.hora = None                        #hora actual en string
        self.estado = "iniciando"               #estados iniciando - reducido - expandido - notificando
        self.ventana = tk.Tk()                  #Ventana basada en tkinter
        self.v_d =[100,48,None,None]            #pcicion y dimenciones x y --- ancho largo
        self.nombre = "Akura"                   #Nombre del programa
        self.notificar="Notificandow"           #Lo que se va a notificar
        self.terminar_notificar = "reducido"    #Complemento para notificar
        self.boton_maus = False                 #False si el boton de hora no tiene el mause arriba
        self.Low = False                        #Modo Economico
        self.mostrar_menu = "nada"              #Estado del menu
        self.b_m_b =[None,None,None,None,None]  #Botones base del menu
        self.c_d_v = [100,48,None,None,         #Posicion Del Reducido
                      300,248,None,None]        #Pocicion del expandido
        self.validacion = True                  #Para la ventana escondida

    def tiempo (self,Correct=False):
        try:
            if Correct == False:
                while True:
                    if self.estado == "reducido" or self.estado == "expandido":
                        if self.Low == True or self.boton_maus==True:
                            self.boton_hora.config(text=temperatura,fg="Red")
                            time.sleep(5)
                        elif self.Low == False:
                            self.hora= time.strftime("%I:%M")
                            self.boton_hora.config(text=self.hora,fg="Blue")
                            time.sleep (15)    
                    time.sleep(5)
            else:
                if self.estado == "reducido" :
                    if self.Low == True or self.boton_maus==True:
                        self.boton_hora.config(text=temperatura)
                    elif self.Low == False:
                        self.hora= time.strftime("%I:%M")
                        self.boton_hora.config(text=self.hora,fg="Blue")    
                elif self.estado == "expandido":
                    self.boton_hora.config(text="akura",fg="Green")
        except:
            print("Error al mostrar hora")
        
    def Notifica(self,notificacion,terminar="reducido"):
        while self.estado != "reducido":
            if self.Low ==True:
                self.estado="reducido"
                self.constructor()
            time.sleep(1)
        self.notificar = notificacion
        self.estado = "notificando"
        self.terminar_notificar = terminar
        self.temporizador_de_notificando = 5
        self.constructor()
        pass

    def boton_h(self):
        if self.estado == "reducido":
            self.estado = "expandido"
            self.constructor()
        elif self.estado == "notificando":
            self.temporizador_de_notificando = 0
        else :
            self.estado = "reducido"
            self.constructor()
    
    def boton_h_apuntado(self,objeto):
        self.boton_maus = True
        C.temperatura(Correct=True)
        self.tiempo(Correct=True)

    def boton_h_desapuntado(self,objeto):
        self.boton_maus = False
        self.tiempo(Correct=True)
            
    def constructor(self):
        if self.estado == "iniciando":
            self.v_d[2]=self.ventana.winfo_screenwidth() -95        #distancia en x
            self.v_d[3]=self.ventana.winfo_screenheight() // 4 +300 #distancia en y

            self.ventana.title(self.nombre)           #Nombre del programa
            self.ventana.overrideredirect(1)               #Botones de ventana por defecto apagados
            self.ventana.attributes('-topmost',True)       #siempre encima
            self.ventana.geometry("%dx%d+%d+%d"%(self.v_d[0],self.v_d[1],self.v_d[2],self.v_d[3]))
            self.ventana.config(background="black")
            
            self.boton_hora = Button(self.ventana,text=self.nombre,anchor="nw",
                                     font=("Arial", 22),height=1,width=4, bg="Black",fg="Red",
                                     command=self.boton_h,activeforeground="Red",activebackground="Black")
            self.boton_hora.place(x=0,y=0)
            self.boton_hora.bind("<Enter>",self.boton_h_apuntado)
            self.boton_hora.bind("<Leave>",self.boton_h_desapuntado)
            self.estado = "reducido"
            threading.Thread(target=self.tiempo).start()
        elif self.estado=="expandido":              #Expandir
            def expandir():
                try:
                    self.v_d[0]=300
                    self.v_d[1]=248
                    self.v_d[2]=self.ventana.winfo_screenwidth() -295        #distancia en x
                    self.v_d[3]=self.ventana.winfo_screenheight() // 4 +100 #distancia en y
                    self.ventana.geometry("%dx%d+%d+%d"%(self.v_d[0],self.v_d[1],self.v_d[2],self.v_d[3]))  
                    threading.Thread(target=self.menu).start()
                except:
                    print("error al expandir")
            threading.Thread(target=expandir).start()           #LLamada a Menu  
        elif self.estado=="reducido":              #REDUCIR
            def reducir():
                try:
                    self.v_d[0]=100
                    self.v_d[1]=48
                    self.v_d[2]=self.ventana.winfo_screenwidth() -95        #distancia en x
                    self.v_d[3]=self.ventana.winfo_screenheight() // 4 +300 #distancia en y
                    self.ventana.geometry("%dx%d+%d+%d"%(self.v_d[0],self.v_d[1],self.v_d[2],self.v_d[3]))
                except:
                    print("error al reducir")
            threading.Thread(target=reducir).start()
        elif self.estado=="notificando":              #NOTIFICANDO
            def notificando():
                try:
                    while self.v_d[0]< 300:
                        self.ventana.geometry("%dx%d+%d+%d"%(
                            self.v_d[0],self.v_d[1],self.v_d[2],self.v_d[3]))
                        self.v_d[0]=self.v_d[0]+1
                        self.v_d[1]=self.v_d[1]
                        self.v_d[2]=self.v_d[2]-1
                        self.v_d[3]=self.v_d[3]
                    etiqueta = Label(self.ventana,text=self.notificar,anchor="nw",
                                     height=3,width=25,wraplength=200)
                    etiqueta.place(x=90,y=0)
                    while self.temporizador_de_notificando >0 or self.boton_maus == True:
                        time.sleep(0.1)
                        if self.boton_maus == False:
                            self.temporizador_de_notificando = self.temporizador_de_notificando-0.1
                        elif self.temporizador_de_notificando == 0:
                            break
                    etiqueta.destroy()
                    while self.v_d[0]> 100:
                        self.ventana.geometry("%dx%d+%d+%d"%(
                            self.v_d[0],self.v_d[1],self.v_d[2],self.v_d[3]))
                        self.v_d[0]=self.v_d[0]-1
                        self.v_d[1]=self.v_d[1]
                        self.v_d[2]=self.v_d[2]+1
                        self.v_d[3]=self.v_d[3]
                    self.estado = self.terminar_notificar
                    self.constructor()
                except:
                    print("error al notificar")
            threading.Thread(target=notificando).start()
        elif self.estado=="escondido":
            try:
                self.estado ="reducido"
                self.constructor()
                self.estado="escondiendo"
                self.ventana.withdraw()
                def Validacion():
                    try:
                        if self.validacion == True:
                            def atadura (o):
                                validar.destroy()
                                self.ventana.deiconify()
                                self.estado="reducido"
                            def cerrar():
                                validar.destroy()
                                self.validacion =True
                            self.validacion = False
                            validar = tk.Tk()
                            validar.overrideredirect(True)
                            validar.attributes('-topmost',True)
                            validar.geometry("+%d+%d"%(self.v_d[2],self.v_d[3]))
                            marco = tk.Frame(validar,highlightbackground="Black",highlightthickness=2,bd=0)
                            marco.pack()
                            confirmar=Button(marco,width=1,height=1,bg="DarkBlue",activebackground="DarkBlue")
                            confirmar.pack()
                            confirmar.bind("<Enter>",atadura)
                            validar.after(3000,cerrar)
                            validar.mainloop()
                    except:
                        print("Fallo en la validacion")
                def capturar_raton():
                    self.validacion = True
                    s = pyautogui.position()
                    d = self.ventana.winfo_screenwidth()
                    while self.estado == "escondiendo":
                        if s[0] == d-1 :
                            if self.validacion == True:
                                threading.Thread(target=Validacion).start()
                            pass
                        time.sleep(1)
                        s = pyautogui.position()

                threading.Thread(target=capturar_raton).start()
            except:
                print("Fallo al esconder")
        elif self.estado=="plus":
            try:
                pantalla = self.ventana.winfo_screenwidth()
                alto_partido = self.ventana.winfo_screenheight()//2
                self.ventana.geometry("%dx%d+0+%d"%(pantalla,alto_partido,self.v_d[3]))
                threading.Thread(target=self.menu).start()
                
            except:
                print("Error al cambiar a plus")   

    def menu(self):
        if self.estado == "expandido":
            try:
                def boton_4():
                    self.estado="escondido"
                    self.constructor()
                def boton_3():
                    if self.estado == "expandido":
                        self.estado = "plus"
                        self.constructor()
                def boton_0():
                    def B0():
                        if self.mostrar_menu != "0":
                            try:
                                self.mostrar_menu = "0"
                                self.etiquetas = [None,None,None,None]
                                self.etiquetas[0] = Label(self.ventana,anchor="nw",height=1,width=10,)
                                self.etiquetas[1] = Label(self.ventana,anchor="nw",height=1,width=10,)
                                self.etiquetas[2] = Label(self.ventana,anchor="nw",height=1,width=10,)
                                self.etiquetas[3] = Label(self.ventana,anchor="nw",height=1,width=10,)
                                self.etiquetas[0].place (x=10,y=70)
                                self.etiquetas[1].place (x=150,y=70)
                                self.etiquetas[2].place (x=10,y=140)
                                self.etiquetas[3].place (x=150,y=140)
                                while self.mostrar_menu == "0" and self.estado == "expandido":
                                    self.etiquetas[0].config(text="CPU %s C"%(temperatura))
                                    time.sleep(0.1)
                                if self.etiquetas[0] != None:
                                    for etiqueta in self.etiquetas:
                                        etiqueta.destroy()
                            except:
                                print ("Problema en el menu Celsius")
                        else:
                            try:
                                for etiqueta in self.etiquetas:
                                 etiqueta.destroy()
                                 self.mostrar_menu = "nada"
                            except:
                                print("Problema en el else de menu celsius")
                    threading.Thread(target=B0).start()
                
                #--------------------------------BOTONES------------------------
                self.b_m_b[0]=Button(self.ventana,width=1,height=1,text="Ξ",fg="Darkred",command=boton_0,background="Blue",activebackground="Blue")
                self.b_m_b[1]=Button(self.ventana,width=1,height=1)
                self.b_m_b[2]=Button(self.ventana,width=1,height=1)
                self.b_m_b[3]=Button(self.ventana,width=1,height=1,text="⇐",background="green",command=boton_3,activebackground="green")
                self.b_m_b[4]=Button(self.ventana,width=1,height=1,text="⊖",background="DarkBlue",command=boton_4,activebackground="DarkBlue")
                self.b_m_b[0].place(x=100,y=0)
                self.b_m_b[1].place(x=140,y=0)
                self.b_m_b[2].place(x=180,y=0)
                self.b_m_b[3].place(x=220,y=0)
                self.b_m_b[4].place(x=260,y=0)

                while self.estado == "expandido":
                    time.sleep (0.5)
                for i in self.b_m_b:
                    i.destroy()  
            except:
                print("Fallo en los botones base del menu")
        elif self.estado =="plus":
            
            pass

        

class Cardinal_System:
    def __init__(self):
        self.cpu_temperatura = None
        self.cpu_celsius = None

    def temperatura(self,Correct=False):
        global temperatura
        try:
            if Correct == False:
                while True:
                    if self.cpu_temperatura == False:
                        break
                    print ("A-------")
                    temperatures = psutil.sensors_temperatures()
                    if "coretemp" in temperatures:
                        core_temps = temperatures["coretemp"]
                        for entry in core_temps:
                            if entry.label.startswith("Core"):
                                temperatura =entry.current
                            
                                if entry.current >= 70.00 and A.Low == False:
                                    A.Notifica(ismar.m_cpu_t_Heat())
                                    A.Low = True
                                elif A.Low == True:
                                    if entry.current <= 50.00:
                                        A.Low = False
                                        A.Notifica(ismar.m_cpu_t_normal())
                                else:
                                    time.sleep(40)
                                time.sleep(5)
            else:
                temperatures = psutil.sensors_temperatures()
                if "coretemp" in temperatures:
                    core_temps = temperatures["coretemp"]
                    for entry in core_temps:
                        if entry.label.startswith("Core"):
                            temperatura =entry.current        
                            if entry.current >= 70.00 and A.Low == False:
                                A.Notifica(ismar.m_cpu_t_Heat())
                                A.Low = True
                            elif A.Low == True:
                                if entry.current <= 50.00:
                                    A.Low = False
                                    A.Notifica(ismar.m_cpu_t_normal())
        except:
            print("Error en el servicio de Temperatura")

    def RGB(self):
        r, g, b = 0, 0, 0
        try:
            while True:
                #Cambiar Colores
                r = (r + 5) % 256
                g = (g + 2) % 256
                b = (b + 3) % 256
                color = f"#{r:02x}{g:02x}{b:02x}"
                A.ventana.config(bg=color)
                if A.estado == "expandido":
                    A.boton_hora.config(bg="black")
                    time.sleep(0.1)
                elif A.estado == "reducido":
                    A.boton_hora.config(bg="black")
                    time.sleep(1)
                elif A.estado == "notificando":
                    A.boton_hora.config(bg=color)
                    time.sleep(0.1)
                else:
                    A.boton_hora.config(bg="black")
                    time.sleep(2)
                ss = threading.active_count()
                print (f"Numero de Hilos :",{ss},end="\r")
            
        except:
            print("Fallo en el estado RGB")
            time.sleep(40)
            self.RGB()

    def Cardinal_start (self):
        threading.Thread (target=self.RGB).start()   
        threading.Thread (target=self.temperatura).start()



ismar = ismart.GText()

A =Akura()
A.constructor()
A.Notifica(ismar.saludo())


C = Cardinal_System()
C.Cardinal_start()




A.ventana.mainloop()




        

 

        