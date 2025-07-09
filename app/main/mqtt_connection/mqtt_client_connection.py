import json
import random

import paho.mqtt.client as mqtt
import time
import certifi
import ssl

from interface.config import BUFFS, DEBUFFS


class MqttState:
    tempo_inicio = 0
    check_points = 0
    lap = 0
    efeito = None

mqtt_state = MqttState()

class MqttClientConnection:
    def __init__(self, broker_ip: str, port: int, client_name: str, keepalive: int =60, topics: list[str] = ['/teste']):
        self.__broker_ip = broker_ip
        self.__port = port
        self.__client_name = client_name
        self.__keepalive = keepalive
        self.__topics = topics

        self.__client = mqtt.Client(client_id=self.__client_name, protocol=mqtt.MQTTv5)
        self.__client.tls_set(certifi.where(), cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)
        self.__client.username_pw_set(username='aula', password='zowmad-tavQez')

        # callbacks
        self.__client.on_connect = self.on_connect
        self.__client.on_subscribe = self.on_subscribe
        self.__client.on_message = self.on_message

    def on_connect(self, client, user_data, flags, reasonCode, properties):
        if reasonCode == 0:
            print(f"[MQTT] Cliente conectado com sucesso! Cliente = {client}")
            [client.subscribe(topico) for topico in self.__topics]
        else:
            print(f'[MQTT] Erro ao conectar! Code: {reasonCode}')

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print(f'Cliente inscrito nos topicos: {[topico for topico in self.__topics]}')

    def on_message(self, client, userdata, msg):
        print(f"[MQTT] Mensagem recebida no tópico {msg.topic}: {msg.payload.decode('utf-8')}")
        payload = json.loads(msg.payload)
        print(payload)
        if msg.topic == 'lap_jogo_carrinho':
            mqtt_state.check_points += 1
            mqtt_state.lap = payload['lap']

        elif msg.topic == 'obstaculos_jogo_carrinho':
            buff = payload['led']
            if buff:
                mqtt_state.efeito = random.choice(BUFFS)
                efeito = {"buff":mqtt_state.efeito}
                efeito_json = json.dumps(efeito)
                self.publish('efeitos_jogo_carrinho/buff', efeito_json)
            else:
                if not (mqtt_state.efeito and mqtt_state.efeito == 'Imunidade'):
                    mqtt_state.efeito = random.choice(DEBUFFS)
                    efeito = {"debuff": mqtt_state.efeito}
                    efeito_json = json.dumps(efeito)
                    if mqtt_state.efeito == 'Inverter':
                        self.publish('efeitos_jogo_carrinho/inverter', True)
                    else:
                        self.publish('efeitos_jogo_carrinho/debuff', efeito_json)
                else:
                    mqtt_state.efeito = None

            mqtt_state.tempo_inicio = time.time()


    # Inicia a conexao e faz o loop para verificar se esta recebendo alguma informacao do broker
    def start_connection(self):
        self.__client.connect(host=self.__broker_ip, port=self.__port, keepalive=self.__keepalive)

        self.__client.loop_start()

    def end_connection(self):
        try:
            self.__client.loop_stop()
            self.__client.disconnect()
            return True
        except Exception as e:
            print(e)
            return False

    def publish(self, topico: str, payload: str, qos: int = 0, retain: bool = False):
        result = self.__client.publish(topico, payload, qos, retain)
        status = result.rc
        if status == mqtt.MQTT_ERR_SUCCESS:
            print(f"[MQTT] Mensagem publicada com sucesso no tópico {topico}")
        else:
            print(f"[MQTT] Falha ao publicar a mensagem no tópico {topico}, código de erro: {status}")
