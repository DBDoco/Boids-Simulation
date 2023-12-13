
<h1 align="center">
  Boids Simulation With Quadtree Optimization
  <br>
</h1>

<h4 align="center">Boids simulation implemented in Python. The simulation environment is visualized using  <a href="https://www.pygame.org/news">Pygame</a>, providing an interactive and visually appealing demonstration.</h4>

<p align="center">
  <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2QxMTk4NGR5c2hyNTgydGpraHp2ODVpbDV4bDJ2eXZ6NWo5bmZpbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/DitrjPJ4ybAfAMdgtG/giphy.gif" alt="boids" />
</p>

## Features

- **Flocking Behavior**: Boids exhibit cohesive, alignment, and separation behaviors, creating realistic flocking patterns.
- **QuadTree Optimization**: The simulation uses a QuadTree data structure for efficient neighbor searches, enhancing performance with a large number of agents.
- **Interactive Visualization**: The Pygame interface allows users to observe and interact with the dynamic flocking behavior in real-time.
- **Boundary Handling**: Boids are constrained within the window boundaries, preventing them from leaving the visible area.
- **Predator**: Introduced a predator with shark-like behavior, enhancing the simulation's realism and adding an additional layer of interaction with smaller boids.


## Requirements

- Python 3.x
- Pygame Library

## How To Use

Clone this repository
```bash
$ git clone https://github.com/DBDoco/boids-simulation.git
```

Go into the repository
```bash
$ cd boids-simulation
```

Install Pygame
```bash
$ pip install pygame
```

Run the script
```bash
$ py ./boids_quadtree.py
```
