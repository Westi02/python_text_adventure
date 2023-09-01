import math
import time
from typing import List, Callable, Tuple

from src.io_manager import IOManager
from src.items import Item, HealthPotion, RedManaPotion, BlueManaPotion


class Player:
    def __init__(self, name: str, defense: int = 15, attack: int = 10, base_health: int = 100) -> None:
        self._defense: int = defense
        self._attack: int = attack
        self._base_health: int = base_health
        self._current_health: int = self._base_health
        self._red_mana: int = 1
        self._blue_mana: int = 1
        self._experience: int = 0
        self._name: str = name
        self._inventory: List[Item] = []

    def get_name(self) -> str:
        return self._name

    def get_attack(self) -> int:
        return self._attack

    def get_defense(self) -> int:
        return self._defense

    def get_red_mana(self) -> int:
        return self._red_mana

    def get_blue_mana(self) -> int:
        return self._blue_mana

    def set_red_mana(self, amount: int) -> None:
        self._red_mana = amount

    def set_blue_mana(self, amount: int) -> None:
        self._blue_mana = amount

    def get_current_health(self) -> int:
        return self._current_health

    def get_base_health(self) -> int:
        return self._base_health

    def set_current_health(self, health: int) -> None:
        self._current_health = health

    def level_up(self) -> None:
        pass

    def get_inventory(self) -> List[Item]:
        return self._inventory

    def receive_loot(self, loot: Item) -> None:
        self.get_inventory().append(loot)

    def get_red_mana_attack(self) -> Tuple[str, int, Callable]:
        pass

    def get_blue_mana_attack(self) -> Tuple[str, int, Callable]:
        pass

    def consume(self, item: Item) -> None:
        IOManager.print_text(f"Du konsumierst: {item.get_name()}")
        if isinstance(item, HealthPotion):
            self._current_health += 25
        elif isinstance(item, RedManaPotion):
            self._red_mana += 1
        elif isinstance(item, BlueManaPotion):
            self._blue_mana += 1


class Wiebke(Player):
    def __init__(self):
        super().__init__("Wiebke", 30, 10, 50)

    def get_red_mana_attack(self) -> Tuple[str, int, Callable]:
        return "Bogen schießen", 60, lambda: 0

    def get_blue_mana_attack(self) -> Tuple[str, int, Callable]:
        return "Einschläfern", 99999999, lambda: self.set_current_health(math.ceil(self.get_current_health() / 2))


class Florian(Player):
    def __init__(self):
        super().__init__("Florian", 30, 5, 100)

    def get_red_mana_attack(self) -> Tuple[str, int, Callable]:
        return "Killer-Blick", 50, lambda: 0

    def get_blue_mana_attack(self) -> Tuple[str, int, Callable]:
        return "Mampfen", 30, lambda: self.set_current_health(
            self.get_current_health() + math.ceil(self.get_current_health() / 2))


class Henrik(Player):
    def __init__(self) -> None:
        super().__init__("Henrik", 10, 10, 75)

    def get_red_mana_attack(self) -> Tuple[str, int, Callable]:
        return "Langweilen", 55, self._cause_boredom

    def _cause_boredom(self) -> None:
        for _ in range(5):
            IOManager.print_text(f"{self.get_name()} verursacht Langeweile...")
            time.sleep(1)

    def _emotional_damage(self, self_damage: int) -> None:
        self.set_current_health(self.get_current_health() - self_damage)

    def get_blue_mana_attack(self) -> Tuple[str, int, Callable]:
        half_life: int = math.ceil(self.get_current_health() / 2)
        return "Emotionaler Schaden", 50 + 2 * half_life, lambda: self._emotional_damage(half_life)


class Vogelsang(Player):
    def __init__(self) -> None:
        super().__init__("Herr Vogelsang", 20, 30, 60)

    def get_red_mana_attack(self) -> Tuple[str, int, Callable]:
        return "Flügelschlag", 80, lambda: 0

    def get_blue_mana_attack(self) -> Tuple[str, int, Callable]:
        return "Verhöhnen", 40, lambda: self.set_current_health(math.ceil(self.get_base_health() * 0.75))
