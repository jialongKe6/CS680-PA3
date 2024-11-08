'''
Define animation interface at here, which is used to control update of our object by frame.
:author: xxx
:version: 2024.11.1
'''

class Animation:
    """
    Abstract class used for animation object. Object inherit from this should implement animationUpdate method.
    """
    def animationUpdate(self):
        """
        Called when animation object need to update
        """
        raise NotImplementedError("animationUpdate method not implemented yet")