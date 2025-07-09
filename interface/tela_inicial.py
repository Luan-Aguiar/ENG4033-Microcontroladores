import pygame
import sys
from config import *

def tela_inicial(tela):
    largura, altura = tela.get_size()

    # Fonte
    fonte_botao = pygame.font.SysFont("Arial", 36)

    # Imagem de fundo
    fundo = pygame.image.load("backgrounds/background.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    # Botão Start
    botao_largura, botao_altura = 215, 85
    botao_x = (largura - botao_largura) // 2
    botao_y = (altura * 4 // 5)
    rect_botao = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)

    def desenhar():
        tela.blit(fundo, (0, 0))

        # Botão START
        mouse = pygame.mouse.get_pos()
        cor_botao = AZUL_CLARO if rect_botao.collidepoint(mouse) else BEGE
        pygame.draw.rect(tela, cor_botao, rect_botao, border_radius=10)

        # Borda botão START
        pygame.draw.rect(tela, PRETO, rect_botao, 3, border_radius=10)

        texto_start = fonte_botao.render("START", True, PRETO)
        rect_texto_start = texto_start.get_rect(center=rect_botao.center)
        tela.blit(texto_start, rect_texto_start)

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
