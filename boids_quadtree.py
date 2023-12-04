import pygame
import random
from quadtree import QuadTree, Point, Rectangle

screen_size = 800
MARGIN = screen_size * 0.05

class Boid:
    NUM_BOIDS = 100
    DISTANCE_VISIBLE = 42
    DISTANCE_SEPERATION = 20
    MAX_SPEED = 0.1
    COHERENCE_FACTOR  = 0.0001
    ALIGNMENT_FACTOR  = 0.008
    SEPARATION_FACTOR = 0.001
    
    def __init__(self, color=(0,255,255)):
        # Inicijalizacija boida s bojom i nasumičnom pozicijom i brzinom
        self.position = pygame.math.Vector2(random.randint(0, screen_size), random.randint(0, screen_size))
        self.velocity = pygame.math.Vector2(random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED), random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED))
        self.velocity_buffer = self.velocity.copy()
        self.color = color
    
    def cohere(self, boids):
        # Središte mase: Pronalaženje prosječne pozicije vidljivih boida i prilagođavanje brzine prema tom smjeru
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
        # Poravnanje: Pronalaženje prosječne brzine vidljivih boida i prilagođavanje brzine prema tom smjeru
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
        # Razdvajanje: Udaljavanje od drugih boida u blizini kako bi se izbjegli sudari
        move_away = pygame.math.Vector2(0, 0)

        for other_boid in boids:
            if other_boid != self and self.position.distance_to(other_boid.position) < Boid.DISTANCE_SEPERATION:
                move_away += self.position - other_boid.position

        self.velocity_buffer += Boid.SEPARATION_FACTOR * move_away
    
    def keep_in_bounds(self):
        # Držanje unutar granica prozora
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
        # Ažuriranje pozicije temeljeno na trenutnoj brzini
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
        
        # Kreiranje QuadTree-a kao korijenskog čvora
        qtree = QuadTree(Rectangle(screen_size / 2, screen_size / 2, screen_size / 2, screen_size / 2))
        # Ubacivanje svih boida (kao točaka) u QuadTree
        for boid in boids:
            qtree.insert(Point(boid))

        for boid in boids:
            # Definiranje područja oko boida koje će se uzeti u obzir prilikom traženja drugih boida
            rect_range = Rectangle(boid.position.x, boid.position.y, Boid.DISTANCE_VISIBLE / 2, Boid.DISTANCE_VISIBLE / 2)
            # Pronalaženje boida unutar područja pomoću QuadTree upita
            inrange_boids = qtree.query(rect_range)

            # Filtriranje vidljivih, bliskih i udaljenih boida
            visible_boids = [other_boid for other_boid in inrange_boids if boid.position.distance_to(other_boid.position) < Boid.DISTANCE_VISIBLE]
            close_boids = [other_boid for other_boid in inrange_boids if boid.position.distance_to(other_boid.position) < Boid.DISTANCE_SEPERATION]
            far_visible_boids = [other_boid for other_boid in inrange_boids if boid.position.distance_to(other_boid.position) >= Boid.DISTANCE_SEPERATION]

            # Primjena pravila ponašanja na boid
            boid.cohere(far_visible_boids)
            boid.align(far_visible_boids)
            boid.separate(close_boids)
            
            # Održavanje unutar granica prozora, ažuriranje pozicije i crtanje na ekranu
            boid.keep_in_bounds()
            boid.update_position()
            pygame.draw.circle(screen, boid.color, (int(boid.position.x), int(boid.position.y)), 2)
            
        # Crtanje QuadTree-a na ekranu
        qtree.draw(screen)

        pygame.display.update()

main()
