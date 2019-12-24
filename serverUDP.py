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
import subprocess
import IPython
import gtts
from gtts import gTTS
#import IPyhton
from pydub import AudioSegment

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

    print(lista, frecuencia_1)
    length = waveFile.getnframes()
    print("Este es la longitud del archivo: ",length)

def revisar():                                              # Rutina que revisa si el archivo tiene extenxion .wav

    global error
    global audio
    wav = int(7823734)
    mensaje_r = mensaje                                     # Si no la tiene lo convierte, 
    mensaje_l = mensaje
    mensaje_r = mensaje_r[len(mensaje_r)-3:]                # Solo se queda con la extenxion 
    mensaje_r = int.from_bytes(mensaje_r, byteorder = 'big')# Para convertir la cadena byte a int
    lista_musica = os.listdir(directorio)

    try:
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

    fragmento = int ((length/1024) + float(1))
    contador = 0
    print("El bucle deberia repetirse: "+str(fragmento) +"veces")
    #x = input("ingresa algo")
    for i in range(0, fragmento):
        datos = waveFile.readframes(1024)
        for i in range(0, len(direcciones)):
            addr = (direcciones[i], UDP_port)
            s.sendto(datos, addr)
            #if(contador==60):
            #time.sleep(0.019666666999999999999)
            #time.sleep(0.016666666999999999999)
                #time.sleep(0.01666666999999999999)
                #contador=0
            #time.sleep(0.0091)
        #else:
         #   time.sleep(0.09999996942749023)

#=============================================================================

# Fin funciones para convertir formatos de audio y envio - Programa Principal

#=============================================================================

#====================================
# Inicio del Main - Programa General
#====================================

if __name__ == '__main__':

    global direcciones
    global directorio
    UDP_port = 44444

    #direcciones =["192.168.1.10","192.168.1.11","192.168.1.12","192.168.1.13","192.168.1.14"]

    direcciones =["192.168.1.52"]
    directorio = '/home/kevin/audios/'

    IP_UDP = socket.gethostbyname_ex(socket.gethostname())[2][0]
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Asignando socket para conexion UDP
    s.bind(('',UDP_port))

    p = pyaudio.PyAudio()

    mensaje=b'synthesize.wav'

    while True:                             # El servidor UDP se queda mandando constantemente.
                
        if mensaje == b'Funcion_1':
            pass

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
