# Importing libraries
import pyglet
from pyglet import shapes
from pyglet.window import key
from math import hypot, floor

# Constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360
GRAVITY = 9.8
NUMBER_OF_PARTICLES = 150
PARTICLE_RADIUS = 10
CELL_SIZE = 2 * PARTICLE_RADIUS
SPACING = 20
PARTICLE_COLOUR = (65, 166, 246) # From the Sweetie 16 Palette
DT_SCALE = 1
ELASTICTY = 0.4
SEPERATION_FACTOR = 2

# Function that calculates the dot product of 2 vectors
def dot_2d(x1, x2, y1, y2):
    return (x1*x2) + (y1*y2)
   
# List of particles and a dictionary with particle indexes and positions 
particles = []
particle_index_pos = {}

# Creating dictionary and number of grid cells
cells = {}
cells_tall = (WINDOW_HEIGHT // CELL_SIZE) + 1
cells_wide = (WINDOW_WIDTH // CELL_SIZE) + 1

# Creating the dictionary that is all the cell coords and the empty lists that will hold which particles are in them
for y in range(cells_tall):
    for x in range(cells_wide):
        cells[(x, y)] = []

# Making the window and setting it to be in the middle of the screen (on a 1080p screen)
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption = 'Fluid Simulation')
window.set_location(440, 240)

# Getting key functionality in Pyglet
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Batch for rendering
sprites_batch = pyglet.graphics.Batch()

# Loading in the image used to simulate the blur
particle_image = pyglet.image.load("Particle.png")

images = []

# Particle Class
class Particle:
    
    # Initiation method
    def __init__(self, index, colour = PARTICLE_COLOUR, x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 2) -> None:
        self.circle = shapes.Circle(x = x, y = y, radius = PARTICLE_RADIUS, color = colour)
        self.circle.opacity = 200
        self.index = index
        self.velocity = [0, 0]

    # Function to update the particle's position each frame
    def update_particle(self, dt):
        dt = dt/DT_SCALE
        self.velocity[1] -= GRAVITY

        # Keep in the boundary | if the particle hits an edge move it back inside the boundary and reverse its velocity
        if self.circle.y <= self.circle.radius:
            self.circle.y = self.circle.radius
            self.velocity[1] *= -ELASTICTY
        if self.circle.y >= WINDOW_HEIGHT - self.circle.radius:
            self.circle.y = WINDOW_HEIGHT - self.circle.radius - 5
            self.velocity[1] *= -ELASTICTY
        if self.circle.x <= self.circle.radius:
            self.circle.x = self.circle.radius
            self.velocity[0] *= -ELASTICTY
        if self.circle.x >= WINDOW_WIDTH - self.circle.radius:
            self.circle.x = WINDOW_WIDTH - self.circle.radius
            self.velocity[0] *= -ELASTICTY
             
        # Applying the updated velocities to the particle's position
        self.circle.x += self.velocity[0] * dt
        self.circle.y += self.velocity[1] * dt
    
# Background rectangle
background = shapes.Rectangle(x = 0, y = 0, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, color = (26, 28, 44))

colour = int(255 / NUMBER_OF_PARTICLES)

# Generating the particles
for i in range(NUMBER_OF_PARTICLES):
    particles.append(Particle(i, (65, 166, 246), i, i))
    particle_index_pos[i] = (particles[i].circle.x, particles[i].circle.y)
    
    # Creating the sprites to place on each particle
    single_particle_image = pyglet.sprite.Sprite(particle_image, particles[i].circle.x, particles[i].circle.y, batch = sprites_batch)
    single_particle_image.scale = PARTICLE_RADIUS / 454.5454545454545
    images.append(single_particle_image)
    
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
    
    # Getting key input to impart force on the particles
    if keys[key.SPACE]:
        for i in range(len(particles)):
            particles[i].velocity[1] += 40
    if keys[key.LEFT]:
        for i in range(len(particles)):
            particles[i].velocity[0] -= 12
    if keys[key.RIGHT]:
        for i in range(len(particles)):
            particles[i].velocity[0] += 12
            
    # Updating the delta time to be in slomo or not
    dt = dt/DT_SCALE
    
    for y in range(cells_tall):
        for x in range(cells_wide):
            cells[(x, y)] = []
    
    # Creating the dictionary of particle indexes and positions
    for particle in particles:
        
        # Adding
        cell_x = particles[particle.index].circle.x // CELL_SIZE
        cell_y = particles[particle.index].circle.y // CELL_SIZE
        
        # Ensuring we dont go outside the grid
        if cell_x < 0:
            cell_x = 0
        if cell_x > cells_wide - 1:
            cell_x = cells_wide - 1
        if cell_y < 0:
            cell_y = 0
        if cell_y > cells_tall - 1:
            cell_y = cells_tall - 1
        
        cells[(cell_x, cell_y)].append(particle.index)
        
        particle_index_pos[particle.index] = (particles[particle.index].circle.x, particles[particle.index].circle.y)
            
    
    # Looping over every particle
    for i in range(len(particles) - 1):
        
        # Getting the x, y position of the particle from dictionary containing it
        particle_pos = particle_index_pos[i]
        
        # Getting grid position of cell (with decimal)
        x = particle_pos[0] / CELL_SIZE
        y = particle_pos[1] / CELL_SIZE
        
        # Getting the int grid coords of where the particle is
        cell_coords = [floor(x), floor(y)]
        
        # Finding just the value after the decimal place, eg 3.71 becomes 0.71
        x_dec = x - cell_coords[0]
        y_dec = y - cell_coords[1]
        
        check_cells = []
        
        # Collecting four surrounding cells to check for collisions using that decimal value
        # For x
        if x_dec > 0.5 and cell_coords[0] < cells_wide:
            check_cells.append(1)
        elif x_dec < 0.5 and cell_coords[0] > 0:
            check_cells.append(-1)
        else:
            check_cells.append(0)
            
        # For y
        if y_dec > 0.5 and cell_coords[1] < cells_tall:
            check_cells.append(1)
        elif y_dec < 0.5 and cell_coords[1] > 0:
            check_cells.append(-1)
        else:
            check_cells.append(0)
        
        # Creaing a list of cells that need to be looped over (aka the four cells the particle is laying between)
        # Has to be list to alter values, wish it could be a set
        cells_to_loop_over = [cell_coords, [cell_coords[0] + check_cells[0], cell_coords[1]], [cell_coords[0], cell_coords[1] + check_cells[1]], [cell_coords[0] + check_cells[0], cell_coords[1] + check_cells[1]]]
        
        # Creating the list of particles in those cells
        particles_in_collision_cells = []
        
        # For every cell we need to check add particles in those cells to a list
        for cell in cells_to_loop_over:
            
            # Keeping cell coords in the predefined grid size
            if cell[0] < 0:
                cell[0] = 0
            if cell[0] > cells_wide - 1:
                cell[0] = cells_wide - 1
            if cell[1] < 0:
                cell[1] = 0
            if cell[1] > cells_tall - 1:
                cell[1] = cells_tall - 1
            
            # Adding particles that need to be collided with into a list
            for particle in cells[tuple(cell)]:
                particles_in_collision_cells.append(particle)
            
        # Looping over every particle in said list and running collision code    
        for j in particles_in_collision_cells:
            
            # Getting the other particles position 
            other_pos = particle_index_pos[j]
            
            # Assigning the positions to variables
            x1, y1 = particle_pos
            x2, y2 = other_pos
            
            # Calculate the distance between them
            distance = hypot(abs(x1 - x2), abs(y1 - y2))
            
            # Checking if the particles collided
            if distance <= 2 * PARTICLE_RADIUS:
                
                # Avoiding divide by 0 error
                if abs(distance) == 0:
                    distance = 0.0000000000000000000000000000000000000000000000000001
                
                # This section of math is taken from Eric Leong: https://ericleong.me/research/circle-circle/#dynamic-circle-circle-collision
                
                # Finding the normal of the collision
                norm_of_vector_x = (x2 - x1) / distance
                norm_of_vector_y = (y2 - y1) / distance
                
                # p = How closely particle 1's vector is alligned with the collision vector - How closely particle 2's vector is alligned with the collision vector
                p = (dot_2d(particles[i].velocity[0], norm_of_vector_x, particles[i].velocity[1], norm_of_vector_y)) - (dot_2d(particles[j].velocity[0], norm_of_vector_x, particles[j].velocity[1], norm_of_vector_y))
                
                # Updating the particle velocities based on the previous calculations
                particles[i].velocity[0] -= (p * norm_of_vector_x)
                particles[i].velocity[1] -= (p * norm_of_vector_y)
                particles[j].velocity[0] += (p * norm_of_vector_x)
                particles[j].velocity[1] += (p * norm_of_vector_y)
                # -----------------------------------------------------------------------------------------------------------------------------
                
                # This forces the particles apart by moving the particles apart along the normalised vectors
                particles[i].circle.x -= norm_of_vector_x * SEPERATION_FACTOR
                particles[i].circle.y -= norm_of_vector_y * SEPERATION_FACTOR
                particles[j].circle.x += norm_of_vector_x * SEPERATION_FACTOR
                particles[j].circle.y += norm_of_vector_y * SEPERATION_FACTOR
        
        # Scale factor
        scale_factor = ((PARTICLE_RADIUS / 454.5454545454545) * 100)
        
        # Updating the position of the sprite to match the position of the particle  
        images[i].x = particles[i].circle.x - PARTICLE_RADIUS * scale_factor
        images[i].y = particles[i].circle.y - PARTICLE_RADIUS * scale_factor
        
    # Updating the last particle's image location
    images[-1].x = particles[-1].circle.x - PARTICLE_RADIUS * scale_factor
    images[-1].y = particles[-1].circle.y - PARTICLE_RADIUS * scale_factor
             
    # Looping over every particle and updating them   
    for i in range(len(particles)):
        particles[i].update_particle(dt)
    
# Basically saying call the update function 60 times per second
pyglet.clock.schedule_interval(update, 1/60)
# Needs to be the last line
pyglet.app.run() 