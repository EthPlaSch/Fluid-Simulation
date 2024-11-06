# Importing libraries
import pyglet
from pyglet import shapes
from pyglet.window import key
from random import randint
from math import floor

# MUST BE 16:9
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CELL_SIZE = 8

# deciding number of horizontal and vertical cells
num_cells_wide = int(WINDOW_WIDTH / CELL_SIZE)
num_cells_tall = int(WINDOW_HEIGHT / CELL_SIZE)

# Making the window and setting it to be in the middle of the screen (on a 1080p screen)
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption = 'Eulerian Fluid Simulation')
window.set_location(150, 100)

# Getting key functionality in Pyglet
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Batch for rendering
sprites_batch = pyglet.graphics.Batch()

# Background rectangle
background = shapes.Rectangle(x = 0, y = 0, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, color = (26, 28, 44))

colour_cells = []

def set_up():
    
    cells = []
    velos = []

    # Creating a 160 x 90 cell grid to later use the indexes for checking velocity values
    # eg cell 0 = cells[0][0] so its 4 surrounding velos are velos[1][1] etc
    for i in range(num_cells_tall):
        cells.append([])
        for j in range(num_cells_wide):
            if i == 0 or i == num_cells_tall - 1 or j == 0 or j == num_cells_wide - 1:
                cells[i].append([i, j, 0, 0])
            else:
                cells[i].append([i, j, 1, 0])
                
    # Setting up number of rows
    for i in range(183):
        velos.append([])

    # Filling odd rows with 162 values
    for i in range(1, len(velos), 2):
        for j in range(162):
            velos[i].append(0)
            
    # Filling even rows with 161 values
    for i in range(0, len(velos), 2):
        for j in range(161):
            velos[i].append(0)
            
    return cells, velos

def divergence(cells, velos):
    
    # Loop over every water cell (not border cells) and perform divergence to make the fluid incompressible
    for row in range(1, (len(cells) - 1)):
        for cell in range(1, (len(cells[row]) - 1)):
        
            # access cell x and y: cells[row][cell]
            n_velo = velos[((2 * row) + 1)][(cell + 1)]
            e_velo = velos[((2 * row) + 2)][(cell + 1)]
            s_velo = velos[((2 * row) + 3)][(cell + 1)]
            w_velo = velos[((2 * row) + 2)][(cell)]
            
            # average velocity
            avg_v = abs((n_velo + e_velo + s_velo + w_velo) / 4)
            cells[row][cell][3] = avg_v
            
            # Divergence method:
            # 1. Calculate divergence   
            # 2. Force incompressibility
            divergence = (n_velo + e_velo - s_velo - w_velo)
            
            # Accounting for walls by removing ability to add velocity in the direction of a cell wall
            s_up = cells[row - 1][cell][2]
            s_right = cells[row][cell + 1][2]
            s_down = cells[row + 1][cell][2]
            s_left = cells[row][cell - 1][2]
            
            scalar =  s_up + s_right + s_down + s_left
            
            # why negative?
            p = divergence / scalar
            
            # overrelaxation
            p *= 1.9
            
            # Updating velocities
            n_velo -= s_up * p
            e_velo -= s_right * p
            s_velo += s_down * p
            w_velo += s_left * p
            
            velos[((2 * row) + 1)][(cell + 1)] = n_velo
            velos[((2 * row) + 2)][(cell + 1)] = e_velo
            velos[((2 * row) + 3)][(cell + 1)] = s_velo
            velos[((2 * row) + 2)][(cell)] = w_velo
            
    return cells, velos

def sampleField(x, y, field, z):
    
    h = CELL_SIZE
    h1 = 1 / h
    h2 = h / 2
    
    # clamping the x and y inside the grid
    new_x = max(min(x, num_cells_wide * h), h)
    new_y = max(min(x, num_cells_tall * h), h)
    
    dx = 0
    dy = 0
    
    # Setting a blank value, pass in the 2D velocity array
    f = None
    
    match field:
        case "u_field": 
            f = z
            dy = h2
            
        case "v_field":
            f = z
            dx = h2
        case "s_field":
            f = z
            dx = h2
            dy = h2
    
    # clamping values?
    x0 = min(floor((new_x - dx) * h1), num_cells_wide - 1)
    tx = ((new_x - dx) - x0 * h) * h1
    x1 = min(x0 + 1, num_cells_wide - 1)
    
    y0 = min(floor((new_y - dy) * h1), num_cells_tall - 1)
    ty = ((new_y - dy) - y0 * h) * h1
    y1 = min(y0 + 1, num_cells_tall - 1)
    
    sx = 1 - tx
    sy = 1 - ty
    
    # interpolated velocity (either u or v) based on weighted sums
    # Turns out f is a 2D array that needs to be indexed, loop at example file
    # needs to be x0 * number of cells tall... i think, cause of his dumb index thing
    val = ((sx * sy) * (f[x0][y0])) + ((tx * sy) * (f[x1][y0])) + ((tx * ty) * (f[x1][y1])) + ((sx * ty) * (f[x0][y1]))
    
    return val
    
def advection(velos, dt):
    
