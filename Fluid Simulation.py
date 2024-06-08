import pyglet
from pyglet import shapes
from math import hypot, atan, acos, asin

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360
GRAVITY = 9.8
NUMBER_OF_PARTICLES = 2
PARTICLE_RADIUS = 10
SPACING = 20
# Sweetie 16 Palette
PARTICLE_COLOUR = (65, 166, 246)
COLLISION_FORCE = 40
DT_SCALE = 1
ELASTICTY = 0.2

particles = []
particle_index_pos = {}

# Making the window and setting it to be in the middle of the screen (on a 1080p screen)
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption = 'Fluid Simulation')
window.set_location(440, 240)

# Batch for rendering
shapes_batch = pyglet.graphics.Batch()

# Particle Class
class Particle:
    
    def __init__(self, index, colour = PARTICLE_COLOUR, x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 2) -> None:
        self.circle = shapes.Circle(x = x, y = y, radius = PARTICLE_RADIUS, color = colour, batch = shapes_batch)
        self.circle.opacity = 200
        self.index = index
        self.velocity = [0, 0]

    def update_ball(self, dt):
        dt = dt/DT_SCALE
        self.velocity[1] -= GRAVITY

        # Keep in the boundary
        if self.circle.y <= self.circle.radius:
            self.circle.y = self.circle.radius
            self.velocity[1] *= -ELASTICTY
        if self.circle.y >= WINDOW_HEIGHT - self.circle.radius:
            self.circle.y = WINDOW_HEIGHT - self.circle.radius
            self.velocity[1] *= -ELASTICTY
        if self.circle.x <= self.circle.radius:
            self.circle.x = self.circle.radius
            self.velocity[0] *= -ELASTICTY
        if self.circle.x >= WINDOW_WIDTH - self.circle.radius:
            self.circle.x = WINDOW_WIDTH - self.circle.radius
            self.velocity[0] *= -ELASTICTY
                
        self.circle.x += self.velocity[0] * dt
        self.circle.y += self.velocity[1] * dt
    
# Shapes
background = shapes.Rectangle(x = 0, y = 0, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, color = (26, 28, 44), batch = shapes_batch)


# for i in range(NUMBER_OF_PARTICLES):
#     particles.append(Particle(i, (i, i, i)))
#     particle_index_pos[i] = (particles[i].circle.x, particles[i].circle.y)

particles.append(Particle(0, (177, 62, 83), 300, 200))
particles.append(Particle(1, (239, 125, 87), 290, 150))
particles.append(Particle(2, (255, 205, 117), 350, 250))
particles.append(Particle(3, (56, 183, 100), 350, 300))
particles.append(Particle(4, (65, 166, 246), 250, 100))
particle_index_pos[0] = (particles[0].circle.x, particles[0].circle.y)
particle_index_pos[1] = (particles[1].circle.x, particles[1].circle.y)
particle_index_pos[2] = (particles[2].circle.x, particles[2].circle.y)
particle_index_pos[3] = (particles[3].circle.x, particles[3].circle.y)
particle_index_pos[4] = (particles[4].circle.x, particles[4].circle.y)

# Running the actual functions
@window.event
def on_draw():
    window.clear()
    shapes_batch.draw()
    
def update(dt):
    dt = dt/DT_SCALE
    
    for particle in particles:
        particle_index_pos[particle.index] = (particles[particle.index].circle.x, particles[particle.index].circle.y)
        
    for i in range(len(particles) - 1):
        particle_pos = particle_index_pos[i]
        # Loop over every other particle
        for j in range(i + 1, len(particles)):
            other_pos = particle_index_pos[j]
            x1, y1 = particle_pos
            x2, y2 = other_pos
            # Calculate the distance between them
            distance = hypot(x1 - x2, y1 - y2)
            
            if distance <= 2 * PARTICLE_RADIUS:
                print("COLLISION")
                if abs(distance) == 0:
                    distance = 0.0000000000000000000000000000000000000000000000000001
                
                # This section of math is taken from Eric Leong: https://ericleong.me/research/circle-circle/#dynamic-circle-circle-collision
                
                # Finding the norm of the vectors
                norm_of_vector_x = (x2 - x1) / distance
                norm_of_vector_y = (y2 - y1) / distance
                
                # I believe this is the relative velocity?
                p = (particles[i].velocity[0] * norm_of_vector_x) + (particles[i].velocity[1] * norm_of_vector_y)
                
                # Updating the particle velocities based on the previous calculations
                particles[i].velocity[0] -= (p * norm_of_vector_x)
                particles[i].velocity[1] -= (p * norm_of_vector_y)
                particles[j].velocity[0] += (p * norm_of_vector_x)
                particles[j].velocity[1] += (p * norm_of_vector_y)
                # -----------------------------------------------------------------------------------------------------------------------------
                
    for i in range(len(particles)):
        particles[i].update_ball(dt)
    

# Basically saying call the update function 60 times per second
pyglet.clock.schedule_interval(update, 1/60)
# Needs to be the last line
pyglet.app.run() 