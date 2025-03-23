####Potente libreria creada por WiseHolos para usar simultaneamente con (((AKURA)))

import random
import time
import tkinter as tk
import sqlite3
import json
import yt_dlp
import threading
import os
import psutil
usuario = os.environ["USERNAME"]

colores={"0":"White","1":"Black","2":"Green","3":"Blue","4":"gray",
         "5":"Red","6":"Pink","7":"DarkBlue","8":"yellow","9":"gold"}

class GText:
    def __init__(self):
        #Formas de saludo
        self.libreria_1=["Buenas","Hola","Bienvenido","Es un placer","Ya te extrañaba", 
                        "Al fin regresas","Te tardaste en volver","Ya era hora",
                        "Regresaste","Que hacemos","Que tal","¡Hey!","Mi distinguido",
                        "Es un placer","Que tal tu dia","Okaeri-Nasai","Ohaio"]
        random.shuffle(self.libreria_1)
        #Formas de referirse al usuario
        self.libreria_2=["Amo","Maestro","Sensei","Mentor","Dueño","Patrón","Guía",
                         "Soberano","Jefe","Propitario","Aniki","Onii-Chan","Anata","Kami-sama"]
        random.shuffle(self.libreria_2)
        #Formas de referirse al CPU
        self.libreria_3=["Nucleo","Core","CPU","Procesador",]
        random.shuffle(self.libreria_3)
        #Formas de llamar al calor
        self.libreria_4=["Caliente","Ardiendo","Inestable","OverHeat","Sobreviviendo",
                         "LLorando"]
        random.shuffle(self.libreria_4)
        #Formas de llamar a la estabilidad
        self.libreria_5=["Estable","Normal","Fuera de peligro","En rango","Vivo","Mejor"]
        random.shuffle(self.libreria_5)
        #Formas de aliviarse
        self.libreria_6=["Que alivio","Menos mal","Me preocupe","Eso fue peligroso",
                         "No lo Hagas seguido","Al FIN"]
        random.shuffle(self.libreria_6)
        #Formas de referirse a los programas malos
        self.libreria_7=["Traidores","Enemigos","Parasitos","Enemigos de la sociedad","Virus","programas maliciosos"]
        random.shuffle(self.libreria_7)
        #Formas de posecion tiene
        self.libreria_8=["tiene","posee","aloja","mantiene","trabaja para","ayuda"]
        random.shuffle(self.libreria_8)
        #Formas de referirse al tiempo
        self.libreria_9=["hora","es tiempo","ya debe","debería","requiere",]
        random.shuffle(self.libreria_9)
        #Formas de referirse a termine
        self.libreria_10=["Terminé","Acabé","Acabo","Finalicé","Conluí","Completé"]
        random.shuffle(self.libreria_10)
        #Formas de referirse al texto
        self.libreria_11=["las lineas","las palabras","las fraces","el mensaje","el codigo","la tarea","el artículo"]
        random.shuffle(self.libreria_11)
        #Formas de referirse a Escribir
        self.libreria_12=["escribir","componer","redactar","crear","formular","generar","dictar","procesar"]
        random.shuffle(self.libreria_12)
        #Formas par detectar
        self.libreria_13=["encontré","detecté","hallé","descubrí","copiaste","activaste","señalaste"]
        random.shuffle(self.libreria_13)
        #Formas de enlace
        self.libreria_14=["un enlace","un vínculo","una ruta","una dirección"]
        random.shuffle(self.libreria_14)
        #lo quieres?
        self.libreria_15=["lo quieres?","lo descargo?","lo deseas?","lo necesitas?","lo bajo?","te apetece?","intento?",]
        random.shuffle(self.libreria_15)
    def saludo (self):
        random.shuffle(self.libreria_1)   
        return "%s %s"%(self.libreria_1[0],self.libreria_2[0])
    def m_cpu_t_Heat(self):
        random.shuffle(self.libreria_4)    
        random.shuffle(self.libreria_3)    
        return "%s el %s está %s"%(self.libreria_2[0],self.libreria_3[0],self.libreria_4[0])
    def m_cpu_t_normal(self):
        random.shuffle(self.libreria_5)    
        random.shuffle(self.libreria_6)    
        return "%s %s el %s está %s"%(self.libreria_6[0],self.libreria_2[0],self.libreria_3[0],self.libreria_5[0])
    def cosumo_cpu_alto(self,uno,dos,tres):
        #Amo el Cpu aloja un haker
        random.shuffle(self.libreria_8)
        return f"{self.libreria_2[0]} el {self.libreria_3[0]} {self.libreria_8[0]} unos {self.libreria_7[0]}\n {uno}--{dos}--{tres}"
    def consumo_cpu_normal(self):
        #amo el cpu esta estable
        random.shuffle(self.libreria_5)
        return f"{self.libreria_2[0]} el {self.libreria_3[0]} esta {self.libreria_5[0]}"
    def hora_de(self,nececidad="vaguear"):
        #Amo hora de desyunar
        random.shuffle(self.libreria_9)
        return f"{self.libreria_2[0]} {self.libreria_9[0]} de {nececidad}"
    def ia_genero_texto(self):
        #Termine de escribir el texto para ti Amo
        random.shuffle(self.libreria_10)
        random.shuffle(self.libreria_12)
        random.shuffle(self.libreria_11)
        return f"{self.libreria_10[0]} de {self.libreria_12[0]} {self.libreria_11[0]} para ti {self.libreria_2[0]}"
    def enlace_detectado(self):
        #Amo encontre un enlace a Youtube . lo descargo?
        random.shuffle(self.libreria_13)
        random.shuffle(self.libreria_14)
        random.shuffle(self.libreria_15)
        return f"{self.libreria_2[0]} {self.libreria_13[0]} {self.libreria_14[0]} a YouTube {self.libreria_15[0]}"

