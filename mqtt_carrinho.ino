
#include <ESP8266WiFi.h>   
#include <WiFiClientSecure.h>  
#include "certificados.h"
#include <MQTT.h>
#include <BearSSLHelpers.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>

WiFiClient conexaoSegura;
MQTTClient mqtt(1000);

void reconectarWiFi() {
 if (WiFi.status() != WL_CONNECTED) {
 WiFi.begin("Projeto", "2022-11-07");
 Serial.print("Conectando ao WiFi...");
 while (WiFi.status() != WL_CONNECTED) {
 Serial.print(".");
 delay(1000);
 }

 Serial.print("conectado ao wifi!\nEndereço IP: ");
 Serial.println(WiFi.localIP());
 }
}

void reconectarMQTT() {
  if (!mqtt.connected()) {
    Serial.print("Conectando MQTT...");
    while(!mqtt.connected()) {
    mqtt.connect("ppaulopaulo", "aula", "zowmad-tavQez");
    Serial.print(".");
    delay(1000);
  }
  Serial.println(" conectado ao mqtt!");

  mqtt.subscribe("controle_jogo_carrinho");
  mqtt.subscribe("efeitos_jogo_carrinho/buff");
  mqtt.subscribe("efeitos_jogo_carrinho/debuff");
  
  }
}

// continuação do código anterior...
void recebeuMensagem(String topico, String conteudo) {
 //Serial.println(topico + ": " + conteudo);
  StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, conteudo);

    if (error) {
      Serial.print("Erro no parse do JSON: ");
      Serial.println(error.f_str());
      return;
    } 

    // Extrai os dados
    if (topico == "controle_jogo_carrinho"){
    float curva = doc["curva"];
    float acelera = doc["acelera"];
    const char* cor = doc["cor"];

    Serial.print(acelera);
    Serial.print(",");
    Serial.print(curva);
    Serial.print(",");
    Serial.println(cor);
    }else if (topico == "efeitos_jogo_carrinho/buff"){
      const char* nitro = doc["buff"];
      Serial.println(nitro);
    }else if(topico == "efeitos_jogo_carrinho/debuff"){
      const char* desacelera = doc["debuff"];
      Serial.println(desacelera);
    }
}


void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200); 
  delay(500);
  
  reconectarWiFi();

  
  mqtt.begin("mqtt.janks.dev.br",1883, conexaoSegura);
  mqtt.onMessage(recebeuMensagem);
  reconectarMQTT();
}

void loop() {
  reconectarWiFi();
  reconectarMQTT();
  //Serial.println("Mensagem enviada ao Arduino!");
   mqtt.loop();
}
