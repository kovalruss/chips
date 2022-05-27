import os
from ..services.main import ChipService
from ..common.messages_service import MessagesService


def setup(venv: str = "on", venv_path: str = ""):
    messages = MessagesService()

    if venv == "on":
        # ADD EXEC VARIABLE TO VENV
        _CHIPS_EXEC = "\n\n" \
                      "# 👾 Chips exec (https://github.com/kovalruss/chips)" \
                      "\n" \
                      "export chips=(python -m chips)"

        if not venv_path:
            venv_path = os.getcwd() + '/venv'

        _activate_path = venv_path + "/bin/activate"

        if not os.path.exists(_activate_path):
            messages.error(f"Could not find /activate on path {_activate_path}. \n"
                           f"Try to specify a custom venv path with -p --path argument!")
        else:
            with open(_activate_path, "r") as read_venv:
                venv_config = read_venv.read()
                read_venv.close()
                if _CHIPS_EXEC not in venv_config:
                    with open("/Users/russkovalchuk/PycharmProjects/chip_test_2/venv/bin/activate", "a") as edit_file:
                        edit_file.write(_CHIPS_EXEC)
                        edit_file.close()
                        messages.default("Added executable variable $chips to virtualenv. Start a new terminal to proceed!")

    # PERFORM BASIC SETUP
    ChipService.setup()
