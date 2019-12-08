#include <WiFi.h>
#include <WiFiUdp.h>

#define MAX_INTENTOS 15       // Número de intentos para conectarse a wifi
#define LED_PIN 2             // Led azul
#define OUTPUT_BUFFER 40960   // Tamaño máxmo de buffer de salida de audio
#define RECV_BUFFER_UDP 1024  // Tamaño de buffer de recepción de paquete UDP(Pareciera que fuera el máximo)
#define PORT_UDP 44444        // Puerto de recepción del Servidor UDP

/* WiFi network name and password PRUEBAS*/ //Se va a utilizar mientras se realiza la interfaz de conexión con bluethoo
const char * ssid = "esp32";
const char * pwd = "12345678";

//const char * udpAddress = "192.168.1.11"; //Dirección IP del servidor UDP
const int udpPort = PORT_UDP; //Puerto del servidor UDP

//create UDP instance
WiFiUDP udp;

unsigned char completeBuffer[OUTPUT_BUFFER];  // Buffer donde se almacena un tamaño finito de reproducción de aproximadamente 3 segundos
unsigned char packetBuffer[RECV_BUFFER_UDP];

void setup(){
  Serial.begin(115200);
  int intentos = 0; //
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
  
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP()); // Mostrando dirección IP entregado por el servidor DHCP
  udp.begin(udpPort);             // Escuchando por el puerto 44444
  
}

void loop(){

  /*if (udp.parsePacket()) {
    udp.read(packetBuffer, 1024);
    //Serial.println(sizeof(packetBuffer));
      for (int i=0; i<1024; i++){
        if(i==256 || i==512 || i== 768)
          Serial.println("..........");
        Serial.print(packetBuffer[i], HEX);
        }
    Serial.println(".");
    Serial.println(".");
    Serial.println(".");
    Serial.println(".");
   }*/

  for (int j=0; j<40; j++){
    if (udp.parsePacket()){
      udp.read(packetBuffer, 1024);
      for (int i=0; i<1024; i++){
        completeBuffer[i+(j*1024)]=packetBuffer[i];
      }
    }
    else --j;
  }

  //reproducir lo que está en el buffer
}

void reproducir(unsigned char* buffer_reproduccion){
  for(int i=0; i<40960; i++){
    dacWrite(25, buffer_reproduccion[i]);
    delayMicroseconds(38); // ((1/22050)*1000000) - 7//*/
  }
}
