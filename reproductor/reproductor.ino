#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include "FIFO.h"
#include "soc/timer_group_struct.h"
#include "soc/timer_group_reg.h"

#define MAX_INTENTOS 15       // Número de intentos para conectarse a wifi
#define LED_PIN 2             // Led azul
#define DAC 25                // Salida Digital-Analogico
#define RECV_BUFFER_UDP 1024  // Tamaño de buffer de recepción de paquete UDP(Pareciera que fuera el máximo)

/* WiFi network name and password PRUEBAS*/ //Se va a utilizar mientras se realiza la interfaz de conexión con bluethoo
const char * ssid = "esp32";
const char * pwd = "1234567890";

//const char * udpAddress = "192.168.1.11"; //Dirección IP del servidor UDP
const int udpPort = 44444; //Puerto del servidor UDP

//create UDP instance
WiFiUDP udp;
FIFO completeBuffer;

unsigned char packetBuffer[RECV_BUFFER_UDP]; //Buffer de recepción de paquete UDP

void setup(){
  Serial.begin(115200);
  int intentos = 0;         // Contador de intentos de conexión
  pinMode(LED_PIN, OUTPUT); // Led azul como salida
  
  WiFi.begin(ssid, pwd);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LED_PIN, HIGH);
    delay(250);
    Serial.print(".");
    digitalWrite(LED_PIN, LOW);
    delay(250);
    if(intentos==MAX_INTENTOS)
      break;
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
    delay(5000);
  }
  xTaskCreatePinnedToCore(recibir, "recibir", 4096, NULL, 2, NULL, 1);
  xTaskCreatePinnedToCore(reproducir, "reproducir", 10000, NULL, 5, NULL, 0);
}
void loop(){
  //vTaskDelay(portTICK_PERIOD_MS);
  vTaskDelete(NULL);
}

void reproducir(void *pvParameters) {
  while(1) {
    TIMERG0.wdt_wprotect=TIMG_WDT_WKEY_VALUE;
    TIMERG0.wdt_feed=1;
    TIMERG0.wdt_wprotect=0;
    while(completeBuffer.size()>0){
      dacWrite(DAC, completeBuffer.pop()); // Sacando el valor digital por el conversor Digital-Analogico del ESP32
      delayMicroseconds(38);                // (1/22050)*1000000 - 7(Aproximación de lo que se tarda el ciclo for)
    }
  }
}

void recibir(void *pvParameters){
  while(1){
    TIMERG0.wdt_wprotect=TIMG_WDT_WKEY_VALUE;
    TIMERG0.wdt_feed=1;
    TIMERG0.wdt_wprotect=0;
    while (udp.parsePacket()){
      udp.read(packetBuffer, RECV_BUFFER_UDP);
      for (int i=0; i<RECV_BUFFER_UDP; i++){
        completeBuffer.push(packetBuffer[i]);
      }
    }
  }
}
