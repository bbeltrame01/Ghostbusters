import pygame
import random
import heapq

# Definir algumas constantes
LARGURA_TELA = 800
ALTURA_TELA = 800
TAMANHO_CELULA = 10
LINHAS = LARGURA_TELA // TAMANHO_CELULA
COLUNAS = ALTURA_TELA // TAMANHO_CELULA
RAIO_RADAR = 10
QUANTIDADE_FANTASMAS = 50

# Pesos dos terrenos
PESOS = {'G': 1, 'A': 5, 'M': 10}

# Definir cores
CINZA = (169, 169, 169)
VERDE = (34, 177, 76)
AZUL = (0, 0, 255)
MARRON = (139, 69, 19)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)

# Inicializar o Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Caça-Fantasmas")

# Gerar o mapa
def gerar_mapa(linhas, colunas):
  tipos_terreno = ['G', 'A', 'M']
  mapa = []
  for _ in range(linhas):
    linha = [random.choice(tipos_terreno) for _ in range(colunas)]
    mapa.append(linha)
  return mapa

# Função para desenhar o mapa
def draw_map(mapa, jogador_pos, fantasmas):
  # Desenhar o mapa
  for i in range(len(mapa)):
    for j in range(len(mapa[i])):
      terreno = mapa[i][j]
      if terreno == 'G':
        cor = VERDE
      elif terreno == 'A':
        cor = AZUL
      elif terreno == 'M':
        cor = MARRON
      pygame.draw.rect(tela, cor, (j * TAMANHO_CELULA, i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
  
  # Desenhar os fantasmas
    for fantasma in fantasmas:
      x, y = fantasma
      pygame.draw.rect(tela, BRANCO, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

  # Desenhar o jogador
  x, y = jogador_pos
  pygame.draw.rect(tela, AMARELO, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

# Função para gerar os fantasmas
def gerar_fantasmas(qtd, linhas, colunas):
  fantasmas = set()
  while len(fantasmas) < qtd:
    x, y = random.randint(0, colunas - 1), random.randint(0, linhas - 1)
    fantasmas.add((x, y))
  return fantasmas

# Radar do jogador
def radar(jogador_pos, fantasmas, raio):
  x, y = jogador_pos
  visiveis = []
  for dx in range(-raio, raio + 1):
    for dy in range(-raio, raio + 1):
      if (x + dx, y + dy) in fantasmas:
        visiveis.append((x + dx, y + dy))
  return visiveis

# Distância de Manhattan
def heuristica(a, b):
  return abs(b[0] - a[0]) + abs(b[1] - a[1])

# Algoritmo A* para encontrar o caminho menos custoso
def a_star(mapa, inicio, final):  
  fila = []
  heapq.heappush(fila, (0, inicio))
  custos = {inicio: 0}
  caminhos = {inicio: None}

  while fila:
    _, atual = heapq.heappop(fila)
    
    if atual == final:
      caminho = []
      while atual:
        caminho.append(atual)
        atual = caminhos[atual]
      return caminho[::-1]  # Retorna o caminho na ordem correta

    x, y = atual
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Movimentos possíveis
      nx, ny = x + dx, y + dy
      if 0 <= nx < COLUNAS and 0 <= ny < LINHAS:  # Dentro do mapa
        novo_custo = custos[atual] + PESOS[mapa[ny][nx]]
        if (nx, ny) not in custos or novo_custo < custos[(nx, ny)]:
          custos[(nx, ny)] = novo_custo
          prioridade = novo_custo + heuristica((nx, ny), final)
          heapq.heappush(fila, (prioridade, (nx, ny)))
          caminhos[(nx, ny)] = atual
    
  # Caso não encontre um caminho
  return None

# Função principal para rodar o jogo
def jogo():
  mapa = gerar_mapa(LINHAS, COLUNAS)
  fantasmas = gerar_fantasmas(QUANTIDADE_FANTASMAS, LINHAS, COLUNAS)
  jogador_pos = (random.randint(0, COLUNAS - 1), random.randint(0, LINHAS - 1))
  running = True
  while running:
    tela.fill(CINZA)
    draw_map(mapa, jogador_pos, fantasmas)
    
    pygame.display.update()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # Radar para detectar fantasmas próximos
    fantasmas_visiveis = radar(jogador_pos, fantasmas, RAIO_RADAR)

    if fantasmas_visiveis:
      # Selecionar o fantasma mais próximo como alvo
      menor_distancia = float('inf')
      alvo = None

      for fantasma in fantasmas_visiveis:
        distancia = heuristica(jogador_pos, fantasma)
        if distancia < menor_distancia:
          menor_distancia = distancia
          alvo = fantasma

      caminho = a_star(mapa, jogador_pos, alvo)
      if caminho and len(caminho) > 1:
        jogador_pos = caminho[1]  # Move para a próxima célula do caminho
        if jogador_pos == alvo:
          fantasmas.remove(alvo)  # Remove o fantasma capturado
    else:
      # Movimento aleatório se nenhum fantasma estiver visível
      dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
      novo_x, novo_y = jogador_pos[0] + dx, jogador_pos[1] + dy
      if 0 <= novo_x < COLUNAS and 0 <= novo_y < LINHAS:
        jogador_pos = (novo_x, novo_y)

    if not fantasmas:
      print("Todos os fantasmas foram capturados!")
      running = False

# Rodar o jogo
if __name__ == "__main__":
    jogo()
    pygame.quit()