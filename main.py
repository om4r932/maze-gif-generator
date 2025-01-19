import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
import os

# Dimensions du labyrinthe
rows, cols = 20, 20

# Variables pour stocker les étapes intermédiaires
maze_states = []
maze_solution_states = []

cmap = plt.get_cmap("Greys") # Sélection de la colormap (sélectionné : nuances de gris)

index = 0
while os.path.exists(f"./maze_{index}.gif"):
    index += 1

# Génération du labyrinthe avec capture des étapes (algorithme utilisé : DFS)
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)] # 1 = mur, 0 = chemin
    visited = [[False for _ in range(cols)] for _ in range(rows)] # utilisé pour DFS
    start_x, start_y = start_pos = (0, 0)

    farthest_cell = (start_x, start_y) # Utilisé pour placer automatiquement la sortie
    max_steps = 0

    def is_valid(x, y): # Evite les débordements
        return 0 <= x < rows and 0 <= y < cols and not visited[x][y]

    def dfs(start, steps=0): # DFS
        nonlocal farthest_cell, max_steps

        x, y = start
        maze[x][y] = 0
        visited[x][y] = True

        maze_states.append(np.copy(maze)) # Capture une image permettant à la création du GIF

        if steps > max_steps:
            max_steps = steps
            farthest_cell = (x, y)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if is_valid(nx, ny):
                maze[x + dx][y + dy] = 0
                dfs((nx, ny), steps + 1)

    dfs(start_pos)
    goal_x, goal_y = farthest_cell
    maze[goal_x][goal_y] = 2 # 2 = sortie

    return maze

# Génération du labyrinthe avec capture des étapes
maze = generate_maze(rows, cols)

for x in range(len(maze_states)): # Permet de rajouter les bordures manquants
    temp = maze_states[x].tolist()
    for i in range(len(temp)):
        temp[i].insert(0, 1)
    temp.insert(0, [1 for _ in range(len(temp[0]))])
    maze_states[x] = np.copy(temp)

for _ in range(50): # Prolonge la fin du GIF permettant de voir le labyrinthe final
    maze_states.append(np.copy(maze_states[-1]))

# Solution du labyrinthe avec capture des étapes (algorithme utilisé : DFS)
def solve_maze(maze):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    start_pos = (0, 0)
    path = []

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and not visited[x][y] and maze[x][y] != 1

    def dfs(start):
        x, y = start
        visited[x][y] = True
        path.append((x, y))

        # Capture l'état actuel du labyrinthe
        current_state = np.copy(maze)
        for px, py in path:
            current_state[px][py] = 3  # Marque le chemin actuel
        maze_solution_states.append(np.copy(current_state))

        if maze[x][y] == 2:
            return True

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                if dfs((nx, ny)):
                    return True

        path.pop()
        return False

    dfs(start_pos)
    return path

solve_maze(maze)

for x in range(len(maze_solution_states)):
    temp = maze_solution_states[x].tolist()
    # add borders
    for i in range(len(temp)):
        temp[i].insert(0, 1)
    temp.insert(0, [1 for _ in range(len(temp[0]))])
    maze_solution_states[x] = np.copy(temp)

for _ in range(50):
    maze_solution_states.append(np.copy(maze_solution_states[-1]))

final_maze_states = maze_states + maze_solution_states

# Création du GIF

fig, ax = plt.subplots(figsize=(6, 6))
ax.axis("off")

def update_final(frame):
    ax.clear()
    ax.axis("off")
    ax.imshow(final_maze_states[frame], cmap=cmap, vmin=0, vmax=3)

ani_final = animation.FuncAnimation(fig, update_final, frames=len(final_maze_states), interval=100)

# Sauvegarde du GIF
final_gif_path = f"./maze_{index}.gif"
ani_final.save(final_gif_path, writer="imagemagick", fps=20)