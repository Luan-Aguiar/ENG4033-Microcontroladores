import pygame
import sys
import time

from hud import HUD
from ranking import salvar_no_ranking
from app.main.mqtt_connection.mqtt_client_connection import mqtt_state

def mostrar_cronometro(tela, id_jogador, nome_jogador, nome_prox_jogador, modo_jogo):

    largura, altura = tela.get_size()
    fundo = pygame.image.load("backgrounds/tela_configuracoes.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    hud = HUD(nome_jogador, largura)
    input_nome = pygame.Rect(300, 475, 190, 40)
    btn_go = pygame.Rect(350, 540, 100, 40)

    rodando = True
    texto_digitado = ''
    escrevendo_nome = False
    check_points_anterior = 0
    while rodando:
        if not hud.cronometro_parado and mqtt_state.check_points != check_points_anterior:
            hud.check_points += 1
            check_points_anterior = mqtt_state.check_points

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN and escrevendo_nome:
                if evento.key == pygame.K_RETURN:
                    escrevendo_nome = False
                    nome_prox_jogador = texto_digitado
                    rodando = False
                elif evento.key == pygame.K_BACKSPACE:
                    texto_digitado = texto_digitado[:-1]
                else:
                    texto_digitado += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse = evento.pos

                if btn_go.collidepoint(mouse):
                    rodando = False

                if input_nome.collidepoint(mouse):
                    escrevendo_nome = True

        if rodando:
            # Verifica se passou todos os objetivos para parar o cronometro
            if hud.check_points == 3 and not hud.cronometro_parado:
                hud.parar_cronometro(time.time())

            tela.blit(fundo, (0, 0))
            # Tela proximo jogador ou fim corrida
            if nome_prox_jogador and hud.check_points == 3:
                hud.desenhar_tela_corrida(tela, True, input_nome, btn_go, texto_digitado, mqtt_state.efeito)
            else:
                hud.desenhar_tela_corrida(tela, False, input_nome, btn_go, texto_digitado, mqtt_state.efeito)

            pygame.display.update()
            # Desativa o efeito
            if mqtt_state.efeito and (time.time() - mqtt_state.tempo_inicio) >= 5:
                mqtt_state.efeito = None

            # Para o cronometro
            if hud.cronometro_parado:
                pygame.time.delay(30)
                if not nome_prox_jogador:
                    rodando = False
            else:
                pygame.time.delay(1000)

    tempo_final = int(hud.tempo_fim - hud.tempo_inicio)
    salvar_no_ranking(id_jogador, nome_jogador, tempo_final, modo_jogo)

    return texto_digitado

