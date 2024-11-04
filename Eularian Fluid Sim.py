# --------------------------------------------------------------- Importing libraries ---------------------------------------------------------------
import pyglet
from pyglet import shapes
from pyglet.window import key
from random import randint
import numpy as np

# --------------------------------------------------------------- Constants ---------------------------------------------------------------

# MUST BE 16:9
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

NUM_X_POINTS = int((WINDOW_HEIGHT / 8) + 1)
NUM_Y_POINTS = int(WINDOW_HEIGHT / 8)

GRAVITY = -9.807

# --------------------------------------------------------------- Variables ---------------------------------------------------------------

# np grid
x_range = np.linspace(0, WINDOW_WIDTH, NUM_X_POINTS)
y_range = np.linspace(0, WINDOW_HEIGHT, NUM_Y_POINTS)

coords_x, coords_y = np.meshgrid(x_range, y_range)

# Intial condition, creating the velcotity grids
velocity_x = np.zeros((NUM_Y_POINTS + 1, NUM_X_POINTS))
velocity_y = np.zeros((NUM_Y_POINTS, NUM_X_POINTS + 1))

new_velo_x = np.empty_like(velocity_x)
new_velo_y = np.empty_like(velocity_y)

# Making the window and setting it to be in the middle of the screen (on a 1080p screen)
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption = 'PIC/FLIP Simulation')
window.set_location(150, 100)

# Getting key functionality in Pyglet
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Batch for rendering
sprites_batch = pyglet.graphics.Batch()

# Background rectangle
background = shapes.Rectangle(x = 0, y = 0, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, color = (26, 28, 44))
    
# --------------------------------------------------------------- Functions ---------------------------------------------------------------
    
def adding_gravity(velo_y, dt):
    
    n_v_y = velo_y
    for x in n_v_y:
        for j in range(len(x)):
            new_y = (x[j] + GRAVITY)
            x[j] = new_y
      
    # Setting the top and bottom boundaries to velocity 0 (they are walls)      
    n_v_y[0, :] = 0
    n_v_y[-1, :] = 0
    
    return n_v_y

def main():

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

        velo_y = adding_gravity(velocity_y, dt)
        print(len(velo_y[0]))
        print(len(velocity_x[0]))

    # Basically saying call the update function 60 times per second
    pyglet.clock.schedule_interval(update, 1/60)
    # Needs to be the last line
    pyglet.app.run() 

if __name__ == '__main__':
    main()