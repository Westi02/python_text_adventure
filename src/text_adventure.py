import os
import random
from typing import List

from src.events import all_events, Event
from src.io_manager import IOManager
from src.items import Item, Sword, Shield, HealthPotion, RedManaPotion, BlueManaPotion
from src.player import Player, Wiebke, Florian, Henrik, Vogelsang


class Game:
    def __init__(self, player: Player) -> None:
        self._running: bool = True
        self._player: Player = player
        self.game_loop()

    def game_loop(self) -> None:
        while self._running:
            random.choice(all_events)(self._player).execute()


def prolog(player: Player):
    IOManager.print_text(
        """
        Du verlässt dein Dorf.
        Dich erwartet ein großes Abenteuer.
        Dein Schwert hast du dabei und du bist bereit dich lauernden Gefahren zu stellen.
    
        Als erstes kommst du an eine Kreuzung und du musst dich entscheiden in welche Richtung du gehen willst.
        """
    )

    Event(player).player_decision(["links", "rechts"])


def composition_root() -> None:
    name: str = IOManager.get_input("Wie heißt du? ")
    player_classes: List[str] = ["Wiebke", "Florian", "Henrik", "Herr Vogelsang"]
    player_class: str = ""
    player: Player | None = None
    while player_class not in player_classes:
        player_class = IOManager.get_input(f"Welcher Klasse gehörst du an? ({', '.join(player_classes)})")
    if player_class == "Wiebke":
        player = Wiebke()
    elif player_class == "Florian":
        player = Florian()
    elif player_class == "Henrik":
        player = Henrik()
    elif player_class == "Herr Vogelsang":
        player = Vogelsang()

    player_inventory: List[Item] = player.get_inventory()
    player_inventory.append(Sword())
    player_inventory.append(Shield())

    prolog(player)
    Game(player)


if __name__ == '__main__':
    os.system("")  # aktiviert ansi-escape sequences in windows cmd (für farbigen Text)
    composition_root()
