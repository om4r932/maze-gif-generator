import pygame, sys, os
from functions import *

def get_asset_path(relative_path):
    # Si le script est exécuté sous forme d'exécutable PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Définition des propriétés de la fenêtre
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 16

# Définition des couleurs utilisées
GREY = (127, 127, 127)
DARK_RED = (139, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialisation de la fenêtre et de ses paramètres
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labyrinthe - Omar ID EL MOUMEN")
clock = pygame.time.Clock()

# Préparation des sprites d'animation du personnage
sprites = {}
base = pygame.image.load(get_asset_path('assets/man.png')) # L'image doit contenir 12 sprites 16x16 chacun (dont 4 lignes pour chaque direction et 3 colonnes pour chaque état)
rectPlayer = pygame.Rect(0, 0, 16, 16)
w, h = rectPlayer.size

for i, xx in enumerate(["N", "E", "S", "W"]):
    for pos in range(4):
        img_name = f"man{xx}{pos}"
        xpos = pos
        if pos == 3:
            xpos = 1
        merged_surface = pygame.Surface.subsurface(base, xpos * w, i * h, w, h)
        sprites[img_name] = pygame.transform.scale(merged_surface, (TILE_SIZE, TILE_SIZE)) # Redimensionne les sprites selon la taille des cellules

maze = generate_maze(HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE) # Génère un labyrinthe aléatoire (voir functions.py)

player = {
    "x": 0,
    "y": 0,
    'direction': 'S',
    "state": 0
} # Données du joueur

movement_delay = 125 # Délai, en millisecondes, entre chaque mouvement
speed = 1 # Vitesse du joueur, par case
last_move_time = pygame.time.get_ticks()
gave_up = False

while True:
    window.fill(GREY)

    for event in pygame.event.get(): # Vérifie les événements nécessaires
        if event.type == pygame.QUIT: # Lorsque l'utilisateur ferme la fenêtre
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Si le joueur souhaite abandonner, appuyer Espace affiche la solution pendant 10 secondes, puis quitte la partie
            solution = solve_maze(maze)
            for y, x in solution:
                maze[y][x] = (3, solution.index((y, x)) * 255 / len(solution))
            print("Abandon :'(")
            pygame.time.set_timer(pygame.QUIT, 10000)

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    if current_time - last_move_time >= movement_delay: # Gestion des mouvements du joueur
        if keys[pygame.K_UP]:
            if maze[player['y']-1][player['x']] != 1:
                player['y'] -= speed
                player['state'] = (player['state'] + 1) % 4
                player['direction'] = 'N'
                last_move_time = current_time
        if keys[pygame.K_DOWN]:
            if maze[player['y']+1][player['x']] != 1:
                player['y'] += speed
                player['state'] = (player['state'] + 1) % 4
                player['direction'] = 'S'
                last_move_time = current_time
        if keys[pygame.K_LEFT]:
            if maze[player['y']][player['x']-1] != 1:
                player['x'] -= speed
                player['state'] = (player['state'] + 1) % 4
                player['direction'] = 'W'
                last_move_time = current_time
        if keys[pygame.K_RIGHT]:
            if maze[player['y']][player['x']+1] != 1:
                player['x'] += speed
                player['state'] = (player['state'] + 1) % 4
                player['direction'] = 'E'
                last_move_time = current_time

    if maze[player['y']][player['x']] == 2: # Si le joueur atteint l'objectif, il gagne
        print("Gagné !")
        pygame.quit()
        sys.exit()

    for y in range(len(maze)): # Affichage des objets dans la fenêtre
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(window, BLACK, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if isinstance(maze[y][x], tuple) and maze[y][x][0] == 3:
                pygame.draw.rect(window, (maze[y][x][1], 255, 255), (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if maze[y][x] == 2 and not gave_up:
                pygame.draw.rect(window, GREEN, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if maze[y][x] == 5 and not gave_up:
                window.blit(sprites[f"man{player['direction']}{player['state']}"], (player['x']*TILE_SIZE, player['y']*TILE_SIZE))

    pygame.display.flip()
    clock.tick(30) # Limite le nombre d'images par seconde à 30