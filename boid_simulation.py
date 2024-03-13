import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors defintion for boids and predators (hoiks)
BLUE = (0, 128, 255)
RED = (255, 0, 0)

# Boid and Predator properties
BOID_SPEED = 5 # speed of the boids 
BOID_RADIUS = 2.5 # radius of boids 
PREDATOR_SPEED = 2 # speed of predators
PREDATOR_RADIUS = 5 # radius of predators 
VISION_RADIUS = 100 # detection radius 

# Number of boids and predators in the simulation 
NUM_BOIDS = 100 
NUM_PREDATORS = 3 

# Normalize vector length unit 
def normalize(vector):
    length = math.sqrt(vector[0]**2 + vector[1]**2)
    if length == 0:
        return (0, 0)
    return (vector[0] / length, vector[1] / length)
# calculating distance between two points 
def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

# The base class entities in the simulation for boids and predators 
class Entity:
    def __init__(self, position, color, radius):
        self.position = position # Entity's position on the screen.
        self.color = color # Entity's color.
        self.radius = radius  # Entity's radius for drawing.

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), int(self.radius))

# class for boids 
class Boid(Entity):
    def __init__(self, position):
        super().__init__(position, BLUE, BOID_RADIUS)
        self.velocity = normalize((random.uniform(-1, 1), random.uniform(-1, 1)))  # Initialize with random direction

# Update boid's position based on flocking behaviors.
    def update(self, boids):
        alignment = self.align(boids) # Steer towards the average heading of local flockmates.
        cohesion = self.cohere(boids) # Move towards the average position of local flockmates.
        separation = self.separate(boids)  # Avoid crowding local flockmates.
 
 # Update velocity based on the combination of behaviors.
        self.velocity = normalize((self.velocity[0] + alignment[0] + cohesion[0] + separation[0],
                                   self.velocity[1] + alignment[1] + cohesion[1] + separation[1]))
        # Update position based on the new velocity.
        self.position = ((self.position[0] + self.velocity[0] * BOID_SPEED) % WIDTH,
                         (self.position[1] + self.velocity[1] * BOID_SPEED) % HEIGHT)

  # align, cohere, and separate methods are implemented here, each contributing to the boid's overall behavior.
   
    def align(self, boids):
        avg_velocity = [0, 0]
        total = 0
        for boid in boids:
            if distance(self.position, boid.position) < VISION_RADIUS and boid != self:
                avg_velocity[0] += boid.velocity[0]
                avg_velocity[1] += boid.velocity[1]
                total += 1
        if total > 0:
            avg_velocity = [avg_velocity[0] / total, avg_velocity[1] / total]
            return normalize(avg_velocity)
        return (0, 0)

    def cohere(self, boids):
        center_mass = [0, 0]
        total = 0
        for boid in boids:
            if distance(self.position, boid.position) < VISION_RADIUS and boid != self:
                center_mass[0] += boid.position[0]
                center_mass[1] += boid.position[1]
                total += 1
        if total > 0:
            center_mass = [center_mass[0] / total - self.position[0], center_mass[1] / total - self.position[1]]
            return normalize(center_mass)
        return (0, 0)

    def separate(self, boids):
        move_away = [0, 0]
        total = 0
        for boid in boids:
            dist = distance(self.position, boid.position)
            if dist < VISION_RADIUS / 2 and boid != self:
                move_away[0] += self.position[0] - boid.position[0]
                move_away[1] += self.position[1] - boid.position[1]
                total += 2
        if total > 0:
            move_away = [move_away[0] / total, move_away[1] / total]
            return normalize(move_away)
        return (0, 0)


# Generate a position far enough from existing boids to avoid overlap.
def generate_unique_position(boids, min_distance, width, height):
    while True:
        new_position = (random.randint(3, width), random.randint(3, height))
        if all(distance(new_position, boid.position) >= min_distance for boid in boids):
            return new_position

# create a list of boids with unique starting positions
def initialize_boids(num_boids, min_distance, width, height):
    boids = []
    for _ in range(num_boids):
        unique_position = generate_unique_position(boids, min_distance, width, height)
        boids.append(Boid(unique_position))
    return boids

# class representing an individual predator (hoiks)
class Predator(Entity):
    def __init__(self, position):
        super().__init__(position, RED, PREDATOR_RADIUS)
        self.velocity = normalize((random.uniform(-1, 1), random.uniform(-1, 1)))
# Update predator's position to chase and "eat" boids
    def update(self, boids):
        nearest_boid_distance = float('inf')  # Find the nearest boid to chase.
        nearest_boid = None
        for boid in boids:
            dist = distance(self.position, boid.position)
            if dist < nearest_boid_distance:
                nearest_boid_distance = dist
                nearest_boid = boid
        # Move towards the nearest boid.
        if nearest_boid is not None:
            direction = (nearest_boid.position[0] - self.position[0], nearest_boid.position[1] - self.position[1])
            self.velocity = normalize(direction)
            self.position = ((self.position[0] + self.velocity[0] * PREDATOR_SPEED) % WIDTH,
                             (self.position[1] + self.velocity[1] * PREDATOR_SPEED) % HEIGHT)

        # Check for boids to "eat"
        for boid in list(boids):  
            if distance(self.position, boid.position) <= self.radius:
                self.radius += 0.5  # Grow the predator's size
                boids.remove(boid)  # Remove the eaten boid

# Initialize boids and predators in the simulation.
boids = initialize_boids(NUM_BOIDS, 2 * BOID_RADIUS, WIDTH, HEIGHT)
predators = [Predator((random.randint(0, WIDTH), random.randint(0, HEIGHT))) for _ in range(NUM_PREDATORS)]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255)) # Clear the screen for the next frame.

  # Update and draw each boid and predator.
    for boid in boids:
        boid.update(boids)
        boid.draw()

    for predator in predators:
        predator.update(boids)
        predator.draw()

    pygame.display.flip() # Update the display with the new frame.
    pygame.time.delay(20)  # Short delay to control frame rate.

pygame.quit() # Exit Pygame when the main loop ends. 
