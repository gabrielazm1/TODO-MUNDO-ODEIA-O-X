import pygame
import sys
import math
import random
import os

pygame.init()

WIDTH, HEIGHT = 900, 650
FPS = 60
ASSETS = os.path.join(os.path.dirname(__file__), "assets")

BLACK        = (0,   0,   0)
WHITE        = (255, 255, 255)
DARK_BG      = (10,  0,  22)
PURPLE       = (90,  0, 150)
LIGHT_PURPLE = (180, 80, 255)
GOLD         = (255, 210,  50)
CYAN         = (0,  220, 255)
RED          = (220,  50,  50)
PINK         = (255, 100, 180)
DARK_PURPLE  = (40,   0,  70)
DIM_PURPLE   = (60,  10, 100)
BTN_HOVER    = (130,  40, 220)
BTN_NORMAL   = (80,   0, 150)
GREEN        = (50,  230,  80)

ST_MENU    = 0
ST_INSTRUCT = 1
ST_NAME    = 2
ST_BODY    = 3
ST_OUTFIT  = 4
ST_HAIR    = 5
ST_PREVIEW = 6
ST_GAME    = 7
ST_WIN     = 8
ST_LOSE    = 9

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Todo Mundo Odeia...")
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)

def font(size): return pygame.font.SysFont("arial", size, bold=False)
def bold_font(size): return pygame.font.SysFont("arial", size, bold=True)

F_TITLE = bold_font(54)
F_BIG   = bold_font(38)
F_MED   = font(28)
F_SMALL = font(20)
F_TINY  = font(16)
F_INPUT = bold_font(32)

def load_sheet(name):
    path = os.path.join(ASSETS, name)
    return pygame.image.load(path).convert_alpha()

def extract_frame(sheet_surf, col, row, fw=32, fh=32):
    frame = pygame.Surface((fw, fh), pygame.SRCALPHA)
    frame.blit(sheet_surf, (0, 0), (col * fw, row * fh, fw, fh))
    return frame

def create_galaxy_bg(w, h):
    surf = pygame.Surface((w, h))
    surf.fill(DARK_BG)
    for _ in range(6):
        cx = random.randint(0, w)
        cy = random.randint(0, h)
        radius = random.randint(120, 320)
        color = (random.randint(40, 100), 0, random.randint(80, 180))
        for r in range(radius, 0, -10):
            alpha_val = max(0, int(60 * (1 - r / radius)))
            nebula = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.ellipse(nebula, (*color, alpha_val), (0, 0, r*2, r*2))
            surf.blit(nebula, (cx - r, cy - r), special_flags=pygame.BLEND_RGBA_ADD)
    for _ in range(300):
        x = random.randint(0, w)
        y = random.randint(0, h)
        brightness = random.randint(120, 255)
        size = random.choice([1, 1, 1, 2, 2, 3])
        color = (brightness, brightness, min(255, brightness + random.randint(0, 60)))
        if size == 1:
            surf.set_at((x, y), color)
        else:
            pygame.draw.circle(surf, color, (x, y), size // 2)
    return surf
class Button:
    def __init__(self, rect, text, font_obj=None, color=BTN_NORMAL, hover=BTN_HOVER):
        self.rect  = pygame.Rect(rect)
        self.text  = text
        self.font  = font_obj or F_MED
        self.color = color
        self.hover = hover

    def draw(self, surf):
        mpos = pygame.mouse.get_pos()
        col = self.hover if self.rect.collidepoint(mpos) else self.color
        pygame.draw.rect(surf, (20, 0, 40), self.rect.move(3, 3), border_radius=12)
        pygame.draw.rect(surf, col, self.rect, border_radius=12)
        pygame.draw.rect(surf, LIGHT_PURPLE, self.rect, 2, border_radius=12)
        lbl = self.font.render(self.text, True, WHITE)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))
