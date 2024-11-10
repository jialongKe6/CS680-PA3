"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun), Zack (Wanzhi Wang)
:version: 2021.11.09
"""
import random

import ColorType
from Point import Point
from Component import Component
from Animation import Animation
from ModelTank import Tank
from ModelLinkage import Predator, Prey, Food
from EnvironmentObject import EnvironmentObject


class Vivarium(Component, Animation):
    """
    The Vivarium for our animation
    """
    components = None  # List of all components in the vivarium
    parent = None  # Parent class that has the current context
    tank = None  # The tank environment where creatures live
    tank_dimensions = None  # Dimensions of the tank
    creatures = None  # List to keep track of the creatures in the tank

    def __init__(self, parent):
        """
        Initialize the vivarium with a parent context, tank, and initial creatures.

        :param parent: The parent class that has the current context.
        """
        self.parent = parent

        self.tank_dimensions = [4, 4, 4]
        tank = Tank(parent, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))

        # Build the relationship between the tank and the vivarium
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list for later access
        self.components = [tank]
        self.creatures = []
        # Add five prey creatures and one predator creature
        self.addNewObjInTank(Prey(parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.RED))
        self.addNewObjInTank(Prey(parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.YELLOW))
        self.addNewObjInTank(Prey(parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.ORANGE))
        self.addNewObjInTank(Prey(parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
                                  ColorType.SILVER))
        self.addNewObjInTank(Prey(parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
                                  ColorType.GREEN))
        self.addNewObjInTank(Prey(parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
                                  ColorType.BLUE))
        self.addNewObjInTank(Predator(parent, Point((-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4))))

    # This function resets the vivarium
    def reset(self):
        """
        Reset the vivarium by removing all creatures and adding new ones.
        """
        for c in self.creatures:
            self.delObj(c)
        self.creatures = []
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.RED))
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.YELLOW))
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.ORANGE))
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
                                  ColorType.SILVER))
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
                                  ColorType.GREEN))
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
                                  ColorType.BLUE))
        self.addNewObjInTank(Predator(self.parent, Point((-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4))))

        self.update()
    def reset2(self):
        """
        Reset the vivarium by removing all creatures and adding new ones.
        """
        for c in self.creatures:
            self.delObj(c)
        self.creatures = []
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.RED))
        # self.addNewObjInTank(Prey(self.parent, Point(
        #     (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.YELLOW))
        # self.addNewObjInTank(Prey(self.parent, Point(
        #     (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.ORANGE))
        # self.addNewObjInTank(Prey(self.parent, Point(
        #     (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
        #                           ColorType.SILVER))
        # self.addNewObjInTank(Prey(self.parent, Point(
        #     (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
        #                           ColorType.GREEN))
        # self.addNewObjInTank(Prey(self.parent, Point(
        #     (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
        #                           ColorType.BLUE))
        self.addNewObjInTank(Predator(self.parent, Point((-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4))))

        self.update()
    # This function adds a food to the vivarium
    def add_food(self):
        """
        Add a food object to the vivarium at a random position.
        """
        self.addNewObjInTank(Food(self.parent, Point((-1.8+random.random()*3.8, 1.8, -1.8+random.random()*3.8))))
        self.update()

    def animationUpdate(self):
        """
        Update all creatures in the vivarium.
        """
        for c in self.components[::-1]:
            if isinstance(c, EnvironmentObject):
                if c.species_id == 1 or c.species_id == 0:
                    if (c.vanish_flag):
                        self.delObjInTank(c)
                        self.update()
            if isinstance(c, Animation):
                c.animationUpdate()

    def delObjInTank(self, obj):
        """
        Remove an object from the tank and the list of components.

        :param obj: The object to be removed.
        """
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            self.creatures.remove(obj)
            del obj

    # A delete function specifically called in reset()
    def delObj(self, obj):
        """
        Remove an object from the tank and the list of components.

        :param obj: The object to be removed.
        """
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent):
        """
        Add a new object to the tank and the list of components.

        :param newComponent: The object to be added.
        """
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
        if isinstance(newComponent, EnvironmentObject):
            if newComponent.species_id >= 0:
                self.creatures.append(newComponent)
            # Add environment components list reference to this new object
            newComponent.env_obj_list = self.components