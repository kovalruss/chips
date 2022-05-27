from ..services.main_service import ChipService
from ..common.messages_service import MessagesService


def remove(path: str = None, result_type: str = "list_files"):
    service = ChipService()
    messages = MessagesService()
    chipping_result, chipped_failure_files_list, chipped_skipped_files_list = \
        service.remove_chips(result_type="count_files")
    if chipping_result:

        # list skipped files
        if chipped_skipped_files_list:
            messages.default("Removing chips skipped for next files: %s" % ", ".join(chipped_skipped_files_list))

        # list failed files
        if chipped_failure_files_list:
            messages.warning("Removing chips failed for next files: %s" % ", ".join(chipped_failure_files_list))

        messages.result(chipping_result)
