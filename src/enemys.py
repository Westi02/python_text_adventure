from typing import List, Type

from src.items import Item


class Enemy:
    def __init__(self, name: str, inventory: List[Item], max_health: int, attack: int, defense: int) -> None:
        self._name: str = name
        self._inventory: List[Item] = inventory
        self._max_health: int = max_health
        self._current_health: int = max_health
        self._attack: int = attack
        self._defense: int = defense

    def get_name(self) -> str:
        return self._name

    def get_inventory(self) -> List[Item]:
        return self._inventory

    def get_attack(self) -> int:
        return self._attack

    def get_defense(self) -> int:
        return self._defense

    def get_max_health(self) -> int:
        return self._max_health

    def get_current_health(self) -> int:
        return self._current_health

    def set_health(self, health: int) -> None:
        self._current_health = health


class ButterGolem(Enemy):
    def __init__(self, inventory: List[Item]) -> None:
        super().__init__("Buttergolem", inventory, 150, 1, 15)


class RiverTroll(Enemy):
    def __init__(self, inventory: List[Item]) -> None:
        super().__init__("Flusstroll", inventory, 70, 5, 10)


all_enemys: List[Type[Enemy]] = [ButterGolem, RiverTroll]
