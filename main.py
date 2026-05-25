# ══════════════════════════════════════════════════════════════════════════════
# IMPORTAÇÕES — bibliotecas que o jogo precisa para funcionar
# ══════════════════════════════════════════════════════════════════════════════
import pygame          # Biblioteca principal usada para criar o jogo (gráficos, som, eventos)
import sys             # Usada para encerrar o programa com sys.exit()
import math            # Usada para cálculos matemáticos (seno, cosseno, distâncias, etc.)
import random          # Usada para gerar números aleatórios (posições, velocidades, cores)
import os              # Usada para mexer com caminhos de arquivos do sistema operacional
import numpy as np     # Biblioteca de arrays numéricos (usada para manipular pixels da imagem da arma)

# ══════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO DO PYGAME E DO SISTEMA DE ÁUDIO
# ══════════════════════════════════════════════════════════════════════════════
# Configura o mixer ANTES de inicializar o pygame para evitar atraso (lag) nos sons
# frequency=44100 → qualidade de CD; size=-16 → 16 bits; channels=2 → estéreo; buffer=512 → resposta rápida
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()          # Inicializa todos os módulos do pygame (vídeo, fontes, eventos, etc.)
pygame.mixer.init()    # Inicializa o sistema de áudio (mixer) para poder tocar sons

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTES GLOBAIS DO JOGO
# ══════════════════════════════════════════════════════════════════════════════
WIDTH, HEIGHT = 900, 650   # Largura e altura da janela do jogo, em pixels
FPS = 60                   # Quantos quadros por segundo o jogo desenha (taxa de atualização)
MUSIC_VOL_MENU = 0.5       # Volume da música no menu (médio) — escala de 0.0 a 1.0
MUSIC_VOL_GAME = 0.1       # Volume da música durante a partida (baixo, para ouvir os efeitos)

# Caminho absoluto até a pasta "assets" (onde estão as imagens e sons)
ASSETS = os.path.join(os.path.dirname(__file__), "assets")

# ── CORES NO FORMATO RGB (0-255 para cada componente Vermelho, Verde, Azul) ──
BLACK        = (0,   0,   0)     # Preto puro
WHITE        = (255, 255, 255)   # Branco puro
DARK_BG      = (10,  0,  22)     # Roxo bem escuro (fundo)
PURPLE       = (90,  0, 150)     # Roxo padrão
LIGHT_PURPLE = (180, 80, 255)    # Roxo claro (destaques e bordas)
GOLD         = (255, 210,  50)   # Dourado (títulos e estrelas)
CYAN         = (0,  220, 255)    # Ciano (mira e tiros que erraram)
RED          = (220,  50,  50)   # Vermelho (acertos e nome do alvo)
PINK         = (255, 100, 180)   # Rosa (mensagens especiais)
DARK_PURPLE  = (40,   0,  70)    # Roxo escuro alternativo
DIM_PURPLE   = (60,  10, 100)    # Roxo levemente apagado (botões secundários)
BTN_HOVER    = (130,  40, 220)   # Cor do botão quando o mouse passa por cima
BTN_NORMAL   = (80,   0, 150)    # Cor padrão dos botões
GREEN        = (50,  230,  80)   # Verde (confetes da tela de vitória)

# ── IDENTIFICADORES (IDs) DOS ESTADOS/TELAS DO JOGO ──
# Cada número representa uma tela diferente; usamos isso pra saber em que tela estamos
ST_MENU     = 0   # Tela inicial com botões "Jogar" e "Instruções"
ST_INSTRUCT = 1   # Tela explicando as regras do jogo
ST_NAME     = 2   # Tela onde o usuário digita o nome do alvo
ST_BODY     = 3   # Tela de escolha do tipo de corpo do personagem
ST_OUTFIT   = 4   # Tela de escolha da roupa do personagem
ST_HAIR     = 5   # Tela de escolha do cabelo do personagem
ST_PREVIEW  = 6   # Tela que mostra o personagem montado antes de começar
ST_GAME     = 7   # Tela do jogo em si (gameplay)
ST_WIN      = 8   # Tela de vitória (quando mata o alvo)
ST_LOSE     = 9   # Tela de derrota (quando a munição acaba antes de matar)

# ══════════════════════════════════════════════════════════════════════════════
# CRIAÇÃO DA JANELA DO JOGO
# ══════════════════════════════════════════════════════════════════════════════
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Cria a janela com as dimensões definidas
pygame.display.set_caption("Todo Mundo Odeia...")   # Define o título da janela (barra superior)
clock = pygame.time.Clock()                          # Cria um relógio para controlar os FPS do jogo
pygame.mouse.set_visible(True)                       # Faz o cursor do mouse aparecer (visível por padrão)

# ══════════════════════════════════════════════════════════════════════════════
# FONTES DE TEXTO
# ══════════════════════════════════════════════════════════════════════════════
# Funções auxiliares para criar fontes com tamanho variável (uma normal e uma em negrito)
def font(size): return pygame.font.SysFont("arial", size, bold=False)
def bold_font(size): return pygame.font.SysFont("arial", size, bold=True)

# Pré-criamos várias fontes em tamanhos diferentes para usar ao longo do jogo
F_TITLE = bold_font(54)   # Fonte gigante usada nos títulos das telas
F_BIG   = bold_font(38)   # Fonte grande para textos importantes
F_MED   = font(28)        # Fonte média (botões, mensagens principais)
F_SMALL = font(20)        # Fonte pequena para descrições e instruções
F_TINY  = font(16)        # Fonte miúda (HUD, status)
F_INPUT = bold_font(32)   # Fonte usada no campo de digitação do nome

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES PARA CARREGAR IMAGENS (SPRITES)
# ══════════════════════════════════════════════════════════════════════════════
def load_sheet(name):
    """Carrega uma imagem (sprite sheet) da pasta assets e mantém a transparência."""
    path = os.path.join(ASSETS, name)                       # Monta o caminho completo
    return pygame.image.load(path).convert_alpha()          # Carrega e converte para uso rápido

def extract_frame(sheet_surf, col, row, fw=32, fh=32):
    """Recorta UM frame (quadradinho) de uma sprite sheet.
    sheet_surf = imagem inteira; col/row = posição na grade; fw/fh = tamanho do frame (32x32)."""
    frame = pygame.Surface((fw, fh), pygame.SRCALPHA)       # Cria superfície vazia transparente
    frame.blit(sheet_surf, (0, 0), (col * fw, row * fh, fw, fh))  # Copia só o pedaço desejado
    return frame                                             # Retorna o frame extraído

def extract_gun_from_sheet():
    """Extrai a imagem da arma de um sprite sheet maior (usado como fallback se não existir 'New Piskel.png')."""
    from PIL import Image                                    # Importa Pillow (manipulação avançada de imagem)
    import numpy as np
    gun_full = Image.open(os.path.join(ASSETS, "gun_sheet.png"))  # Abre o sheet completo
    gun_frame = gun_full.crop((1115, 1025, 1683, 1632))     # Recorta a região onde está a arma desejada
    arr2 = np.array(gun_frame)                               # Converte para array numpy (matriz de pixels)
    nonblack = arr2.max(axis=2) > 10                         # Identifica pixels que NÃO são pretos
    rows_c = np.where(nonblack.any(axis=1))[0]               # Encontra as linhas que têm pixels não pretos
    cols_c = np.where(nonblack.any(axis=0))[0]               # Encontra as colunas que têm pixels não pretos
    if len(rows_c) == 0 or len(cols_c) == 0:                 # Se não achou nada, desiste
        return None
    # Recorta exatamente em torno da arma, eliminando o espaço preto ao redor
    gun_tight = gun_frame.crop((cols_c[0], rows_c[0], cols_c[-1]+1, rows_c[-1]+1))
    gun_rgba = gun_tight.convert("RGBA")                     # Converte para formato com canal alpha (transparência)
    data = np.array(gun_rgba)                                # Array numpy com os pixels
    # Encontra os pixels muito escuros (quase pretos) para torná-los transparentes
    is_dark = (data[:,:,0] < 25) & (data[:,:,1] < 25) & (data[:,:,2] < 25)
    data[is_dark, 3] = 0                                     # Define alpha (transparência) = 0 nos pixels escuros
    from PIL import Image as PILImage
    gun_pil = PILImage.fromarray(data)                       # Converte array de volta para imagem PIL
    target_w = 90                                            # Largura final desejada para a arma
    ratio = target_w / gun_pil.width                         # Calcula a proporção de redimensionamento
    gun_pil = gun_pil.resize((target_w, int(gun_pil.height * ratio)), PILImage.LANCZOS)  # Redimensiona mantendo proporção
    import io
    buf = io.BytesIO()                                       # Cria um buffer de memória (arquivo virtual)
    gun_pil.save(buf, format="PNG")                          # Salva a imagem nesse buffer como PNG
    buf.seek(0)                                              # Volta o ponteiro pro início do buffer
    return pygame.image.load(buf).convert_alpha()            # Carrega o PNG do buffer como surface do pygame

