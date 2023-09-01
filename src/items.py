from typing import List, Type


class Item:
    def __init__(self, name: str) -> None:
        self._name: str = name

    def get_name(self) -> str:
        return self._name


class Weapon(Item):
    def __init__(self, name: str, damage: int) -> None:
        super().__init__(name)
        self._damage = damage

    def get_damage(self) -> int:
        return self._damage


class Armor(Item):
    def __init__(self, name: str, protection: int) -> None:
        super().__init__(name)
        self._protection: int = protection

    def get_protection(self) -> int:
        return self._protection


class Consumable(Item):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class HealthPotion(Consumable):
    def __init__(self) -> None:
        super().__init__("Lebenstrank")


class ManaPotion(Consumable):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class RedManaPotion(ManaPotion):
    def __init__(self) -> None:
        super().__init__("Roter Mana Trank")


class BlueManaPotion(ManaPotion):
    def __init__(self) -> None:
        super().__init__("Blauer Mana Trank")


class Sword(Weapon):
    def __init__(self) -> None:
        super().__init__("Schwert", 10)


class Axe(Weapon):
    def __init__(self) -> None:
        super().__init__("Axt", 3)


class Shield(Armor):
    def __init__(self) -> None:
        super().__init__("Schild", 10)


all_weapons: List[Type[Item]] = [Sword]
all_armor: List[Type[Item]] = [Shield]
all_consumables: List[Type[Item]] = [BlueManaPotion, RedManaPotion, HealthPotion]
all_items: List[Type[Item]] = all_weapons + all_armor + all_consumables