# computing 2D vector at each point
    for row in range(1, len(velos) - 1):
            
        # Method for the horizontal (u) values
        if row % 2 == 0:
    
            for velo in range(1, 161):
            
                # calculating the initial particle position and velocity
                x = velo * CELL_SIZE
                y = velo * CELL_SIZE + CELL_SIZE/2
                u = velos[row][velo]
                
                # setting v component to average of surrounding v velocities
                v = (velos[row - 1][velo] + velos[row - 1][velo + 1] + velos[row + 1][velo] + velos[row + 1][velo + 1]) / 4
                
                # back calculating position
                x -= dt * u
                y -= dt * v
    
                # Taking a sample from a random point
                u = sampleField(x, y, "u_field", velos)
                
                # Updating the velocity
                velos[row][velo] = u
            
        # Method for the vertical (v) values
        else:
            
            for velo in range(1, 160):
                
                # calculating the initial particle position and velocity
                x = velo * CELL_SIZE + CELL_SIZE/2
                y = velo * CELL_SIZE
                v = velos[row][velo]
                
                # setting u component to average of surrounding u velocities
                u = (velos[row - 1][velo - 1] + velos[row - 1][velo] + velos[row + 1][velo - 1] + velos[row + 1][velo]) / 4
                
                # back calculating position
                x -= dt * u
                y -= dt * v
    
                # Taking a sample from a random point
                v = sampleField(x, y, "v_field", velos)
                
                # Updating the velocity
                velos[row][velo] = v
                                
    return velos
    
def draw():
    
    for row in range(1, 89):
        for cell in range(1, 159):
            
            # Umm x = y and y = x
            # 
            # Source cell (red)
            # if cells[row][cell][0] == 45 and cells[row][cell][1] == 80:
            #     cell_colour = shapes.Rectangle(x = (cell * CELL_SIZE), y = (row * CELL_SIZE), width = CELL_SIZE, height = CELL_SIZE, color = (255, 100, 100), batch = sprites_batch)
            #     colour_cells.append(cell_colour)
                
            # Bottom left (purple)
            if cells[row][cell][0] == 10 and cells[row][cell][1] == 10:
                cell_colour = shapes.Rectangle(x = (cell * CELL_SIZE), y = (row * CELL_SIZE), width = CELL_SIZE, height = CELL_SIZE, color = (255, 100, 255), batch = sprites_batch)
                colour_cells.append(cell_colour)
                
            # Top left (orange)
            elif cells[row][cell][0] == 80 and cells[row][cell][1] == 10:
                cell_colour = shapes.Rectangle(x = (cell * CELL_SIZE), y = (row * CELL_SIZE), width = CELL_SIZE, height = CELL_SIZE, color = (255, 130, 0), batch = sprites_batch)
                colour_cells.append(cell_colour)
                
            # Bottom right (green)
            elif cells[row][cell][0] == 10 and cells[row][cell][1] == 150:
                cell_colour = shapes.Rectangle(x = (cell * CELL_SIZE), y = (row * CELL_SIZE), width = CELL_SIZE, height = CELL_SIZE, color = (100, 255, 100), batch = sprites_batch)
                colour_cells.append(cell_colour)
                
            # Top right (blue)
            elif cells[row][cell][0] == 80 and cells[row][cell][1] == 150:
                cell_colour = shapes.Rectangle(x = (cell * CELL_SIZE), y = (row * CELL_SIZE), width = CELL_SIZE, height = CELL_SIZE, color = (100, 100, 255), batch = sprites_batch)
                colour_cells.append(cell_colour)
                
            # Fluid
            elif cells[row][cell][3] > 0.1:
                cell_colour = shapes.Rectangle(x = (cell * CELL_SIZE), y = (row * CELL_SIZE), width = CELL_SIZE, height = CELL_SIZE, color = (200, 200, 255), batch = sprites_batch)
                colour_cells.append(cell_colour)
            elif cells[row][cell][3] > 1000:
                cell_colour = shapes.Rectangle(x = (cell * CELL_SIZE), y = (row * CELL_SIZE), width = CELL_SIZE, height = CELL_SIZE, color = (200, 200, 255), batch = sprites_batch)
                colour_cells.append(cell_colour)
                print("/n")
                print(f"MEGA VELOCITY DETECTED AT: {cells[row][cell]}")
                print("\n")
            else:
                cell_colour = shapes.Rectangle(x = (cell * CELL_SIZE), y = (row * CELL_SIZE), width = CELL_SIZE, height = CELL_SIZE, color = (0, 0, 0), batch = sprites_batch)
                colour_cells.append(cell_colour)
            
cells, velos = set_up()
velos_updated = velos
cell_list = cells
        
# Running the actual functions
@window.event
def on_draw():
    
    # Clearing the window
    window.clear()
    
    # Drawing the sprites 
    sprites_batch.draw()



# Update function
def update(dt):
    
    # Global for access reasons
    global velos_updated
    global cell_list
    
    # updating velocites / running simulation
    cell_list, velos_updated = divergence(cell_list, velos_updated)
    velos_updated = advection(velos_updated, dt)
    
    # # Getting key input to impart force on the particles
    # if keys[key.LEFT]:
    #     for row in range(100, 105, 2):
    #         for value in range(80, 85):
    #             velos_updated[row][value] -= 1
    #             # value += 1
    # print(f'Rando outter: {velos_updated[2][5]}, Center: {velos_updated[42][75]}, Left: {velos_updated[36][60]}')    
    # elif keys[key.RIGHT]:
    #     for row in range(2, len(velos_updated) - 1, 2):
    #         for value in range(1, 160):
    #             velos_updated[row][value] -= 1
    #             # value += 1
    #     print(velos_updated[4][6])     
    
    
    if keys[key.LEFT]:
        velos_updated[45][80] -= 100
    print(f'source cell: {velos_updated[45][80]}, Bottom Left: {velos_updated[10][10]}, Top Left: {velos_updated[70][10]}, Bottom Right: {velos_updated[10][130]}, Top Right: {velos_updated[70][130]}')   
    
    draw()
    
    colour_cells = []
    # print(velos)
    # print("")
        

# Basically saying call the update function 60 times per second
pyglet.clock.schedule_interval(update, 1/60)
# Needs to be the last line
pyglet.app.run() 