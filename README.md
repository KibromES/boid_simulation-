# Boid Simulation Project

This Python project simulates the flocking behavior in birds, and is simulated as boids, alongside the inclusion of predators (termed "hoiks") that interact with these boids by chasing and consuming them. As the simulation progresses, predators increase in size with each boid they successfully "eat".

## Features

- **Flocking Simulation:** Implements a simplified model of flocking behavior based on three core rules - alignment, cohesion, and separation, allowing for the organic formation and movement of boid flocks.
- **Predator Mechanics:** Introduces predators into the ecosystem, which pursue and consume nearby boids, growing in size with each one they eat, providing an additional layer of interaction within the simulation.
- **Customization:** Offers the ability to adjust various parameters including the speed, size, and vision radius of both boids and predators to experiment with different dynamics within the simulation.

## Getting Started

### Prerequisites

Before running the simulation, you will need to have Python installed on your system as well as the Pygame library, which is used for rendering the simulation.

- **Python:** The project is developed with Python. If you do not have Python installed, visit [python.org](https://www.python.org/downloads/) to download and install it.
- **Pygame:** Pygame is required for running the simulation, which provides the necessary functions for rendering and event handling.

### Installation

To get started with the boid simulation, first ensure that Python is installed on your system. Then, install Pygame using pip, Python's package installer. Open your terminal or command prompt and execute the following command:

```bash
pip install pygame
