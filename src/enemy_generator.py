import random
from src.enemys import Enemy, all_enemys, ButterGolem
from src.items import all_items, Item, Axe


class EnemyGenerator:
    @staticmethod
    def generate_enemy() -> Enemy:
        enemy: Enemy = random.choice(all_enemys)
        if isinstance(enemy, ButterGolem):
            item: Axe = Axe()
        else:
            item: Item = random.choice(all_items)
        return enemy([item])