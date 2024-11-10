"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun), Zack (Wanzhi Wang)
:version: 2021.11.09
"""
import random
import math

from Component import Component
from Point import Point
import ColorType as Ct
from Displayable import Displayable
from Animation import Animation
from EnvironmentObject import EnvironmentObject
from Vivarium import Tank
from DisplayableSphere import DisplayableSphere
from DisplayableHalfRoundCylinder import DisplayableHalfRoundCylinder
from DisplayableCylinder import DisplayableCylinder
from DisplayableRoundCylinder import DisplayableRoundCylinder

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, linkageLength=0.5, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        link1 = Component(Point((0, 0, 0)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link1.setDefaultColor(Ct.DARKORANGE1)
        link2 = Component(Point((0, 0, linkageLength)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link2.setDefaultColor(Ct.DARKORANGE2)
        link3 = Component(Point((0, 0, linkageLength)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link3.setDefaultColor(Ct.DARKORANGE3)
        link4 = Component(Point((0, 0, linkageLength)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link4.setDefaultColor(Ct.DARKORANGE4)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        self.components = [link1, link2, link3, link4]


class HookLinkage(Component):
    """
    Define a linkage that forms an arm of a hook
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, linkageLength=0.5, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        joint = Component(Point((0, 0, 0)),
                          DisplayableSphere(self.contextParent, linkageLength))
        joint.setDefaultColor(Ct.SILVER)
        part1 = Component(Point((0, 0, 0)),
                          DisplayableCube(self.contextParent, 1,
                                          [linkageLength * 0.8, linkageLength * 0.8, linkageLength * 4]))
        part1.setDefaultColor(Ct.SILVER)
        part2 = Component(Point((0, 0, linkageLength * 3.7)),
                          DisplayableCube(self.contextParent, 1,
                                          [linkageLength * 0.8, linkageLength * 0.8, linkageLength * 3]))
        part2.setDefaultColor(Ct.SILVER)
        part2.setDefaultAngle(part2.uAxis, 60)

        self.addChild(joint)
        joint.addChild(part1)
        part1.addChild(part2)

        self.components = [joint]


class BodyLinkage(Component):
    """
    Define a linkage that forms the body of an Android
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, color, LinkageLength=0.1, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        topBody = Component(Point((0, 0, 0)),
                            DisplayableHalfRoundCylinder(self.contextParent, 1 * LinkageLength, 0.5 * LinkageLength))
        topBody.setDefaultColor(color)
        topBody.vRange = [-90, 90]

        head = Component(Point((0, 1 * LinkageLength, 0.6 * LinkageLength)),
                         DisplayableSphere(self.contextParent, 0.8 * LinkageLength))
        head.setDefaultColor(color)
        head.uRange = [-65, 45]
        head.vRange = [-73, 73]
        head.wRange = [-20, 20]

        botBody = Component(Point((0, 0, 0)),
                            DisplayableCylinder(self.contextParent, 1 * LinkageLength, 1 * LinkageLength))
        botBody.setDefaultColor(color)

        leftEye = Component(Point((-0.35 * LinkageLength, 0.2 * LinkageLength, 0.66 * LinkageLength)),
                            DisplayableSphere(self.contextParent, 0.1 * LinkageLength))
        leftEye.setDefaultColor(Ct.RED)
        leftEye.uRange = [-45, 45]
        leftEye.vRange = [-45, 45]

        rightEye = Component(Point((0.35 * LinkageLength, 0.2 * LinkageLength, 0.66 * LinkageLength)),
                             DisplayableSphere(self.contextParent, 0.1 * LinkageLength))
        rightEye.setDefaultColor(Ct.RED)
        rightEye.uRange = [-45, 45]
        rightEye.vRange = [-45, 45]

        self.addChild(topBody)
        self.addChild(botBody)
        topBody.addChild(head)
        head.addChild(leftEye)
        head.addChild(rightEye)

        self.components = []


class ArmLinkage(Component):
    """
    Define a linkage that forms the arm of an Android
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, color, LinkageLength=0.1, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        self.chained_rotate = 1

        humeri = Component(Point((0, 0, 0)),
                           DisplayableCylinder(self.contextParent, 0.1 * LinkageLength, 0.5 * LinkageLength))
        humeri.setDefaultColor(color)
        humeri.setDefaultAngle(humeri.wAxis, 90)
        humeri.uRange = [-225, 45]
        humeri.wRange = [90, 90]

        shoulder = Component(Point((0, 0, -0.25 * LinkageLength)), DisplayableCube(self.contextParent, 1,
                                                                                   [0.4 * LinkageLength,
                                                                                    0.25 * LinkageLength,
                                                                                    0.8 * LinkageLength]))
        shoulder.setDefaultColor(color)
        shoulder.uRange = [-20, 5]
        # Since the children of shoulder does not contain any joint,
        # we chain shoulder and its children so they can be colored together when selected.
        shoulder.chained_child = 1

        upperArm = Component(Point((0, 0, 0.8 * LinkageLength)),
                             DisplayableHalfRoundCylinder(self.contextParent, 0.1 * LinkageLength, 0.4 * LinkageLength))
        upperArm.setDefaultColor(color)
        upperArm.setDefaultAngle(upperArm.uAxis, 90)

        foreArm = Component(Point((0, 0.4 * LinkageLength, 0)),
                            DisplayableRoundCylinder(self.contextParent, 0.1 * LinkageLength, 0.3 * LinkageLength))
        foreArm.setDefaultColor(color)
        foreArm.uRange = [0, 20]
        foreArm.vRange = [-45, 45]
        foreArm.wRange = [-110, 0]

        hand = Component(Point((0, 0.3 * LinkageLength, 0)), DisplayableCube(self.contextParent, 1,
                                                                             [0.4 * LinkageLength, 0.25 * LinkageLength,
                                                                              0.8 * LinkageLength]))
        hand.setDefaultAngle(hand.uAxis, -90)
        hand.setDefaultColor(color)
        hand.uRange = [-120, -60]
        hand.vRange = [-20, 20]
        hand.wRange = [-90, 90]

        self.setDefaultAngle(self.uAxis, 90)

        self.addChild(humeri)
        humeri.addChild(shoulder)
        shoulder.addChild(upperArm)
        upperArm.addChild(foreArm)
        foreArm.addChild(hand)

        self.components = [humeri]


