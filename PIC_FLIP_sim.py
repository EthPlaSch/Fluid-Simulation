# Importing libraries
import pyglet
from pyglet import shapes
from pyglet.window import key
from random import randint
import numpy as np

# Constants

# MUST BE 16:9
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

NUM_OF_PARTICLES = 100
NUM_X_POINTS = 160
NUM_Y_POINTS = 90

# Variables

# np grid
x_range = np.linspace(0, WINDOW_WIDTH, NUM_X_POINTS)
y_range = np.linspace(0, WINDOW_HEIGHT, NUM_Y_POINTS)

coords_x, coords_y = np.meshgrid(x_range, y_range)

# Intial condition, creating the velcotity grids
prev_velo_x = np.full((NUM_X_POINTS, NUM_Y_POINTS+ 1), None)
prev_velo_y = np.full((NUM_Y_POINTS, NUM_X_POINTS + 1), None)
print(f"Elements in prev_velo_x: {len(prev_velo_x)}")
print(f"Elements in prev_velo_y: {len(prev_velo_y)}")

velo_x = np.empty_like(prev_velo_x)
velo_y = np.empty_like(prev_velo_y)
print(f"Elements in velo_y: {len(velo_y)}")

particles = []
visualise_x = []
reference_points = []
lines = []

# Making the window and setting it to be in the middle of the screen (on a 1080p screen)
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption = 'PIC/FLIP Simulation')
window.set_location(150, 100)

# Getting key functionality in Pyglet
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Batch for rendering
sprites_batch = pyglet.graphics.Batch()
particles_batch = pyglet.graphics.Batch()

# Background rectangle
background = shapes.Rectangle(x = 0, y = 0, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, color = (26, 28, 44))

# Particle Class
class Particle:
    
    # Initiation method
    def __init__(self, position = [0, 0])-> None:
        self.position = position
        self.velocity = [0, 0]
        
def generate_particles():
    
    for i in range(NUM_OF_PARTICLES):
        particle = (Particle([randint(15, int((WINDOW_WIDTH - 15) / 2)), randint(15, WINDOW_HEIGHT - 15)]))
        circle = shapes.Circle(particle.position[0], particle.position[1], radius = 5, color = (255, 0 , 0), batch = particles_batch)
        particles.append((particle, circle))
    
    
def main():    
        
    generate_particles()
    
    # for i in range(len(velo_x)):
    #     for j in range(i):
    #         circle = shapes.Circle(j * 8, i * 8, radius = 3, color = (255, 0 , 0), batch = sprites_batch)
    #         visualise_x.append(circle)
            
    for i, line in enumerate(velo_y):
        for j, value in enumerate(line):
            circle = shapes.Circle(i * x_range[1], j * y_range[1], radius = 2, color = (0, 255 , 0), batch = sprites_batch)
            visualise_x.append(circle)
            
    # visualisiing the grid
    for i in x_range:
        line = shapes.Line(i, 0, i, 720, 1, color = (100, 100, 100), batch = sprites_batch)
        lines.append(line)
    
    for i in y_range:
        line = shapes.Line(0, i, 1280, i, 1, color = (100, 100, 100), batch = sprites_batch)
        lines.append(line)
        
    # # visualisiing the grid
    # for i in x_range:
    #     line = shapes.Line(i + 4, 0, i + 4, 720, 1, color = (100, 100, 200), batch = sprites_batch)
    #     lines.append(line)
    
    # for i in y_range:
    #     line = shapes.Line(0, i, 1280, i, 1, color = (100, 100, 200), batch = sprites_batch)
    #     lines.append(line)
        
    # # visualisiing the grid
    # for i in x_range:
    #     line = shapes.Line(i, 0, i, 720, 1, color = (200, 100, 100), batch = sprites_batch)
    #     lines.append(line)
    
    # for i in y_range:
    #     line = shapes.Line(0, i + 4, 1280, i + 4, 1, color = (200, 100, 100), batch = sprites_batch)
    #     lines.append(line)

    # Running the actual functions
    @window.event
    def on_draw():
        
        # Clearing the window
        window.clear()
        
        # Drawing the background
        background.draw()

        # Drawing the sprites 
        sprites_batch.draw()
        
    # Update function
    def update(dt):
        pass

    # Basically saying call the update function 60 times per second
    pyglet.clock.schedule_interval(update, 1/60)
    # Needs to be the last line
    pyglet.app.run() 

if __name__ == '__main__':
    main()