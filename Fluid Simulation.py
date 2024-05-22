import pyglet
from pyglet import shapes
from math import hypot

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360
GRAVITY = 9.8
NUMBER_OF_PARTICLES = 10
PARTICLE_RADIUS = 10
SPACING = -2
# Sweetie 16 Palette
PARTICLE_COLOUR = (65, 166, 246)
COLLISION_FORCE = 400
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
    
    def __init__(self, index, offset, radius = PARTICLE_RADIUS, x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 2) -> None:
        self.circle = shapes.Circle(x = x + offset, y = y + offset, radius = PARTICLE_RADIUS, color = PARTICLE_COLOUR, batch = shapes_batch)
        self.circle.opacity = 200
        self.index = index
        self.velocity = [0, 0]

    def update_ball(self, dt):
        dt = dt/DT_SCALE
        self.velocity[1] -= GRAVITY
        # self.circle.y -= self.speed
        
        # Keep in the boundary
        if self.circle.y < self.circle.radius:
            self.circle.y = self.circle.radius
            # if self.speed < 3:
            #     self.speed = 0
            # else:
            #     # Bounce
            self.velocity[1] *= -ELASTICTY
        if self.circle.y > WINDOW_HEIGHT - self.circle.radius:
            self.circle.y = WINDOW_HEIGHT - self.circle.radius
            self.velocity[1] *= -ELASTICTY
        if self.circle.x < 0:
            self.circle.x = self.circle.radius
            self.velocity[0] *= -ELASTICTY
        elif self.circle.x > WINDOW_WIDTH:
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

for i in range(NUMBER_OF_PARTICLES):
    particles.append(Particle(i, offset))
    particle_index_pos[i] = (particles[i].circle.x, particles[i].circle.y)
    offset += PARTICLE_RADIUS * 2 + SPACING

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
                # particle_vel_x = particles[i].velocity[0]
                # particle_vel_y = particles[i].velocity[1]
                # other_vel_x = particles[j].velocity[0]
                # other_vel_y = particles[j].velocity[1]
                # dist_x = x1 - x2
                # dist_y = y1 - y2
                # dot_prod = (dist_x*particle_vel_x + dist_y*particle_vel_y) / (dist_x**2 + dist_y**2)
                
                # particles[i].velocity[0] += 2 * dist_x * dot_prod
                # particles[i].velocity[1] += 2 * dist_y * dot_prod
                # particles[j].velocity[0] = 0
                # particles[j].velocity[1] = 0
                if (x2 - x1) <= 0: # j to the left of i
                    particles[i].velocity[0] += (COLLISION_FORCE/abs(distance))
                    particles[j].velocity[0] -= (COLLISION_FORCE/abs(distance))
                else: # j to the right of i
                    particles[i].velocity[0] -= (COLLISION_FORCE/abs(distance))
                    particles[j].velocity[0] += (COLLISION_FORCE/abs(distance))
                    
                if (y2 - y1) <= 0:
                    particles[i].velocity[1] += (COLLISION_FORCE/abs(distance))
                    particles[j].velocity[0] -= (COLLISION_FORCE/abs(distance))
                else:
                    particles[i].velocity[1] -= (COLLISION_FORCE/abs(distance))
                    particles[j].velocity[1] += (COLLISION_FORCE/abs(distance))
                
                # Later, use math to find the point of collision on the circle and apply a force in that direction to push the other particles away
                
        particles[i].update_ball(dt)
    particles[-1].update_ball(dt)

# Basically saying call the update function 60 times per second
pyglet.clock.schedule_interval(update, 1/60)
# Needs to be the last line
pyglet.app.run() 