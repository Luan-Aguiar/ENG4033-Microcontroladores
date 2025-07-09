import json

import pygame

from app.main.main import start
from hud import HUD
import ranking
from ranking import carregar_ranking, apaga_ranking_multiplayer
from tela_configuracoes import tela_configuracoes
from tela_final import tela_final
from tela_inicial import tela_inicial
from tela_jogo import mostrar_cronometro
from controle.controle_remoto import main as controle

import threading

def main():

    mqtt_jogo =start()

    thread = threading.Thread(target=controle)
    thread.daemon = True
    thread.start()


    pygame.init()
    largura, altura = 800, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Micro Kart")
    lista_ids_jogadores = []

    tela_inicial(tela)
    modo_jogo, pista, num_jogadores, nome_jogador = tela_configuracoes(tela)
    nome_prox_jogador = True
    hud = HUD(nome_jogador, largura)


    payload = {'start': 1,
               'end': 0,
               'modo_jogo': modo_jogo
               }

    str_payload = json.dumps(payload)

    mqtt_jogo.publish(topico='status_jogo_carrinho', payload=str_payload)

    for i in range(1, num_jogadores+1):
        id_jogador = len(carregar_ranking(modo_jogo))
        if num_jogadores == 1 or i == num_jogadores:
            nome_prox_jogador = False
        hud.animar_semaforo(tela, altura * 0.5)
        nome_jogador = mostrar_cronometro(tela, id_jogador, nome_jogador, nome_prox_jogador, modo_jogo)
        lista_ids_jogadores.append(id_jogador)


    if modo_jogo != 'Multiplayer':
        texto_ranking = ranking.ranking_geral(lista_ids_jogadores[0], modo_jogo)
        tela_final(tela, texto_ranking= texto_ranking)
    else:
        competidores = ranking.ranking_multiplayer(lista_ids_jogadores)
        tela_final(tela, competidores=competidores)
        apaga_ranking_multiplayer()

    payload['end'] = 1
    str_payload = json.dumps(payload)

    mqtt_jogo.publish(topico='status_jogo_carrinho', payload=str_payload)



if __name__ == "__main__":
    main()
