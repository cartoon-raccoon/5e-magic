from abc import ABC, abstractmethod
from enum import Enum

from . import SpellEffect, Damage

class Target(ABC):
    """
    A generic target of a spell.

    This can either be an object or a character, and their
    behaviour differs based on this quality.

    `Target` defines two self-explanatory abstract methods: `heal` and `damage`.
    Classes inheriting from this class are expected to override these
    methods with their own implementations.
    """

    @abstractmethod
    def heal(self, amount: int):
        pass

    @abstractmethod
    def damage(self, ty: Damage):
        pass

class CreatureState(Enum):
    """
    Indicates the state of a creature.
    """
    ALIVE = 0
    DEAD = 1

class Creature(Target):
    """
    A subclass of Target that is a living creature.

    You should not instantiate this class directly,
    instead create subclasses of this class representing
    the Target more directly, e.g. if a spell is
    targeting a commoner, then create a Commoner subclass
    of this class.
    """

    def __init__(self, max_hp: int, ac: int):
        self.max = max_hp
        self.hp = max_hp
        self.ac = ac
        self.state = CreatureState.ALIVE

    def heal(self, amount: int):
        self.hp += amount

        # cap hp at max if healed to full
        if self.hp > self.max:
            self.hp = self.max

    def damage(self, damage: Damage) -> CreatureState:
        """
        Damages the creature, accounting for any vulnerabilities or
        resistances it might have.

        In this generic `Creature` class, this simply deals damage as-is.

        This should only be called if the damage can actually be dealt,
        i.e. failed save or passing attack roll.
        """
        self.hp -= damage.amount
        if self.hp <= 0:
            self.state = CreatureState.DEAD
            return CreatureState.DEAD
        else:
            return CreatureState.ALIVE


class ObjectState(Enum):
    """
    """
    WHOLE = 0
    DESTROYED = 1


class Object(Target):
    """
    A subclass of Target that is an inanimate object.

    You should not instantiate this class directly,
    instead create subclasses of this class representing
    the Target more directly, e.g. if a spell is
    targeting a rope, then create a Rope subclass
    of this class.
    """

    def __init__(self, max_hp, threshold):
        # the maximum hp this object can have.
        self.max = max_hp
        # the current hp of the object.
        self.hp = max_hp

        self.threshold = threshold

    def heal(self, amount: int):
        """
        Heals (or mends) the object by the given amount.
        """
        self.hp += amount

        # cap hp at max if healed to full
        if self.hp > self.max:
            self.hp = self.max


    def damage(self, damage: Damage):
        """
        Damages the object, accounting for damage threshold
        and any vulnerabilities and resistances the object might have.
        """
        if damage.amount > self.threshold:
            # do the damage
            pass

    def reinforce(self, effect: SpellEffect):
        """
        Raises the damage threshold of the object.
        """
        pass