import pyglet
from pyglet import shapes
from math import hypot, atan, acos, asin

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360
GRAVITY = 9.8
NUMBER_OF_PARTICLES = 2
PARTICLE_RADIUS = 20
SPACING = -2
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
    
    def __init__(self, index, offset = 0, colour = PARTICLE_COLOUR, radius = PARTICLE_RADIUS, x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 2) -> None:
        self.circle = shapes.Circle(x = x + (offset / 2.01), y = y + offset, radius = PARTICLE_RADIUS, color = colour, batch = shapes_batch)
        self.circle.opacity = 200
        self.index = index
        self.velocity = [0, 0]

    def update_ball(self, dt):
        dt = dt/DT_SCALE
        self.velocity[1] -= GRAVITY
        # Keep in the boundary
        if self.circle.y < self.circle.radius:
            self.circle.y = self.circle.radius
            self.velocity[1] *= -ELASTICTY
        if self.circle.y > WINDOW_HEIGHT - self.circle.radius:
            self.circle.y = WINDOW_HEIGHT - self.circle.radius
            self.velocity[1] *= -ELASTICTY
        if self.circle.x < self.circle.radius:
            self.circle.x = self.circle.radius
            self.velocity[0] *= -ELASTICTY
        if self.circle.x > WINDOW_WIDTH - self.circle.radius:
            self.circle.x = WINDOW_WIDTH - self.circle.radius
            self.velocity[0] *= -ELASTICTY
                
        self.circle.x += self.velocity[0] * dt
        self.circle.y += self.velocity[1] * dt
    
        # self.velocity[0] *= 0.9
        # self.velocity[1] *= 0.9

# Shapes
background = shapes.Rectangle(x = 0, y = 0, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, color = (26, 28, 44), batch = shapes_batch)

# Generating some particles (change later)
offset = -(NUMBER_OF_PARTICLES * PARTICLE_RADIUS * 2 + (SPACING * NUMBER_OF_PARTICLES)) / 2

# for i in range(NUMBER_OF_PARTICLES):
#     particles.append(Particle(i, offset))
#     particle_index_pos[i] = (particles[i].circle.x, particles[i].circle.y)
#     offset += PARTICLE_RADIUS * 2 + SPACING

particles.append(Particle(0, 50))
particles.append(Particle(1, 0, (177, 62, 83)))
particle_index_pos[0] = (particles[0].circle.x, particles[0].circle.y)
particle_index_pos[1] = (particles[1].circle.x, particles[1].circle.y)

# Running the actual functions
@window.event
def on_draw():
    window.clear()
    shapes_batch.draw()
    
def update(dt):
    dt = dt/DT_SCALE
    
    for particle in particles:
        particle_index_pos[particle.index] = (particles[particle.index].circle.x, particles[particle.index].circle.y)
    
    for i in range(len(particles)-1):
        particle = particle_index_pos[i]
        # Loop over every other particle
        for j in range(i+1, len(particles)):
            other = particle_index_pos[j]
            x1, y1 = particle
            x2, y2 = other
            # Calculate the distance between them
            distance = hypot(x2 - x1, y2 - y1)
            if distance <= 2 * PARTICLE_RADIUS:
                if abs(distance) == 0:
                    distance = 0.0000000000000000000000000000000000000000000000000001
                
                point_of_collision_x = ((x2 - x1) / (PARTICLE_RADIUS * 2))
                point_of_collision_y = ((y2 - y1) / (PARTICLE_RADIUS * 2))
                print(f'X collision: {point_of_collision_x}, Y collision: {point_of_collision_y}')
                
                # Drawing the point where the circles collide
                global point
                point = shapes.Circle(x = particles[0].circle.x + point_of_collision_x * PARTICLE_RADIUS, y = particles[0].circle.y + point_of_collision_y * PARTICLE_RADIUS, radius = 3, color = (255, 205, 117), batch = shapes_batch)
                point.draw()
                
        particles[i].update_ball(dt)
    particles[-1].update_ball(dt)
    

# Basically saying call the update function 60 times per second
pyglet.clock.schedule_interval(update, 1/60)
# Needs to be the last line
pyglet.app.run() 