import tkinter as tk
from tkinter import Button,Label
import screen_brightness_control as sbc
import time
import re
import pyperclip
import threading
import psutil
import pyautogui
import pygetwindow as gw
import win32gui                             #pywin32
import win32process
import keyboard
import os
import subprocess
#-----------------I+D------------
import ollama
import ismart
from ismart import particula


# Resolucion de pantalla 1024 x 768
# :::::ADVERTENCIA:::::: El boton A en Akura apaga instantaneamente el PC
#::::::WARNING:::::::::: Button A in Akura instantly shuts down the PC

usuario = os.environ["USERNAME"]
colorglobal = None
color_rgb={}
Activo = True



ismar = ismart.GText()

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
        self.horarios ={"19:00":"comer",        #Diccionario para contener horarios
                        "07:00":"desayunar",
                        "12:00":"almorzar",
                        "00:00":"dormir",
                        "01:00":"acostarte"}
        self.messages = []                      #Guarda los mensajes rol y contenido para dar seguimiento
        self.texto_generado = "Vamos a Empezar" #String donde se guarda el ultimo mensaje
        self.seleccion =200                     #Que tanto texto generara la IA
        self.medicion = None                    #Panel que muestra el consumo de red
        self.medicion_Active = False            #Para decidir si activar la ventana o no
        self.red= True                          #Para red
        self.ventana_red =True                  #Para habilitar o no la ventana de red
        self.etiqueta_red =None                 #Para red
        self.consumo_de_red="0B--0B"            #Para guardar el consumo de la red actual
        self.portapapeles=""                    #Aqui se guarda lo que esta copiado actualmente en el portapapeles
        self.detectado_enlace=False             #Permite mostrar una advertencia al detectar un enlace
        self.enlaces=["Nada"]                   #Guarda los enlaces ya capturados
        self.descargas={1:False,2:False,3:False}#aqui se registran los hilos de descarga
        try:
            self.brightnes = sbc.get_brightness()
            self.brightnes = True if not None else False
        except:
            self.brightnes = False

    def tiempo (self,Correct=False):
        try:
            if Correct == False:
                while Activo == True:
                    if self.hora!=time.strftime("%I:%M"):
                        self.hora= time.strftime("%I:%M")
                        self.boton_hora.config(text=self.hora,fg="Blue")
                        hora = time.strftime("%H:%M")
                        for clave,valor in self.horarios.items():
                            if clave == hora:
                                self.Notifica(ismar.hora_de(valor))
                                break
                    time.sleep (45)   
                    
            else:
                self.hora= time.strftime("%I:%M")
                self.boton_hora.config(text=self.hora,fg="Blue")    
        except:
            print("Error al mostrar hora")
        
    def Notifica(self,notificacion,terminar="reducido"):
        while self.estado == "notificando":
            time.sleep(2)
        self.estado="reducido"
        self.constructor()
        self.notificar = notificacion
        self.estado = "notificando"
        self.terminar_notificar = terminar
        self.temporizador_de_notificando = 20
        self.constructor()
        pass

    def boton_h(self):
        if self.estado == "reducido":
            self.estado = "expandido"
            self.constructor()
        elif self.estado == "notificando":
            self.temporizador_de_notificando = "evento"        #si se da click muestre el area que exige la notificacion
        elif self.estado =="plus" :
            self.plus.lift()
        else :
            self.estado = "reducido"
            self.constructor()

    def medir_datos(self,maus=None,correct=True):            
        def interfaz_de_red(maus=False):
            try:
                if self.red == True and self.medicion_Active == False and maus == False and self.ventana_red ==True:
                    self.medicion_Active = True
                    self.medicion = tk.Toplevel(self.ventana)
                    self.etiqueta_red = Label(self.medicion,text=self.consumo_de_red)
                    self.etiqueta_red.pack(expand=True)
                    self.medicion.geometry(f"+{self.v_d[2]}+10")
                    self.medicion.overrideredirect(1)               #Botones de ventana por defecto apagados
                    self.medicion.attributes('-topmost',True)       #siempre encima
                elif self.red == False or maus == True:
                    self.medicion_Active = False
                    self.medicion.destroy()
            except:
                pass
        def control_de_red():
            def convertir_byts(valor):
                conversion =["B","Kb","Mb","Gb","Tb"]
                i = 0
                while valor >= 1024:
                    valor=valor/1024
                    i=i+1
                return f"{round(valor,2)}{conversion[i]}"
            valor_anterior = 0
            iterador = 0
            while Activo == True:
                try:
                    consumo =psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
                except:
                    consumo = 0                
                if consumo != valor_anterior:
                    self.red = True
                    iterador = 100
                    consumo_actual= consumo - valor_anterior
                    CONSUMO = convertir_byts(consumo)
                    CONSUMO_ACTUAL =convertir_byts(consumo_actual)
                    try:
                        self.consumo_de_red=f"{CONSUMO_ACTUAL}--{CONSUMO}"
                        self.etiqueta_red.config(text=f"{CONSUMO_ACTUAL}--{CONSUMO}")
                    except:
                        pass
                else:
                    if iterador >= 0:
                        iterador = iterador-1
                        CONSUMO = convertir_byts(consumo)
                        try:
                            self.consumo_de_red=f"0B--{CONSUMO}"
                            self.etiqueta_red.config(text=f"0B--{CONSUMO}")
                        except:
                            pass
                    else:
                        self.red=False
                time.sleep(1)
                valor_anterior = consumo
            pass
        if correct == True:
            control_de_red()
        else:
            interfaz_de_red(maus=maus)
        
    def DO(self):
        def es_enlace_youtube(url):
            return re.match(r'https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)', url) is not None
        try:
            self.portapapeles = pyperclip.paste()
            if self.estado!="notificando"and self.detectado_enlace==False and es_enlace_youtube(self.portapapeles) and not self.portapapeles in self.enlaces:
                self.enlaces.append(self.portapapeles)
                self.Notifica(ismar.enlace_detectado(),"youtube")
        except:
            pass
        if C.maus_esquina == True:
            self.medir_datos(maus=True,correct=False)
        else:
            self.medir_datos(maus=False,correct=False)
        self.ventana.after(1000,self.DO)

    def boton_h_apuntado(self,objeto):
        if self.estado == "reducido" and self.mostrar_menu != "popup":
            self.mostrar_menu = "popup"
            self.menu()
        
    def boton_h_desapuntado(self,objeto):
        #self.boton_maus = False
        #self.tiempo(Correct=True)
        pass  

    def boton_h_ck_derecho(self,objeto):
        self.estado = "escondido"
        self.constructor()

    def constructor(self):
        if self.estado == "iniciando":
            global color_rgb
            self.v_d[2]=self.ventana.winfo_screenwidth() -95        #distancia en x
            self.v_d[3]=self.ventana.winfo_screenheight() // 4 +300 #distancia en y

            self.ventana.title(self.nombre)           #Nombre del programa
            self.ventana.overrideredirect(1)               #Botones de ventana por defecto apagados
            self.ventana.attributes('-topmost',True)       #siempre encima
            self.ventana.geometry("+%d+%d"%(self.v_d[2],self.v_d[3]))
            self.ventana.config(background="black")
            
            #zona = Canvas(self.ventana,bg="White")
            #zona.pack(side=tk.TOP, anchor='w')
            self.marco = tk.Frame(self.ventana,highlightthickness=1,highlightbackground="Blue",highlightcolor="Blue")
            self.marco.pack(side="left")
            color_rgb.update({self.marco:"frame"})
            self.boton_hora = Button(self.marco,text=self.nombre,anchor="nw",
                                     font=("Arial", 22),height=1,width=5, bg="Black",fg="Red",
                                     command=self.boton_h,activeforeground="Red",activebackground="Black")
            self.boton_hora.pack()
            
            self.boton_hora.bind("<Enter>",self.boton_h_apuntado)
            self.boton_hora.bind("<Leave>",self.boton_h_desapuntado)
            self.boton_hora.bind("<Button-3>",self.boton_h_ck_derecho)
            self.estado = "reducido"
            threading.Thread(target=self.tiempo).start()
            threading.Thread(target=self.medir_datos).start()
            self.ventana.after(3000,self.DO)
        elif self.estado=="expandido":               #Expandir
            try:
                self.menu()           #LLamada a Menu  
            except Exception as e:
                print(f"Error al expandir {e}")
                self.Notifica(f"Error al expandir {e}")
        elif self.estado=="reducido":                #REDUCIR
            try:
                self.ventana.geometry("+%d+%d"%(self.v_d[2],self.v_d[3]))
            except:
                print("error al reducir")
        elif self.estado=="notificando":             #NOTIFICAR
            def notificando():
                def animation():
                    particula(self.ventana,"Plop",escala=5,x=self.v_d[2],y=self.v_d[3]-40).auto()
                try:
                    while self.v_d[0]< 300:
                        self.ventana.geometry("%dx%d+%d+%d"%(
                            self.v_d[0],self.v_d[1],self.v_d[2],self.v_d[3]))
                        self.v_d[0]=self.v_d[0]+1
                        self.v_d[1]=self.v_d[1]
                        self.v_d[2]=self.v_d[2]-1
                        self.v_d[3]=self.v_d[3]
                    etiqueta = Label(self.ventana,text=self.notificar,anchor="nw",
                                     height=3,width=29,wraplength=200,bg="Black",fg="spring green")
                    etiqueta.place(x=90,y=0)
                    self.ventana.after(100,animation)
                    while self.temporizador_de_notificando >0 or self.boton_maus == True:
                        time.sleep(0.1)
                        if self.boton_maus == False and self.temporizador_de_notificando != "evento":
                            self.temporizador_de_notificando = self.temporizador_de_notificando-0.1
                        elif self.temporizador_de_notificando == 0 or self.temporizador_de_notificando == "evento":
                            break
                    etiqueta.destroy()
                    while self.v_d[0]> 100:
                        self.ventana.geometry("%dx%d+%d+%d"%(
                            self.v_d[0],self.v_d[1],self.v_d[2],self.v_d[3]))
                        self.v_d[0]=self.v_d[0]-1
                        self.v_d[1]=self.v_d[1]
                        self.v_d[2]=self.v_d[2]+1
                        self.v_d[3]=self.v_d[3]
                    if self.temporizador_de_notificando == "evento":
                        self.estado = self.terminar_notificar
                    else:
                        self.estado = "reducido"
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
                            confirmar=Button(marco,width=3,height=1,bg="DarkBlue",activebackground="DarkBlue")
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
                    self.ventana.deiconify()
                threading.Thread(target=capturar_raton).start()
            except:
                print("Fallo al esconder")
        elif self.estado=="plus":
            try:
                self.menu()
            except:
                print("Error al cambiar a plus")   
        elif self.estado=="youtube":
            def revisar_espacio():
                for clave,valor in self.descargas.items():
                    if valor==False:
                        return clave
                return "NoSpace"
            def VIDEO():
                audio.destroy()
                video.destroy()
                a=revisar_espacio()
                if a == "NoSpace":
                    self.Notifica("Maximas descargas alcanzadas")
                    return
                p=particula(self.ventana,"Load",escala=5,x=self.v_d[2]+10,y=self.v_d[3]+60*a,color_global=colorglobal)
                ismart.Descargar(self.portapapeles,model=self,p=p,ID=a).start()
                progreso.config(text="Se ha iniciado la descarga")
                self.ventana.after(200,SALIR)
            def AUDIO():
                audio.destroy()
                video.destroy()
                a=revisar_espacio()
                if a == "NoSpace":
                    self.Notifica("Maximas descargas alcanzadas")
                    return
                p=particula(self.ventana,"Load",escala=5,x=self.v_d[2]+10,y=self.v_d[3]+60*a,color_global=colorglobal)
                ismart.Descargar(self.portapapeles,video=False,model=self,p=p).start()
                progreso.config(text="Se ha iniciado la descarga")
                self.ventana.after(200,SALIR)
            def SALIR():
                self.estado="reducido"
                descargar.destroy()
                self.detectado_enlace=False
            self.detectado_enlace=True
            descargar=tk.Toplevel(self.ventana)
            descargar.overrideredirect(True)
            descargar.attributes("-topmost",True)
            marco=tk.Frame(descargar,highlightbackground=colorglobal,highlightcolor=colorglobal,highlightthickness=3)
            marco.pack()
            video=Button(marco,text="Video",command=VIDEO,bg="black",fg="green")
            audio=Button(marco,text="Audio",command=AUDIO,bg="black",fg="green")
            salir=Button(marco,text="Salir",command=SALIR,bg="black",fg="green")
            progreso=Label(marco,text="Selecciona el formato",bg="black",fg="spring green")
            salir.pack()
            video.pack(side="left")
            audio.pack(side="right")
            progreso.pack()
            descargar.geometry(f"+{self.v_d[2]-250}+{self.v_d[3]}")

    def menu(self):
        if self.estado == "expandido":
            try:
                def boton_4():
                    self.ventana.destroy()
                def boton_3():
                    if self.estado == "expandido":
                        self.estado = "plus"
                        self.constructor()
                def boton_2():
                    try:
                        # Apaga la computadora
                        os.system("shutdown -p")
                    except Exception as e:
                        print(f"Hubo un error al apagar la computadora: {e}")
                        self.Notifica(f"Hubo un error al apagar la computadora: {e}")
                    pass
                def boton_0():
                    def salir(event=None):
                        global color_rgb
                        del color_rgb[control_panel_contenedor]
                        control_panel.destroy()
                    def shif_ventana():
                        if C.shif_ventana ==True:
                            C.shif_ventana =False
                            control_panel_shif.config(text="Apagado")

                        else:
                            C.shif_ventana =True
                            control_panel_shif.config(text="Encendido")
                            threading.Thread(target=C.canviar_ventana).start()
                    def anadir(o=None,u=None):
                        horario = entrada_horario.get()
                        if horario:
                            partes =horario.split(".")
                            self.horarios.update({partes[0]:partes[1]})
                            entrada_horario.delete(0,tk.END)
                    def red():
                        if self.ventana_red ==True:
                            self.ventana_red =False
                            Boton_red.config(text="Apagado")
                        else:
                            self.ventana_red =True
                            Boton_red.config(text="Encendido")
                    def cpu():
                        if C.cpu_notif==True:
                            C.cpu_notif=False
                            Boton_cpu.config(text="Apagado")
                        else:
                            C.cpu_notif=True
                            threading.Thread(target=C.cpu_control).start()
                            Boton_cpu.config(text="Encendido")
                    def YB():
                        self.enlaces=["Nada"]
                        youtube_boton.config(text="Reiniciado YB")
                    try:
                        self.estado ="reducido"
                        global color_rgb
                        control_panel = tk.Toplevel(self.ventana,background="black")
                        control_panel.overrideredirect(1)
                        control_panel.attributes('-topmost',True)

                        control_panel_contenedor=tk.Frame(control_panel,highlightthickness=8,bg="black")
                        control_panel_contenedor.pack()
                        color_rgb.update({control_panel_contenedor:"frame"})

                        control_panel_salir = Button(control_panel_contenedor,command=salir,text="Salir",bg="black",fg="spring green")
                        control_panel_salir.pack()

                        control_panel_shif=Button(control_panel_contenedor,command=shif_ventana,text="Shif ventana",bg="black",fg="spring green")
                        control_panel_shif.pack()
                        Boton_red=Button(control_panel_contenedor,command=red,text="Medir Red",bg="black",fg="spring green")
                        Boton_red.pack()
                        Boton_cpu=Button(control_panel_contenedor,command=cpu,text="consumo CPU",bg="black",fg="spring green")
                        Boton_cpu.pack()
                        youtube_boton=Button(control_panel_contenedor,text="Reset YB",command=YB,bg="black",fg="spring green")
                        youtube_boton.pack()
                        horario_frame=tk.Frame(control_panel_contenedor)
                        horario_frame.pack()
                        etiqueta_horario=Label(horario_frame,text="09:00.ir a",bg="black",fg="spring green")
                        etiqueta_horario.pack(side="left")
                        entrada_horario = tk.Entry(horario_frame,width=10,bg="black",fg="spring green")
                        entrada_horario.pack(side="right")
                        entrada_horario.bind('<Return>',anadir)
                        entrada_horario.bind('<Escape>',salir)

                        control_panel.geometry(f"+{self.v_d[2]-100}+{self.v_d[3]-300}")

                    except Exception as e:
                        print(f"Fallo al mostrar el menu {e}")
                def brillo(valor):
                    try:
                        valor = int(float(valor))
                        sbc.set_brightness(valor)  # Establecer el brillo
                        etiqueta_brillo.config(text= f"Brillo \n{valor} ")
                    except:
                        pass
                #-------------------------------Ventana-------------------------
                expandido =tk.Toplevel(self.ventana,bg="black")
                expandido.overrideredirect(True)
                expandido.attributes('-topmost',True)
                expandido.geometry("+%d+%d"%(self.v_d[2],self.v_d[3]-200))
                #--------------------------------BOTONES------------------------
                marco = tk.Frame(expandido,highlightthickness=1,highlightbackground="blue",highlightcolor="blue")
                marco.pack()
                self.b_m_b[0]=Button(marco,width=3,height=1,text="Ξ",fg="Black",command=boton_0,background="Blue",activebackground="Blue")
                self.b_m_b[1]=Button(marco,width=3,height=1,bg="black",fg="green")
                self.b_m_b[2]=Button(marco,width=3,height=1,text="A",command=boton_2,bg="black",fg="spring green")
                self.b_m_b[3]=Button(marco,width=3,height=1,text="⇐",background="green",command=boton_3,activebackground="green",fg="Black")
                self.b_m_b[4]=Button(marco,width=3,height=1,text="⊖",background="DarkBlue",command=boton_4,activebackground="DarkBlue",fg="black")
                self.b_m_b[0].pack()
                self.b_m_b[1].pack()
                self.b_m_b[2].pack()
                self.b_m_b[3].pack()
                self.b_m_b[4].pack()
                if self.brightnes == True:
                    slider = tk.ttk.Scale(expandido, from_=0, to=100, orient='horizontal',command=brillo)
                    slider.set(sbc.get_brightness())
                    etiqueta_brillo = Label(expandido,text= f"Brillo \n{slider.get()} ",bg="black",fg="spring green")
                    etiqueta_brillo.pack()
                    slider.pack()
                else:
                    print("Se esta usando PC o adaptador no compatible con el brillo")
                def mantener_expancion():
                    while self.estado == "expandido" and C.maus_esquina==True:
                        color_rgb.update({marco:"frame"})
                        time.sleep (0.1)
                    try:
                        del color_rgb[marco]
                        expandido.destroy()
                        self.estado="reducido"
                    except:
                        pass
                threading.Thread(target=mantener_expancion).start()
            except Exception as e:
                print(f"Fallo en los botones base del menu {e}")
        elif self.estado =="plus":
            try:
                def empezar(argumento):
                    def generar_texto():
                        try:
                            def añadir_mensaje(rol,contenido):
                                self.messages.append({"role":rol,"content":contenido})
                                pass
                            YY=chat.get()
                            chat.config(state="readonly")
                            añadir_mensaje("User",YY)
                            if self.seleccion==0:
                                stream = ollama.chat(model="Akura",messages=self.messages,stream=True,)    
                            else:
                                stream = ollama.chat(model="Akura",messages=self.messages,stream=True,options={"num_predict":self.seleccion})
                            A=[]
                            self.texto_generado=self.texto_generado+"\n\n"
                            texto_etiqueta.insert   (tk.END,"\n\n")
                            contador = 0
                            for chunk in stream:
                                A.append(chunk["message"]["content"])
                                self.texto_generado=self.texto_generado+str(A[contador])
                                if texto_etiqueta.winfo_exists():
                                    texto_etiqueta.insert   (tk.END,A[contador])
                                    texto_etiqueta.yview(tk.END)
                                contador = contador+1
                            añadir_mensaje("assistant",self.texto_generado)
                            if self.estado != "plus":
                                self.Notifica(ismar.ia_genero_texto(),terminar="plus")
                            if chat.winfo_exists():
                                chat.config(state="normal")
                        except Exception as e:
                            print(f"Fallo en la generacion de contenido {e}")
                            self.Notifica(f"Fallo en la generacion de contenido {e}")
                    threading.Thread(target=generar_texto).start()
                def RESET():
                    self.messages = []
                    texto_etiqueta.delete(1.0, tk.END)
                    texto_etiqueta.insert(tk.END,"Estas en una nueva instancia")
                    self.texto_generado = "Estas en una nueva instancia"
                def copy_text():
                    try:
                        # Copiar el texto seleccionado al portapapeles
                        self.ventana.clipboard_clear()  # Limpiar el portapapeles
                        self.ventana.clipboard_append(self.texto_generado)  # Añadir el texto seleccionado
                    except:
                        pass  # No hay texto seleccionado
                
                #-------------------------Ventana-------------------
                self.plus = tk.Toplevel(self.ventana)
                def Salir():
                    global color_rgb
                    self.estado="reducido"
                    del color_rgb[frame]
                    del color_rgb[contenedor]
                    del color_rgb[contenedor_de_botones]
                    del color_rgb[contenedor_de_radio]
                    del color_rgb[Conten]
                    self.plus.destroy()
                self.plus.protocol("WM_DELETE_WINDOW",Salir)

                #-------------------------Objetos-------------------
                Conten = tk.Frame(self.plus,highlightthickness=2)
                Conten.pack(side="right")
                contenedor_de_botones =tk.Frame(Conten,highlightthickness=1)
                contenedor_de_botones.pack()
                contenedor_de_radio = tk.Frame(Conten,highlightbackground="blue",  # Color del borde cuando no está enfocado
                                                            highlightcolor="red",        # Color del borde cuando está enfocado
                                                            highlightthickness=1)        # Grosor del borde)
                contenedor_de_radio.pack()
                contenedor = tk.Frame(self.plus,highlightbackground="blue",highlightcolor="blue",highlightthickness=2)
                contenedor.pack(expand=True,side="left")
                
                frame = tk.Frame(contenedor,highlightthickness=1)
                frame.pack()
                texto_etiqueta = tk.Text(frame,bg="Black",wrap=tk.WORD,fg="White",font=("Arial", 16,),width=50,height=10)
                texto_etiqueta.insert(tk.END, self.texto_generado)
                texto_etiqueta.pack()   
                chat = tk.Entry(contenedor,width=100)
                chat.pack()
                chat.bind('<Return>',empezar)
            
                reset = Button(contenedor_de_botones,command=RESET,text="Reset",)
                reset.pack(side="left")
                copy = Button(contenedor_de_botones,command=copy_text,text="Copiar")
                copy.pack(side="right")
                #-------------------Botones Radio-----------------------------
                selector_1 =tk.Radiobutton(contenedor_de_radio, text="Limitar a 200", variable=self.seleccion, value=200)
                selector_1.pack(anchor=tk.W)
                selector_2 =tk.Radiobutton(contenedor_de_radio, text="Limitar a 500", variable=self.seleccion, value=500)
                selector_2.pack(anchor=tk.W)
                selector_3 =tk.Radiobutton(contenedor_de_radio, text="Ilimitado 💀", variable=self.seleccion, value=0)
                selector_3.pack(anchor=tk.W)
                global color_rgb
                color_rgb.update({frame:"frame",contenedor:"frame",contenedor_de_botones:"frame",contenedor_de_radio:"frame",Conten:"frame"})
                destructor_plus=Button(contenedor_de_botones,command=Salir)
                destructor_plus.pack()        

            except Exception as e:
                print (f"Fallo en el sector de IA {e}")
                self.Notifica(f"Fallo en el sector de IA {e}")
        elif self.mostrar_menu == "popup" and self.estado == "reducido" :
            try:
                def crear_objeto_miniventana(code,yode):
                    try:
                        def comprobar():
                            if self.mostrar_menu != "popup" or self.estado != "reducido" or C.maus_esquina==False:
                                atadura(correct=True)
                            else:
                                popup.after(200,comprobar)
                        def atadura (o=None,correct=False):
                            self.mostrar_menu ="nada"
                            popup.destroy()
                            if correct == False:
                                if code == 4:
                                    os.startfile(rf"C:\\Users\{usuario}")
                                elif code == 2:
                                    #subprocess.run("cmd.exe")
                                    pass
                                elif code == 1:
                                    def opera():
                                        subprocess.run([rf"C:\\Users\{usuario}\AppData\Local\Programs\Opera\opera.exe"])
                                    threading.Thread(target=opera).start()
                                elif code == 3:
                                    def vscode():
                                        subprocess.run([rf"C:\Users\{usuario}\AppData\Local\Programs\Microsoft VS Code\Code.exe"])
                                    threading.Thread(target=vscode).start()

                        file = {1:["O",self.v_d[2]+40,self.v_d[3]+100,"Red"],
                                2:["C",self.v_d[2]-40,self.v_d[3]+100,"Blue"],
                                3:["V",self.v_d[2]+40,self.v_d[3]-70,"Green"],
                                4:["E",self.v_d[2]-40,self.v_d[3]-70,"Yellow"]}
                        popup = tk.Toplevel(self.ventana)
                        popup.overrideredirect(True)
                        popup.attributes('-topmost',True)
                        popup.geometry("+%d+%d"%(file[code][1],file[code][2]))
                        marco = tk.Frame(popup,highlightbackground=file[code][3],highlightthickness=2,bd=0)
                        marco.pack()
                        confirmar=Button(marco,width=3,height=1,bg="DarkBlue",activebackground="DarkBlue",text=file[code][0],fg="White")
                        confirmar.pack()
                        confirmar.bind("<Enter>",atadura,)
                        popup.after(100,comprobar)
                    except Exception as e:
                        print(f"Fallo individual en la miniventana {code} del tipo {e}")
                for i in range (1,5):
                    crear_objeto_miniventana(i,i)
                    

            except:
                print("Fallo al crear ventana PopUP")

        

