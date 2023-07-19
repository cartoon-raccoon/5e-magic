from abc import ABC, abstractmethod

class ClassTable(object):
    pass

class Class(ABC):
    """
    An abstract class representing a 5e player class.

    Do not instantiate this class, create classes that inherit from this.
    """

    @abstractmethod
    def class_table(self) -> ClassTable:
        """
        Return the class table of this particular class.
        """
        pass

    @abstractmethod
    def features(self, level):
        """
        Return the features gained by the class at `level`.
        """
        pass