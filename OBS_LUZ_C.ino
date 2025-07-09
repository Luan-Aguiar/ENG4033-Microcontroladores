

#include <WiFi.h>
#include "WiFiClientSecure.h"
#include "certificados.h"
#include <MQTT.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>

//Sensor de cor
#define S0 19
#define S1 18
#define S2 2
#define S3 4
#define sensorOut 21

// Servo motor
# define SERVO_PIN 26

//Sinalização
const int led_g = 22;
const int led_r = 23;
const int led_b = 5;
Servo servoMotor;

bool jogo = false; //Boleano informando se o jogo está ocorrendo ou não

// Strings que armazenam as ordens do python
JsonDocument ordens1; // String que armazena as ordens do python
JsonDocument ordens2;
JsonDocument ordens3;

bool Obs_1 = true; // Controle para saber se o obstaculo está ativo
long status_led; //Controle de buffs e debuffs
long cor; // cor da vez

//Variaveis para controle do sensor de cor
int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;
unsigned long  azul =0;
unsigned long vermelho = 0;
unsigned long verde = 0;
unsigned long anterior= 0;
unsigned long atual =0;



WiFiClientSecure conexaoSegura;
MQTTClient mqtt(1000);
const char* ssid ="Projeto"; //"LIENG" ;      //"Projeto";
const char* password ="2022-11-07";// //"2022-11-07";"LPIS-2025"

unsigned long instanteAtual;



int Verifica_obs1(long l){
  atual = millis();
 
  // Setting RED (R) filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  
  // Reading the output frequency
  redFrequency = pulseIn(sensorOut, LOW);
  delay(100);
  
  // Setting GREEN (G) filtered photodiodes to be read
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  
  // Reading the output frequency
  greenFrequency = pulseIn(sensorOut, LOW);
  delay(100);
  
  
 
  // Setting BLUE (B) filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  
  // Reading the output frequency
  blueFrequency = pulseIn(sensorOut, LOW);
  delay(100);
  
  azul += blueFrequency;
  vermelho += redFrequency;
  verde += greenFrequency;

  if (atual > anterior + 1000) {

    if(vermelho<verde && vermelho<azul){
      delay(1000);
      if(l==0){
        for (int pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
		    servoMotor.write(pos);    // tell servo to go to position in variable 'pos'
		    delay(15);             // waits 15ms for the servo to reach the position
	    }
      Serial.println("vermelho");
      return 1;
      }
      else{
        return 0;
      }
      
    }
    else if (verde<vermelho && verde<azul){
      Serial.println("verde");
      delay(1000);
      if(l==1){
        for (int pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
		    servoMotor.write(pos);    // tell servo to go to position in variable 'pos'
		    delay(15);             // waits 15ms for the servo to reach the position
	    }
      Serial.println("verde");
      return 1;
      }
      else{
        return 0;
      }
    }
    else if(azul<verde && azul<vermelho){
     
      delay(1000);
      if(l==2){
        for (int pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
		    servoMotor.write(pos);    // tell servo to go to position in variable 'pos'
		    delay(15);             // waits 15ms for the servo to reach the position
	    }
       Serial.println("azul");
      return 1;
      }
      else{
        return 0;
      }
    }
    else{
      Serial.println("outra cor");
      anterior = atual;
      azul =0;
      verde =0;
      vermelho =0;
      return 0;
      
      
    }
  
  
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
      mqtt.connect("ESP32_10_LIENG", "aula","zowmad-tavQez");
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
  // Inicia os pinos dos leds
  pinMode(led_b, OUTPUT);
  pinMode(led_g, OUTPUT);
  pinMode(led_r, OUTPUT);
  
  //Inicia os pinos do sensor de cor

  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);

  // Configuração daescala de frequencia do sensor
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);

  // Set do servo
  servoMotor. attach (SERVO_PIN);

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
    cor = random(0,3);
    Serial.println(cor);
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
      obstaculo_1 = Verifica_obs1(cor);
      if (obstaculo_1==1 && Obs_1 ==true){
      ordens3["Obstaculo"]=4;
      ordens3["LED"]=status_led;
      String textoJson; 
      serializeJson(ordens3, textoJson); 
      mqtt.publish("obstaculos_carrinho",textoJson);
      Obs_1 = false;
      digitalWrite(led_g,HIGH);
      digitalWrite(led_r,HIGH);
      digitalWrite(led_b,HIGH);
}   else{
      if(cor == 0){
        digitalWrite(led_g,HIGH);
        digitalWrite(led_r,LOW);
        digitalWrite(led_b,HIGH);
    }
      else if (cor==1){
        digitalWrite(led_g,LOW);
        digitalWrite(led_r,HIGH);
        digitalWrite(led_b,HIGH);
    }
    else if (cor==2){
        digitalWrite(led_g,HIGH);
        digitalWrite(led_r,HIGH);
        digitalWrite(led_b,LOW);
    }

}
    }
    
    }
  else{
    digitalWrite(led_g,HIGH);
    digitalWrite(led_r,HIGH);
    digitalWrite(led_b,HIGH);
  }
 
  
 
  
  
  
  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    Serial.println(texto);
    if(texto=="envio"){
       

    }
}
mqtt.loop();
}