# Programa escrito na IDLE PyCharm na linguagem Python por Arnaldo Lucas (adm deste github)
# Código de execução do jogo Snake (cobrinha)

# from typing import Tuple
import sys
import pygame  # pygame é um pacote de desenvolvimento em python, necessário para este programa
import random
from pygame.locals import *
from pygame import Surface

# from pygame.event import Event  # imporatmos a biblioteca de eventos/ações

# definição de dimensões e inicialização de janela (ou tela, screen)
dimensoes = (600, 600)
tela = pygame.display.set_mode(dimensoes)  # a tela será um quadrado de 640 pixels de lado
# a tela consiste numa matriz que começa no ponto (0[x],0[y])
# e os pontos aumentando representam um sentido para as direita e para baixo, respectivamente
pygame.display.set_caption('Snake')  # nomeamos e abrimos a janela do jogo (window name)

# cobrinha (ícone) - a cobrinha nada mais é do que uma lista de seguimentos que muda de posição
snake_skin: Surface = pygame.Surface((10, 10))  # definimos o espaço total (px^2) que cada parte da cobrinha ocupará
snake = [(200, 200), (210, 200), (220, 200)]  # representamos ela com uma tupla das posições do corpo da cobrinha
snake_skin.fill((255, 255, 255))  # definimos a cor da cobrinha, no caso branca (RGB)
direcao = K_LEFT  # definimos a direção inicial que a cobrinha irá seguir


def on_grid_random():  # função que gera um número aleatório adequado ao grid 10x10 que criamos
    x = random.randint(0, 590)   # 590 porque se o valor for maior que este, em algum momento a maçã poderá nascer
    y = random.randint(0, 590)   # numa posição que excede os limites da tela (600x600)
    return x // 10 * 10, y // 10 * 10


def colisao(c1, c2):   # função para detectar colisões
    return c1[0] == c2[0] and c1[1] == c2[1]


def fora_dos_limites(posicao):  # função que indica se uma posição está fora dos limites da tela ou não
    if 0 <= posicao[0] < dimensoes[0] and 0 <= posicao[1] < dimensoes[1]:
        return False  # se não, retona falso
    else:
        return True   # se sim, retorna verdadeiro


# maçã (apple - ícone) ------ (0, 590) pois a maçã terá 10px, então assim não sairá dos limites da tela (600px^2)
posicao_maca = on_grid_random()  # a posição da maçã será aleatória
maca = pygame.Surface((10, 10))  # definimos o espaço ocupados pela maçã
maca.fill((255, 0, 0))  # definimos a cor vermelha para a maçã

# INÍCIO
check_errors = pygame.init()  # criamos uma variável que recebe a inicialização do pygame para checar erros
if check_errors[1] > 0:  # checamos se ocorreu algum erro de inicialização
    print("Erro: " + check_errors[1])  # se sim, imprimimos o erro
else:
    print("jogo inicializado com sucesso")  # se não, imprimimos que o jogo foi inicializado


# A dinâmica de um jogo consiste na criação de um laço (loop) infinito que tem no mínimo 3 ações:
# detectar eventos/mudanças causadas por ações do jogador (clicks, entradas de dados, instruções passadas)
# exibir, alterar e atualizar a tela
# definir os movimentos ou ações feitos pelos elementos (ex: iniciar, mover, reiniciar, etc) do jogo


while True:  # loop infinito do jogo
    # para que o movimento não seja muito rápido, usamos o objeto clock, que limita o fps do jogo
    pygame.time.Clock().tick(12)

    # Para começar, primeiramente, limpamos a tela a tod0 momento
    tela.fill((0, 0, 0))  # pintamos a tela de preto

    # evento: Event  # determinamos 'evento' como variável do tipo event (função de pygaame para detectar eventos)
    for event in pygame.event.get():  # laço para detectar eventos
        if event.type == QUIT:  # verificamos se o evento é sair do jogo
            pygame.quit()  # se for, fecha-se a janela
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key in [K_UP or ord("w"), K_DOWN or ord("s"), K_LEFT or ord("d"), K_RIGHT or ord("a")]:
                direcao = event.key

    # quando a cobrinha comer a maçã, adiciona-se mais uma parte a ela
    if colisao(snake[0], posicao_maca):
        posicao_maca = on_grid_random()
        snake.append((0, 0))

    # direcionamento do corpo, tendo como base a direcionamento da cabeça da cobrinha
    # cada parte do corpo da cobrinha se move para a posição antes ocupada pela parte mais próxima da cabeça
    # para expressar isso, começando do rabo (última posição), criamos um loop que leva cada parte para a penúltima posição anterior
    for i in range(len(snake) - 1, 0, -1):  # começamos da última posição, até a posição inicial da cabeça
        if colisao(snake[0], snake[i]) or fora_dos_limites(snake[0]):  # se houver colisão, o jogo reseta
            snake = [(200, 200), (210, 200), (220, 200)]      # posição inicial da cobrinha
            posicao_maca = on_grid_random()                   # posição inicial da maçã
            direcao = K_LEFT                                  # direção inicial
            break  # quebra o loop, que recomeça, "reiniciando" o jogo
        snake[i] = snake[i - 1]  # (snake[i - 1][0], snake[i - 1][1])  # atribuímos a nova posição com base na anterior (i-1)

    # direcionamento da cabeça da cobrinha
    if direcao == K_UP:  # para a cobrinha ir para cima, atribuímos a cabeça da cobra (snake[0]) a posição de cima
        snake[0] = (snake[0][0], snake[0][1] - 10)  # -> cima, eixo y diminuindo, logo voltamos 10px no eixo y
    elif direcao == K_DOWN:  # para a cobrinha ir para baixo, atribuímos a cabeça da cobra a posição de baixo
        snake[0] = (snake[0][0], snake[0][1] + 10)  # -> baixo, eixo y aumentando, logo aumentamos 10px no eixo y
    elif direcao == K_RIGHT:  # para a cobrinha ir para a direita, atribuímos a cabeça da cobra a posição da direita
        snake[0] = (snake[0][0] + 10, snake[0][1])  # -> direita, eixo x diminuindo, logo aumentamos 10px no eixo x
    elif direcao == K_LEFT:  # para a cobrinha ir para a esquerda, atribuímos a cabeça da cobra a posição da esquerda
        snake[0] = (snake[0][0] - 10, snake[0][1])  # -> esquerda, eixo x diminuindo, logo voltamos 10px no eixo x

    # para plotar a cobrinha e a maçã na tela, usamos a função BLIT, para cada pixel da cobrinha e para os da maçã
    tela.blit(maca, posicao_maca)  # mostramos a maçã numa posição aleatória da tela
    for pos in snake:  # para mostrar cada parte da cobrinha, usamos um loop
        tela.blit(snake_skin, pos)  # passamos a superfície (a que a skin ocupa) e uma posição (passamos a da cobrinha)

    pygame.display.update()  # atualizamos a tela a tod0 momento