class LegLinkage(Component):
    """
    Define a linkage that forms the leg of an Android
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, color, LinkageLength=0.1, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        self.chained_rotate = 1

        thigh = Component(Point((0, 0, 0)),
                          DisplayableCylinder(self.contextParent, 0.2 * LinkageLength, 0.2 * LinkageLength))
        thigh.setDefaultColor(color)
        thigh.setDefaultAngle(thigh.wAxis, 90)
        thigh.uRange = [-30, 30]
        thigh.wRange = [90, 90]
        # Since the children of thigh does not contain any joint,
        # we chain thigh and its children so they can be colored together when selected.
        thigh.chained_child = 1

        leg = Component(Point((0, -0.1 * LinkageLength, -0.5 * LinkageLength)), DisplayableCube(self.contextParent, 1,
                                                                                                [0.4 * LinkageLength,
                                                                                                 0.2 * LinkageLength,
                                                                                                 0.5 * LinkageLength]))
        leg.setDefaultColor(color)
        # Since the children of leg does not contain any joint,
        # we chain leg and its children so they can be colored together when selected.
        leg.chained_child = 1

        foot = Component(Point((0, 0, -0.1 * LinkageLength)), DisplayableCube(self.contextParent, 1,
                                                                              [1.6 * LinkageLength, 0.7 * LinkageLength,
                                                                               0.1 * LinkageLength]))
        foot.setDefaultColor(color)

        self.setDefaultAngle(self.uAxis, -90)

        self.addChild(thigh)
        thigh.addChild(leg)
        leg.addChild(foot)

        self.components = [thigh]


class DisplayableCube(Displayable):
    """
    Create a enclosed cylinder whose one end is at z=0 and it grows along z coordinates
    """

    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    scale = None
    edgeLength = 1
    _bufferData = None

    def __init__(self, parent, edgeLength, scale=None):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.edgeLength = edgeLength
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale

    def draw(self):
        gl.glCallList(self.callListHandle)

    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        v_l = [
            [-self.edgeLength / 2, -self.edgeLength / 2, -self.edgeLength / 2],
            [self.edgeLength / 2, -self.edgeLength / 2, -self.edgeLength / 2],
            [self.edgeLength / 2, self.edgeLength / 2, -self.edgeLength / 2],
            [- self.edgeLength / 2, self.edgeLength / 2, -self.edgeLength / 2],
            [- self.edgeLength / 2, -self.edgeLength / 2, self.edgeLength / 2],
            [self.edgeLength / 2, -self.edgeLength / 2, self.edgeLength / 2],
            [self.edgeLength / 2, self.edgeLength / 2, self.edgeLength / 2],
            [- self.edgeLength / 2, self.edgeLength / 2, self.edgeLength / 2],
        ]

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()

        gl.glScale(*self.scale)
        gl.glTranslate(0, 0, self.edgeLength / 2)

        # a primitive cube
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex3f(*v_l[1])
        gl.glVertex3f(*v_l[0])
        gl.glVertex3f(*v_l[3])
        gl.glVertex3f(*v_l[2])

        gl.glVertex3f(*v_l[4])
        gl.glVertex3f(*v_l[5])
        gl.glVertex3f(*v_l[6])
        gl.glVertex3f(*v_l[7])

        gl.glVertex3f(*v_l[0])
        gl.glVertex3f(*v_l[4])
        gl.glVertex3f(*v_l[7])
        gl.glVertex3f(*v_l[3])

        gl.glVertex3f(*v_l[7])
        gl.glVertex3f(*v_l[6])
        gl.glVertex3f(*v_l[2])
        gl.glVertex3f(*v_l[3])

        gl.glVertex3f(*v_l[5])
        gl.glVertex3f(*v_l[1])
        gl.glVertex3f(*v_l[2])
        gl.glVertex3f(*v_l[6])

        gl.glVertex3f(*v_l[0])
        gl.glVertex3f(*v_l[1])
        gl.glVertex3f(*v_l[5])
        gl.glVertex3f(*v_l[4])

        gl.glEnd()

        gl.glPopMatrix()
        gl.glEndList()


class Predator(Component, Animation, EnvironmentObject):
    """
    Define a predator object (hook)
    """
    components = None
    rotation_speed = None
    translation_speed = None
    up_vector = Point((0, 1, 0))
    local_n_vector = None
    local_v_vector = None
    local_u_vector = None

    def __init__(self, parent, position):
        super(Predator, self).__init__(position)
        hook1 = HookLinkage(parent, Point((0, 0, 0)), 0.05)
        hook2 = HookLinkage(parent, Point((0, 0, 0)), 0.05)
        hook2.setDefaultAngle(hook2.vAxis, 180)
        self.setDefaultAngle(self.vAxis, 270)

        self.components = hook1.components + hook2.components
        self.addChild(hook1)
        self.addChild(hook2)

        self.rotation_speed = []
        for comp in self.components:
            comp.setRotateExtent(comp.uAxis, 0, 50)
            self.rotation_speed.append([1, 0, 0])

        self.translation_speed = Point([random.random() - 0.5 for _ in range(3)]).normalize() * 0.05
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.2
        self.species_id = 2

        self.target_prey = None  # Currently pursued prey
        self.perception_distance = 3.5  # Perception range, adjustable as needed
        self.catch_distance = 0.1  # Catch distance, defines success when close enough to prey

        self.initialize()

    def animationUpdate(self):
        # Create a periodic animation for predator joints
        for i, comp in enumerate(self.components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            if comp.uAngle in comp.uRange:
                self.rotation_speed[i][0] *= -1

        tank = None  # For storing the tank object

        # If there is no current target or the target is invalid, find a new target
        if self.target_prey is None or self.target_prey.vanish_flag:
            min_distance_prey = float('inf')
            min_distance_food = float('inf')
            closest_food = None

            # Traverse environment objects to find prey and food
            for item in self.env_obj_list:
                if isinstance(item, Tank):
                    tank = item  # Store tank object for wall collision handling later
                elif isinstance(item, EnvironmentObject):
                    if item.species_id == 1:  # Find prey
                        distance = (item.current_position - self.current_position).norm()
                        if distance < min_distance_prey and distance <= self.perception_distance:
                            min_distance_prey = distance
                            self.target_prey = item  # Lock onto a new prey target
                    elif item.species_id == 0:  # Find food
                        distance = (item.current_position - self.current_position).norm()
                        if distance < min_distance_food and distance <= self.perception_distance:
                            min_distance_food = distance
                            closest_food = item  # Find the nearest food

            # If no prey is found, and food is found, set food as the target
            if self.target_prey is None and closest_food is not None:
                self.target_prey = closest_food  # Set food as the target

        # Handle logic for pursuing prey or eating food
        if self.target_prey is not None:
            # Get direction to target and set speed
            direction_to_target = (self.target_prey.current_position - self.current_position).normalize()
            self.translation_speed = direction_to_target * 0.015  # Predator speed

            # Check if target is caught
            distance_to_prey = (self.target_prey.current_position - self.current_position).norm()
            if distance_to_prey <= self.catch_distance:
                # Successful catch, mark target as vanished
                self.target_prey.vanish_flag = True
                self.target_prey = None  # Unlock target

        # If there is no target, set a fixed random direction
        if self.target_prey is None and not hasattr(self, 'patrol_direction'):
            # Generate a random direction for initial patrol
            self.patrol_direction = Point([random.uniform(-1, 1) for _ in range(3)]).normalize() * 0.005

        # Set current patrol direction as speed
        if self.target_prey is None:
            self.translation_speed = self.patrol_direction

        # Handle wall collision
        if tank is not None:
            next_position = self.current_position + self.translation_speed
            for i in range(3):  # For x, y, z axes
                if not (-tank.tank_dimensions[i] / 2 + self.bound_radius <
                        next_position[i] <
                        tank.tank_dimensions[i] / 2 - self.bound_radius):
                    # Reverse speed on the corresponding axis to achieve bounce and change patrol direction
                    self.translation_speed.coords[i] *= -1
                    self.patrol_direction = self.translation_speed  # Update patrol direction

        # Update orientation (keep facing movement direction)
        if self.translation_speed.norm() > 0:
            self.local_n_vector = self.translation_speed.normalize()
            self.local_v_vector = self.local_n_vector.cross3d(self.up_vector).normalize()
            self.local_u_vector = self.local_n_vector.cross3d(self.local_v_vector).normalize()
            self.pre_rotation_matrix = [
                [self.local_n_vector.coords[0], self.local_n_vector.coords[1], self.local_n_vector.coords[2], 0],
                [self.local_v_vector.coords[0], self.local_v_vector.coords[1], self.local_v_vector.coords[2], 0],
                [self.local_u_vector.coords[0], self.local_u_vector.coords[1], self.local_u_vector.coords[2], 0],
                [0, 0, 0, 1]
            ]

        # Update position
        self.current_position = self.current_position + self.translation_speed
        self.bound_center += self.translation_speed  # Update boundary center
        self.update()

class Prey(Component, Animation, EnvironmentObject):
    """
    Define a prey object (An Android)
    """
    components = None
    rotation_speed = None
    translation_speed = None
    up_vector = Point((0, 1, 0))
    local_x_vector = None
    local_y_vector = None
    local_z_vector = None
    vanish_flag = False

    def __init__(self, parent, position, color):
        super(Prey, self).__init__(position)
        body = BodyLinkage(parent, Point((0, 0, 0)), color)
        body.setDefaultAngle(body.wAxis, 180)

        rightArm = ArmLinkage(parent, Point((-0.13, 0.05, -0.005)), color)
        leftArm = ArmLinkage(parent, Point((0.13, 0.05, -0.005)), color)

        rightLeg = LegLinkage(parent, Point((-0.05, -0.1, 0)), color)
        leftLeg = LegLinkage(parent, Point((0.03, -0.1, 0)), color)

        body.addChild(rightArm)
        body.addChild(leftArm)
        body.addChild(rightLeg)
        body.addChild(leftLeg)

        self.components = body.components + rightArm.components + leftArm.components + leftLeg.components + rightLeg.components
        self.addChild(body)
        self.rotation_speed = []
        self.collision_cooldown = 0

        for i in range(4):
            self.components[i].setRotateExtent(self.components[i].uAxis, -45, 45)
            if i % 2 == 0:
                self.rotation_speed.append([2, 0, 0])
            if i % 2 == 1:
                self.rotation_speed.append([-2, 0, 0])

        self.translation_speed = Point([random.random() - 0.5 for _ in range(3)]).normalize() * 0.02

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.2
        self.species_id = 1

        self.initialize()

    def animationUpdate(self):
        # Update prey "walking motion" animation
        for i, comp in enumerate(self.components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            if comp.uAngle in comp.uRange:
                self.rotation_speed[i][0] *= -1  # Reverse direction when rotation reaches limit

        # Update cooldown timer
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1  # Reduce cooldown timer each frame

        closest_food = None
        min_distance_food = float('inf')
        is_being_chased = False
        closest_predator = None
        min_distance_predator = float('inf')
        chase_distance = 0.5  # Detection distance for pursuit, adjustable as needed
        tank = None  # For storing the tank object

        # Traverse environment objects to detect predators and food, store tank object
        for item in self.env_obj_list:
            if isinstance(item, Tank):
                tank = item  # Store tank object for wall collision handling later
            elif isinstance(item, EnvironmentObject):
                if item.species_id == 2:  # Predator
                    distance = (item.current_position - self.current_position).norm()
                    if distance < min_distance_predator:
                        min_distance_predator = distance
                        closest_predator = item  # Find the nearest predator
                    if distance < chase_distance:
                        is_being_chased = True  # Being pursued by a predator
                    if distance <= (item.bound_radius + self.bound_radius):
                        self.vanish_flag = True  # Caught by a predator, disappear
                elif item.species_id == 1 and item != self:
                    # Collision with other prey; handle collision bounce if cooldown has ended
                    if (item.current_position - self.current_position).norm() <= (
                            item.bound_radius + self.bound_radius) and self.collision_cooldown == 0:
                        # Handle collision bounce to avoid frequent direction changes causing jitter
                        self.translation_speed = self.translation_speed.reflect(
                            item.current_position - self.current_position)
                        item.translation_speed = item.translation_speed.reflect(
                            self.current_position - item.current_position)
                        # Set collision cooldown to avoid frequent direction adjustments
                        self.collision_cooldown = 10
                        item.collision_cooldown = 10
                elif item.species_id == 0:  # Food
                    # Only choose food that is not locked by another prey
                    if not hasattr(item, 'locked_by') or item.locked_by is None or item.locked_by == self:
                        distance = (item.current_position - self.current_position).norm()
                        if distance < min_distance_food:
                            min_distance_food = distance
                            closest_food = item  # Find the nearest available food

        if is_being_chased and closest_predator is not None:
            # If being pursued, prioritize fleeing, set speed away from the predator
            direction_away_from_predator = (self.current_position - closest_predator.current_position).normalize()
            self.translation_speed = direction_away_from_predator * 0.02  # Escape speed, adjustable
            # Unlock the food
            if closest_food and hasattr(closest_food, 'locked_by') and closest_food.locked_by == self:
                closest_food.locked_by = None

        elif closest_food is not None:
            # If not pursued, move towards the nearest food
            if hasattr(closest_food, 'locked_by') and closest_food.locked_by is None:
                closest_food.locked_by = self  # Lock food to itself
            direction_to_food = (closest_food.current_position - self.current_position).normalize()
            self.translation_speed += direction_to_food * 0.005  # Adjust speed increment as needed
            self.translation_speed = self.translation_speed.normalize() * 0.02

        # Update position
        self.current_position = self.current_position + self.translation_speed
        self.bound_center += self.translation_speed  # Update boundary center

        # Reinforce boundary check to ensure prey stays within bounds
        if tank is not None:
            for i in range(3):  # For x, y, z axes
                if self.current_position[i] > tank.tank_dimensions[i] / 2 - self.bound_radius:
                    # Exceeds positive boundary
                    self.current_position.coords[i] = tank.tank_dimensions[i] / 2 - self.bound_radius
                    if is_being_chased:
                        # When cornered by a predator, choose a direction to slide along the wall
                        self.translation_speed.coords[i] = 0
                        wall_axes = [0, 1, 2]
                        wall_axes.remove(i)  # Use the remaining two axes to slide along the wall
                        direction_away_from_predator = (self.current_position - closest_predator.current_position)
                        projected_direction = Point([direction_away_from_predator.coords[axis] for axis in wall_axes])

                        if projected_direction.norm() > 0:
                            normalized_direction = projected_direction.normalize()
                            for idx, axis in enumerate(wall_axes):
                                self.translation_speed.coords[axis] = normalized_direction.coords[idx] * 0.02
                        else:
                            # If direction cannot be determined, choose a random direction to avoid "bobbing"
                            for axis in wall_axes:
                                self.translation_speed.coords[axis] = random.uniform(-0.02, 0.02)
                    else:
                        # If not being chased, bounce back normally
                        self.translation_speed.coords[i] *= -1
                elif self.current_position[i] < -tank.tank_dimensions[i] / 2 + self.bound_radius:
                    # Exceeds negative boundary
                    self.current_position.coords[i] = -tank.tank_dimensions[i] / 2 + self.bound_radius
                    if is_being_chased:
                        # When cornered by a predator, choose a direction to slide along the wall
                        self.translation_speed.coords[i] = 0
                        wall_axes = [0, 1, 2]
                        wall_axes.remove(i)  # Use the remaining two axes to slide along the wall
                        direction_away_from_predator = (self.current_position - closest_predator.current_position)
                        projected_direction = Point([direction_away_from_predator.coords[axis] for axis in wall_axes])

                        if projected_direction.norm() > 0:
                            normalized_direction = projected_direction.normalize()
                            for idx, axis in enumerate(wall_axes):
                                self.translation_speed.coords[axis] = normalized_direction.coords[idx] * 0.02
                        else:
                            # If direction cannot be determined, choose a random direction to avoid "bobbing"
                            for axis in wall_axes:
                                self.translation_speed.coords[axis] = random.uniform(-0.02, 0.02)
                    else:
                        # If not being chased, bounce back normally
                        self.translation_speed.coords[i] *= -1

        # Update orientation (keep facing movement direction)
        if self.translation_speed.norm() > 0:
            self.local_z_vector = self.translation_speed.normalize()
            self.local_x_vector = self.local_z_vector.cross3d(self.up_vector).normalize()
            self.local_y_vector = self.local_z_vector.cross3d(self.local_x_vector).normalize()
            self.pre_rotation_matrix = [
                [self.local_x_vector.coords[0], self.local_x_vector.coords[1], self.local_x_vector.coords[2], 0],
                [self.local_y_vector.coords[0], self.local_y_vector.coords[1], self.local_y_vector.coords[2], 0],
                [self.local_z_vector.coords[0], self.local_z_vector.coords[1], self.local_z_vector.coords[2], 0],
                [0, 0, 0, 1]
            ]

        self.update()

class Food(Component, Animation, EnvironmentObject):
    """
    Defines a food object.
    """
    components = None
    translation_speed = None
    local_n_vector = None
    local_v_vector = None
    local_u_vector = None
    vanish_flag = False

    def __init__(self, parent, position):
        super(Food, self).__init__(position)
        food = Component(Point((0, 0, 0)), DisplayableSphere(parent, 0.03))
        food.setDefaultColor(Ct.DARKGREEN)

        self.components = [food]
        self.addChild(food)
        self.initialize()

        self.translation_speed = Point([0, -0.02, 0])
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1
        self.species_id = 0

    def animationUpdate(self):

        for item in self.env_obj_list:
            # Collision detection (tank)
            if isinstance(item, Tank):
                if not (item.tank_dimensions[0] / 2 - self.bound_radius) > (
                        self.current_position[0] + self.translation_speed[0]) > (
                               -item.tank_dimensions[0] / 2 + self.bound_radius):
                    self.translation_speed.coords[0] = 0
                if not (item.tank_dimensions[1] / 2 - self.bound_radius > self.current_position[1] +
                        self.translation_speed[1] > -item.tank_dimensions[1] / 2 + self.bound_radius):
                    self.translation_speed.coords[1] = 0
                if not (item.tank_dimensions[2] / 2 - self.bound_radius > self.current_position[2] +
                        self.translation_speed[2] > -item.tank_dimensions[2] / 2 + self.bound_radius):
                    self.translation_speed.coords[2] = 0

            # Collision detection (creature), if collide, the object vanishes.
            elif isinstance(item, EnvironmentObject):
                if item.species_id > self.species_id:
                    if (item.current_position - self.current_position).norm() <= (
                            item.bound_radius + self.bound_radius):
                        self.vanish_flag = True

        self.current_position = self.current_position + self.translation_speed
        self.update()