class Cardinal_System:
    def __init__(self):
        self.selector = None
        self.cpu_temperatura = None
        self.cpu_estado = None
        self.cpu_notif=True
        self.maus_esquina = False
        self.shif_ventana = True
        self.shif_UI =tk.Toplevel(A.ventana)
        self.shif_UI.overrideredirect(1)               #Botones de ventana por defecto apagados
        self.shif_UI.attributes('-topmost',True)       #siempre encima
        self.shif_UI.withdraw()
        self.marco=None                                #El marco de la ventana shift UI

    def RGB(self):
        r, g, b = 0, 0, 0
        try:
            global colorglobal
            global color_rgb
            while Activo == True:
                #Cambiar Colores
                r = (r + 5) % 256
                g = (g + 2) % 256
                b = (b + 3) % 256
                color = f"#{r:02x}{g:02x}{b:02x}"
                A.ventana.config(bg=color)
                colorglobal = color
                try:
                    for clave,valor in color_rgb.items():
                        if valor== "frame":
                            clave.config(highlightbackground=color,highlightcolor=color)
                except:
                    pass
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

    def cpu_control(self,contador=0):
        try:
            while Activo == True and self.cpu_notif==True:
                self.cpu_estado = psutil.cpu_percent()
                if self.cpu_estado >= 60:
                    contador = contador+1
                    if contador == 15:
                        for _ in range (0,2):
                            procesos = [(p.info["name"],p.info["cpu_percent"])for p in psutil.process_iter(["name","cpu_percent"])]
                            procesos.sort(key=lambda x:x[1],reverse=True)
                            time.sleep(1)
                        if str(procesos[1][0]) == "Python.exe":A.Notifica("Me siento mal")                            
                        else:A.Notifica(ismar.cosumo_cpu_alto(procesos[1][0],procesos[2][0],procesos[3][0]))
                        procesos = None
                else:
                    if contador >= 15:
                        A.Notifica(ismar.consumo_cpu_normal())
                    contador = 0
                time.sleep(1)
        except Exception as e:
            print(f"Error al medir la cpu ERROR CODE {e}")
            A.Notifica(f"Error al medir CPU {e}")

    def canviar_ventana(self):
        def iniciar():
            def obtener_pid_por_titulo(titulo):
                hwnd = win32gui.FindWindow(None, titulo)  # Encuentra la ventana por su título
                if hwnd:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Obtiene el PID
                    return pid
                return None
            def obtener_nombre_programa(titulo):
                pid = obtener_pid_por_titulo(titulo)
                if pid:
                    try:
                        p = psutil.Process(pid)
                        return p.name()  # Retorna solo el nombre del programa
                    except psutil.NoSuchProcess:
                        return None
                return None
            def listar_ventanas():
                ventanas = gw.getAllTitles()
                nombres_programas = {}
                ignorar = ["","Program Manager","Host de experiencia del shell de Windows","Administrador de tareas","Akura"]
                for titulo in ventanas:
                    if titulo in ignorar:
                        continue
                    nombre_programa = obtener_nombre_programa(titulo)
                    if nombre_programa:
                        nombres_programas[titulo] = nombre_programa
                return nombres_programas
            def mantener():
                try:
                    while keyboard.is_pressed("shift"):
                        time.sleep(0.1)
                    try:
                        del color_rgb[self.marco]
                        self.marco.destroy()
                        self.shif_UI.withdraw()
                    except:
                        pass
                except:
                    pass

            ventanas = listar_ventanas()
            #------------------Ventana-----------------
            maus = pyautogui.position()
            self.shif_UI.deiconify()
            self.shif_UI.geometry(f"+{maus[0]}+{maus[1]}")
            
            self.marco = tk.Frame(self.shif_UI,highlightthickness=4,highlightbackground=colorglobal,highlightcolor=colorglobal)
            self.marco.pack()
            color_rgb.update({self.marco:"frame"})
            class boto:
                def __init__(self,Titulo,frame):
                    self.titulo = Titulo
                    self.frame =frame
                    boton = Button(frame,command=self.desactivar)
                    boton.pack(side="left")
                    boton.bind("<Enter>",self.activar)
                def desactivar(self):
                    try:
                        ventana = gw.getWindowsWithTitle(self.titulo)[0]
                        ventana.close()
                        self.frame.destroy()
                    except IndexError:
                        print("Ventana no encontrada.")
                def activar(self,evento=None):
                    try:
                        ventana = gw.getWindowsWithTitle(self.titulo)[0]
                        ventana.minimize()  # Minimizar la ventana
                        ventana.restore()   # Restaurar la ventana
                        ventana.activate()  # Activar la ventana
                    except IndexError:
                        print("Ventana no encontrada.")
            for i, (titulo, nombre) in enumerate(ventanas.items()):
                t = tk.Frame(self.marco,highlightthickness=1,highlightbackground="Blue",highlightcolor="Blue")
                label = Label(t,text=f"{nombre} ({titulo})")
                c=boto(Titulo=titulo,frame=t)
                t.pack(anchor="w")
                label.pack(side="right")
            mantener() 
        def bucle():
            while not keyboard.is_pressed("shift") and Activo == True and self.shif_ventana == True:
                time.sleep(0.1)
            if self.shif_ventana == True:
                iniciar()
                bucle()
        bucle()
        
    def Comprobar_Maus(self):
        def comprobar():
            while Activo == True:
                position = pyautogui.position()
                if position[0] > A.v_d[2]-100:
                    self.maus_esquina = True
                else:
                    self.maus_esquina = False
                time.sleep(0.1)
                
        comprobar()

    def Cardinal_start (self):
        threading.Thread (target=self.RGB).start()   
        threading.Thread (target=self.cpu_control).start()
        threading.Thread(target=self.Comprobar_Maus).start()
        threading.Thread(target=self.canviar_ventana).start()
        

    






A =Akura()
A.constructor()
A.Notifica(ismar.saludo())



C = Cardinal_System()
C.Cardinal_start()



A.ventana.mainloop()
Activo=False
A.estado="Cerrando"
time.sleep(1)

import sys
sys.exit()

        

 

        