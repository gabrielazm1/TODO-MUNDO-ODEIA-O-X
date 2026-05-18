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