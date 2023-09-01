import math
import os
from collections import Counter
from typing import List, Callable, Tuple

from src.enemys import Enemy
from src.io_manager import IOManager
from src.items import Item, Weapon, Armor, Consumable, HealthPotion, RedManaPotion, BlueManaPotion
from src.player import Player
from src.values import COLOR_RED, COLOR_DEFAULT, COLOR_BRIGHT_RED, COLOR_BLUE


class Encounter:
    def __init__(self, player: Player, enemy: Enemy) -> None:
        self._player: Player = player
        self._enemy: Enemy = enemy

    def execute(self) -> None:
        enemy_attack: int = self._enemy.get_attack()
        enemy_defense: int = self._enemy.get_defense()
        enemy_inventory: List[Item] = self._enemy.get_inventory()
        for item in enemy_inventory:
            if isinstance(item, Weapon):
                enemy_attack += item.get_damage()
            elif isinstance(item, Armor):
                enemy_defense += item.get_protection()

        player_attack: int = self._player.get_attack()
        player_defense: int = self._player.get_defense()
        player_inventory: List[Item] = self._player.get_inventory()
        for item in player_inventory:
            if isinstance(item, Weapon):
                player_attack += item.get_damage()
            elif isinstance(item, Armor):
                player_defense += item.get_protection()

        red_mana_attack: Tuple[str, int, Callable] = self._player.get_red_mana_attack()
        blue_mana_attack: Tuple[str, int, Callable] = self._player.get_blue_mana_attack()

        while self._enemy.get_current_health() > 0 or self._player.get_current_health() > 0:
            # Enemy attack:
            IOManager.print_text(f"\n{self._enemy.get_name()} greift an...")
            damage_to_player = math.ceil(enemy_attack / player_defense)
            IOManager.print_text(f"Du bekommst {damage_to_player} Schaden.")
            self._player.set_current_health(self._player.get_current_health() - damage_to_player)
            if damage_to_player < 0:
                self._player.set_current_health(0)
            IOManager.print_text(f"Du hast noch {self._player.get_current_health()} Lebenspunkte.\n")
            if self._player.get_current_health() <= 0:
                IOManager.print_text(f"Du hast den Kampf verloren und bist tot.")
                exit("GAME OVER")

            # Player attack:
            while True:
                user_input: str = IOManager.get_input(f"""
            ╔══════════════════════╦═════════╗
            ║ {self._enemy.get_name().ljust(20)} ║ {COLOR_RED}♥{COLOR_DEFAULT} {str(self._enemy.get_current_health()).ljust(5)} ║
            ╚══════════════════════╩═════════╝      
                    ╦  ╦╔═╗
                    ╚╗╔╝╚═╗
                     ╚╝ ╚═╝
            ╔══════════════════════╦═════════╦═════════╦═════════╗
            ║ {self._player.get_name().ljust(20)} ║ {COLOR_RED}♥{COLOR_DEFAULT} {str(self._player.get_current_health()).ljust(5)} ║ {COLOR_BRIGHT_RED}r◊{COLOR_DEFAULT} {str(self._player.get_red_mana()).ljust(4)} ║ {COLOR_BLUE}b◊{COLOR_DEFAULT} {str(self._player.get_blue_mana()).ljust(4)} ║
            ╚══════════════════════╩═════════╩═════════╩═════════╝
            Was möchtest du tun?
            1. Angriff   2. {COLOR_BRIGHT_RED}{red_mana_attack[0]}{COLOR_DEFAULT}   3. {COLOR_BLUE}{blue_mana_attack[0]}{COLOR_DEFAULT}   4. Item
            """)
                if user_input == "1":
                    damage_to_enemy = math.ceil(player_attack / enemy_defense)
                    self._deal_damage_to_enemy(damage_to_enemy)
                    break
                elif user_input == "2":
                    if self._player.get_red_mana() < 1:
                        IOManager.print_text("Du hast nicht genug rotes Mana!")
                        continue
                    IOManager.print_text(f"\n{self._player.get_name()} setzt {red_mana_attack[0]} ein.")
                    damage_to_enemy: int = math.ceil(red_mana_attack[1] / enemy_defense)
                    special_ability: Callable = red_mana_attack[2]
                    special_ability()
                    self._player.set_red_mana(self._player.get_red_mana() - 1)
                    self._deal_damage_to_enemy(damage_to_enemy)
                    break
                elif user_input == "3":
                    if self._player.get_blue_mana() < 1:
                        IOManager.print_text("Du hast nicht genug blaues Mana!")
                        continue
                    IOManager.print_text(f"\n{self._player.get_name()} setzt {blue_mana_attack[0]} ein.")
                    damage_to_enemy: int = math.ceil(blue_mana_attack[1] / enemy_defense)
                    special_ability: Callable = blue_mana_attack[2]
                    special_ability()
                    self._player.set_blue_mana(self._player.get_blue_mana() - 1)
                    self._deal_damage_to_enemy(damage_to_enemy)
                    break
                elif user_input == "4":
                    player_inventory: List[Item] = self._player.get_inventory()
                    consumables_in_inventory: List[Item] = list(
                        filter(lambda x: isinstance(x, Consumable), player_inventory))
                    if len(consumables_in_inventory) > 0:
                        indent: str = "            "
                        item_display: str = f"{indent}╔═════════════════════════════════╗\n"
                        item_counter: Counter = Counter([c.get_name() for c in consumables_in_inventory])
                        for number, item_name in enumerate(item_counter.keys()):
                            item_display += f"{indent}║ {str(number).rjust(3)}. {str(item_name).ljust(20)} x {str(list(item_counter.values())[number]).rjust(3)} ║\n"
                        item_display += f"{indent}╚═════════════════════════════════╝\n"
                        item_display += f"{indent}Leere eingabe um zurück zu kommen.\n"

                        item_input: str = "HenrikSydow&FlorianWestphal"

                        while item_input != "" and item_input not in range(len(item_counter.items())):
                            item_input = IOManager.get_input(item_display)
                            if item_input == "":
                                break
                            try:
                                item_input: int = int(item_input)
                            except ValueError:
                                continue

                            item_name: str = list(item_counter.keys())[item_input]
                            for item in self._player.get_inventory().copy():
                                if item.get_name() == item_name:
                                    self._player.consume(item)
                                    self._player.get_inventory().remove(item)
                                    break

                        break
                    else:
                        IOManager.print_text("Du hast keine benutzbaren Items in deinem Inventar")

            if self._enemy.get_current_health() <= 0:
                self._player.get_inventory().append(self._enemy.get_inventory()[0])
                IOManager.print_text(f"\n\nDu hast den Kampf gewonnen!")
                IOManager.print_text(f"Du bekommst {self._enemy.get_inventory()[0].get_name()} von {self._enemy.get_name()}")
                break

    def _deal_damage_to_enemy(self, damage: int) -> None:
        self._enemy.set_health(self._enemy.get_current_health() - damage)
        IOManager.print_text(f"\nDu fügst {self._enemy.get_name()} {damage} Schaden zu.")
        IOManager.print_text(f"Der Gegner hat noch {self._enemy.get_current_health()} Lebenspunkte.")
