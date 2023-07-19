"""
Superclasses for all elements of a spell.
"""

from enum import Enum, IntEnum
from abc import ABC, abstractmethod
from typing import Any

from .target import Target
from .error import *

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
    
class SpellLevel(IntEnum):
    """
    The level a spell is cast at.

    All spells have a MINIMUM_LEVEL and
    MAXIMUM_LEVEL class attribute that
    determines the lower and upper bounds of
    that spell's level.

    Generally, all non-cantrip spells will
    have a MAXIMUM_LEVEL of `SpellLevel.LEVEL5`.
    """
    CANTRIP = 0
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3
    LEVEL4 = 4
    LEVEL5 = 5

    # ...what? you were expecting higher? psh, this is
    # for artificers only, level 5 is as high as we go.
    # now piss off.

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

class Spell(ABC):
    """
    Abstract class representing a D&D 5e Spell.
    All other Spells inherit from this class.

    This type cannot be instantiated.
    """

    MINIMUM_LEVEL = SpellLevel.LEVEL1
    MAXIMUM_LEVEL = SpellLevel.LEVEL5

    @abstractmethod
    def components(self) -> list[str]:
        """When called, returns the components needed as strings.
        """
        pass

    @abstractmethod
    def cast(self, components, roll) -> SpellEffect:
        """Casts the spell.
        """
        pass


class Cantrip(Spell):
    """
    The superclass for all Cantrips.

    This class does not override the abstract methods
    specified in Spell, so attempting to cast those
    will lead to an error.

    Generally, you should create your own sub-cantrip
    by inheriting from this class and overriding the
    methods specified.
    """

    # cantrips are a special class of spell that
    # scale according to class level, not spell
    # slot level, so their min and max levels
    # are both SpellLevel.CANTRIP.
    MINIMUM_LEVEL = SpellLevel.CANTRIP
    MAXIMUM_LEVEL = SpellLevel.CANTRIP

    def __init__(self, class_level: int, components: list[Component]):
        self.class_level = class_level
        self.provided_components = components


class LeveledSpell(Spell):
    """
    The superclass for all Leveled Spells (i.e. Level 1 and up).
    """

    MINIMUM_LEVEL = SpellLevel.LEVEL1
    MAXIMUM_LEVEL = SpellLevel.LEVEL5

    def __init__(self, level: SpellLevel, components: list[Component]):
        if level < self.MINIMUM_LEVEL:
            raise LevelError(level, self.MINIMUM_LEVEL)
        self.given_comps = components

