#================================================================================================
#					Reproductor Streaming
#================================================================================================

#==============
# Bibliotecas
#==============
import pyaudio
import socket
import threading
import time
#======================
# Fin de importaciones
#======================

#====================================
# Inicio del Main - Programa General
#====================================
if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    p = pyaudio.PyAudio()                   # Encargado de reproducir el audio 
    sock.bind(('', 44444))                   # Enlazando direccion ip del reproductor y puerto del server UDP
    #stream = p.open(format=32, channels=1, rate=22050, output=True)
    stream = p.open(format=8, channels=2, rate=44100, output=True)


    while True:
        data,addr = sock.recvfrom(4000)    # Recibe datos del servidor UDP, se recibe 4000 ya que ese es lo que manda el stream.mp3 por alguna razon 
        #print(data)
        stream.write(data)
#        time.sleep(0.015)                 # Lo reproduce y vuelve con el ciclo
#=================================
# Fin del Main - Programa General
#=================================