# ══════════════════════════════════════════════════════════════════════════════
# GERAÇÃO DO FUNDO ESTRELADO (GALÁXIA) — usado se a imagem do espaço não existir
# ══════════════════════════════════════════════════════════════════════════════
def create_galaxy_bg(w, h):
    """Cria uma imagem de fundo de galáxia com nebulosas e estrelas aleatórias."""
    surf = pygame.Surface((w, h))                            # Cria a superfície do tamanho da tela
    surf.fill(DARK_BG)                                       # Preenche tudo com cor roxa escura

    # ── Desenha 6 nebulosas roxas borradas em posições aleatórias ──
    for _ in range(6):
        cx = random.randint(0, w)                            # Posição X aleatória do centro da nebulosa
        cy = random.randint(0, h)                            # Posição Y aleatória do centro da nebulosa
        radius = random.randint(120, 320)                    # Raio aleatório (tamanho da nebulosa)
        color = (random.randint(40, 100), 0, random.randint(80, 180))  # Cor roxa aleatória
        # Desenha vários círculos concêntricos cada vez menores, com transparência decrescente (efeito de brilho)
        for r in range(radius, 0, -10):
            alpha_val = max(0, int(60 * (1 - r / radius)))   # Calcula transparência (mais opaco no centro)
            nebula = pygame.Surface((r*2, r*2), pygame.SRCALPHA)  # Cria superfície temporária para o círculo
            pygame.draw.ellipse(nebula, (*color, alpha_val), (0, 0, r*2, r*2))  # Desenha elipse colorida
            surf.blit(nebula, (cx - r, cy - r), special_flags=pygame.BLEND_RGBA_ADD)  # Mistura aditiva (brilho)

    # ── Desenha 300 estrelinhas em posições aleatórias ──
    for _ in range(300):
        x = random.randint(0, w)                             # Posição X aleatória da estrela
        y = random.randint(0, h)                             # Posição Y aleatória da estrela
        brightness = random.randint(120, 255)                # Brilho aleatório (cinza até branco)
        size = random.choice([1, 1, 1, 2, 2, 3])             # Tamanho aleatório (a maioria pequenas)
        color = (brightness, brightness, min(255, brightness + random.randint(0, 60)))  # Tom esbranquiçado/azulado
        if size == 1:
            surf.set_at((x, y), color)                       # Estrela de 1 pixel = só pinta o pixel
        else:
            pygame.draw.circle(surf, color, (x, y), size // 2)  # Estrelas maiores = círculo
    return surf                                              # Retorna a superfície de galáxia pronta

# ══════════════════════════════════════════════════════════════════════════════
# CLASSE BUTTON — botão clicável com efeito de hover (mouse passando por cima)
# ══════════════════════════════════════════════════════════════════════════════
class Button:
    def __init__(self, rect, text, font_obj=None, color=BTN_NORMAL, hover=BTN_HOVER):
        """Cria um botão com retângulo, texto, fonte e cores customizáveis."""
        self.rect  = pygame.Rect(rect)         # Retângulo que define posição e tamanho do botão
        self.text  = text                       # Texto que aparece dentro do botão
        self.font  = font_obj or F_MED          # Fonte do texto (usa F_MED se nenhuma for passada)
        self.color = color                      # Cor normal do botão
        self.hover = hover                      # Cor quando o mouse está em cima

    def draw(self, surf):
        """Desenha o botão na superfície surf."""
        mpos = pygame.mouse.get_pos()                                          # Pega a posição atual do mouse
        col = self.hover if self.rect.collidepoint(mpos) else self.color       # Escolhe cor (hover ou normal)
        pygame.draw.rect(surf, (20, 0, 40), self.rect.move(3, 3), border_radius=12)  # Sombra atrás do botão
        pygame.draw.rect(surf, col, self.rect, border_radius=12)               # Corpo principal do botão (arredondado)
        pygame.draw.rect(surf, LIGHT_PURPLE, self.rect, 2, border_radius=12)   # Borda roxa clara em volta
        lbl = self.font.render(self.text, True, WHITE)                         # Renderiza o texto em branco
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))                  # Centraliza texto dentro do botão

    def clicked(self, event):
        """Retorna True se este botão foi clicado (botão esquerdo do mouse)."""
        return (event.type == pygame.MOUSEBUTTONDOWN and    # Verifica se é um clique
                event.button == 1 and                        # Verifica se é o botão esquerdo
                self.rect.collidepoint(event.pos))           # Verifica se o clique caiu dentro do botão

# ══════════════════════════════════════════════════════════════════════════════
# CLASSE TWINKLESTAR — estrelinha que pisca no fundo (apenas quando não há imagem do universo)
# ══════════════════════════════════════════════════════════════════════════════
class TwinkleStar:
    def __init__(self):
        self.reset()                            # Ao criar, já inicializa propriedades aleatórias

    def reset(self):
        """Sorteia novas propriedades aleatórias para a estrela."""
        self.x     = random.randint(0, WIDTH)                              # Posição X aleatória
        self.y     = random.randint(0, HEIGHT)                             # Posição Y aleatória
        self.max_r = random.uniform(1.5, 3.5)                              # Raio máximo (tamanho do brilho)
        self.phase = random.uniform(0, math.pi * 2)                        # Fase inicial da animação (defasagem)
        self.speed = random.uniform(1.5, 4.0)                              # Velocidade de piscar
        self.color = random.choice([WHITE, CYAN, LIGHT_PURPLE, (255,255,180)])  # Cor aleatória

    def draw(self, surf, t):
        """Desenha a estrela com tamanho oscilando conforme o tempo t (efeito de piscar)."""
        r = self.max_r * (0.5 + 0.5 * math.sin(self.phase + t * self.speed))  # Raio varia com seno (oscila)
        if r > 0.5:                                                            # Só desenha se for visível
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), int(r))

