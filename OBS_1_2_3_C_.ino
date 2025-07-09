#include <WiFi.h>
#include "WiFiClientSecure.h"
#include "certificados.h"
#include <MQTT.h>
#include <ArduinoJson.h>

//Configurações do sensor de distancia ultrasonico
const int sensor1 = 5;
const int led_g = 18;
const int led_r = 19;
//const int sensor3 = 6;
//const int sensor4 = 7;
int s1=0; //estado do sensor1
int s2=0; //estado do sensor2
bool jogo = false; //Boleano informando se o jogo está ocorrendo ou não
JsonDocument ordens1; // String que armazena as ordens do python
JsonDocument ordens2;
JsonDocument ordens3;
bool Obs_1 = true; // Controle para saber se o obstaculo está ativo
long status_led;
int distancia = 30; //Em cm


WiFiClientSecure conexaoSegura;
MQTTClient mqtt(1000);
const char* ssid ="LIENG"; //"LIENG" ;      //"Projeto";
const char* password ="LPIS-2025";// //"2022-11-07";"LPIS-2025"
unsigned long anterior =0;
unsigned long instanteAtual;



int Verifica_obs1(long l){
  if(digitalRead(sensor1) == LOW){
      Serial.println("passou");
      return 1;
    }
  else{
    return 0;
  }
    
  }
  



void reconectarWiFi() {
  if(WiFi.status() != WL_CONNECTED){
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("Connecting to WiFi..");
      }
    Serial.println("Connected to the WiFi network");
    Serial.print("conectado!\nEndereço IP: ");
    Serial.println(WiFi.localIP());
  }
  
}
 
   
  

void reconectarMQTT() {
  if (!mqtt.connected()) {
    Serial.print("Conectando MQTT...");
    while (!mqtt.connected()) {
      mqtt.connect("ESP32_7_LIENG", "aula","zowmad-tavQez");
      Serial.print(".");
      delay(1000);
    }
    Serial.println(" conectado!");

    mqtt.subscribe("obstaculos_carrinho");
    mqtt.subscribe("status_jogo_carrinho");
    mqtt.subscribe("Lap_carrinho");                  // qos = 0
    //mqtt.subscribe("topico2/+/parametro", 1);  // qos = 1
  }
}
void recebeuMensagem(String topico, String conteudo) {
  Serial.println(topico + ": " + conteudo);
  if(topico=="status_jogo_carrinho"){
    deserializeJson(ordens1,conteudo);
    int f = ordens1["start"];
    
    delay(1000);
     
  }
  else if(topico=="Lap_carrinho"){
    deserializeJson(ordens2,conteudo);

  }
  else if(topico=="obstaculos_carrinho"){
    deserializeJson(ordens3,conteudo);
  }

}
void setup() {
  pinMode(sensor1, INPUT);
  pinMode(led_g, OUTPUT);
  pinMode(led_r, OUTPUT);
  //pinMode(sensor3, INPUT);
  //pinMode(sensor4, INPUT);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  delay(500);
  reconectarWiFi();
  conexaoSegura.setCACert(certificado1);
  mqtt.begin("mqtt.janks.dev.br", 8883, conexaoSegura);
  mqtt.onMessage(recebeuMensagem);
  mqtt.setKeepAlive(10);
  mqtt.setWill("tópico da desconexão", "3000");
  reconectarMQTT();
}
void loop() {
  //Serial.println(ordens);
  instanteAtual = millis();
  if (instanteAtual > anterior + 5000) {
  //Serial.println("+1 segundo");
    anterior = instanteAtual;
    reconectarWiFi();
    reconectarMQTT();
  }
  int s = ordens1["start"];
  //Serial.println(s);
  int e = ordens1["end"];
  if (s == 1 && e == 0){
    Serial.println("Ligou");
    ordens1["start"]=0; // Limpa a variável para evitar re-gatilhos
    Obs_1 = true; // Reinicia o controle do obstáculo para um novo jogo
    status_led = random(0,2);
    jogo = true;
  }
  if (e == 1){
    //Serial.println("Desligou");
    jogo=false;
    Serial.println("Desliga");
    ordens1["end"]=0; 
  }
  

  
  if(jogo){
    int obstaculo_1;
    if(Obs_1){
      obstaculo_1 = Verifica_obs1(status_led);
      if (obstaculo_1==1 && Obs_1 ==true){
      ordens3["Obstaculo"]=1;
      ordens3["LED"]=status_led;
      String textoJson; 
      serializeJson(ordens3, textoJson); 
      mqtt.publish("obstaculos_carrinho",textoJson);
      Obs_1 = false;
      digitalWrite(led_g,HIGH);
      digitalWrite(led_r,HIGH);
}   else{
      if(status_led == 0){
        digitalWrite(led_g,LOW);
        digitalWrite(led_r,HIGH);
    }
      else {
        digitalWrite(led_r,LOW);
        digitalWrite(led_g,HIGH);
    }

}
    }
    
    }
  else{
    digitalWrite(led_g,LOW);
    digitalWrite(led_r,HIGH);
  }
 
  
 
  
  
  
  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    Serial.println(texto);
    if(texto=="envio"){
       

    }
}
mqtt.loop();
}