#================================================================================================
#                                 Servidor UDP-Streaming
#================================================================================================

#==============
# Bibliotecas
#==============
import socket  
import wave, struct
import pyaudio
import os
import threading
import time
import urllib
import urllib.request, urllib.parse, urllib.error
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from pydub import AudioSegment
#======================
# Fin de importaciones
#======================

#=====================================
# Funciones MQTT - Programa Principal
#=====================================
def on_connect (cliente, userdata, flags, rc):  # Funcion de devolucion de llamada para conectar.
    client.subscribe ("udp")                    # Topic del UDP.

def on_message (client, userdata, msg):         # Funcion de devolucion de llamada para recibir msj.
    global mensaje
    mensaje = msg.payload                       # Guarda el valor de la variable recibida en mensaje.
#=========================================
# Fin funciones MQTT - Programa Principal
#=========================================


#=========================================================================
# Funciones para convertir formatos de audio y envio - Programa Principal
#=========================================================================
def convertidor(nombre_archivo):                # Funcion que permite convertir un archivo .WAV 8Khz, 8bits a muestras PCM
    global waveFile
    global length
    global frecuencia_1
    
    nombre_archivo = nombre_archivo + "wav"
    waveFile = wave.open(directorio + nombre_archivo, 'rb') # Se van a abrir los archivos que esten en esa carpeta

    formato = p.get_format_from_width(waveFile.getsampwidth())
    canales = waveFile.getnchannels()
    frecuencia_1 = waveFile.getframerate()
    frecuencia = int(waveFile.getframerate()/8000)
    
    lista = str(formato) + '.' + str(canales) + '.' + str(frecuencia)
   # publish.single('parametros', lista, hostname= broker)
    print(lista, frecuencia_1)
    length = waveFile.getnframes()
    
def revisar():                                              # Rutina que revisa si el archivo tiene extenxion .wav
    global error
    global audio
    wav = int(7823734)
    mensaje_r = mensaje                                     # Si no la tiene lo convierte, 
    mensaje_l = mensaje
    mensaje_r = mensaje_r[len(mensaje_r)-3:]                # Solo se queda con la extenxion 
    mensaje_r = int.from_bytes(mensaje_r, byteorder = 'big')# Para convertir la cadena byte a int
    lista_musica = os.listdir(directorio)
    #print(lista_musica)
    #print(mensaje.decode())
   # print(lista_musica.index(mensaje.decode()))
    try:
        #print(lista_musica.index(mensaje.decode()))
        lista_musica.index(mensaje.decode())
        try:
            audio_revisar = mensaje.decode()[:len(mensaje)-3] + "wav"
            lista_musica.index(audio_revisar)

        except ValueError:
            print('No se encuentra en formato .wav')
            
            if (mensaje_r - wav) != 0:
                mensaje_n = mensaje
                mensaje_3 = mensaje[len(mensaje)-3:]
            
                if mensaje_3 == b'mp3':
                    print('Convirtiendo de formato .mp3 a formato .wav ...')
                    sound_mp3 = AudioSegment.from_mp3(directorio + mensaje_n.decode())
                    sound_mp3.export(directorio + mensaje_n.decode()[:len(mensaje)-3] + 'wav', format="wav")

                elif mensaje_3 == b'ogg':
                    print('Convirtiendo de formato .ogg a formato .wav ...')
                    sound_ogg = AudioSegment.from_ogg(directorio + '\\' + mensaje_n.decode())
                    sound_ogg.export(directorio + '\\' + mensaje_n.decode()[:len(mensaje)-3] + 'wav', format="wav")    

                elif mensaje_3 == b'flv':
                    print('Convirtiendo de formato .flv a formato .wav ...')
                    sound_flv = AudioSegment.from_ogg(directorio + '\\' + mensaje_n.decode())
                    sound_flv.export(directorio + '\\' + mensaje_n.decode()[:len(mensaje)-3] + 'wav', format="wav")    

                elif mensaje_3 == b'aac':
                    print('Convirtiendo de formato .aac a formato .wav ...')
                    sound_aac = AudioSegment.from_file(directorio + '\\' + mensaje_n.decode(), 'aac')
                    sound_aac.export(directorio + '\\' + mensaje_n.decode()[:len(mensaje)-3] + 'wav', format="wav")    
            
    except ValueError:
        print('no se encuentra el audio requerido')
        error = b'error'
           
