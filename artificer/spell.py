from enum import Enum
from abc import ABC, abstractmethod

from typing import Any

from .target import Target

class Component(object):
    """
    Abstract type representing a spell component.
    """
    VERBAL = 0
    SOMATIC = 1
    MATERIAL = 2

    def __init__(self, ty: int, details: Any):
        self.ty = ty
        self.detail = details

    def details(self) -> tuple[int, object]:
        """
        Return information on its type and details, if any.

        Generally, its details will only be not None if
        its type is `Component.MATERIAL`.
        """
        return (self.ty, self.detail)


class Spell(ABC):
    """
    Abstract class representing a 5e Spell.
    All other Spells inherit from this class.

    This type cannot be instantiated.
    """

    @abstractmethod
    def components(self) -> list:
        """When called, returns the components needed.
        """
        pass

    @abstractmethod
    def cast(self, components, roll, target: Target):
        """Casts the spell.
        """
        pass


class SpellEffect(ABC):
    """
    The result of a spell. This can either be healing
    or damage of some type, or some arbitrary effect
    to account for spells that do neither.

    For the purposes of ergonomics, healing is implemented
    as "negative" damage, i.e. gives HP instead of taking away.
    """

    @abstractmethod
    def take_effect(self, target: Target):
        """
        Run the desired effect on the Target.
        """
        pass


class DamageType(Enum):
    ACID = "Acid"
    BLUDGEONING = "Bludgeoning"
    COLD = "Cold"
    FIRE = "Fire"
    FORCE = "Force"
    LIGHTNING = "Lightning"
    NECROTIC = "Necrotic"
    PIERCING = "Piercing"
    POISON = "Poison"
    PSYCHIC = "Psychic"
    RADIANT = "Radiant"
    SLASHING = "Slashing"
    THUNDER = "Thunder"


class Damage(SpellEffect):
    """
    Damage caused by a spell.
    """
    def __init__(self, ty: DamageType, amount: int):
        self.ty = ty
        self.amount = amount

    def take_effect(self, target: Target):
        # just deal the damage, the target will
        # account for its own resistances and vulns
        target.damage(self)


class Healing(SpellEffect):
    """
    A healing effect of a spell.
    """
    def __init__(self, value: int):
        self.value = value

    def take_effect(self, target: Target):
        target.heal(self.value)