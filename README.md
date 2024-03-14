# boid_simulation-


This project simulates the flocking behavior of birds using a simple set of rules applied to each boid (bird-oid object). The simulation includes predators (referred to as "hoiks") that chase and "eat" boids. As predators consume boids, they grow larger.

## Features

- Boids that flock together using three basic principles: alignment, cohesion, and separation.
- Predators that chase the nearest boid and grow in size when they "eat" a boid.
- Customizable parameters for the speed, size, and vision radius of both boids and predators.

## Getting Started

### Prerequisites

The simulation requires Python and Pygame. Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/). You'll also need Pygame, which can be installed using pip:

```bash
pip install pygame
