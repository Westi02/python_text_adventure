from collections import Counter
from typing import List, Type
import random

from src.encounter import Encounter
from src.enemy_generator import EnemyGenerator
from src.enemys import Enemy
from src.io_manager import IOManager
from src.items import Item, all_items
from src.player import Player


class Event:
    def __init__(self, player: Player) -> None:
        self._player: Player = player

    def execute(self) -> None:
        pass

    def player_decision(self, possibilities: List) -> str:
        answer = None
        while answer not in possibilities:
            IOManager.print_text(" - ".join(possibilities) + " - Inventar" )
            answer = IOManager.get_input("Was möchtest du tun?")
            if answer == "Inventar":
                player_inventory: List[Item] = self._player.get_inventory()
                if len(player_inventory) > 0:
                    indent: str = "            "
                    item_display: str = f"{indent}╔═════════════════════════════════╗\n"
                    item_counter: Counter = Counter([c.get_name() for c in player_inventory])
                    for number, item_name in enumerate(item_counter.keys()):
                        item_display += f"{indent}║ {str(number).rjust(3)}. {str(item_name).ljust(20)} x {str(list(item_counter.values())[number]).rjust(3)} ║\n"
                    item_display += f"{indent}╚═════════════════════════════════╝\n"

                    IOManager.print_text(item_display)
                else:
                    IOManager.print_text("Du hast keine Items in deinem Inventar")
        return answer


class Crossing(Event):
    def execute(self) -> None:
        IOManager.print_text("""Du kommst an eine Kreuzung und du musst dich entscheiden in welche Richtung du gehen willst.""")
        answer = self.player_decision(["links", "rechts"])
        number = random.randint(0, 1)

        if number == 1:
            Encounter(self._player, EnemyGenerator.generate_enemy()).execute()


class Fairy(Event):
    def execute(self) -> None:
        IOManager.print_text("""Vor dir erscheint eine Fee. Sie bietet dir 2 verschiedene Tränke an. Welchen wählst du? Links oder rechts?""")
        answer = self.player_decision(["links", "rechts"])
        number = random.randint(0, 1)

        if number == 1:
            Encounter(self._player, EnemyGenerator.generate_enemy()).execute()
        else:
            self._player.set_current_health(self._player.get_current_health() - 10)
            if self._player.get_current_health() <= 0:
                exit("Der Trank war vergitet. Du bist tot.")


class Forest(Event):
    def execute(self) -> None:
        IOManager.print_text("""Du kommst in einem dunklen Wald an. Links befindet sich ein beleuchteter Weg und rechts ist ein dunkler, unheimlicher Pfad. Welchen Weg wählst du?""")
        answer = self.player_decision(["links", "rechts"])
        number = random.randint(0, 1)

        if number == 1:
            Encounter(self._player, EnemyGenerator.generate_enemy()).execute()
        else:
            IOManager.print_text("""Du hast eine Kiste im Wald gefunden.""")
            loot_item: Item = random.choice(all_items)()
            self._player.receive_loot(loot_item)
            IOManager.print_text(f"Glückwunsch, du hast folgenden Gegenstand gefunden: {loot_item.get_name()}")


class StraightPath(Event):
    def execute(self) -> None:
        IOManager.print_text(
            """
            Deine Reise ist gerade sehr langweilig... Du befindest dich auf einem geraden Weg. 
            Möchtest du deine Reise fortsetzen oder abbrechen?
            """
        )
        answer = self.player_decision(["fortsetzen", "abbrechen"])
        if answer == "abbrechen":
            exit("GAME OVER")


class Hole(Event):
    def execute(self) -> None:
        IOManager.print_text(
            """
            Die Erde bebt und plötzlich tut sich ein riesiges Loch vor dir auf. Du musst wählen: stehenbleiben oder springen?
            """
        )
        answer = self.player_decision(["stehenbleiben", "springen"])
        if answer == "springen":
            exit("Das Loch war zu groß. GAME OVER")


class Cave(Event):
    def execute(self) -> None:
        IOManager.print_text("""Du hast eine Hoehle entdeckt. Sie ist sehr dunkel und sieht bedrohlich aus.""")
        answer = self.player_decision(["hineingehen", "flucht"])

        if answer == "hineingehen":
            number = random.randint(0, 1)

            if number == 1:
                Encounter(self._player, EnemyGenerator.generate_enemy()).execute()
            else:
                IOManager.print_text("""Du hast eine Truhe gefunden.""")
                loot_item: Item = random.choice(all_items)()
                self._player.receive_loot(loot_item)
                IOManager.print_text(f"Du hast folgenden Gegenstand gefunden: {loot_item.get_name()}")


class EnemySpotted(Event):
    def execute(self) -> None:
        IOManager.print_text("""Auf deinem Weg ist ein Gegner.""")
        answer = self.player_decision(["kampf", "flucht"])

        if answer == "kampf":
            enemy: Enemy = EnemyGenerator.generate_enemy()
            Encounter(self._player, enemy).execute()


class Fieldtrip(Event):
    def execute(self) -> None:
        IOManager.print_text("""Du befindest dich mitten in einem Feld mit sehr hohem Gras. Plötzlich raschelt es hinter dir. Was wählst du? Kampf oder Flucht?""")
        answer = self.player_decision(["kampf", "flucht"])

        if answer == "kampf":
            enemy: Enemy = EnemyGenerator.generate_enemy()
            Encounter(self._player, enemy).execute()


class Wiseman(Event):
    def execute(self) -> None:
        IOManager.print_text("""\n
        Vor dir erscheint ein weiser Mann und stellt dir ein Rätsel: 
        
        Ich bin ein kleines zittrig Ding auf unbequemem Sitze,
        doch geb ich manchen guten Wink mit meiner Nasenspitze.
        """)
        answer: str = IOManager.get_input("Was kann das sein?")

        if isinstance(answer, str) and answer.lower() == "kompassnadel":
            IOManager.print_text("Deine Antwort war richtig!")
            loot_item: Item = random.choice(all_items)()
            self._player.receive_loot(loot_item)
            IOManager.print_text(f"Du hast folgenden Gegenstand gefunden: {loot_item.get_name()}")

        else:
            exit("Die Antwort war falsch. Game over.")


all_events: List[Type[Event]] = [Crossing, StraightPath, Cave, EnemySpotted, Wiseman, Fieldtrip, Hole, Forest, Fairy]