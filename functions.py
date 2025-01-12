import random

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def generate_maze(rows, cols, start_pos=(0, 0)): # Crée un labyrinthe aléatoire à l'aide de l'algorithme de recherche en profondeur ou DFS (Depth First Search)
    maze = [[1 for _ in range(cols)] for _ in range(rows)] # Crée une grille de cellules remplies de murs
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    start_x, start_y = start_pos

    # Variables permettant le placement de l'objectif à la fin du labyrinthe
    farthest_cell = (start_x, start_y)
    max_steps = 0

    def is_valid(x, y): # Vérifie si la cellule est dans les limites et non encore visitée
        return 0 <= x < rows and 0 <= y < cols and not visited[x][y]

    def dfs(start, steps=0): # L'algorithme de recherche en profondeur en récursif
        nonlocal farthest_cell, max_steps # Utilise les variables déclarées en dehors de la fonction

        x, y = start
        maze[x][y] = 0
        visited[x][y] = True

        if steps > max_steps:
            max_steps = steps
            farthest_cell = (x, y)
    
        random.shuffle(DIRECTIONS) # Randomise les directions pour éviter les biais
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if is_valid(nx, ny):
                maze[x + dx][y + dy] = 0
                dfs((nx, ny), steps + 1)
    
    dfs(start_pos)

    goal_x, goal_y = farthest_cell
    
    # Définir les positions du joueur et de l'objectif
    maze[start_x][start_y] = 5  # Joueur
    maze[goal_x][goal_y] = 2  # Objectif
    
    return maze

def solve_maze(maze): # Résout le labyrinthe à l'aide de l'algorithme de recherche en profondeur
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    start_x, start_y = 0, 0
    path = []

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and not visited[x][y] and maze[x][y] != 1

    def dfs(x, y):
        visited[x][y] = True
        path.append((x, y))

        if maze[x][y] == 2:
            return True

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                if dfs(nx, ny):
                    return True

        path.pop()
        return False

    dfs(start_x, start_y)
    return path