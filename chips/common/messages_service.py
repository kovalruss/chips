from colorama import Fore, Style


class MessagesService:
    def __init__(self):
        pass

    def info(self, text):
        self._colored_print(Fore.RESET, text)

    def default(self, text):
        self._colored_print(Fore.WHITE, text)

    def warning(self, text):
        self._colored_print(Fore.YELLOW, text)

    def error(self, text):
        self._colored_print(Fore.RED, text)

    def success(self, text):
        self._colored_print(Fore.GREEN, text)

    def result(self, text):
        self._colored_print(Fore.MAGENTA, text)

    @staticmethod
    def _colored_print(color, text):
        print(color + text + Style.RESET_ALL)
