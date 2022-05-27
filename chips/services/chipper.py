import json
import os
from ..services.main import ChipService


class Chipper:
    def __init__(self):
        pass

    def send_signal(self, chip_id: str, live: bool):
        if os.path.exists('.chipping_results/_sys/triggered') and \
                os.path.exists('.chipping_results/_sys/code_tree'):
            self._send_signal(chip_id, live)

    @staticmethod
    def _send_signal(chip_id: str, live: bool):
        trig_path = os.getcwd() + '/.chipping_results/_sys/triggered'
        trig_json = json.load(open(trig_path))

        if chip_id not in trig_json:
            trig_json.append(chip_id)
            with open(trig_path, "w") as trig_file:
                json.dump(trig_json, trig_file)
                trig_file.close()

            if live:
                service = ChipService(_setup=False)
                service.results(_silent=True)

        # generate results.py file if it doesn't exist yet
        if live and not os.path.exists('.chipping_results/results.py'):
            service = ChipService(_setup=False)
            service.results(_silent=True)


def trigger(chip_id: str, live: bool = True) -> Chipper():
    return Chipper().send_signal(chip_id, live)
