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

    # Inicializa o controle Xbox
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

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
            if hud.check_points == 3 and not hud.cronometro_parado:
                hud.parar_cronometro(time.time())
                tempo_final = int(hud.tempo_fim - hud.tempo_inicio)
                salvar_no_ranking(id_jogador, nome_jogador, tempo_final, modo_jogo)

            tela.blit(fundo, (0, 0))

            # === Leitura do controle ===
            pygame.event.pump()
            ax_esq_x = joystick.get_axis(0)
            ax_esq_y = joystick.get_axis(1)
            ax_dir_x = joystick.get_axis(2)
            ax_dir_y = joystick.get_axis(3)
            lt = (joystick.get_axis(4) + 1) / 2
            rt = (joystick.get_axis(5) + 1) / 2
            botoes = {
                "A": joystick.get_button(0),
                "B": joystick.get_button(1),
                "X": joystick.get_button(2),
                "Y": joystick.get_button(3)
            }

            # Desenha HUD e tela principal
            if nome_prox_jogador and hud.check_points == 3:
                hud.desenhar_tela_corrida(tela, True, input_nome, btn_go, texto_digitado, mqtt_state.efeito)
            else:
                hud.desenhar_tela_corrida(tela, False, input_nome, btn_go, texto_digitado, mqtt_state.efeito)

            # Desenha botões
            painel_x = largura - 250
            painel_y = 300

            # Analógicos
            def desenhar_analogico(cx, cy, ax, ay):
                pygame.draw.circle(tela, (180, 180, 180), (cx, cy), 25, 1)
                pygame.draw.circle(tela, (255, 255, 255),
                                   (int(cx + ax * 20), int(cy + ay * 20)), 4)

            desenhar_analogico(painel_x + 50, painel_y + 60, ax_esq_x, ax_esq_y)
            desenhar_analogico(painel_x + 150, painel_y + 60, ax_dir_x, ax_dir_y)

            # Gatilhos
            pygame.draw.rect(tela, (80, 80, 80), (painel_x + 30, painel_y + 110, 10, 100), 1)
            pygame.draw.rect(tela, (200, 200, 200),
                             (painel_x + 30, painel_y + 110 + (1 - lt) * 100, 10, lt * 100))

            pygame.draw.rect(tela, (80, 80, 80), (painel_x + 160, painel_y + 110, 10, 100), 1)
            pygame.draw.rect(tela, (200, 200, 200),
                             (painel_x + 160, painel_y + 110 + (1 - rt) * 100, 10, rt * 100))

            # Botões A, B, X, Y
            botoes_xy = {
                "A": ((painel_x + 100, painel_y + 200), (0, 255, 0)),
                "B": ((painel_x + 140, painel_y + 180), (255, 0, 0)),
                "X": ((painel_x + 60, painel_y + 180), (0, 0, 255)),
                "Y": ((painel_x + 100, painel_y + 160), (255, 255, 0)),
            }

            for letra, ((bx, by), cor) in botoes_xy.items():
                pressionado = botoes[letra]
                pygame.draw.circle(tela, cor, (bx, by), 14)
                pygame.draw.circle(tela, (0, 0, 0), (bx, by), 14, 3 if pressionado else 1)
                fonte = pygame.font.SysFont(None, 18)
                texto = fonte.render(letra, True, (0, 0, 0))
                tela.blit(texto, (bx - texto.get_width() // 2, by - texto.get_height() // 2))

            pygame.display.update()

            # Efeito visual temporário (MQTT)
            if mqtt_state.efeito and (time.time() - mqtt_state.tempo_inicio) >= 5:
                mqtt_state.efeito = None

            if hud.cronometro_parado:
                pygame.time.delay(30)
                if not nome_prox_jogador:
                    rodando = False
            else:
                pygame.time.delay(50)


    return texto_digitado
