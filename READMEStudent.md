# Jialong Ke
# No collaborator
# CS680
# PA3

## Introduction
This project extends a 3D vivarium simulation with creature modeling, animation, and interactive behaviors. Polyhedral creatures are introduced with unique features and animations, including predator-prey interactions, collision detection within boundaries, and group dynamics. This repository is organized with modular components for easy maintenance and extension.
It simulates a 3D vivarium with animated polyhedral creatures that interact and move within a confined space. Predators and prey are visually distinguished, and the simulation includes boundary containment, orientation, and potential group behaviors. The design suggests a visually engaging environment for studying simulated creature behaviors and interactions.
The techniques used in this vivarium include but are not limited to the following:
1. Using quaternion to perform arbitrary angle rotation.
2. Tank wall as potential functions so the fish will try to turn when approaching the edges.
3. Prey will try to keep group movement.
4. The predator  will try to eat the prey, and the prey will try to eat the food.
5. the richness of multiple prey.