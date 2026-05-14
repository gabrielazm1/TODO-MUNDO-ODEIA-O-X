import pygame
import sys
import math
import random
import os
import numpy as np

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