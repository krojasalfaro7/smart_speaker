#================================================================================================
 #stream = p.open(format=32, channels=1, rate=22050, output=True)#                                  Reproductor Streaming
#================================================================================================

#==============
# Bibliotecas
#==============
import pyaudio
import socket
import threading
import webbrowser
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
#======================
# Fin de importaciones
#======================

#==================================================
# Funciones MQTT - Programa Principal y secundario
#==================================================
def on_connect (cliente, userdata, flags, rc):  # Funcion de devolucion de llamada para conectar.
    client.subscribe ("udp_ip")                 # Topic.

def on_message (client, userdata, msg):         # Funcion de devolucion de llamada para recibir msj.
    global direccion_UDP
    direccion_UDP = msg.payload 

def publicar_chequear():
    
    def on_connect_s (cliente, userdata, flags, rc):  # Funcion de devolucion de llamada para conectar.
        client_s.subscribe ("udp")                      # Topic.
        client_s.subscribe ("parametros")
        
    def on_message_s (client, userdata, msg):         # Funcion de devolucion de llamada para recibir msj.
        musica = msg.payload
        global stream
        if msg.topic == 'udp':
            print ("La peticion requerida es: " + musica.decode())
                
        elif msg.topic == 'parametros':               # Separa los parametros de formato y canales
            valores = musica.decode().split('.')      # Ademas el valor de frecuencia se multiplica
            formato = int(valores[0])                 # por 8000 por que fue dividido previamente 
            canales = int(valores[1])                 # en el servidor UDP
            frecuencia = int(valores[2])*8000         # Se establecen los valores de stream para que cambien con la nueva musica o se mantenga
            stream = p.open(format=formato, channels=canales, rate=frecuencia, output=True)
    
    client_s = mqtt.Client()                  # Creando instancia de cliente
    client_s.on_connect = on_connect_s        # Enlazando funciones de devolucion de llamada para conectar y msj
    client_s.on_message = on_message_s
    client_s.connect (broker)                 # Utilizando el broker de mosquitto.
    client_s.loop_start()
    
    print ("La direccion ip del reproductor es. " + IP_reproductor)
    while True:
        publish.single('reproductor', IP_reproductor, hostname= broker) # Publica constantemente la direccion ip del reproductor
#=====================================================
# Fin funciones MQTT - Programa Principaly secundario
#=====================================================


#==============
# Funcion HTML 
#==============
def vista_html():
    
    webbrowser.open_new("/home/kevin/FINAL UDP y reproductor")
    mensaje_python_2 = """ <html> <center> </body> <H2> La direccion ip del reproductor UDP es: </body> </html>""" + IP_reproductor

    mensaje_prueba = '<br> <H3> Prueba de vista HTML </H3> </br>'
    f.write(mensaje_python_2)
    f.write(mensaje_prueba)
    f.close()
#==================
# Fin funcion HTML 
#==================

#====================================
# Inicio del Main - Programa General
#====================================
if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    p = pyaudio.PyAudio()                   # Encargado de reproducir el audio 
    sock.bind(('', 9999))                   # Enlazando direccion ip del reproductor y puerto del server UDP
    
    #broker = '127.0.0.1'                    # Utilizando un broker local para MQTT
    #IP_reproductor = socket.gethostbyname_ex(socket.gethostname())[2][0] # Ip del reproductor
    #stream = p.open(format=32, channels=1, rate=22050, output=True)
    stream = p.open(format=8, channels=2, rate=44100, output=True)
   # hilo = threading.Thread(name='publicar_chequear', target = publicar_chequear) # declaracion de hilo                        
   # hilo.start()                            # Inicio de hilo 

   # client = mqtt.Client()                  # Creando instancia de cliente
   # client.on_connect = on_connect          # Enlazando funciones de devolucion de llamada para conectar y msj
    #client.on_message = on_message
    #client.connect (broker)                 # Utilizando el broker de mosquitto.
    #client.loop_start()
    
    #f = open('UDP_mensajes.html','w')       # Se abre un archivo html para que se muestre despues
    #hilo_n = threading.Thread(name='vista_html', target = vista_html) # Declaracion de hilo de HTML                       
    #hilo_n.start()                          # Inicio de hilo

   # while True:                             # Este comando espera a que llegue el msj MQTT,             
    #    try:                                # Si aun no llega se queda esperando.
     #       direccion_UDP = direccion_UDP   # Este condicional hace que guarde el valor de la musica para que se repita
      #      break
      #  except NameError:
       #     pass
   # print("La direccion ip del UDP server es: "+direccion_UDP.decode())

    while True:
        data,addr = sock.recvfrom(4000)    # Recibe datos del servidor UDP, se recibe 4000 ya que ese es lo que manda el stream.mp3 por alguna razon 
        #print(data)
        stream.write(data)
#        time.sleep(0.015)                 # Lo reproduce y vuelve con el ciclo
#=================================
# Fin del Main - Programa General
#=================================
