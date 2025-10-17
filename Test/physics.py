import pymunk
import pymunk.pygame_util
import pygame
import math
import sys

# Inizializzazione
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)

# Utility per disegnare con Pygame
draw_options = pymunk.pygame_util.DrawOptions(screen)

def create_rectangle(space, pos, size, mass=1):
    """Crea un corpo rettangolare"""
    moment = pymunk.moment_for_box(mass, size)
    body = pymunk.Body(mass, moment)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = 0.8
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

def create_line(space, start, end, radius=2):
    """Crea una linea statica"""
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, start, end, radius)
    shape.elasticity = 0.8
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

def create_ellipse(space, pos, radius_x, radius_y, mass=1, segments=20):
    """Crea un'ellisse usando un Poly approssimato"""
    # Crea punti per approssimare l'ellisse
    points = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius_x * math.cos(angle)
        y = radius_y * math.sin(angle)
        points.append((x, y))
    
    moment = pymunk.moment_for_poly(mass, points)
    body = pymunk.Body(mass, moment)
    body.position = pos
    shape = pymunk.Poly(body, points)
    shape.elasticity = 0.8
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

def create_arc(space, center, radius, start_angle, end_angle, mass=1, segments=10):
    """Crea un arco usando segmenti multipli"""
    body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
    body.position = center
    
    # Crea segmenti per approssimare l'arco
    angle_step = (end_angle - start_angle) / segments
    shapes = []
    
    for i in range(segments):
        angle1 = start_angle + i * angle_step
        angle2 = start_angle + (i + 1) * angle_step
        
        x1 = radius * math.cos(angle1)
        y1 = radius * math.sin(angle1)
        x2 = radius * math.cos(angle2)
        y2 = radius * math.sin(angle2)
        
        shape = pymunk.Segment(body, (x1, y1), (x2, y2), 2)
        shape.elasticity = 0.8
        shape.friction = 0.5
        shapes.append(shape)
        space.add(shape)
    
    space.add(body)
    return body, shapes

# Creazione dell'ambiente fisico
def setup_physics():
    # Pavimento
    create_line(space, (100, 500), (700, 500))
    
    # Pareti
    create_line(space, (100, 100), (100, 500))
    create_line(space, (700, 100), (700, 500))
    
    # Rampo inclinata
    create_line(space, (200, 400), (400, 300))
    
    # Piattaforme
    create_line(space, (500, 350), (650, 350))

# Setup iniziale
setup_physics()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Aggiungi oggetti al click
            mouse_pos = pygame.mouse.get_pos()
            
            if event.button == 1:  # Click sinistro - Rettangolo
                create_rectangle(space, mouse_pos, (30, 20))
            elif event.button == 3:  # Click destro - Ellisse
                create_ellipse(space, mouse_pos, 20, 15)
            elif event.button == 2:  # Click centrale - Arco
                create_arc(space, mouse_pos, 25, 0, math.pi)

    # Pulizia schermo
    screen.fill((255, 255, 255))
    
    # Disegna la fisica
    space.debug_draw(draw_options)
    
    # Aggiorna fisica
    space.step(1/60.0)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()