import json
import os
import pygame
from config import ARQUIVO_RANKING, ARQUIVO_HARDCORE_RANKING, ARQUIVO_MULTIPLAYER_RANKING

def carregar_ranking(modo_jogo):
    arquivo = ARQUIVO_RANKING if modo_jogo == 'Arcade' else ARQUIVO_HARDCORE_RANKING if modo_jogo == 'Hardcore' else ARQUIVO_MULTIPLAYER_RANKING
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            return json.load(f)
    return []


def salvar_no_ranking(id_jogador, nome, tempo_segundos, modo_jogo):
    arquivo = ARQUIVO_RANKING if modo_jogo == 'Arcade' else ARQUIVO_HARDCORE_RANKING if modo_jogo == 'Hardcore' else ARQUIVO_MULTIPLAYER_RANKING
    ranking = carregar_ranking(modo_jogo)
    ranking.append({"id": id_jogador, "nome": nome, "tempo": tempo_segundos})
    ranking.sort(key=lambda x: x["tempo"])
    with open(arquivo, "w") as f:
        json.dump(ranking, f, indent=4)


def apaga_ranking_multiplayer():
    with open(ARQUIVO_MULTIPLAYER_RANKING, "w") as f:
        json.dump([], f, indent=4)


def desenhar_ranking(tela, largura_tela):
    ranking = carregar_ranking()
    fonte = pygame.font.SysFont("Arial", 26)

    caixa_larg = 450
    caixa_alt = 360
    caixa_x = (largura_tela - caixa_larg) // 2
    caixa_y = 280

    caixa = pygame.Surface((caixa_larg, caixa_alt))
    caixa.set_alpha(180)
    caixa.fill((0, 0, 0))
    tela.blit(caixa, (caixa_x, caixa_y))

    # Título centralizado
    titulo = fonte.render("Ranking:", True, (255, 255, 0))
    titulo_rect = titulo.get_rect(center=(caixa_x + caixa_larg // 2, caixa_y + 30))
    tela.blit(titulo, titulo_rect)

    # Jogadores centralizados
    for i, jogador in enumerate(ranking[:8]):
        texto = f"{i+1}º. {jogador['nome']} - {jogador['tempo']}s"
        render = fonte.render(texto, True, (255, 255, 255))
        rect = render.get_rect(center=(caixa_x + caixa_larg // 2, caixa_y + 70 + i * 30))
        tela.blit(render, rect)

def ranking_geral(id_jogador, modo_jogo):
    ranking = carregar_ranking(modo_jogo)
    ranking.sort(key=lambda x: x["tempo"])

    texto = ""

    top_5 = ranking[:5]
    for i, jogador in enumerate(top_5):
        texto += f"{i + 1}º. {jogador['nome']} - {jogador['tempo']}s\n"

    ids_top_5 = [competidor['id'] for competidor in top_5]
    if id_jogador not in ids_top_5:
        for i, jogador in enumerate(ranking):
            if jogador["id"] == id_jogador:
                texto += f"{i + 1}º. {jogador['nome']} - {jogador['tempo']}s"
                break

    return texto


def ranking_multiplayer(lista_ids_jogadores):
    ranking = carregar_ranking('Multiplayer')
    competidores = []

    for id_jogador in lista_ids_jogadores:
        for jogador in ranking:
            if jogador["id"] == id_jogador:
                competidores.append(jogador)

    competidores.sort(key=lambda x: x["tempo"])
    return competidores

