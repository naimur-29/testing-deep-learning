import os
import random
import pygame

class Cell:
    def __init__(self, box, color, piece=None):
        self.box = box  
        self.pos = {
            "x": (box[0], box[0] + box[2]),
            "y": (box[1], box[1] + box[3])
        }
        self.color = (255, 207, 159) if color == 0 else (210, 140, 69)
        self.piece = piece
        
    def update(self, piece=None):
        res = self.piece
        self.piece = piece
        return res
        
    def is_inside(self, pos):
        return pos[0] >= cell.pos['x'][0] and pos[0] <= cell.pos['x'][1] and pos[1] >= cell.pos['y'][0] and pos[1] <= cell.pos['y'][1]
    
    def is_empty(self):
        return self.piece == None
        
    def draw(self, fun, surface):
        fun.draw.rect(surface, self.color, self.box)
        if self.piece != None:
            surface.blit(self.piece, (self.pos["x"][0], self.pos["y"][0]))

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True

dt = 0
grid = []
w = screen.get_width() / 8
h = screen.get_height() / 8


# load images:
def load_image(filename):
    surface = pygame.image.load(os.path.join('assets', filename))
    return pygame.transform.smoothscale(surface, (w, h))

pieces = {
    "kl":load_image("Chess_klt45.svg"),
    "kd":load_image("Chess_kdt45.svg"),
    "ql":load_image("Chess_qlt45.svg"),
    "qd":load_image("Chess_qdt45.svg"),
    "bl":load_image("Chess_blt45.svg"),
    "bd":load_image("Chess_bdt45.svg"),
    "knl":load_image("Chess_nlt45.svg"),
    "knd":load_image("Chess_ndt45.svg"),
    "rl":load_image("Chess_rlt45.svg"),
    "rd":load_image("Chess_rdt45.svg"),
    "pl":load_image("Chess_plt45.svg"),
    "pd":load_image("Chess_pdt45.svg"),
}

board = [
    ['rd', 'knd', 'bd', 'kd', 'qd', 'bd', 'knd', 'rd'],
    ['pd', 'pd', 'pd', 'pd', 'pd', 'pd', 'pd', 'pd'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['pl', 'pl', 'pl', 'pl', 'pl', 'pl', 'pl', 'pl'],
    ['rl', 'knl', 'bl', 'ql', 'kl', 'bl', 'knl', 'rl'],
]


for i in range(8):
    row = []
    for k in range(8):
        p = board[k][i]
        piece = pieces[p] if p != '' else None
        if (i+k) % 2 == 0:
            row.append(Cell((i * w, k * h, w, h), 0, piece))
        else: row.append(Cell((i * w, k * h, w, h), 1, piece))
    grid.append(row)

# for i in range(8):
#     for k in range(8):
#         rp = random.choice(pieces)
#         color = (232, 235, 239) if grid[i][k] == 1 else (125, 135, 150)
#         pygame.draw.rect(screen, color, (i * w, k * h, w, h))
#         screen.blit(rp[random.choice(["light", "dark"])], (i*w, k*h))
selected_cell = None
piece_picked = None
mouse_hold = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_hold = True
            for row in grid:
                done = False
                for cell in row:
                    if cell.is_inside(pygame.mouse.get_pos()):
                        selected_cell = cell
                        piece_picked = selected_cell.update()
                        done = True
                        break
                if done: break
                        
        if event.type == pygame.MOUSEBUTTONUP and piece_picked != None and selected_cell != None:
            mouse_pos = pygame.mouse.get_pos()
            mouse_hold = False
            for row in grid:
                done = False
                for cell in row:
                    if cell.is_inside(pygame.mouse.get_pos()):
                        if cell.is_empty():
                            cell.update(piece_picked)
                        else: selected_cell.update(piece_picked)
                        done = True
                        break
                if done: break
            piece_picked = None
            selected_cell = None

    # draw:
    screen.fill("black")
    for row in grid:
        for cell in row:
            cell.draw(pygame, screen)
            
    if mouse_hold and piece_picked != None:
        mouse_pos = pygame.mouse.get_pos()
        pos = (mouse_pos[0] - piece_picked.get_width()/2, mouse_pos[1] - piece_picked.get_height() / 2)
        screen.blit(piece_picked, pos)
            
    # images:

    # seems necessary:
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()