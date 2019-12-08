import socket
import time

PORT = 44444   
BUFFER_SIZE = 4000    
direcciones = ("192.168.1.16", 44444)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))
rList = [255]
lista = [x for x in range(0,256)]
lista = lista*4
print(len(lista))

while True:
    rList[0] = int(input())
    #data = bytes(rList)
    data = bytes(lista)
    print(data)
    s.sendto(data, direcciones)
    print("enviado")
    #time.sleep(2500)
# Close connection
#s.close()
