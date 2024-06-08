import pyglet
from pyglet import shapes
from pyglet.window import key

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# Making the window and setting it to be in the middle of the screen (on a 1080p screen)
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption = 'Fluid Simulation')
window.set_location(150, 75)

# Batch for rendering
shapes_batch = pyglet.graphics.Batch()

# Shapes
background = shapes.Rectangle(x = 0, y = 0, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, color = (26, 28, 44), batch = shapes_batch)

# Running the actual functions
@window.event
def on_draw():
    window.clear()
    shapes_batch.draw()
    
def update(dt):
    pass
    
# Basically saying call the update function 60 times per second
pyglet.clock.schedule_interval(update, 1/60)
# Needs to be the last line
pyglet.app.run() 