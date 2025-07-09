from config import BRANCO

import pygame
import time
import json
import os
from config import *

class HUD:

    def __init__(self, nome, largura):
        self.nome = nome
        self.largura = largura
        self.tempo_inicio = time.time()
        self.tempo_fim = float('inf')
        self.fonte = pygame.font.SysFont("Arial", 26)

        self.cronometro_parado = False
        self.check_points = 0
        self.caixa_larg = 450
        self.caixa_alt = 250
        self.caixa_x = (self.largura - self.caixa_larg) // 2
        self.caixa_y = 280

    def carregar_ranking(self):
        if os.path.exists("ranking.json"):
            with open("ranking.json", "r") as f:
                return json.load(f)
        return []

    def desenhar_tela_corrida(self, tela, nome_prox_jogador, input_nome, btn_go, texto_digitado='', efeito = 'Sem efeito'):

        tempo_atual = int(self.tempo_fim - self.tempo_inicio) if self.cronometro_parado else int(time.time() - self.tempo_inicio)
        minutos = tempo_atual // 60
        segundos = tempo_atual % 60
        tempo_str = f"{minutos:02}:{segundos:02}"

        efeito = "Sem efeito" if not efeito else efeito
        hud_info = [
            f"{self.nome}: {tempo_str}",
            f"Check Points: {self.check_points}",
            f"Efeito: {efeito}"
        ]

        ranking = self.carregar_ranking()

        # Fundo da caixa
        caixa = pygame.Surface((self.caixa_larg + 100, self.caixa_alt))
        caixa.set_alpha(180)
        caixa.fill((0, 0, 0))
        tela.blit(caixa, (self.caixa_x, self.caixa_y))

        # Esquerda (HUD)
        titulo = self.fonte.render("Piloto:", True, (255, 255, 0))
        tela.blit(titulo, (self.caixa_x + 30, self.caixa_y + 10))

        for i, texto in enumerate(hud_info):
            render = self.fonte.render(texto, True, BRANCO)
            tela.blit(render, (self.caixa_x + 30, self.caixa_y + 40 + i * 30))

        # Direita (Ranking)
        titulo = self.fonte.render("Ranking:", True, (255, 255, 0))
        tela.blit(titulo, (self.caixa_x + self.caixa_larg - 150, self.caixa_y + 10))

        for i, jogador in enumerate(ranking[:5]):
            texto = f"{i+1}. {jogador['nome']} - {jogador['tempo']}s"
            render = self.fonte.render(texto, True, BRANCO)
            tela.blit(render, (self.caixa_x + self.caixa_larg - 150, self.caixa_y + 40 + i * 30))


        if nome_prox_jogador:
            texto_nome = self.fonte.render("Próximo:", True, BRANCO)
            tela.blit(texto_nome, (self.caixa_x + 30, self.caixa_y + 200))

            pygame.draw.rect(tela, BRANCO, input_nome, 2)

            nome_surface = self.fonte.render(texto_digitado, True, BRANCO)
            tela.blit(nome_surface, (input_nome.x + 6, input_nome.y + 6))
            self.desenhar_botao(tela, "GO!", btn_go)

    def desenhar_multiplayer(self, tela, num_jogador):
        # Fundo da caixa
        caixa = pygame.Surface((self.caixa_larg, self.caixa_alt))
        caixa.set_alpha(180)
        caixa.fill((0, 0, 0))
        tela.blit(caixa, (self.caixa_x, self.caixa_y))

        # Jogador
        texto_nome = self.fonte.render(f"Nome jogador {num_jogador}:", True, BRANCO)
        tela.blit(texto_nome, (self.caixa_x + 30, self.caixa_y + 10))
        input_nome = pygame.Rect(self.caixa_x + 30, self.caixa_y + 60, 250, 40)
        pygame.draw.rect(tela, BRANCO, input_nome, 2)
        nome_surface = self.fonte.render(texto_nome, True, BRANCO)
        tela.blit(nome_surface, (self.caixa_x + 30, self.caixa_y + 60))

    def desenhar_botao_opcoes(self, tela, texto, rect, habilitado=True):
        cor = AZUL if habilitado else CINZA_CLARO
        pygame.draw.rect(tela, cor, rect, border_radius=8)
        fonte = pygame.font.SysFont("Arial", 24, bold=True)
        label = fonte.render(texto, True, BRANCO if habilitado else CINZA)
        tela.blit(label, label.get_rect(center=rect.center))

    def animar_semaforo(self, tela, caixa_y):
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
                        luz = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
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

    def get_botoes_posicoes(self, texto, fonte, y_base, caixa_x):
        texto_render = fonte.render(texto, True, BRANCO)
        anterior_x = caixa_x + 60
        proximo_x = anterior_x + 290
        return texto_render, anterior_x, proximo_x, y_base

    def desenhar_botao(self, tela, texto, rect, habilitado=True):
        cor = AZUL if habilitado else BEGE
        pygame.draw.rect(tela, cor, rect, border_radius=8)
        fonte = pygame.font.SysFont("Arial", 24, bold=True)
        label = fonte.render(texto, True, BRANCO if habilitado else CINZA)
        tela.blit(label, label.get_rect(center=rect.center))

    def parar_cronometro(self, tempo_fim):
        self.tempo_fim = tempo_fim
        self.cronometro_parado = True