def enviar():
    fragmento = length/1000
    fragmento = int(fragmento)+ 1
    for i in range(0, fragmento):
        datos = waveFile.readframes(1000)
        for i in range(0, len(direcciones)):
            addr = (direcciones[i], 9999)
            #print("Estos son los datos"+ int(datos[i]))
            s.sendto(datos, addr)
           # print("flknsfkjnsdjksndkjfcnsd"+datos)
        if frecuencia_1 == 44100:
            time.sleep(0.019666666999999999999)
            #time.sleep(0.016666666999999999999)
        else:
            time.sleep(0.09999996942749023)
#=============================================================================
# Fin funciones para convertir formatos de audio y envio - Programa Principal
#=============================================================================

#=====================
# Programa Secundario
#=====================
def chequear():
#======================================
# Funciones MQTT - Programa Secundario
#======================================
    def on_connect_s (cliente, userdata, flags, rc):  # Funcion de devolucion de llamada para conectar.
        client_s.subscribe ("reproductor")            # Topics del UDP.
        client_s.subscribe ("esp1")
        client_s.subscribe ("esp2")
        client_s.subscribe ("esp3")

    def on_message_s (client, userdata, msg):         # Funcion de devolucion de llamada para recibir msj.
        global mensaje_s
        mensaje_s = msg.payload.decode()              # Guarda el valor de la variable recibida en mensaje.
        if msg.topic == 'reproductor':
            try:
                direcciones.index(mensaje_s)
            except ValueError:
                direcciones.append(mensaje_s)
                print (direcciones)

        elif msg.topic == 'esp1' or msg.topic == 'esp2' or msg.topic == 'esp3':
            try:
                mensaje_s = mensaje_s.split(' ')
                if len(mensaje_s) == 4:
                     mensaje_s = mensaje_s[0]
                     direcciones.index(mensaje_s)
                else:
                     pass
            except ValueError:
                direcciones.append(mensaje_s)
                print (direcciones)
#==========================================
# Fin funciones MQTT - Programa Secundario
#==========================================

#=======================================
# Inicio del Main - Programa secundario
#=======================================
    client_s = mqtt.Client()                  # Creando instancia de cliente
    client_s.on_connect = on_connect_s        # Enlazando funciones de devolucion de llamada para conectar y msj
    client_s.on_message = on_message_s
    client_s.connect (broker)                 # Utilizando el broker de mosquitto.
    client_s.loop_start()
    while True:                             # Este comando espera a que llegue el msj MQTT,                                      # Este comando espera a que llegue el msj MQTT,             
        publish.single('udp_ip', IP_UDP, hostname= broker)
#=====================================
# Fin del Main - Programa Secuandario
#=====================================
#============================
# Fin de Programa Secundario
#============================

def stream():
    urllib.request.urlretrieve("http://eu.cdn.egostreaming.com:8000/;stream.mp3", "C:\\Users\\kevin\\Desktop\\audios\\stream.mp3")

def stream_convertidor():
    sound_mp3 = AudioSegment.from_mp3(directorio + '\\' + 'stream.mp3')
    while True:
        sound_mp3.export(directorio + '\\' + 'stream.wav', format="wav")
        time.sleep(1)
