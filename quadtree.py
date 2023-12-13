import pygame

class Point:
    def __init__(self, boid):
        # Initialize a point with the coordinates of the boid
        self.x = boid.position.x
        self.y = boid.position.y
        self.boid = boid

class Rectangle:
    def __init__(self, x, y, hw, hh):
        # Initialize a rectangle with the center (x, y) and half-width and half-height (hw, hh)
        self.x = x
        self.y = y
        self.hw = hw
        self.hh = hh

    def contains(self, point):
        # Check if a point is within the rectangle
        does_contain = \
            point.x >= self.x - self.hw and \
            point.x < self.x + self.hw and \
            point.y >= self.y - self.hh and \
            point.y < self.y + self.hh
        return does_contain

    def intersects(self, rect_range):
        # Check if a rectangle intersects with another rectangle
        doesnt_intersect = \
            rect_range.x - rect_range.hw > self.x + self.hw or \
            rect_range.x + rect_range.hw < self.x - self.hw or \
            rect_range.y - rect_range.hh > self.y + self.hh or \
            rect_range.y + rect_range.hh < self.y - self.hh
        return not doesnt_intersect

class QuadTree:
    CAPACITY = 16

    def __init__(self, rectangle):
        # Initialize a QuadTree with a rectangle
        self.rectangle = rectangle
        self.points = []
        self.divided = False
        self.subqtrees = {}

    def subdivide(self):
        # Divide the QuadTree into four sub-trees
        hw = self.rectangle.hw / 2
        hh = self.rectangle.hh / 2
        x = self.rectangle.x
        y = self.rectangle.y

        self.subqtrees["northwest"] = QuadTree(Rectangle(x - hw, y - hh, hw, hh))
        self.subqtrees["northeast"] = QuadTree(Rectangle(x + hw, y - hh, hw, hh))
        self.subqtrees["southwest"] = QuadTree(Rectangle(x - hw, y + hh, hw, hh))
        self.subqtrees["southeast"] = QuadTree(Rectangle(x + hw, y + hh, hw, hh))
        self.divided = True

    def insert(self, point):
        # Insert a point into the appropriate sub-tree
        if len(self.points) < QuadTree.CAPACITY and not self.divided:
            self.points.append(point)
        else:
            if not self.divided:
                self.subdivide()
                for existing_point in self.points:
                    self.insert(existing_point)
                self.points = []
            for subqt in self.subqtrees.values():
                if subqt.rectangle.contains(point):
                    subqt.insert(point)

    def query(self, rect_range):
        # Query points within a specified area
        found = []
        if self.rectangle.intersects(rect_range):
            found.extend([point.boid for point in self.points])

            if self.divided:
                found.extend(self.subqtrees["northwest"].query(rect_range))
                found.extend(self.subqtrees["northeast"].query(rect_range))
                found.extend(self.subqtrees["southwest"].query(rect_range))
                found.extend(self.subqtrees["southeast"].query(rect_range))

        return found

    def draw(self, screen):
        # Draw the QuadTree on the screen
        rect = pygame.Rect(self.rectangle.x - self.rectangle.hw, self.rectangle.y - self.rectangle.hh,
                            self.rectangle.hw * 2, self.rectangle.hh * 2)
        pygame.draw.rect(screen, (100, 100, 0), rect, 1)
        if self.divided:
            for subqt in self.subqtrees.values():
                subqt.draw(screen)
