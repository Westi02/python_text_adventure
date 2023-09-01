import os


class IOManager:

    @staticmethod
    def print_text(text: str) -> None:
        print(text)

    @staticmethod
    def get_input(message: str = "") -> str:
        player_input: str = input(message)
        os.system("cls")
        return player_input
