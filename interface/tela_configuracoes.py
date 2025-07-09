import pygame
import sys
import time

from config import *

# Opções
modo_jogo_opcoes = ["Arcade", "Hardcore", "Multiplayer"]
pistas = ["Cidade", "Deserto", "Montanha"]
num_jogadores_opcoes = [2, 3, 4]

# Estado
modo_jogo_idx = 0
pista_idx = 0
num_jogadores_idx = 0
nome_jogador = ""
escrevendo_nome = False

def desenhar_botao(tela, texto, rect, habilitado=True):
    cor = AZUL if habilitado else CINZA_CLARO
    pygame.draw.rect(tela, cor, rect, border_radius=8)
    fonte = pygame.font.SysFont("Arial", 24, bold=True)
    label = fonte.render(texto, True, BRANCO if habilitado else CINZA)
    tela.blit(label, label.get_rect(center=rect.center))

def get_botoes_posicoes(texto, fonte, y_base, caixa_x):
    texto_render = fonte.render(texto, True, BRANCO)
    anterior_x = caixa_x + 60  # Alinhado com "Nome:"
    proximo_x = anterior_x + 290
    return texto_render, anterior_x, proximo_x, y_base


def animar_semaforo(tela, caixa_y):
    largura, altura = tela.get_size()
    fundo = pygame.image.load("backgrounds/tela_configuracoes.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    # Som semáforo
    pygame.mixer.init()
    som_tick = pygame.mixer.Sound("som_vermelho.mp3")

    # Tamanho e posição da caixa do semáforo
    semaforo_larg = 100
    semaforo_alt = 3 * 60 + 2 * 20 + 40
    semaforo_x = (largura - semaforo_larg) // 2
    semaforo_y = caixa_y

    centro_x = semaforo_x + semaforo_larg // 2
    topo_y = semaforo_y + 50
    raio = 30
    espacamento = 20

    # Inicialmente todas as luzes apagadas
    cores = [CINZA_CLARO, CINZA_CLARO, CINZA_CLARO]

    def desenhar(cores):
        tela.blit(fundo, (0, 0))

        # Caixa com borda arredondada
        caixa_menu = pygame.Surface((semaforo_larg, semaforo_alt), pygame.SRCALPHA)
        caixa_menu.fill((0, 0, 0, 180))
        pygame.draw.rect(caixa_menu, (0, 0, 0, 180), caixa_menu.get_rect(), border_radius=20)
        tela.blit(caixa_menu, (semaforo_x, semaforo_y))

        # Luzes
        for i in range(3):
            x = centro_x
            y = topo_y + i * (2 * raio + espacamento)
            pygame.draw.circle(tela, cores[i], (x, y), raio)


        pygame.display.update()

    def fade_in_luz(indice, cor_final):
        for alpha in range(0, 256, 25):
            tela.blit(fundo, (0, 0))
            caixa_menu = pygame.Surface((semaforo_larg, semaforo_alt), pygame.SRCALPHA)
            caixa_menu.fill((0, 0, 0, 180))
            pygame.draw.rect(caixa_menu, (0, 0, 0, 180), caixa_menu.get_rect(), border_radius=20)
            tela.blit(caixa_menu, (semaforo_x, semaforo_y))

            for i in range(3):
                x = centro_x
                y = topo_y + i * (2 * raio + espacamento)
                if i < indice:
                    pygame.draw.circle(tela, cores[i], (x, y), raio)
                elif i == indice:
                    r, g, b = cor_final
                    luz = pygame.Surface((raio*2, raio*2), pygame.SRCALPHA)
                    pygame.draw.circle(luz, (r, g, b, alpha), (raio, raio), raio)
                    tela.blit(luz, (x - raio, y - raio))
                else:
                    pygame.draw.circle(tela, CINZA_CLARO, (x, y), raio)

            pygame.display.update()
            pygame.time.delay(30)  # 30ms por passo

    # Exibir luzes apagadas por 1 segundo
    desenhar(cores)
    time.sleep(1)

    for i in range(3):
        if i == 2:
            som_tick = pygame.mixer.Sound("som_verde.mp3")

        som_tick.play()

        if i < 2:
            cor_final = (255, 0, 0)  # Vermelho
        else:
            cor_final = (0, 255, 0)  # Verde

        fade_in_luz(i, cor_final)
        cores[i] = cor_final
        time.sleep(1)


def tela_configuracoes(tela):
    global modo_jogo_idx, pista_idx, num_jogadores_idx, nome_jogador, escrevendo_nome

    largura, altura = tela.get_size()
    fonte_opcao = pygame.font.SysFont("Arial", 36, bold=True)
    fonte_pista = pygame.font.SysFont("Arial", 16, bold=True)

    fundo = pygame.image.load("backgrounds/tela_configuracoes.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    caixa_larg = 450
    caixa_alt = 350
    caixa_x = (largura - caixa_larg) // 2
    caixa_y = 250
    caixa_menu = pygame.Surface((caixa_larg, caixa_alt))
    caixa_menu.set_alpha(180)
    caixa_menu.fill((0, 0, 0))

    input_nome = pygame.Rect(caixa_x + 250, caixa_y + 180, 190, 40)
    btn_go = pygame.Rect(caixa_x + 180, caixa_y + 260, 100, 40)


    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN and escrevendo_nome:
                if evento.key == pygame.K_RETURN:
                    escrevendo_nome = False
                elif evento.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
                else:
                    nome_jogador += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse = evento.pos

                if input_nome.collidepoint(mouse):
                    escrevendo_nome = True

                if btn_go.collidepoint(mouse) and (len(nome_jogador) > 0):
                    return (
                        modo_jogo_opcoes[modo_jogo_idx],
                        pistas[pista_idx],
                        num_jogadores_opcoes[num_jogadores_idx] if modo_jogo_opcoes[modo_jogo_idx] == "Multiplayer" else 1,
                        nome_jogador
                    )

                # Modo de jogo
                texto, anterior_x, proximo_x, y = get_botoes_posicoes(modo_jogo_opcoes[modo_jogo_idx], fonte_opcao, caixa_y + 20, caixa_x)
                if pygame.Rect(anterior_x, y, 50, 40).collidepoint(mouse) and modo_jogo_idx > 0:
                    modo_jogo_idx -= 1
                if pygame.Rect(proximo_x, y, 50, 40).collidepoint(mouse) and modo_jogo_idx < len(modo_jogo_opcoes) - 1:
                    modo_jogo_idx += 1

                # Pistas
                texto, anterior_x, proximo_x, y = get_botoes_posicoes(pistas[pista_idx], fonte_opcao, caixa_y + 80, caixa_x)
                if pygame.Rect(anterior_x, y, 50, 40).collidepoint(mouse) and pista_idx > 0:
                    pista_idx -= 1
                if pygame.Rect(proximo_x, y, 50, 40).collidepoint(mouse) and pista_idx < len(pistas) - 1:
                    pista_idx += 1

                # Jogadores
                if modo_jogo_opcoes[modo_jogo_idx] == "Multiplayer":
                    texto, anterior_x, proximo_x, y = get_botoes_posicoes(f"{num_jogadores_opcoes[num_jogadores_idx]} Jogadores", fonte_opcao, caixa_y + 140, caixa_x)
                    if pygame.Rect(anterior_x, y, 50, 40).collidepoint(mouse) and num_jogadores_idx > 0:
                        num_jogadores_idx -= 1
                    if pygame.Rect(proximo_x, y, 50, 40).collidepoint(mouse) and num_jogadores_idx < len(num_jogadores_opcoes) - 1:
                        num_jogadores_idx += 1

        tela.blit(fundo, (0, 0))
        tela.blit(caixa_menu, (caixa_x, caixa_y))

        # Modo de jogo
        texto, anterior_x, proximo_x, y = get_botoes_posicoes(modo_jogo_opcoes[modo_jogo_idx], fonte_opcao, caixa_y + 20, caixa_x)
        tela.blit(texto, (anterior_x + 60, y))
        desenhar_botao(tela, "<", pygame.Rect(anterior_x, y, 50, 40), modo_jogo_idx > 0)
        desenhar_botao(tela, ">", pygame.Rect(proximo_x, y, 50, 40), modo_jogo_idx < len(modo_jogo_opcoes) - 1)

        # Pista
        texto, anterior_x, proximo_x, y = get_botoes_posicoes(pistas[pista_idx], fonte_opcao, caixa_y + 80, caixa_x)
        tela.blit(texto, (anterior_x + 60, y))
        desenhar_botao(tela, "<", pygame.Rect(anterior_x, y, 50, 40), pista_idx > 0)
        desenhar_botao(tela, ">", pygame.Rect(proximo_x, y, 50, 40), pista_idx < len(pistas) - 1)

        # Jogadores
        if modo_jogo_opcoes[modo_jogo_idx] == "Multiplayer":
            texto, anterior_x, proximo_x, y = get_botoes_posicoes(f"{num_jogadores_opcoes[num_jogadores_idx]} Jogadores", fonte_opcao, caixa_y + 140, caixa_x)
            tela.blit(texto, (anterior_x + 60, y))
            desenhar_botao(tela, "<", pygame.Rect(anterior_x, y, 50, 40), num_jogadores_idx > 0)
            desenhar_botao(tela, ">", pygame.Rect(proximo_x, y, 50, 40), num_jogadores_idx < len(num_jogadores_opcoes) - 1)

        # Nome do jogador
        texto_nome = fonte_opcao.render("Jogador 1:", True, BRANCO)
        tela.blit(texto_nome, (input_nome.x - 190, input_nome.y))
        pygame.draw.rect(tela, BRANCO, input_nome, 2)
        nome_surface = fonte_opcao.render(nome_jogador, True, BRANCO)
        tela.blit(nome_surface, (input_nome.x + 5, input_nome.y + 5))

        # Configurações da pista
        extra = 50
        texto_pista = fonte_pista.render('Configuração da pista: ', True, BRANCO)
        tela.blit(texto_pista, (input_nome.x - 190, input_nome.y + extra))
        pista = pistas[pista_idx]
        nome_pistas = FASES[pista].split('\n')
        extra += 10
        for i, pista_texto in enumerate(nome_pistas):
            texto_pista = fonte_pista.render(pista_texto, True, BRANCO)
            extra += 20
            tela.blit(texto_pista, (input_nome.x - 190, input_nome.y + extra))

        # Botão GO!
        if len(nome_jogador) > 0:
            desenhar_botao(tela, "GO!", btn_go)

        pygame.display.update()
