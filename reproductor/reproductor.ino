#include <WiFi.h>
#include <WiFiUdp.h>
#include "FIFO.h"

#define MAX_INTENTOS 15       // Número de intentos para conectarse a wifi
#define LED_PIN 2             // Led azul
#define DAC 25                // Salida Digital-Analogico
#define OUTPUT_BUFFER 40960   // Tamaño máxmo de buffer de salida de audio
#define RECV_BUFFER_UDP 1024  // Tamaño de buffer de recepción de paquete UDP(Pareciera que fuera el máximo)

/* WiFi network name and password PRUEBAS*/ //Se va a utilizar mientras se realiza la interfaz de conexión con bluethoo
const char * ssid = "Glufco";
const char * pwd = "01GLUFCO";

//const char * udpAddress = "192.168.1.11"; //Dirección IP del servidor UDP
const int udpPort = 44444; //Puerto del servidor UDP

//create UDP instance
WiFiUDP udp;
FIFO completeBuffer;

//unsigned char completeBuffer[OUTPUT_BUFFER];  // Buffer donde se almacena un tamaño finito de reproducción de aproximadamente 3 segundos
unsigned char packetBuffer[RECV_BUFFER_UDP];

void setup(){
  Serial.begin(115200);
  int intentos = 0;         // Contador de intentos de conexión
  pinMode(LED_PIN, OUTPUT); // Led azul como sálida
  
  WiFi.begin(ssid, pwd);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED && intentos<MAX_INTENTOS) {
    digitalWrite(LED_PIN, HIGH);
    delay(250);
    Serial.print(".");
    digitalWrite(LED_PIN, LOW);
    delay(250);
    intentos++; //incrementando contador de intentos
  }
  if(intentos!=MAX_INTENTOS){
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP()); // Mostrando dirección IP entregado por el servidor DHCP
    udp.begin(udpPort);             // Escuchando por el puerto 44444
  }else{
    Serial.print("Failed conection");
    delay(50000);
  }
  
}
void loop(){

  if (udp.parsePacket() && !(completeBuffer.size()==61440)){
    udp.read(packetBuffer, RECV_BUFFER_UDP);
    for (int i=0; i<RECV_BUFFER_UDP; i++){
      completeBuffer.push(packetBuffer[i]);
    }
  }

/*  for (int j=0; j<40; j++){       //Recibiendo un total de 40960
  if (udp.parsePacket()){
    udp.read(packetBuffer, RECV_BUFFER_UDP);
    for (int i=0; i<RECV_BUFFER_UDP; i++){
      //completeBuffer[i+(j*RECV_BUFFER_UDP)]=packetBuffer[i];
      completeBuffer.push(packetBuffer[i]);
    }
  }
  else --j;
}*/

  //reproducir lo que está en el buffer
  reproducir(completeBuffer);
}

//Función para reproducir el audio
void reproducir(FIFO buffer_reproduccion){
  digitalWrite(LED_PIN, HIGH);
  while(buffer_reproduccion.size()>0){
    dacWrite(DAC, buffer_reproduccion.pop()); // Sacando el valor digital por el conversor Digital-Analogico del ESP32
    delayMicroseconds(33);                // (1/22050)*1000000 - 7(Aproximación de lo que se tarda el ciclo for)
  }
  digitalWrite(LED_PIN, LOW);
}

/*//Función para reproducir el audio
void reproducir(unsigned char* buffer_reproduccion){
  digitalWrite(LED_PIN, HIGH);
  for(int i=0; i<OUTPUT_BUFFER; i++){
    dacWrite(25, buffer_reproduccion[i]); // Sacando el valor digital por el conversor Digital-Analogico del ESP32
    delayMicroseconds(38);                // (1/22050)*1000000 - 7(Aproximación de lo que se tarda el ciclo for)
  }
  digitalWrite(LED_PIN, LOW);
}*/
/*
void llenarBuffer(){
  for (int j=0; j<40; j++){       //Recibiendo un total de 40960
  if (udp.parsePacket()){
    udp.read(packetBuffer, RECV_BUFFER_UDP);
    for (int i=0; i<RECV_BUFFER_UDP; i++){
      completeBuffer[i+(j*RECV_BUFFER_UDP)]=packetBuffer[i];
    }
  }
  else --j;
}
  }*/
