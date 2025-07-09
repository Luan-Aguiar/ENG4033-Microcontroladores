import pygame
import sys
from config import *


def tela_final(tela, competidores=None, texto_ranking=None):
    largura, altura = tela.get_size()

    # Fonte
    fonte_botao = pygame.font.SysFont("Arial", 36)
    fonte = pygame.font.SysFont("Arial", 24)

    # Imagem de fundo
    fundo = pygame.image.load("backgrounds/tela_final.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    # Botão Start
    botao_largura, botao_altura = 120, 60
    botao_x = (largura - botao_largura) // 2
    botao_y = 535
    rect_botao = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)

    def desenhar():
        tela.blit(fundo, (0, 0))

        # Botão END
        mouse = pygame.mouse.get_pos()
        cor_botao = AZUL_CLARO if rect_botao.collidepoint(mouse) else BEGE
        pygame.draw.rect(tela, cor_botao, rect_botao, border_radius=10)

        # Borda botão END
        pygame.draw.rect(tela, PRETO, rect_botao, 3, border_radius=10)

        texto_end = fonte_botao.render("END", True, PRETO)
        rect_texto_end = texto_end.get_rect(center=rect_botao.center)
        tela.blit(texto_end, rect_texto_end)


        # Fundo da caixa
        caixa_larg = 450
        caixa_alt = 250
        caixa_x = (largura - caixa_larg) // 2
        caixa_y = 280
        caixa = pygame.Surface((caixa_larg, caixa_alt))
        caixa.set_alpha(180)
        caixa.fill((0, 0, 0))
        tela.blit(caixa, (caixa_x, caixa_y))

        # Esquerda Caixa
        texto_titulo = "Ranking Geral:" if texto_ranking else "Ranking Competidores:"
        titulo = fonte.render(texto_titulo, True, (255, 255, 0))
        tela.blit(titulo, (caixa_x + 30, caixa_y + 10))

        if texto_ranking:
            texto = texto_ranking.split("\n")
            render = fonte.render(texto[0], True, BRANCO)
            tela.blit(render, (caixa_x + 30, caixa_y + 40))
            for i, texto in enumerate(texto[1:]):
                render = fonte.render(texto, True, BRANCO)
                tela.blit(render, (caixa_x + 30, caixa_y + 40 + 30*(i+1)))
        else:
            for i, competidor in enumerate(competidores):
                texto = f"{i + 1}. {competidor['nome']} - {competidor['tempo']}s"
                render = fonte.render(texto, True, BRANCO)
                tela.blit(render, (caixa_x + 30, caixa_y + 40 + i * 30))

        pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_botao.collidepoint(evento.pos):
                    return

        desenhar()