class particula:
    def __init__(self,master,dir_name,x=100,y=100,escala=3,i=300,color_global="red"):
        self.i=i
        self.auto_status=True
        self.ventana = master
        self.posicion=(x,y)
        self.escala=escala

        #--------------Conexion a la base de Datos----------------
        conn = sqlite3.connect(rf'C:\Users\{usuario}\3D Objects\Proyecto Akura\Animaciones.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT clave, valores FROM {dir_name}')
        resultados = cursor.fetchall()
        self.dir_ani = {clave: tuple(json.loads(valores)) for clave, valores in resultados}
        conn.close()
        #-------------Desconexion de la base de datos-------------

        self.fotogramas=len(self.dir_ani)-2
        self.fotograma = 0
        self.ventanas={}
        def v_c (i,j,posicion):
            q = (j*self.escala) +self.posicion[0]
            w = (i*self.escala) +self.posicion[1]
            A=tk.Toplevel(self.ventana)
            A.overrideredirect(True)
            A.attributes("-topmost",True)
            A.geometry(f"{self.escala}x{self.escala}+{q}+{w}")
            self.ventanas.update({posicion:A})
            A.withdraw()
        pos=1
        colores.update({"4":color_global})
        for i,tupla in enumerate (self.dir_ani["ventanas"]):
            for j,valor in enumerate(tupla):
                if valor == 1:
                    v_c(i,j,pos)
                pos+=1
        
    def mostrar(self,fragmento):
        try:
            ls_ven=[]
            for tupla in self.dir_ani[str(fragmento)]:
                for posicion,ventana in self.ventanas.items():
                    if tupla[0]==posicion:
                        ventana.deiconify()
                        ventana.config(bg=colores[str(tupla[1])])
                        ls_ven.append(tupla[0])
                    elif not posicion in ls_ven:
                        ventana.withdraw()
            self.fotograma+=1
        except KeyError as e:
            print(f"Error: Intento de acceder a una cantidad no disponible de fotogramas-- {e} de {self.fotogramas}")
            self.destroy()
    
    def auto(self):
        def AUTO():
            if self.fotograma<=self.fotogramas and self.auto_status==True:
                self.mostrar(self.fotograma)
                self.ventana.after(self.i,AUTO)
            else:
                self.destroy()
        AUTO()
    def destroy(self):
        for ven in self.ventanas.values():
                ven.destroy()
        del self.ventanas
        del self.dir_ani
    def counter (self):
        #Fotograma actual/-/todos los disponibles
        return(self.fotograma,self.fotogramas)
    def disableauto(self):
        self.auto_status=False

