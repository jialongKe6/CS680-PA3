"""
An object which defines a half-round cylinder for rendering

:author: micou(Zezhou Sun), Zack (Wanzhi Wang)
:version: 2021.11.09
"""
import os
import numpy as np
import string

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
        import OpenGL.GLUT as glut  # this fails on OS X 11.x
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
        import OpenGL.GLUT as glut
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError

from Displayable import Displayable


class DisplayableHalfRoundCylinder(Displayable):
    """
    Create a enclosed half-round cylinder whose one end is at z=0 and it grows along z coordinates.
    This class is used for rendering a half-cylinder in 3D space.
    """
    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    scale = None
    radius = 1
    height = 1
    _bufferData = None

    def __init__(self, parent, radius, height, scale=None):
        """
        Initialize a new instance of DisplayableHalfRoundCylinder.

        :param parent: The parent object that has the current OpenGL context.
        :param radius: The radius of the half-cylinder.
        :param height: The height of the half-cylinder.
        :param scale: An optional scale factor for the half-cylinder.
        """
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.radius = radius
        self.height = height
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale

    def draw(self):
        """
        Draw the half-round cylinder using the current OpenGL context.
        """
        gl.glCallList(self.callListHandle)

    def initialize(self):
        """
        Initialize the OpenGL display list for the half-round cylinder.
        """
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()

        gl.glScale(*self.scale)

        # Rotate the cylinder to align it with the z-axis
        gl.glRotate(-90, 1, 0, 0)

        # Draw the top disk of the half-cylinder
        gl.glRotate(180, 1, 0, 0)
        glu.gluDisk(self.qd, 0, self.radius, 36, 18)

        # Translate down to the bottom of the cylinder
        gl.glTranslate(0, 0, -self.height)

        # Draw the side of the half-cylinder
        glu.gluCylinder(self.qd,
                        self.radius, self.radius,
                        self.height, 36, 18)

        # Draw the bottom sphere of the half-cylinder
        glu.gluSphere(self.qd, self.radius, 36, 18)

        gl.glPopMatrix()
        gl.glEndList()