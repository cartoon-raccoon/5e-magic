"""
Various errors pertaining to the casting of spells.
"""

from .spell import SpellLevel

class LevelError(Exception):
    """
    An exception raised when a spell is cast at a level 
    incompatible with its specification (e.g. casting
    Invisibility at Level 1)
    """

    def __init__(self, tried_level: SpellLevel, required_level: SpellLevel):
        self.tried = tried_level
        self.required = required_level
    
    def __repr__(self):
        return f"LevelError(tried: {self.tried}, required: {self.required})"
    
    def __str__(self):
        return f"LevelError: Required level {self.required}, was cast with {self.tried}"


class ComponentError(Exception):
    """
    An exception raised when a spell is cast without
    the required components, or with incorrect
    components.
    """