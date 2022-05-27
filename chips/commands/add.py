from ..services.main import ChipService
from ..common.messages_service import MessagesService


def add(path: str = None, auto: str = "on", result_type: str = "list_files"):
    service = ChipService()
    messages = MessagesService()
    chipping_result, chipped_failure_files_list, chipped_skipped_files_list = \
        service.add_chips(result_type=result_type, path=path, auto=auto)
    if chipping_result:

        # list skipped files
        if chipped_skipped_files_list:
            messages.default("Chipping skipped for next files: %s" % ", ".join(chipped_skipped_files_list))

        # list failed files
        if chipped_failure_files_list:
            messages.warning("Chipping failed for next files: %s" % ", ".join(chipped_failure_files_list))

        messages.result(chipping_result)