class Descargar(threading.Thread):
    def __init__(self, url,p,ID,model=None,video=True):
        super().__init__()
        self.url = url
        self.model=model
        self.ID=ID
        self.model.descargas.update({self.ID:True})
        self.progress = 0
        self.progreso=p                                 #p Animacion de progreso
        self.progreso_frame=0
        self.muro=10
        self.ydl_opts={'progress_hooks': [self.hook],
            "quiet":True,
            "outtmpl":f"C:/Users/{usuario}/Downloads/Akura/%(title)s.%(ext)s",
            'noplaylist': True,}
        self.dir_video={'format': 'best'}
        self.dir_audio={'format': 'bestaudio/best','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}]}
        self.video=video

    def run(self):
        self.ydl_opts.update( self.dir_video if self.video else self.dir_audio)
        self.progreso.mostrar(0)
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                archivos = os.listdir(f"C:/Users/{usuario}/Music")+os.listdir(f"C:/Users/{usuario}/Downloads")+os.listdir(f"C:/Users/{usuario}/Videos")
                info_dict = ydl.extract_info(self.url, download=False)
                title = info_dict.get('title', None)
                for archivo in archivos:
                    if title in archivo:
                        raise TypeError("archivo ya descargado")
                ydl.download([self.url])
            except Exception as e:
                self.progreso.destroy()
                self.model.descargas.update({self.ID:False})
                self.model.Notifica(f"ERROR EN LA DESCARGA: {e}")

    def hook(self, d):
        if d['status'] == 'downloading':
            self.progress = d['downloaded_bytes'] / d['total_bytes'] * 100
            if self.progress >=self.muro:
                self.muro+=10
                self.progreso_frame+=1
                self.progreso.mostrar(self.progreso_frame)
            #print(f'Progreso: {self.progress:.2f}%')
        elif d['status'] == 'finished':
            self.progreso.destroy()
            self.model.descargas.update({self.ID:False})
            self.model.Notifica("Descarga Completa")

class ConsumoRed:
    def __init__(self):
        self.consumo =[False,0,0]                      #Actividad/consumo actual/Consumo total
        self.activo=True
        pass
    def iniciar(self):
        pass
    def detener(self):
        pass
    def medir(self):
        def convertir_byts(valor):
            conversion =["B","Kb","Mb","Gb","Tb"]
            i = 0
            while valor >= 1024:
                valor=valor/1024
                i=i+1
            return f"{round(valor,2)}{conversion[i]}"
        valor_anterior=0
        iterador=0
        while self.activo==True:
            try:
                consumo =psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
            except:
                consumo = 0
                iterador=0
                time.sleep(30)
            if consumo != valor_anterior:
                self.consumo[0]=True
                iterador = 100
                consumo_actual= consumo - valor_anterior
                self.consumo[2] = convertir_byts(consumo)
                self.consumo[1] =convertir_byts(consumo_actual)
            else:
                if iterador >= 0:
                    iterador = iterador-1
                    CONSUMO = convertir_byts(consumo)
                else:
                    self.consumo[0]=False
            time.sleep(1)
            valor_anterior = consumo



if __name__ == "__main__":
    smart =GText()
    print(smart.saludo())
    print(smart.m_cpu_t_Heat())
    print(smart.m_cpu_t_normal())
    print(smart.cosumo_cpu_alto("uno","dos","tres"))
    print(smart.hora_de())
    print(smart.ia_genero_texto())
    a = tk.Tk()
    a.withdraw()
    g=particula(a,"Load",escala=5,i=300)
    g.auto()
    a.mainloop()
    video_url = 'https://www.youtube.com/watch?v=5OF8rCUY8wM'
    #download_thread = Descargar(video_url,video=False)
    #download_thread.start()
    #download_thread.join()
    
