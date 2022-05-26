from .services.main_service import ChipService
from .common.messages_service import MessagesService


if __name__ == "__main__":
    service = ChipService()
    messages = MessagesService()

    service.results()