#====================================
# Inicio del Main - Programa General
#====================================
if __name__ == '__main__':

    global direcciones
    global directorio
    #direcciones =["192.168.1.10","192.168.1.11","192.168.1.12","192.168.1.13","192.168.1.14"]
    direcciones =["192.168.1.10"]
    directorio = '/home/kevin/audios/'
    
    IP_UDP = socket.gethostbyname_ex(socket.gethostname())[2][0]
    print(socket.gethostbyname(socket.gethostname()))
    broker = '127.0.0.1'
    print('La direccion ip del server UDP es: ' + IP_UDP)
    #publish.single('udp_ip', IP_UDP, hostname= broker)
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Asignando socket para conexion UDP
    s.bind(('',9999))
    p = pyaudio.PyAudio()
    
    #client = mqtt.Client()                  # Creando instancia de cliente
    #client.on_connect = on_connect          # Enlazando funciones de devolucion de llamada para conectar y msj
    #client.on_message = on_message
    #client.connect (broker)   # Utilizando el broker de mosquitto.
    #client.loop_start()

   # hilo = threading.Thread(name='chequear', target=chequear)                         
    #hilo.start()

    #hilo_stream = threading.Thread(name='stream', target=stream)
    #hilo_stream.start()

    #hilo_stream_convertidor = threading.Thread(name='stream_convertidor', target=stream_convertidor)
    #hilo_stream_convertidor.start()
    mensaje=b'farewell.wav'	#AGREGADO#
    global posicion
    posicion = 0
    while True:                             # El servidor UDP se queda mandando constantemente.
       # while True:                         # Este comando espera a que llegue el msj MQTT,             
       #     try:                            # Si aun no llega se queda esperando. 
       #         mensaje = mensaje
       #         break
       #     except NameError:
       #         publish.single('udp_ip', IP_UDP, hostname= broker)
                
        if mensaje == b'stream.mp3':
            sound_mp3 = AudioSegment.from_mp3(directorio + '\\' + 'stream.mp3')
            sound_mp3.export(directorio + '\\' + 'stream.wav', format="wav")
            waveFile_stream = wave.open(directorio + 'stream.wav', 'rb')

            formato = p.get_format_from_width(waveFile_stream.getsampwidth())
            canales = waveFile_stream.getnchannels()
            frecuencia = int(waveFile_stream.getframerate()/8000)
            lista = str(formato) + '.' + str(canales) + '.' + str(frecuencia)
            publish.single('parametros', lista, hostname= broker)
            
            length_stream = waveFile_stream.getnframes()
            fragmento = length_stream/1000
            fragmento = int(fragmento)
            waveFile_stream.setpos(posicion)
            for i in range(0, fragmento):
                datos_stream = waveFile_stream.readframes(1000)
                for i in range(0, len(direcciones)):
                    addr = (direcciones[i], 9999)
                    s.sendto(datos_stream, addr)
                time.sleep(0.014999999999999999999)
            posicion = waveFile_stream.tell()
                
        elif mensaje == b'Tono 1' or mensaje == b'Tono 2' or mensaje == b'Tono 3' or mensaje == b'apagar':
            datos = mensaje
            for i in range(0, len(direcciones)):
                addr = (direcciones[i], 9999)
                s.sendto(datos, addr)
        else:                               # Revisa si la musica requerida esta en formato .wav
            error = b'-'
            revisar()                       # Si no lo esta lo convierte a ese formato y lo conveirte a PCM
            if error != b'error':
                audio = mensaje.decode()[:len(mensaje)-3] # Convierte el bytes en string
                convertidor(audio)              # Convierte el audio .wav a codificacion PCM
                enviar()                        # Envia los datos de audio al ESP8266
            time.sleep(2)
#=================================
# Fin del Main - Programa General
#=================================


#===============
# Comentarios
#===============
##elif data == b'transmision':
##Este codigo es para descargar el MP3 de cualquier servidor pregrabados falta por trabajar"
##Proximamente realizar el script para grabar audio en tiempo real y pasarlo por las cornetas
#estilo el streming de la radio pero personal..
#=================
# Fin Comentarios
#=================