class TwinkleStar:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x     = random.randint(0, WIDTH)
        self.y     = random.randint(0, HEIGHT)
        self.max_r = random.uniform(1.5, 3.5)
        self.phase = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(1.5, 4.0)
        self.color = random.choice([WHITE, CYAN, LIGHT_PURPLE, (255,255,180)])

    def draw(self, surf, t):
        r = self.max_r * (0.5 + 0.5 * math.sin(self.phase + t * self.speed))
        if r > 0.5:
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), int(r))
    
    TWINKLES = [TwinkleStar() for _ in range(80)]

    def draw_title(surf, text, y, color=GOLD):
        shadow = F_TITLE.render(text, True, (80, 0, 120))
        title  = F_TITLE.render(text, True, color)
        surf.blit(shadow, shadow.get_rect(centerx=WIDTH//2+3, y=y+3))
        surf.blit(title,  title.get_rect(centerx=WIDTH//2, y=y))

    def draw_text(surf, text, y, color=WHITE, font_obj=None):
        f = font_obj or F_MED
        lbl = f.render(text, True, color)
        surf.blit(lbl, lbl.get_rect(centerx=WIDTH//2, y=y))

    def draw_panel(surf, rect, alpha=200):
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        panel.fill((20, 0, 50, alpha))
        surf.blit(panel, rect.topleft)
        pygame.draw.rect(surf, LIGHT_PURPLE, rect, 2, border_radius=10)

print("Loading assets...")
try:
    char_sheet    = load_sheet("Character Model.png")
    hair_sheet    = load_sheet("Hairs.png")
    outfit_sheets = [load_sheet(f"Outfit{i}.png") for i in range(1, 7)]
    heart_path_options = [
        "Heart.png",
        "Pixel Heart Sprite Sheet 32x32.png",
        "Pixel Heart Sprite Sheet 16x16.png",
    ]
    heart_raw = None
    for hp in heart_path_options:
        full = os.path.join(ASSETS, hp)
        if os.path.exists(full):
            heart_raw = pygame.image.load(full).convert_alpha()
            heart_frame_size = 32 if "32x32" in hp else (16 if "16x16" in hp else heart_raw.get_height())
            heart_img = pygame.Surface((heart_frame_size, heart_frame_size), pygame.SRCALPHA)
            heart_img.blit(heart_raw, (0, 0), (0, 0, heart_frame_size, heart_frame_size))
            heart_img = pygame.transform.scale(heart_img, (38, 38))
            break
    if heart_raw is None:
        raise Exception("Nenhuma imagem de coração encontrada em assets/")

    star_path = os.path.join(ASSETS, "Estrela.png")
    if os.path.exists(star_path):
        raw_star = pygame.image.load(star_path).convert_alpha()
        star_img = pygame.transform.scale(raw_star, (44, 44))
    else:
        star_img = None
        print("Aviso: Estrela.png nao encontrado, usando desenho padrao")

    new_gun_path = os.path.join(ASSETS, "New Piskel.png")
    if os.path.exists(new_gun_path):
        raw_gun = pygame.image.load(new_gun_path).convert_alpha()
        gun_w   = 90
        ratio   = gun_w / raw_gun.get_width()
        gun_h   = max(1, int(raw_gun.get_height() * ratio))
        gun_surf = pygame.transform.smoothscale(raw_gun, (gun_w, gun_h))
    else:
        gun_surf = extract_gun_from_sheet()
        if gun_surf is None:
            raise Exception("Gun extraction failed")
    print(f"Gun size: {gun_surf.get_size()}")

    space_bg_path = os.path.join(ASSETS, "cenario universo.png")
    if os.path.exists(space_bg_path):
        raw_bg   = pygame.image.load(space_bg_path).convert()
        SPACE_BG = pygame.transform.smoothscale(raw_bg, (WIDTH, HEIGHT))
    else:
        SPACE_BG = None
except Exception as e:
    import traceback
    print(f"Asset load error: {e}")
    traceback.print_exc()
    input("Pressione Enter para fechar...")
    pygame.quit(); sys.exit()

BODY_OPTIONS = [
    {"name": "Menina Branca", "skin_row": 0, "skin_col": 1, "default_outfit": 0},
    {"name": "Menino Branco", "skin_row": 2, "skin_col": 1, "default_outfit": 3},
    {"name": "Menina Negra",  "skin_row": 3, "skin_col": 1, "default_outfit": 0},
    {"name": "Menino Negro",  "skin_row": 5, "skin_col": 1, "default_outfit": 3},
]

OUTFIT_OPTIONS = [
    {"name": "Vestido Branco", "sheet_idx": 0, "col": 1},
    {"name": "Vestido Rosa",   "sheet_idx": 1, "col": 1},
    {"name": "Saia Azul",      "sheet_idx": 2, "col": 1},
    {"name": "Camisa Laranja", "sheet_idx": 3, "col": 1},
    {"name": "Agasalho Verde", "sheet_idx": 4, "col": 1},
    {"name": "Calça Escura",   "sheet_idx": 5, "col": 1},
]

HAIR_OPTIONS = [
    {"name": "Longo Loiro",  "row": 4, "col": 1},
    {"name": "Longo Moreno", "row": 0, "col": 1},
    {"name": "Curto Loiro",  "row": 5, "col": 1},
    {"name": "Curto Moreno", "row": 7, "col": 1},
]
def compose_character(body_idx, outfit_idx, hair_idx, scale=4):
    s      = 32
    result = pygame.Surface((s, s), pygame.SRCALPHA)
    body   = BODY_OPTIONS[body_idx]
    outfit = OUTFIT_OPTIONS[outfit_idx]
    hair   = HAIR_OPTIONS[hair_idx]
    result.blit(extract_frame(char_sheet,                          body["skin_col"],    body["skin_row"]), (0, 0))
    result.blit(extract_frame(outfit_sheets[outfit["sheet_idx"]], outfit["col"],        0),               (0, 0))
    result.blit(extract_frame(hair_sheet,                          hair["col"],          hair["row"]),     (0, 0))
    return pygame.transform.scale(result, (s * scale, s * scale))

def get_preview_surf(body_idx, outfit_idx, hair_idx):
    return compose_character(body_idx, outfit_idx, hair_idx, scale=5)

random.seed(42)
GALAXY_BG = create_galaxy_bg(WIDTH, HEIGHT)
random.seed()

state              = ST_MENU
target_name        = ""
body_sel           = 0
outfit_sel         = 0
hair_sel           = 0
input_text         = ""
t                  = 0.0
input_cursor_timer = 0

class GameState:
    def _init_(self):
        self.reset()

    def reset(self):
        self.target_lives  = 3
        self.ammo          = 10
        self.max_ammo      = 10
        self.tx            = WIDTH  // 2
        self.ty            = HEIGHT // 2
        self.tvx           = 3.6
        self.tvy           = 3.1
        self.speed_mult    = 1.0
        self.target_char   = None
        self.hit_flash     = 0
        self.miss_flash    = 0
        self.shot_effects  = []
        self.stars         = []
        self.star_timer    = 0
        self.star_bonus    = 3
        self.game_over     = False
        self.shots_fired   = 0
        self.dodge_timer   = 0

GS = GameState()

def start_game():
    GS.reset()
    GS.target_char = compose_character(body_sel, outfit_sel, hair_sel, scale=4)
    GS.tx  = random.randint(200, WIDTH  - 200)
    GS.ty  = random.randint(150, HEIGHT - 150)
    angle  = random.uniform(0, math.pi * 2)
    speed  = 4.1
    GS.tvx = math.cos(angle) * speed
    GS.tvy = math.sin(angle) * speed

def move_target():
    # Desvio aleatório periódico
    GS.dodge_timer += 1
    if GS.dodge_timer > random.randint(40, 90):
        GS.dodge_timer = 0
        angle = random.uniform(0, math.pi * 2)
        cur_speed = math.hypot(GS.tvx, GS.tvy)
        GS.tvx = math.cos(angle) * cur_speed
        GS.tvy = math.sin(angle) * cur_speed

    GS.tx += GS.tvx * GS.speed_mult
    GS.ty += GS.tvy * GS.speed_mult
    char_w = GS.target_char.get_width()
    char_h = GS.target_char.get_height()
    margin = 40
    if GS.tx < margin:                   GS.tx = margin;                   GS.tvx =  abs(GS.tvx)
    if GS.tx > WIDTH  - char_w - margin: GS.tx = WIDTH - char_w - margin;  GS.tvx = -abs(GS.tvx)
    if GS.ty < margin + 40:              GS.ty = margin + 40;              GS.tvy =  abs(GS.tvy)
    if GS.ty > HEIGHT - char_h - margin: GS.ty = HEIGHT - char_h - margin; GS.tvy = -abs(GS.tvy)

def update_stars():
    GS.star_timer += 1
    if GS.star_timer > random.randint(180, 320):
        GS.star_timer = 0
        if len(GS.stars) < 2:
            GS.stars.append([random.randint(60, WIDTH-60), random.randint(80, HEIGHT-80), 180, 180])
    GS.stars = [[x, y, l-1, ml] for x, y, l, ml in GS.stars if l > 1]

def shoot(mx, my):
    global state
    if GS.ammo <= 0:
        return
    GS.ammo -= 1
    GS.shots_fired += 1

    # A cada tiro o alvo acelera
    GS.speed_mult += 0.25

    for star in GS.stars[:]:
        sx, sy, l, ml = star
        if math.hypot(mx - sx, my - sy) < 28:
            GS.ammo = min(GS.ammo + GS.star_bonus, GS.max_ammo)
            GS.stars.remove(star)
            GS.shot_effects.append([sx, sy, 30, 30, GOLD])
            return

    char_w = GS.target_char.get_width()
    char_h = GS.target_char.get_height()
    if pygame.Rect(GS.tx, GS.ty, char_w, char_h).collidepoint(mx, my):
        GS.target_lives -= 1
        GS.hit_flash = 20
        GS.shot_effects.append([mx, my, 25, 25, RED])
        GS.speed_mult += 0.35
        if GS.target_lives <= 0:
            state = ST_WIN
    else:
        GS.miss_flash = 8
        GS.shot_effects.append([mx, my, 15, 15, CYAN])

    if GS.ammo <= 0 and GS.target_lives > 0:
        state = ST_LOSE

def draw_bg(surf, t_val):
    if SPACE_BG is not None:
        surf.blit(SPACE_BG, (0, 0))
        return
    surf.blit(GALAXY_BG, (0, 0))
    for star in TWINKLES:
        star.draw(surf, t_val)

def draw_gun_cursor(surf, mx, my):
    if gun_surf is None:
        pygame.draw.circle(surf, CYAN, (mx, my), 8, 2)
        return
    gun_w, gun_h = gun_surf.get_size()
    draw_x = max(0, mx - gun_w + 8)
    draw_y = my - gun_h // 2
    surf.blit(gun_surf, (draw_x, draw_y))
    pygame.draw.circle(surf, CYAN, (mx, my), 4, 1)

def draw_ammo_bar(surf):
    bar_h = 60
    bar_y = HEIGHT - bar_h
    bar_surf = pygame.Surface((WIDTH, bar_h), pygame.SRCALPHA)
    bar_surf.fill((10, 0, 30, 210))
    surf.blit(bar_surf, (0, bar_y))
    pygame.draw.line(surf, LIGHT_PURPLE, (0, bar_y), (WIDTH, bar_y), 1)

    gun_w, gun_h = gun_surf.get_size()
    icon_scale = min(1.0, (bar_h - 14) / max(1, gun_h))
    icon_w = max(1, int(gun_w * icon_scale))
    icon_h = max(1, int(gun_h * icon_scale))
    icon   = pygame.transform.smoothscale(gun_surf, (icon_w, icon_h))

    spacing = icon_w + 8
    start_x = (WIDTH - GS.max_ammo * spacing) // 2
    icon_y  = bar_y + (bar_h - icon_h) // 2

    for i in range(GS.max_ammo):
        x = start_x + i * spacing
        if i < GS.ammo:
            surf.blit(icon, (x, icon_y))
        else:
            cx = x + icon_w // 2
            cy = icon_y + icon_h // 2
            r  = max(4, icon_h // 2 - 2)
            pygame.draw.line(surf, RED, (cx-r, cy-r), (cx+r, cy+r), 2)
            pygame.draw.line(surf, RED, (cx+r, cy-r), (cx-r, cy+r), 2)
def render_menu(events):
    global state
    draw_bg(screen, t)
    draw_title(screen, "TODO MUNDO ODEIA", 80)
    draw_title(screen, "...", 138, LIGHT_PURPLE)
    btn_play = Button((WIDTH//2 - 120, 290, 240, 60), "Jogar", F_BIG)
    btn_info = Button((WIDTH//2 - 120, 370, 240, 60), "Instruções", F_MED, BTN_NORMAL, DIM_PURPLE)
    btn_play.draw(screen)
    btn_info.draw(screen)
    for ev in events:
        if btn_play.clicked(ev): state = ST_NAME
        if btn_info.clicked(ev): state = ST_INSTRUCT
def render_instructions(events):
    global state
    draw_bg(screen, t)
    draw_panel(screen, pygame.Rect(60, 60, WIDTH-120, HEIGHT-120), alpha=230)
    draw_title(screen, "Instruções", 80)
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
    y = 175
    for text, color, fnt in lines:
        lbl = fnt.render(text, True, color)
        screen.blit(lbl, (90, y))
        y += fnt.size(text)[1] + 4
    btn_back = Button((WIDTH//2 - 100, HEIGHT-100, 200, 50), "Voltar")
    btn_back.draw(screen)
    for ev in events:
        if btn_back.clicked(ev): state = ST_MENU


def render_name_input(events):
    global state, input_text, target_name, input_cursor_timer
    draw_bg(screen, t)
    draw_title(screen, "Todo mundo odeia...", 80)
    draw_panel(screen, pygame.Rect(100, 180, WIDTH-200, 220))
    draw_text(screen, "Qual é o nome do alvo?", 200, LIGHT_PURPLE, F_MED)
    field_rect = pygame.Rect(WIDTH//2 - 220, 255, 440, 55)
    pygame.draw.rect(screen, (30, 0, 60), field_rect, border_radius=8)
    pygame.draw.rect(screen, LIGHT_PURPLE, field_rect, 2, border_radius=8)
    input_cursor_timer += 1
    cursor_char = "|" if (input_cursor_timer // 30) % 2 == 0 else ""
    lbl = F_INPUT.render(input_text + cursor_char, True, WHITE)
    screen.blit(lbl, (field_rect.x + 15, field_rect.y + 10))
    if not input_text:
        hint = F_SMALL.render("Digite o nome e pressione Enter", True, (150, 100, 200))
        screen.blit(hint, hint.get_rect(centerx=WIDTH//2, y=330))
    for ev in events:
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN and input_text.strip():
                target_name = input_text.strip(); state = ST_BODY
            elif ev.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif len(input_text) < 24 and ev.unicode.isprintable():
                input_text += ev.unicode
def render_selection(events, title, options, current_sel, images, next_state, prev_state):
    global body_sel, outfit_sel, hair_sel
    draw_bg(screen, t)
    draw_title(screen, title, 30)
    cols    = min(4, len(options))
    cell_w, cell_h = 160, 180
    start_x = (WIDTH - (cols * cell_w + (cols-1) * 20)) // 2
    boxes = []
    for i, img in enumerate(images):
        x = start_x + (i % cols) * (cell_w + 20)
        y = 120     + (i // cols) * (cell_h + 10)
        box = pygame.Rect(x, y, cell_w, cell_h)
        boxes.append(box)
        is_sel = (i == current_sel)
        pygame.draw.rect(screen, (60,0,120) if is_sel else (20,0,50), box, border_radius=10)
        pygame.draw.rect(screen, GOLD if is_sel else LIGHT_PURPLE, box, 3, border_radius=10)
        iw, ih = img.get_size()
        screen.blit(img, (x + (cell_w-iw)//2, y + (cell_h-ih)//2))
    btn_next = Button((WIDTH-200, HEIGHT-70, 180, 50), "Próximo", F_MED)
    btn_back = Button((20, HEIGHT-70, 150, 50), "Voltar", F_MED)
    btn_next.draw(screen); btn_back.draw(screen)
    for ev in events:
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            for i, box in enumerate(boxes):
                if box.collidepoint(ev.pos):
                    if next_state == ST_OUTFIT:
                        global body_sel;   body_sel   = i
                    elif next_state == ST_HAIR:
                        global outfit_sel; outfit_sel = i
                    elif next_state == ST_PREVIEW:
                        global hair_sel;   hair_sel   = i
        if btn_next.clicked(ev):
            global state; state = next_state
        if btn_back.clicked(ev):
            state = prev_state


def render_preview(events):
    global state
    draw_bg(screen, t)
    draw_panel(screen, pygame.Rect(50, 50, WIDTH-100, HEIGHT-100))
    draw_title(screen, "Seu personagem", 70)
    char_surf = get_preview_surf(body_sel, outfit_sel, hair_sel)
    cw, ch = char_surf.get_size()
    cx, cy = WIDTH//2 - cw//2, HEIGHT//2 - ch//2 + 20
    screen.blit(char_surf, (cx, cy))
    draw_text(screen, f"Nome: {target_name}", cy+ch+20, GOLD, F_MED)
    btn_start = Button((WIDTH//2-130, HEIGHT-90, 260, 60), "Começar o jogo!", F_BIG)
    btn_back  = Button((20, HEIGHT-70, 150, 50), "Voltar", F_MED)
    btn_start.draw(screen); btn_back.draw(screen)
    for ev in events:
        if btn_start.clicked(ev): start_game(); state = ST_GAME
        if btn_back.clicked(ev):  state = ST_HAIR