# Cria uma lista com 80 estrelinhas para o fundo
TWINKLES = [TwinkleStar() for _ in range(80)]

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES PARA DESENHAR TÍTULOS, TEXTOS E PAINÉIS
# ══════════════════════════════════════════════════════════════════════════════
def draw_title(surf, text, y, color=GOLD):
    """Desenha um título grande com sombra roxa, centralizado horizontalmente."""
    shadow = F_TITLE.render(text, True, (80, 0, 120))                       # Renderiza versão da sombra (roxa)
    title  = F_TITLE.render(text, True, color)                               # Renderiza o título principal
    surf.blit(shadow, shadow.get_rect(centerx=WIDTH//2+3, y=y+3))            # Desloca sombra 3px para baixo/direita
    surf.blit(title,  title.get_rect(centerx=WIDTH//2, y=y))                 # Desenha o título por cima

def draw_text(surf, text, y, color=WHITE, font_obj=None):
    """Desenha um texto centralizado horizontalmente na posição Y."""
    f = font_obj or F_MED                          # Usa F_MED se nenhuma fonte for passada
    lbl = f.render(text, True, color)              # Renderiza o texto
    surf.blit(lbl, lbl.get_rect(centerx=WIDTH//2, y=y))  # Centraliza horizontalmente

def draw_panel(surf, rect, alpha=200):
    """Desenha um painel retangular semi-transparente roxo (caixa de fundo para textos)."""
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)      # Cria superfície com transparência
    panel.fill((20, 0, 50, alpha))                                           # Preenche com roxo + alpha (transparência)
    surf.blit(panel, rect.topleft)                                           # Desenha o painel na tela
    pygame.draw.rect(surf, LIGHT_PURPLE, rect, 2, border_radius=10)          # Borda roxa clara em volta

# ══════════════════════════════════════════════════════════════════════════════
# CARREGAMENTO DE TODOS OS ASSETS (IMAGENS E SONS)
# ══════════════════════════════════════════════════════════════════════════════
print("Loading assets...")
try:
    # ── Carrega sprite sheets dos personagens ──
    char_sheet    = load_sheet("Character Model.png")                       # Sprite sheet dos corpos
    hair_sheet    = load_sheet("Hairs.png")                                  # Sprite sheet dos cabelos
    outfit_sheets = [load_sheet(f"Outfit{i}.png") for i in range(1, 7)]      # Lista com as 6 sprite sheets de roupas

    # ── Tenta carregar a imagem do coração (vidas) ──
    # Procura por estes nomes em ordem; usa o primeiro que existir
    heart_path_options = [
        "Heart.png",
        "Pixel Heart Sprite Sheet 32x32.png",
        "Pixel Heart Sprite Sheet 16x16.png",
    ]
    heart_raw = None
    for hp in heart_path_options:
        full = os.path.join(ASSETS, hp)
        if os.path.exists(full):
            heart_raw = pygame.image.load(full).convert_alpha()              # Carrega a imagem do coração
            # Determina o tamanho de cada frame baseado no nome do arquivo
            heart_frame_size = 32 if "32x32" in hp else (16 if "16x16" in hp else heart_raw.get_height())
            heart_img = pygame.Surface((heart_frame_size, heart_frame_size), pygame.SRCALPHA)
            heart_img.blit(heart_raw, (0, 0), (0, 0, heart_frame_size, heart_frame_size))  # Pega só o 1º frame
            heart_img = pygame.transform.scale(heart_img, (38, 38))          # Redimensiona para 38x38 px
            break                                                            # Achou, para de procurar
    if heart_raw is None:                                                    # Se nenhuma imagem foi encontrada, erro
        raise Exception("Nenhuma imagem de coração encontrada em assets/")

    # ── Carrega a imagem da estrela (bônus de munição) ──
    star_path = os.path.join(ASSETS, "Estrela.png")
    if os.path.exists(star_path):
        raw_star = pygame.image.load(star_path).convert_alpha()
        star_img = pygame.transform.scale(raw_star, (44, 44))                # Redimensiona para 44x44 px
    else:
        star_img = None                                                       # Sem imagem = desenha círculo dourado
        print("Aviso: Estrela.png nao encontrado, usando desenho padrao")

    # ── Carrega a imagem da arma (cursor) ──
    new_gun_path = os.path.join(ASSETS, "New Piskel.png")
    if os.path.exists(new_gun_path):
        raw_gun = pygame.image.load(new_gun_path).convert_alpha()
        gun_w   = 90                                                          # Largura desejada da arma
        ratio   = gun_w / raw_gun.get_width()                                # Proporção para redimensionar
        gun_h   = max(1, int(raw_gun.get_height() * ratio))                  # Altura mantendo proporção
        gun_surf = pygame.transform.smoothscale(raw_gun, (gun_w, gun_h))     # Redimensiona com suavização
    else:
        gun_surf = extract_gun_from_sheet()                                  # Fallback: extrai do sheet maior
        if gun_surf is None:
            raise Exception("Gun extraction failed")
    print(f"Gun size: {gun_surf.get_size()}")                                # Imprime tamanho final da arma

    # ── Carrega a imagem de fundo do universo ──
    space_bg_path = os.path.join(ASSETS, "cenario universo.png")
    if os.path.exists(space_bg_path):
        raw_bg   = pygame.image.load(space_bg_path).convert()
        SPACE_BG = pygame.transform.smoothscale(raw_bg, (WIDTH, HEIGHT))     # Redimensiona pra preencher a tela
    else:
        SPACE_BG = None                                                       # Sem imagem = usa galáxia gerada

    # ── Função auxiliar para carregar arquivos de som da pasta assets ──
    def load_sound(name):
        path = os.path.join(ASSETS, name)
        if os.path.exists(path):
            return pygame.mixer.Sound(path)                                  # Carrega o som como objeto Sound
        print(f"Aviso: som '{name}' nao encontrado")
        return None                                                           # Retorna None se o arquivo não existir
    # ── Carrega os 4 efeitos sonoros do jogo ──
    SND_SHOOT   = load_sound("tiro.mp3")           # Som disparado a cada tiro normal
    SND_HIT     = load_sound("menos1vida.mp3")     # Som quando o alvo é atingido
    SND_WIN     = load_sound("ganhar jogo.mp3")    # Som tocado ao ganhar
    SND_LOSE    = load_sound("perder jogo.mp3")    # Som tocado ao perder
    if SND_SHOOT: SND_SHOOT.set_volume(0.4)         # Volume do tiro (mais baixo)

    # ── Carrega a música de fundo (toca em loop o jogo inteiro) ──
    musica_path = os.path.join(ASSETS, "musica de fundo.mp3")
    if os.path.exists(musica_path):
        pygame.mixer.music.load(musica_path)                                 # Carrega a música em memória
        pygame.mixer.music.set_volume(MUSIC_VOL_MENU)                        # Começa no volume médio
        pygame.mixer.music.play(loops=-1)                                    # Toca em loop infinito (-1)
    else:
        print("Aviso: 'musica de fundo.mp3' nao encontrada")

    if SND_HIT:   SND_HIT.set_volume(1.0)            # Volume máximo do som de hit
    if SND_WIN:   SND_WIN.set_volume(0.9)            # Volume alto da vitória
    if SND_LOSE:  SND_LOSE.set_volume(0.9)           # Volume alto da derrota

    # ── Configura canais dedicados de mixagem para cada tipo de som ──
    # Isso evita que um som "engula" o outro quando tocam ao mesmo tempo
    pygame.mixer.set_num_channels(16)                # Aumenta o número total de canais disponíveis
    CH_SHOOT = pygame.mixer.Channel(0)               # Canal exclusivo para o som de tiro
    CH_HIT   = pygame.mixer.Channel(1)               # Canal exclusivo para o som de hit
    CH_END   = pygame.mixer.Channel(2)               # Canal para sons de fim de jogo (win/lose)
except Exception as e:
    # Se qualquer asset falhar, mostra erro detalhado e fecha o jogo
    import traceback
    print(f"Asset load error: {e}")
    traceback.print_exc()
    input("Pressione Enter para fechar...")
    pygame.quit(); sys.exit()

# ══════════════════════════════════════════════════════════════════════════════
# OPÇÕES DE PERSONALIZAÇÃO DO PERSONAGEM
# ══════════════════════════════════════════════════════════════════════════════
# Cada opção indica em qual linha/coluna da sprite sheet está o sprite correspondente
# Linhas com pele clara: 0, 1, 2, 4 | Linhas com pele escura: 3, 5
BODY_OPTIONS = [
    {"name": "Menina Branca", "skin_row": 0, "skin_col": 1, "default_outfit": 0},
    {"name": "Menino Branco", "skin_row": 2, "skin_col": 1, "default_outfit": 3},
    {"name": "Menina Negra",  "skin_row": 3, "skin_col": 1, "default_outfit": 0},
    {"name": "Menino Negro",  "skin_row": 5, "skin_col": 1, "default_outfit": 3},
]

OUTFIT_OPTIONS = [
    {"name": "Vestido Branco", "sheet_idx": 0, "col": 1},   # sheet_idx = qual arquivo Outfit1-6.png
    {"name": "Vestido Rosa",   "sheet_idx": 1, "col": 1},
    {"name": "Saia Azul",      "sheet_idx": 2, "col": 1},
    {"name": "Camisa Laranja", "sheet_idx": 3, "col": 1},
    {"name": "Agasalho Verde", "sheet_idx": 4, "col": 1},
    {"name": "Calça Escura",   "sheet_idx": 5, "col": 1},
]
HAIR_OPTIONS = [
    {"name": "Longo Loiro",  "row": 4, "col": 1},          # row/col = posição na sprite sheet Hairs.png
    {"name": "Longo Moreno", "row": 0, "col": 1},
    {"name": "Curto Loiro",  "row": 5, "col": 1},
    {"name": "Curto Moreno", "row": 7, "col": 1},
]

def compose_character(body_idx, outfit_idx, hair_idx, scale=4):
    """Monta um personagem completo sobrepondo corpo + roupa + cabelo, escalado.
    scale = 4 significa que o resultado é 4x maior que o sprite original (32x32 → 128x128)."""
    s      = 32                                              # Tamanho original do sprite
    result = pygame.Surface((s, s), pygame.SRCALPHA)         # Cria superfície transparente vazia
    body   = BODY_OPTIONS[body_idx]                          # Pega config do corpo escolhido
    outfit = OUTFIT_OPTIONS[outfit_idx]                      # Pega config da roupa escolhida
    hair   = HAIR_OPTIONS[hair_idx]                          # Pega config do cabelo escolhido
    # Empilha em ordem: corpo (base) → roupa (por cima) → cabelo (no topo)
    result.blit(extract_frame(char_sheet,                          body["skin_col"],    body["skin_row"]), (0, 0))
    result.blit(extract_frame(outfit_sheets[outfit["sheet_idx"]], outfit["col"],        0),               (0, 0))
    result.blit(extract_frame(hair_sheet,                          hair["col"],          hair["row"]),     (0, 0))
    return pygame.transform.scale(result, (s * scale, s * scale))  # Aumenta o tamanho final

def get_preview_surf(body_idx, outfit_idx, hair_idx):
    """Versão maior do personagem (scale=5) usada nas telas de pré-visualização."""
    return compose_character(body_idx, outfit_idx, hair_idx, scale=5)

# ══════════════════════════════════════════════════════════════════════════════
# GERA O FUNDO DE GALÁXIA (usado caso a imagem do universo não exista)
# ══════════════════════════════════════════════════════════════════════════════
random.seed(42)                              # Define semente fixa para que o fundo seja sempre igual
GALAXY_BG = create_galaxy_bg(WIDTH, HEIGHT)  # Gera o fundo galáctico
random.seed()                                # Volta a aleatoriedade ao normal (sem semente fixa)

# ══════════════════════════════════════════════════════════════════════════════
# VARIÁVEIS GLOBAIS QUE GUARDAM O ESTADO ATUAL DO JOGO
# ══════════════════════════════════════════════════════════════════════════════
state              = ST_MENU      # Estado/tela atual (começa no menu)
target_name        = ""           # Nome do alvo digitado pelo usuário
body_sel           = 0            # Índice do corpo escolhido (0 a 3)
outfit_sel         = 0            # Índice da roupa escolhida (0 a 5)
hair_sel           = 0            # Índice do cabelo escolhido (0 a 3)
input_text         = ""           # Texto sendo digitado no campo de nome
t                  = 0.0          # Tempo total acumulado (usado em animações)
input_cursor_timer = 0            # Contador para animar o cursor "|" piscando

# ══════════════════════════════════════════════════════════════════════════════
# CLASSE GAMESTATE — guarda todas as informações da partida em andamento
# ══════════════════════════════════════════════════════════════════════════════
class GameState:
    def __init__(self):
        self.reset()                                # Inicializa todos os atributos chamando reset()

    def reset(self):
        """Reinicializa todos os atributos para uma nova partida."""
        self.target_lives  = 3                       # Vidas do alvo (3 corações)
        self.ammo          = 10                      # Munição atual
        self.max_ammo      = 10                      # Munição máxima
        self.tx            = WIDTH  // 2             # Posição X do alvo (começa no centro)
        self.ty            = HEIGHT // 2             # Posição Y do alvo (começa no centro)
        self.tvx           = 3.6                     # Velocidade horizontal do alvo
        self.tvy           = 3.1                     # Velocidade vertical do alvo
        self.speed_mult    = 1.0                     # Multiplicador de velocidade (aumenta a cada tiro)
        self.target_char   = None                    # Surface do personagem-alvo (definido em start_game)
        self.hit_flash     = 0                       # Contador do flash vermelho ao acertar
        self.miss_flash    = 0                       # Contador do flash azul ao errar
        self.shot_effects  = []                      # Lista de efeitos visuais de tiros [x,y,vida,vida_max,cor]
        self.stars         = []                      # Lista de estrelas ativas na tela
        self.star_timer    = 0                       # Contador para spawn de novas estrelas
        self.star_bonus    = 3                       # Quantos tiros uma estrela dá quando acertada
        self.game_over     = False                   # Flag de fim de jogo (não usado, mas mantido)
        self.shots_fired   = 0                       # Total de tiros disparados (mostrado na tela de derrota)
        self.dodge_timer   = 0                       # Contador pra mudar direção do alvo aleatoriamente

GS = GameState()                                     # Cria a instância global do estado do jogo

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO QUE PREPARA UMA NOVA PARTIDA
# ══════════════════════════════════════════════════════════════════════════════
def start_game():
    """Configura tudo para começar uma nova partida (chamada ao apertar 'Começar')."""
    GS.reset()                                                                  # Zera os dados da partida anterior
    GS.target_char = compose_character(body_sel, outfit_sel, hair_sel, scale=4) # Monta o personagem-alvo
    GS.tx  = random.randint(200, WIDTH  - 200)                                  # Posição X inicial aleatória
    GS.ty  = random.randint(150, HEIGHT - 150)                                  # Posição Y inicial aleatória
    angle  = random.uniform(0, math.pi * 2)                                     # Direção inicial aleatória (0 a 360°)
    speed  = 4.1                                                                # Velocidade inicial
    GS.tvx = math.cos(angle) * speed                                            # Componente X da velocidade
    GS.tvy = math.sin(angle) * speed                                            # Componente Y da velocidade

# ══════════════════════════════════════════════════════════════════════════════
# MOVIMENTAÇÃO DO ALVO — chamada a cada quadro durante o jogo
# ══════════════════════════════════════════════════════════════════════════════
def move_target():
    """Move o alvo pela tela com desvios aleatórios periódicos e ricochete nas bordas."""
    # ── Desvio aleatório periódico (alvo muda direção sozinho de vez em quando) ──
    GS.dodge_timer += 1
    if GS.dodge_timer > random.randint(40, 90):                  # A cada ~40-90 frames muda de direção
        GS.dodge_timer = 0                                        # Reseta o contador
        angle = random.uniform(0, math.pi * 2)                    # Nova direção aleatória
        cur_speed = math.hypot(GS.tvx, GS.tvy)                    # Mantém a velocidade atual (módulo do vetor)
        GS.tvx = math.cos(angle) * cur_speed                      # Aplica nova direção X
        GS.tvy = math.sin(angle) * cur_speed                      # Aplica nova direção Y

    # ── Atualiza a posição multiplicando velocidade pelo multiplicador de speed ──
    GS.tx += GS.tvx * GS.speed_mult
    GS.ty += GS.tvy * GS.speed_mult

    # ── Ricochete nas paredes ──
    char_w = GS.target_char.get_width()                           # Largura do sprite do alvo
    char_h = GS.target_char.get_height()                          # Altura do sprite do alvo
    margin = 40                                                    # Margem de borda para não colar na parede
    # Bate na parede esquerda → inverte X positivo
    if GS.tx < margin:                   GS.tx = margin;                   GS.tvx =  abs(GS.tvx)
    # Bate na parede direita → inverte X negativo
    if GS.tx > WIDTH  - char_w - margin: GS.tx = WIDTH - char_w - margin;  GS.tvx = -abs(GS.tvx)
    # Bate no topo → inverte Y positivo (margin+40 para não bater no HUD)
    if GS.ty < margin + 40:              GS.ty = margin + 40;              GS.tvy =  abs(GS.tvy)
    # Bate no chão → inverte Y negativo
    if GS.ty > HEIGHT - char_h - margin: GS.ty = HEIGHT - char_h - margin; GS.tvy = -abs(GS.tvy)

# ══════════════════════════════════════════════════════════════════════════════
# ATUALIZAÇÃO DAS ESTRELAS — gerencia o aparecimento e tempo de vida das estrelas bônus
# ══════════════════════════════════════════════════════════════════════════════
def update_stars():
    """Spawn periódico de novas estrelas e decremento da vida das existentes."""
    GS.star_timer += 1
    if GS.star_timer > random.randint(180, 320):                  # A cada ~3-5 segundos (180-320 frames)
        GS.star_timer = 0                                          # Reseta o contador
        if len(GS.stars) < 2:                                      # Máximo de 2 estrelas simultâneas
            # Spawna em posição aleatória; vida e vida_max iguais a 180 (3 segundos a 60fps)
            GS.stars.append([random.randint(60, WIDTH-60), random.randint(80, HEIGHT-80), 180, 180])
    # Decrementa a vida de cada estrela; remove as que zeraram (l <= 1)
    GS.stars = [[x, y, l-1, ml] for x, y, l, ml in GS.stars if l > 1]

# ══════════════════════════════════════════════════════════════════════════════
# DISPARO — chamada toda vez que o usuário clica com o mouse durante o jogo
# ══════════════════════════════════════════════════════════════════════════════
def shoot(mx, my):
    """Processa um tiro nas coordenadas (mx, my). Trata acerto de estrela, alvo ou erro."""
    global state                                                  # Vamos modificar a variável global 'state'
    if GS.ammo <= 0:                                              # Sem munição = não atira
        return
    GS.ammo -= 1                                                  # Gasta uma munição
    GS.shots_fired += 1                                           # Conta este tiro no total

    # A cada tiro o alvo acelera (fica mais difícil)
    GS.speed_mult += 0.25

    # ── Verifica se o tiro acertou alguma estrela bônus ──
    for star in GS.stars[:]:                                      # Itera uma cópia (pra poder remover durante)
        sx, sy, l, ml = star                                      # Desempacota (posição, vida atual, vida max)
        if math.hypot(mx - sx, my - sy) < 28:                     # Distância do clique até a estrela < 28px
            if SND_SHOOT: CH_SHOOT.play(SND_SHOOT)                # Toca som de tiro
            GS.ammo = min(GS.ammo + GS.star_bonus, GS.max_ammo)   # Ganha bônus (limitado ao máximo)
            GS.stars.remove(star)                                  # Remove a estrela acertada
            GS.shot_effects.append([sx, sy, 30, 30, GOLD])        # Adiciona efeito visual dourado
            return                                                 # Sai da função (não verifica mais nada)

    # ── Verifica se o tiro acertou o alvo (personagem) ──
    char_w = GS.target_char.get_width()
    char_h = GS.target_char.get_height()
    if pygame.Rect(GS.tx, GS.ty, char_w, char_h).collidepoint(mx, my):  # Clique caiu dentro do retângulo do alvo
        GS.target_lives -= 1                                       # Tira uma vida
        GS.hit_flash = 20                                          # Inicia flash vermelho na tela (20 frames)
        GS.shot_effects.append([mx, my, 25, 25, RED])              # Efeito visual vermelho no ponto do clique
        GS.speed_mult += 0.35                                      # Acelera mais ainda
        if GS.target_lives <= 0:                                   # Se acabou as vidas → vitória
            if SND_WIN: CH_END.play(SND_WIN)                       # Toca som de vitória
            state = ST_WIN                                          # Muda para tela de vitória
        else:                                                       # Ainda tem vidas → só perdeu uma
            if SND_HIT: CH_HIT.play(SND_HIT)                       # Toca som de hit (menos1vida)
    else:                                                           # Não acertou nada → tiro perdido
        if SND_SHOOT: CH_SHOOT.play(SND_SHOOT)                     # Toca som de tiro normal
        GS.miss_flash = 8                                          # Flash azul rápido (8 frames)
        GS.shot_effects.append([mx, my, 15, 15, CYAN])             # Efeito visual ciano

    # ── Verifica se acabou a munição sem matar o alvo → derrota ──
    if GS.ammo <= 0 and GS.target_lives > 0:
        if SND_LOSE: CH_END.play(SND_LOSE)                         # Toca som de derrota
        state = ST_LOSE                                             # Muda para tela de derrota

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE DESENHO (BACKGROUND, MIRA, HUD)
# ══════════════════════════════════════════════════════════════════════════════
def draw_bg(surf, t_val):
    """Desenha o fundo do jogo (universo ou galáxia gerada com estrelas piscando)."""
    if SPACE_BG is not None:                                      # Se tem a imagem do universo, usa ela
        surf.blit(SPACE_BG, (0, 0))
        return
    surf.blit(GALAXY_BG, (0, 0))                                  # Senão usa o fundo gerado
    for star in TWINKLES:                                          # E desenha as 80 estrelinhas piscando
        star.draw(surf, t_val)

def draw_gun_cursor(surf, mx, my):
    """Desenha a imagem da arma no lugar do cursor do mouse."""
    if gun_surf is None:                                          # Se não tem imagem, desenha um círculo
        pygame.draw.circle(surf, CYAN, (mx, my), 8, 2)
        return
    gun_w, gun_h = gun_surf.get_size()                            # Pega tamanho da arma
    draw_x = max(0, mx - gun_w + 8)                               # Posiciona arma com cano apontando pra mira
    draw_y = my - gun_h // 2                                       # Centraliza verticalmente
    surf.blit(gun_surf, (draw_x, draw_y))                         # Desenha a arma
    pygame.draw.circle(surf, CYAN, (mx, my), 4, 1)                # Ponto de mira ciano no cursor

def draw_ammo_bar(surf):
    """Desenha a barra inferior com os ícones de munição (cheios e gastos)."""
    bar_h = 60                                                    # Altura da barra
    bar_y = HEIGHT - bar_h                                         # Posição Y (no rodapé)
    bar_surf = pygame.Surface((WIDTH, bar_h), pygame.SRCALPHA)    # Cria superfície semi-transparente
    bar_surf.fill((10, 0, 30, 210))                                # Fundo roxo escuro semi-transparente
    surf.blit(bar_surf, (0, bar_y))
    pygame.draw.line(surf, LIGHT_PURPLE, (0, bar_y), (WIDTH, bar_y), 1)  # Linha roxa separando do jogo

    # ── Calcula um ícone menor da arma para usar como representação de cada munição ──
    gun_w, gun_h = gun_surf.get_size()
    icon_scale = min(1.0, (bar_h - 14) / max(1, gun_h))           # Calcula escala pra caber na barra
    icon_w = max(1, int(gun_w * icon_scale))
    icon_h = max(1, int(gun_h * icon_scale))
    icon   = pygame.transform.smoothscale(gun_surf, (icon_w, icon_h))  # Cria a versão pequena

    spacing = icon_w + 8                                          # Espaço entre cada ícone
    start_x = (WIDTH - GS.max_ammo * spacing) // 2                # Centraliza horizontalmente o conjunto
    icon_y  = bar_y + (bar_h - icon_h) // 2                       # Centraliza verticalmente na barra

    # ── Desenha 10 slots: ícone se munição disponível, X vermelho se gasta ──
    for i in range(GS.max_ammo):
        x = start_x + i * spacing
        if i < GS.ammo:                                            # Munição ainda disponível
            surf.blit(icon, (x, icon_y))                          # Desenha ícone da arma
        else:                                                      # Munição já gasta
            cx = x + icon_w // 2                                  # Centro do slot
            cy = icon_y + icon_h // 2
            r  = max(4, icon_h // 2 - 2)
            pygame.draw.line(surf, RED, (cx-r, cy-r), (cx+r, cy+r), 2)  # Linha diagonal do X
            pygame.draw.line(surf, RED, (cx+r, cy-r), (cx-r, cy+r), 2)  # Outra diagonal (forma X)

# ══════════════════════════════════════════════════════════════════════════════
# RENDERIZADORES DE TELA — cada função desenha uma tela específica do jogo
# ══════════════════════════════════════════════════════════════════════════════

def render_menu(events):
    """Tela inicial com 'Jogar' e 'Instruções'."""
    global state
    draw_bg(screen, t)                                            # Fundo
    draw_title(screen, "TODO MUNDO ODEIA", 80)                    # Título grande no topo
    draw_title(screen, "...", 138, LIGHT_PURPLE)                  # Continuação do título em roxo
    btn_play = Button((WIDTH//2 - 120, 290, 240, 60), "Jogar", F_BIG)                                # Botão principal
    btn_info = Button((WIDTH//2 - 120, 370, 240, 60), "Instruções", F_MED, BTN_NORMAL, DIM_PURPLE)   # Botão secundário
    btn_play.draw(screen)
    btn_info.draw(screen)
    # Processa eventos: cliques nos botões mudam o estado/tela
    for ev in events:
        if btn_play.clicked(ev): state = ST_NAME                  # Vai pra tela de digitar nome
        if btn_info.clicked(ev): state = ST_INSTRUCT              # Vai pras instruções


def render_instructions(events):
    """Tela mostrando as regras do jogo."""
    global state
    draw_bg(screen, t)                                            # Fundo
    draw_panel(screen, pygame.Rect(60, 60, WIDTH-120, HEIGHT-120), alpha=230)  # Painel roxo de fundo
    draw_title(screen, "Instruções", 80)                           # Título
    # ── Lista das linhas de texto: (texto, cor, fonte) ──
    lines = [
        ("Objetivo:", GOLD, F_MED),
        ("Mate o alvo antes que suas munições acabem!", WHITE, F_SMALL),
        ("", WHITE, F_SMALL),
        ("Mire com o mouse e clique para atirar.", CYAN, F_SMALL),
        ("O alvo possui 3 vidas representadas por corações.", LIGHT_PURPLE, F_SMALL),
        ("A cada tiro o alvo fica mais rápido!", RED, F_SMALL),
        ("Você começa com 10 munições.", WHITE, F_SMALL),
        ("Estrelas aparecem às vezes — acerte para ganhar mais munições!", GOLD, F_SMALL),
        ("", WHITE, F_SMALL),
        ("Boa sorte... você vai precisar!", PINK, F_MED),
    ]
    y = 175                                                       # Posição Y inicial das linhas
    for text, color, fnt in lines:                                # Desenha cada linha empilhada verticalmente
        lbl = fnt.render(text, True, color)
        screen.blit(lbl, (90, y))
        y += fnt.size(text)[1] + 4                                # Avança Y de acordo com a altura da fonte
    btn_back = Button((WIDTH//2 - 100, HEIGHT-100, 200, 50), "Voltar")
    btn_back.draw(screen)
    for ev in events:
        if btn_back.clicked(ev): state = ST_MENU                  # Botão Voltar leva ao menu


def render_name_input(events):
    """Tela onde o usuário digita o nome do alvo."""
    global state, input_text, target_name, input_cursor_timer
    draw_bg(screen, t)
    draw_title(screen, "Todo mundo odeia...", 80)
    draw_panel(screen, pygame.Rect(100, 180, WIDTH-200, 220))
    draw_text(screen, "Qual é o nome do alvo?", 200, LIGHT_PURPLE, F_MED)
    # ── Caixa de input ──
    field_rect = pygame.Rect(WIDTH//2 - 220, 255, 440, 55)
    pygame.draw.rect(screen, (30, 0, 60), field_rect, border_radius=8)              # Fundo da caixa
    pygame.draw.rect(screen, LIGHT_PURPLE, field_rect, 2, border_radius=8)          # Borda roxa
    # ── Cursor "|" piscando ──
    input_cursor_timer += 1
    cursor_char = "|" if (input_cursor_timer // 30) % 2 == 0 else ""                # Pisca a cada 30 frames
    lbl = F_INPUT.render(input_text + cursor_char, True, WHITE)                     # Renderiza texto + cursor
    screen.blit(lbl, (field_rect.x + 15, field_rect.y + 10))
    # ── Dica abaixo, se ainda não digitou nada ──
    if not input_text:
        hint = F_SMALL.render("Digite o nome e pressione Enter", True, (150, 100, 200))
        screen.blit(hint, hint.get_rect(centerx=WIDTH//2, y=330))
    # ── Processa teclado ──
    for ev in events:
        if ev.type == pygame.KEYDOWN:                                                # Tecla pressionada
            if ev.key == pygame.K_RETURN and input_text.strip():                    # Enter (com texto não vazio)
                target_name = input_text.strip(); state = ST_BODY                   # Confirma e vai pra próxima
            elif ev.key == pygame.K_BACKSPACE:                                       # Backspace
                input_text = input_text[:-1]                                         # Remove último caractere
            elif len(input_text) < 24 and ev.unicode.isprintable():                  # Outra tecla imprimível
                input_text += ev.unicode                                             # Adiciona ao texto (até 24 chars)


def render_selection(events, title, options, current_sel, images, next_state, prev_state):
    """Tela genérica de seleção (usada para corpo, roupa e cabelo).
    Mostra uma grade de imagens; usuário clica em uma e avança."""
    global body_sel, outfit_sel, hair_sel
    draw_bg(screen, t)
    draw_title(screen, title, 30)                                                    # Título da seleção
    # ── Calcula layout da grade (4 colunas, células de 160x180) ──
    cols    = min(4, len(options))
    cell_w, cell_h = 160, 180
    start_x = (WIDTH - (cols * cell_w + (cols-1) * 20)) // 2                         # Centraliza horizontalmente
    boxes = []                                                                       # Lista de retângulos pra detectar clique
    for i, img in enumerate(images):
        x = start_x + (i % cols) * (cell_w + 20)                                     # Posição X conforme coluna
        y = 120     + (i // cols) * (cell_h + 10)                                    # Posição Y conforme linha
        box = pygame.Rect(x, y, cell_w, cell_h)                                      # Retângulo da célula
        boxes.append(box)
        is_sel = (i == current_sel)                                                  # Esta opção está selecionada?
        # Cor de fundo diferente se for a seleção atual
        pygame.draw.rect(screen, (60,0,120) if is_sel else (20,0,50), box, border_radius=10)
        # Borda dourada se selecionado, roxa se não
        pygame.draw.rect(screen, GOLD if is_sel else LIGHT_PURPLE, box, 3, border_radius=10)
        iw, ih = img.get_size()
        screen.blit(img, (x + (cell_w-iw)//2, y + (cell_h-ih)//2))                   # Centraliza imagem na célula
    btn_next = Button((WIDTH-200, HEIGHT-70, 180, 50), "Próximo", F_MED)
    btn_back = Button((20, HEIGHT-70, 150, 50), "Voltar", F_MED)
    btn_next.draw(screen); btn_back.draw(screen)
    # ── Processa cliques ──
    for ev in events:
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:                     # Clique esquerdo
            for i, box in enumerate(boxes):
                if box.collidepoint(ev.pos):                                          # Clicou em alguma célula
                    # Atualiza a variável global correspondente baseado em qual seleção é
                    if next_state == ST_OUTFIT:
                        global body_sel;   body_sel   = i
                    elif next_state == ST_HAIR:
                        global outfit_sel; outfit_sel = i
                    elif next_state == ST_PREVIEW:
                        global hair_sel;   hair_sel   = i
        if btn_next.clicked(ev):
            global state; state = next_state                                          # Avança para próxima tela
        if btn_back.clicked(ev):
            state = prev_state                                                        # Volta para tela anterior


def render_preview(events):
    """Tela de pré-visualização do personagem antes de começar a partida."""
    global state
    draw_bg(screen, t)
    draw_panel(screen, pygame.Rect(50, 50, WIDTH-100, HEIGHT-100))                   # Painel de fundo
    draw_title(screen, "Seu personagem", 70)
    char_surf = get_preview_surf(body_sel, outfit_sel, hair_sel)                     # Monta personagem em tamanho grande
    cw, ch = char_surf.get_size()
    cx, cy = WIDTH//2 - cw//2, HEIGHT//2 - ch//2 + 20                                # Centraliza na tela
    screen.blit(char_surf, (cx, cy))
    draw_text(screen, f"Nome: {target_name}", cy+ch+20, GOLD, F_MED)                 # Mostra o nome embaixo
    btn_start = Button((WIDTH//2-130, HEIGHT-90, 260, 60), "Começar o jogo!", F_BIG)
    btn_back  = Button((20, HEIGHT-70, 150, 50), "Voltar", F_MED)
    btn_start.draw(screen); btn_back.draw(screen)
    for ev in events:
        if btn_start.clicked(ev): start_game(); state = ST_GAME                      # Começa a partida
        if btn_back.clicked(ev):  state = ST_HAIR                                    # Volta pra escolher cabelo


def render_game(events):
    """Renderiza a tela do jogo em si (gameplay completo)."""
    global state
    draw_bg(screen, t)                                                                # Fundo do universo
    move_target()                                                                      # Move o alvo
    update_stars()                                                                     # Atualiza estrelas bônus

    # ── Flash vermelho na tela quando acerta o alvo ──
    if GS.hit_flash > 0:
        flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        flash.fill((255, 0, 0, int(80 * GS.hit_flash / 20)))                          # Vermelho com alpha decrescente
        screen.blit(flash, (0, 0))
        GS.hit_flash -= 1                                                              # Decrementa contador

    # ── Flash azul rápido quando erra o tiro ──
    if GS.miss_flash > 0:
        flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        flash.fill((0, 100, 200, int(40 * GS.miss_flash / 8)))                        # Azul com alpha decrescente
        screen.blit(flash, (0, 0))
        GS.miss_flash -= 1

    # ── Desenha cada estrela bônus ativa ──
    for sx, sy, life, max_life in GS.stars:
        ratio = life / max_life                                                        # Fração de vida (1.0 → 0.0)
        pulse = 0.85 + 0.15 * math.sin(t * 5)                                          # Efeito de pulsação (0.7 a 1.0)
        if star_img is not None:
            # Tem imagem da estrela: redimensiona e ajusta transparência
            base_w, base_h = star_img.get_size()
            sw = max(1, int(base_w * pulse))
            sh = max(1, int(base_h * pulse))
            star_scaled = pygame.transform.scale(star_img, (sw, sh))
            star_scaled.set_alpha(int(255 * ratio))                                    # Alpha diminui com a vida
            screen.blit(star_scaled, star_scaled.get_rect(center=(sx, sy)))
        else:
            # Sem imagem: desenha círculo dourado
            star_r = int(22 * pulse)
            sh = star_r * 2
            ss = pygame.Surface((star_r*2+4, star_r*2+4), pygame.SRCALPHA)
            pygame.draw.circle(ss, (*GOLD, int(200*ratio)), (star_r+2, star_r+2), star_r)
            screen.blit(ss, (sx-star_r-2, sy-star_r-2))
        # Mostra "+3" embaixo da estrela
        bonus_lbl = F_TINY.render(f"+{GS.star_bonus}", True, WHITE)
        screen.blit(bonus_lbl, bonus_lbl.get_rect(centerx=sx, y=sy + sh//2 + 2))

    # ── Atualiza e desenha os efeitos visuais dos tiros ──
    GS.shot_effects = [[x, y, l-1, ml, c] for x, y, l, ml, c in GS.shot_effects if l > 0]  # Decrementa vida
    for sx, sy, life, max_life, color in GS.shot_effects:
        ratio = life / max_life                                                        # Quanto resta de vida
        r = int(30 * (1 - ratio))                                                      # Raio cresce com o tempo (expande)
        es = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
        pygame.draw.circle(es, (*color, int(220*ratio)), (r+1, r+1), max(1, r))        # Círculo da explosão
        screen.blit(es, (sx-r-1, sy-r-1))

    # ── Desenha o nome do alvo acima dele e o sprite do alvo ──
    name_lbl = F_SMALL.render(target_name, True, RED)
    tw = GS.target_char.get_width()
    screen.blit(name_lbl, name_lbl.get_rect(centerx=GS.tx+tw//2, y=GS.ty-28))         # Nome 28px acima do alvo
    screen.blit(GS.target_char, (int(GS.tx), int(GS.ty)))                              # Sprite do alvo

    # ── HUD superior (vidas, velocidade, contador de tiros) ──
    hud = pygame.Surface((WIDTH, 50), pygame.SRCALPHA)
    hud.fill((10, 0, 30, 200))                                                         # Faixa roxa semi-transparente
    screen.blit(hud, (0, 0))
    pygame.draw.line(screen, LIGHT_PURPLE, (0, 50), (WIDTH, 50), 1)                    # Linha separadora
    # Desenha um coração para cada vida restante (do canto direito pra esquerda)
    for i in range(max(0, GS.target_lives)):
        screen.blit(heart_img, (WIDTH-50-i*46, 5))
    # Mostra velocidade atual no centro
    spd_lbl = F_TINY.render(f"Velocidade: x{GS.speed_mult:.1f}", True, LIGHT_PURPLE)
    screen.blit(spd_lbl, spd_lbl.get_rect(centerx=WIDTH//2, y=16))
    # Mostra contador de munição no canto esquerdo
    screen.blit(F_TINY.render(f"Tiros: {GS.ammo}/{GS.max_ammo}", True, CYAN), (16, 16))

    # ── Barra inferior com ícones de munição ──
    draw_ammo_bar(screen)

    # ── Captura posição do mouse e processa tiros ──
    mx, my = pygame.mouse.get_pos()                                                    # Posição atual do mouse
    for ev in events:
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:                       # Clique esquerdo
            shoot(mx, my)                                                              # Dispara!
    draw_gun_cursor(screen, mx, my)                                                    # Desenha a arma como cursor


def render_win(events):
    """Tela de vitória — confete colorido girando e o personagem riscado."""
    global state
    draw_bg(screen, t)
    # ── Desenha 12 confetes que giram em círculo ──
    for i in range(12):
        angle = t * 1.5 + i * (math.pi * 2 / 12)                                       # Ângulo de cada confete
        r  = 180 + 30 * math.sin(t * 2 + i)                                            # Raio oscilante
        cx = WIDTH//2  + int(r * math.cos(angle))                                      # Posição X conforme ângulo
        cy = HEIGHT//2 + int(r * 0.5 * math.sin(angle))                                # Posição Y (achatada na vertical)
        pygame.draw.circle(screen, [GOLD,CYAN,PINK,GREEN,LIGHT_PURPLE][i%5], (cx,cy), 5)  # Cor rotativa
    draw_panel(screen, pygame.Rect(80, 100, WIDTH-160, HEIGHT-200), alpha=220)         # Painel central
    draw_title(screen, "PARABÉNS!", 130, GOLD)                                          # Título dourado
    line1 = F_BIG.render(f"Você matou {target_name}!", True, WHITE)                    # Mensagem com nome do alvo
    screen.blit(line1, line1.get_rect(centerx=WIDTH//2, y=220))
    # ── Desenha o personagem com X vermelho por cima (morto) ──
    char_surf = get_preview_surf(body_sel, outfit_sel, hair_sel)
    char_copy = char_surf.copy()                                                       # Cópia pra não estragar original
    cw, ch = char_copy.get_size()
    pygame.draw.line(char_copy, RED, (0,0), (cw,ch), 8)                                # Diagonal de canto a canto
    pygame.draw.line(char_copy, RED, (cw,0), (0,ch), 8)                                # Outra diagonal (X)
    screen.blit(char_copy, (WIDTH//2-cw//2, 290))                                      # Centraliza horizontalmente
    btn_menu = Button((WIDTH//2-150, HEIGHT-110, 300, 60), "Menu Principal", F_MED)
    btn_menu.draw(screen)
    for ev in events:
        if btn_menu.clicked(ev): state = ST_MENU                                       # Volta ao menu


def render_lose(events):
    """Tela de derrota — mensagem e botões pra tentar de novo ou voltar."""
    global state, input_text
    draw_bg(screen, t)
    draw_panel(screen, pygame.Rect(80, 100, WIDTH-160, HEIGHT-200), alpha=220)
    draw_title(screen, "FIM DE JOGO", 120, RED)
    l1 = F_BIG.render(f"{target_name} venceu!", True, PINK)                            # Diz que o alvo venceu
    screen.blit(l1, l1.get_rect(centerx=WIDTH//2, y=210))
    l2 = F_MED.render("você falhou...", True, (200,100,100))
    screen.blit(l2, l2.get_rect(centerx=WIDTH//2, y=260))
    # ── Estatísticas finais ──
    for i, s in enumerate([f"Vidas restantes do alvo: {GS.target_lives}",
                            f"Tiros disparados: {GS.shots_fired}"]):
        lbl = F_SMALL.render(s, True, LIGHT_PURPLE)
        screen.blit(lbl, lbl.get_rect(centerx=WIDTH//2, y=320+i*32))
    btn_retry = Button((WIDTH//2-160, HEIGHT-120, 320, 55), "Tente novamente", F_MED)
    btn_menu  = Button((WIDTH//2-120, HEIGHT- 52, 240, 44), "Menu Principal", F_SMALL)
    btn_retry.draw(screen); btn_menu.draw(screen)
    for ev in events:
        if btn_retry.clicked(ev): start_game(); state = ST_GAME                        # Reinicia partida
        if btn_menu.clicked(ev):  input_text = ""; state = ST_MENU                     # Volta ao menu e limpa o nome

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES PARA GERAR AS IMAGENS DAS OPÇÕES (mostradas nas telas de seleção)
# ══════════════════════════════════════════════════════════════════════════════
def make_body_images():
    """Cria as 4 thumbnails dos tipos de corpo (110x110)."""
    imgs = []
    for b in BODY_OPTIONS:
        s = pygame.Surface((32, 32), pygame.SRCALPHA)
        s.blit(extract_frame(char_sheet, b["skin_col"], b["skin_row"]), (0,0))         # Pega frame do sprite sheet
        imgs.append(pygame.transform.scale(s, (110, 110)))                              # Amplia pra preview
    return imgs

def make_outfit_images():
    """Cria as 6 thumbnails das roupas (100x100)."""
    imgs = []
    for o in OUTFIT_OPTIONS:
        s = pygame.Surface((32, 32), pygame.SRCALPHA)
        s.blit(extract_frame(outfit_sheets[o["sheet_idx"]], o["col"], 0), (0,0))
        imgs.append(pygame.transform.scale(s, (100, 100)))
    return imgs

def make_hair_images():
    """Cria as 4 thumbnails dos cabelos (100x100)."""
    imgs = []
    for h in HAIR_OPTIONS:
        s = pygame.Surface((32, 32), pygame.SRCALPHA)
        s.blit(extract_frame(hair_sheet, h["col"], h["row"]), (0,0))
        imgs.append(pygame.transform.scale(s, (100, 100)))
    return imgs

# Gera todas as imagens das opções uma única vez (na inicialização)
print("Building selection images...")
BODY_IMGS   = make_body_images()
OUTFIT_IMGS = make_outfit_images()
HAIR_IMGS   = make_hair_images()
print("Done. Starting game loop.")

# ══════════════════════════════════════════════════════════════════════════════
# LOOP PRINCIPAL DO JOGO — roda a 60 FPS enquanto o jogo estiver aberto
# ══════════════════════════════════════════════════════════════════════════════
def main():
    global t, state, body_sel, outfit_sel, hair_sel

    while True:                                                                        # Loop infinito (sai com sys.exit)
        events = []                                                                    # Lista para acumular eventos do frame

        # ── Ajusta o volume da música conforme a tela atual ──
        target_vol = MUSIC_VOL_GAME if state == ST_GAME else MUSIC_VOL_MENU            # Baixo no jogo, médio no resto
        if pygame.mixer.music.get_volume() != target_vol:                              # Só altera se for diferente
            pygame.mixer.music.set_volume(target_vol)

        # ── Processa todos os eventos pendentes (teclado, mouse, fechar janela) ──
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:                                                 # Usuário fechou a janela
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:                # Tecla ESC pressionada
                if state == ST_GAME: state = ST_MENU                                   # No jogo: volta ao menu
                else: pygame.quit(); sys.exit()                                        # Em qualquer outra tela: fecha
            events.append(ev)                                                          # Guarda o evento pra repassar

        t += 1 / FPS                                                                   # Incrementa tempo (em segundos)
        pygame.mouse.set_visible(state != ST_GAME)                                     # Mouse some no jogo (vira arma)

        # ── Chama o renderizador da tela atual ──
        if   state == ST_MENU:     render_menu(events)
        elif state == ST_INSTRUCT: render_instructions(events)
        elif state == ST_NAME:     render_name_input(events)
        elif state == ST_BODY:                                                         # Tela escolher corpo
            render_selection(events, "Escolha o corpo",  BODY_OPTIONS,   body_sel,
                             BODY_IMGS,   ST_OUTFIT,  ST_NAME)
        elif state == ST_OUTFIT:                                                       # Tela escolher roupa
            render_selection(events, "Escolha a roupa",  OUTFIT_OPTIONS, outfit_sel,
                             OUTFIT_IMGS, ST_HAIR,    ST_BODY)
        elif state == ST_HAIR:                                                         # Tela escolher cabelo
            render_selection(events, "Escolha o cabelo", HAIR_OPTIONS,   hair_sel,
                             HAIR_IMGS,   ST_PREVIEW, ST_OUTFIT)
        elif state == ST_PREVIEW:  render_preview(events)
        elif state == ST_GAME:     render_game(events)
        elif state == ST_WIN:      render_win(events)
        elif state == ST_LOSE:     render_lose(events)

        pygame.display.flip()                                                          # Mostra tudo que foi desenhado na tela
        clock.tick(FPS)                                                                # Controla pra não passar de 60 FPS

# ══════════════════════════════════════════════════════════════════════════════
# PONTO DE ENTRADA — executa o main() quando rodamos o arquivo
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        main()                                                                         # Inicia o jogo
    except KeyboardInterrupt:                                                          # Se usuário apertou Ctrl+C no terminal
        print("\nJogo encerrado pelo usuario.")
        pygame.quit()
        sys.exit()