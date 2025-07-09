import pygame
import time
import json
import threading
import paho.mqtt.client as mqtt
import certifi
import ssl

# Configurações MQTT
MQTT_BROKER = "mqtt.janks.dev.br"
MQTT_PORT = 8883
MQTT_TOPIC_COMANDO = "controle_jogo_carrinho"
MQTT_TOPIC_INVERTER = "efeitos_jogo_carrinho/inverter"
MQTT_TOPIC_VIBRAR = "efeitos_jogo_carrinho/vibrar"
MQTT_TOPIC_DEBUFF = "efeitos_jogo_carrinho/debuff"
RECONNECT_DELAY = 5

# Variáveis globais
modo_invertido = True
modo_lock = threading.Lock()

controle_bloqueado = False
controle_lock = threading.Lock()

vibrando = False
vibrando_lock = threading.Lock()
joystick_global = None  # Referência global para controle da vibração

client = mqtt.Client()
client.tls_set(certifi.where(), cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.username_pw_set(username="aula", password="zowmad-tavQez")

# Funções MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Conectado com sucesso.")
        client.subscribe(MQTT_TOPIC_INVERTER)
        client.subscribe(MQTT_TOPIC_VIBRAR)
        client.subscribe(MQTT_TOPIC_DEBUFF)
    else:
        print(f"[MQTT] Falha ao conectar. Código: {rc}")

def on_message(client, userdata, msg):
    global modo_invertido, joystick_global, vibrando, controle_bloqueado

    payload = msg.payload.decode("utf-8").strip().lower()

    print(msg.topic)

    if msg.topic == MQTT_TOPIC_INVERTER:
        if payload == "true":
            with modo_lock:
                if not modo_invertido:
                    modo_invertido = False
                    print("[MODIFICADOR] Modo invertido ativado por 5 segundos!")
                    threading.Thread(target=temporizador_inversao, daemon=True).start()

    elif msg.topic == MQTT_TOPIC_VIBRAR:
        with vibrando_lock:
            if payload == "pedra" or payload == "true":
                if not vibrando:
                    vibrando = True
                    print("[VIBRAÇÃO] Ativando vibração contínua...")
                    threading.Thread(target=loop_vibracao, daemon=True).start()
            elif payload == "false":
                vibrando = False
                print("[VIBRAÇÃO] Vibração desativada.")


    elif msg.topic == MQTT_TOPIC_DEBUFF:
        with controle_lock:
            payload = json.loads(payload)
            debuff = payload['debuff']
            if debuff == "casca":
                threading.Thread(target=bloqueia_controle, daemon=True).start()



def conectar_mqtt():
    client.on_connect = on_connect
    client.on_message = on_message
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            break
        except Exception as e:
            print(f"[MQTT] Erro ao conectar: {e}. Tentando novamente em {RECONNECT_DELAY}s.")
            time.sleep(RECONNECT_DELAY)

def temporizador_inversao():
    global modo_invertido
    time.sleep(5)
    with modo_lock:
        modo_invertido = False
    print("[MODIFICADOR] Modo invertido desativado.")

def bloqueia_controle():
    global controle_bloqueado
    controle_bloqueado = True
    print("Controle BLOQUEADO")
    time.sleep(5)
    with controle_lock:
        controle_bloqueado = False
    print("Controle DESBLOQUEADO")

def loop_vibracao():
    global vibrando
    try:
        while True:
            with vibrando_lock:
                if not vibrando:
                    if joystick_global:
                        joystick_global.stop_rumble()
                    break
            if joystick_global:
                joystick_global.rumble(0.5, 0.5, 1000)  # Duração de 1 segundo
            time.sleep(1.0)  # Reaplica a vibração
    except Exception as e:
        print(f"[ERRO] Erro na vibração contínua: {e}")

def inicializar_joystick():
    global joystick_global
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        raise RuntimeError("Nenhum joystick detectado.")
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"[JOYSTICK] Conectado: {joystick.get_name()}")
    joystick_global = joystick
    return joystick

max_aceleracao = 210
max_re = 120
max_curva = 90

global cor
cor = ""

def ler_controle(joystick):
    pygame.event.pump()

    eixo_dir_x = round(joystick.get_axis(2), 2)
    eixo_esq_y = round(joystick.get_axis(1), 2)
    rt = round(joystick.get_axis(5), 2)
    lt = round(joystick.get_axis(4), 2)
    
    global cor

    if joystick.get_button(0):
        cor = "verde"
    elif joystick.get_button(1):
        cor = "vermelho"
    elif joystick.get_button(2):
        cor = "azul"
    elif joystick.get_button(3):
        cor = "" 

    # Normalizar pequenas variações
    if abs(eixo_esq_y) < 0.1:
        eixo_esq_y = 0.0
    if abs(eixo_dir_x) < 0.1:
        eixo_dir_x = 0.0
    if abs(rt) < 0.1:
        rt = 0.0
    if abs(lt) < 0.1:
        lt = 0.0

    # Aceleração para frente (positivo)
    frente = max(rt, -eixo_esq_y)  # eixo pra frente é negativo
    frente = frente if frente > 0.1 else 0.0

    # Ré (negativo)
    tras = max(lt, eixo_esq_y)  # eixo pra trás é positivo
    tras = tras if tras > 0.1 else 0.0

    acelera = frente * max_aceleracao - tras * max_re

    # Corrigir resíduos como -3.0, 79.999, etc
    if abs(acelera) < 1:
        acelera = 0.0

    # Arredondar resultado final
    acelera = round(acelera, 1)

    with modo_lock:
        if modo_invertido:
            acelera *= -1
            eixo_dir_x *= -1

    return {'curva': round(eixo_dir_x, 2) * max_curva + 90, 'acelera': acelera, 'cor': cor}


def main():
    print("[SISTEMA] Iniciando controle remoto com modo invertido e vibração contínua...")
    conectar_mqtt()
    client.loop_start()

    try:
        joystick = inicializar_joystick()
    except Exception as e:
        print(f"[ERRO] Falha ao iniciar joystick: {e}")
        input("Pressione Enter para sair...")
        return

    ultimo_comando = {'curva': 0.0, 'acelera': 0.0, 'cor': ''}

    try:
        while True:
            if not controle_bloqueado:
                comando = ler_controle(joystick)
                if comando != ultimo_comando:
                    print("[ENVIADO]", comando)
                    client.publish(MQTT_TOPIC_COMANDO, json.dumps(comando))
                    ultimo_comando = comando
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[INFO] Encerrado pelo usuário.")
    except Exception as e:
        print(f"[ERRO FATAL] {e}")
        input("Pressione Enter para sair...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERRO CRÍTICO] {e}")
        input("Pressione Enter para sair...")


#mosquitto_pub -h localhost -t "teste/vibrar" -m "pedra"
#mosquitto_pub -h localhost -t "teste/vibrar" -m "false"
#mosquitto_pub -h localhost -t "teste/inverter" -m "true"
