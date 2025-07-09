import threading
from interface import main

from app.main.main import start


if __name__ == '__main__':
    start('teste_jogo_carrinho')


    # chamada no terminal
    # cd "C:\Program Files (x86)\mosquitto"
    # mosquitto_sub -t /teste -h localhost
    # mosquitto_pub -h localhost -t /teste -m "mensagem"