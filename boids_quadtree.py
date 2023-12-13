import pygame
import random
from quadtree import QuadTree, Point, Rectangle

screen_size = 800
MARGIN = screen_size * 0.05

class Boid:
    NUM_BOIDS = 100
    DISTANCE_VISIBLE = 42
    DISTANCE_SEPARATION = 20
    MAX_SPEED = 0.1
    COHERENCE_FACTOR  = 0.0001
    ALIGNMENT_FACTOR  = 0.008
    SEPARATION_FACTOR = 0.001
    
    def __init__(self, color=(0,255,255)):
        # Initialize a boid with color and random position and velocity
        self.position = pygame.math.Vector2(random.randint(0, screen_size), random.randint(0, screen_size))
        self.velocity = pygame.math.Vector2(random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED), random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED))
        self.velocity_buffer = self.velocity.copy()
        self.color = color
    
    def cohere(self, boids):
        # Center of Mass: Find the average position of visible boids and adjust velocity towards that direction
        center_of_mass = pygame.math.Vector2(0, 0)
        count = 0

        for other_boid in boids:
            if other_boid != self and self.position.distance_to(other_boid.position) < Boid.DISTANCE_VISIBLE:
                center_of_mass += other_boid.position
                count += 1

        if count > 0:
            center_of_mass /= count
            self.velocity_buffer += Boid.COHERENCE_FACTOR * (center_of_mass - self.position)

    def align(self, boids):
        # Alignment: Find the average velocity of visible boids and adjust velocity towards that direction
        avg_velocity = pygame.math.Vector2(0, 0)
        count = 0

        for other_boid in boids:
            if other_boid != self and self.position.distance_to(other_boid.position) < Boid.DISTANCE_VISIBLE:
                avg_velocity += other_boid.velocity
                count += 1

        if count > 0:
            avg_velocity /= count
            self.velocity_buffer += Boid.ALIGNMENT_FACTOR * (avg_velocity - self.velocity)

    def separate(self, boids):
        # Separation: Move away from other nearby boids to avoid collisions
        move_away = pygame.math.Vector2(0, 0)

        for other_boid in boids:
            if other_boid != self and self.position.distance_to(other_boid.position) < Boid.DISTANCE_SEPARATION:
                move_away += self.position - other_boid.position

        self.velocity_buffer += Boid.SEPARATION_FACTOR * move_away
    
    def keep_in_bounds(self):
        # Keep within the window boundaries
        TURN_FACTOR = 0.01
        turn = Boid.MAX_SPEED * TURN_FACTOR
        if self.position.x < MARGIN:
            self.velocity_buffer.x += turn
        if self.position.x > screen_size - MARGIN:
            self.velocity_buffer.x -= turn
        if self.position.y < MARGIN:
            self.velocity_buffer.y += turn
        if self.position.y > screen_size - MARGIN:
            self.velocity_buffer.y -= turn
    
    def update_position(self):
        # Update position based on the current velocity
        if self.velocity_buffer.length() > Boid.MAX_SPEED:
            self.velocity_buffer *= 0.9
        self.velocity = self.velocity_buffer.copy()
        self.position += self.velocity

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_size, screen_size))
    
    color_range = {"a": 50, "b": 255}
    boids = [Boid((random.randint(**color_range),
                   random.randint(**color_range),
                   random.randint(**color_range))) for _ in range(Boid.NUM_BOIDS)]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        screen.fill((0,0,0))
        
        # Create QuadTree as the root node
        qtree = QuadTree(Rectangle(screen_size / 2, screen_size / 2, screen_size / 2, screen_size / 2))
        # Insert all boids (as points) into the QuadTree
        for boid in boids:
            qtree.insert(Point(boid))

        for boid in boids:
            # Define the area around the boid to consider when searching for other boids
            rect_range = Rectangle(boid.position.x, boid.position.y, Boid.DISTANCE_VISIBLE / 2, Boid.DISTANCE_VISIBLE / 2)
            # Find boids within the area using QuadTree queries
            inrange_boids = qtree.query(rect_range)

            # Filter visible, close, and far boids
            visible_boids = [other_boid for other_boid in inrange_boids if boid.position.distance_to(other_boid.position) < Boid.DISTANCE_VISIBLE]
            close_boids = [other_boid for other_boid in inrange_boids if boid.position.distance_to(other_boid.position) < Boid.DISTANCE_SEPARATION]
            far_visible_boids = [other_boid for other_boid in inrange_boids if boid.position.distance_to(other_boid.position) >= Boid.DISTANCE_SEPARATION]

            # Apply behavior rules to the boid
            boid.cohere(far_visible_boids)
            boid.align(far_visible_boids)
            boid.separate(close_boids)
            
            # Keep within window bounds, update position, and draw on the screen
            boid.keep_in_bounds()
            boid.update_position()
            pygame.draw.circle(screen, boid.color, (int(boid.position.x), int(boid.position.y)), 2)
            
        # Draw the QuadTree on the screen
        qtree.draw(screen)

        pygame.display.update()

main()
