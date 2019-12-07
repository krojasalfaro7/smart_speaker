import socket
import time

PORT = 44444   
BUFFER_SIZE = 4000    

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('', PORT))
while True:
    direcciones = ("192.168.1.13", 44444)
    rList = [1, 2, 3, 4, 5, 6]
    data = bytes(rList)
    s.sendto(data, direcciones)
    time.sleep(2500)
# Close connection
#s.close()
