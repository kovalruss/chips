import os
from gitignore_parser import parse_gitignore

from common.messages_service import MessagesService
from basic_excludes import BASIC_EXCLUDES

messages = MessagesService()


class ChipService:
    chip = "print('chipped')"
    CHIPS_IGNORE_PATH = ""

    def __init__(self, custom_chip: str = None):
        """
        :param custom_chip: change default chip
        """

        if custom_chip:
            self.chip = custom_chip

        setup_result = self._check_setup()
        if setup_result != "success":
            raise Exception("Chips setup failed! Read logs for more info!")

    @classmethod
    def _check_setup(cls):
        messages.info("👾 Checking Chips setup...")

        chipsignore_exists = False
        for root, dirs, files in os.walk(os.getcwd()):
            # remove hidden files and excluded dirs
            files = [f for f in files if not f[0] == '.' or f == ".chipsignore"]
            dirs[:] = [d for d in dirs if not d[0] == '.' and d not in BASIC_EXCLUDES]

            for filename in files:
                if filename == ".chipsignore":
                    chipsignore_exists = True
                    cls.CHIPS_IGNORE_PATH = os.path.join(root, filename)

        if not chipsignore_exists:
            messages.default('.chips_ignore file not found on path. \n'
                             'trying to create .chips_ignore based on current .gitignore config')
            setup_result = cls._setup_chips()
            if setup_result == "failure":
                messages.error("Chips setup failed!")
            elif setup_result == "success":
                messages.success("Chips setup completed!")
        else:
            setup_result = "success"
            messages.success("Chips setup completed!")
        return setup_result

    @classmethod
    def _setup_chips(cls):
        gitignore_exists = False
        gitignore_path = None
        for root, dirs, files in os.walk(os.getcwd()):
            # remove hidden files and excluded dirs
            files = [f for f in files if not f[0] == '.' or f == ".gitignore"]
            dirs[:] = [d for d in dirs if not d[0] == '.' and d not in BASIC_EXCLUDES]

            for filename in files:
                if filename == ".gitignore":
                    gitignore_path = os.path.join(root, filename)
                    gitignore_exists = True

        if gitignore_exists and gitignore_path:
            messages.default(f".gitignore found on path {gitignore_path}\n"
                             "creating .chipsignore based on .gitignore")
            chipsignore_creation_result = cls._create_chipsignore_based_on_gitignore(gitignore_path)
            return chipsignore_creation_result
        else:
            messages.error("Failure: .gitignore not found, create gitignore to proceed")
            return "failure"

    @classmethod
    def _create_chipsignore_based_on_gitignore(cls, gitignore_path):
        try:
            with open(gitignore_path, 'r') as gitignore_file:
                gitignore_text = gitignore_file.read()
                gitignore_file.close()
            with open('.chipsignore', 'w') as chipsignore_file:
                chipsignore_text = gitignore_text + "\n"

                if BASIC_EXCLUDES:
                    chipsignore_text += "# BASIC CHIPS EXCLUDES"

                    for basic_exlude in BASIC_EXCLUDES:
                        # TODO: add better matching options. for now chips and my_chips are the same
                        # skip matches in basic_exclude and gitignore file
                        if basic_exlude not in gitignore_text:
                            chipsignore_text += "\n" + basic_exlude

                    chipsignore_text += "\n\n# CUSTOM CHIPS EXCLUDES"
                chipsignore_file.write(chipsignore_text)
                chipsignore_file.close()

                cls.CHIPS_IGNORE_PATH = os.path.realpath(chipsignore_file.name)

        except ModuleNotFoundError as e:
            messages.error(".chipsignore creation error")
            return "failure"
        else:
            messages.info(".chipsignore created successfully")
            return "success"

    def add_chips(self,
                  folder_path: str = None,
                  result_type: str = "list_files") -> (str, list):
        """
        Add chips to current project
        :param result_type:
        list_files (default) - list all affected files,
        blind = no output,
        count_files - print number of files affected
        :param folder_path: custom folder path to run, default = current project
        :return:
        arg1: chipping result in str
        arg2: list of failed files
        """
        current_work_dir = folder_path if folder_path else os.getcwd()
        messages.default(f'Chipping directory == {current_work_dir}')

        chipped_success_files_list = []
        chipped_failure_files_list = []
        chipped_skipped_files_list = []

        # parse chipsignore file
        matches = parse_gitignore(self.CHIPS_IGNORE_PATH)

        for root, dirs, files in os.walk(current_work_dir):
            files = [f for f in files if not matches(f)]
            dirs[:] = [d for d in dirs if not matches(d)]

            for filename in files:
                # if filename.endswith(filetypes):

                # TODO: add not only for .py files
                # .py only for now
                chipping_result = self._add_chip_to_file(os.path.join(root, filename))
                if chipping_result == "success":
                    chipped_success_files_list.append(filename)
                elif chipping_result == "failure":
                    chipped_failure_files_list.append(filename)
                elif chipping_result == "skipped":
                    chipped_skipped_files_list.append(filename)

        # write success files names to stdout
        if chipped_success_files_list:
            if result_type == "list_files":
                return "Chipped %s" % ", ".join(chipped_success_files_list), chipped_failure_files_list, chipped_skipped_files_list
            elif result_type == "count_files":
                return "Chipped %s files" % len(chipped_success_files_list), chipped_failure_files_list, chipped_skipped_files_list
            elif result_type == "blind":
                return "Chipping completed", chipped_failure_files_list, chipped_skipped_files_list
        else:
            return "No files were chipped", chipped_failure_files_list, chipped_skipped_files_list

    def remove_chips(self,
                     folder_path: str = None,
                     result_type: str = "list_files") -> (str, list):
        """
        Remove chips from current project
        :param result_type:
        list_files (default) - list all affected files,
        blind = no output,
        count_files - print number of files affected
        :param folder_path: custom folder path to run, default = current project
        :return:
        arg1: removing chips result in str
        arg2: list of failed files
        """
        current_work_dir = folder_path if folder_path else os.getcwd()
        messages.default(f'Chipping directory == {current_work_dir}')

        success_files_list = []
        failure_files_list = []
        skipped_files_list = []

        # parse chipsignore file
        matches = parse_gitignore(self.CHIPS_IGNORE_PATH)

        for root, dirs, files in os.walk(current_work_dir):
            files = [f for f in files if not matches(f)]
            dirs[:] = [d for d in dirs if not matches(d)]

            for filename in files:
                # if filename.endswith(filetypes):

                # TODO: add not only for .py files
                # .py only for now
                remove_chips_result = self._remove_chip_from_file(os.path.join(root, filename))
                if remove_chips_result == "success":
                    success_files_list.append(filename)
                elif remove_chips_result == "failure":
                    failure_files_list.append(filename)
                elif remove_chips_result == "skipped":
                    skipped_files_list.append(filename)

        # write success files names to stdout
        if success_files_list:
            if result_type == "list_files":
                return "Removed chips from %s" % ", ".join(success_files_list), failure_files_list, skipped_files_list
            elif result_type == "count_files":
                return "Removed chips from %s files" % len(success_files_list), failure_files_list, skipped_files_list
            elif result_type == "blind":
                return "Chips removal completed", failure_files_list, skipped_files_list
        else:
            return "Chips were removed from 0 files", failure_files_list, skipped_files_list

    def _add_chip_to_file(self, file: str):
        try:
            with open(file, "r") as file_to_read:
                file_code = file_to_read.read()
                file_to_read.close()

            # get chipped file code + amount of chips added
            chipped_file, chips_added_amount = self._insert_chips_into_funcs(file_code)

            # rewrite file with updated code
            if chips_added_amount != 0:
                with open(file, "w") as file_to_write:
                    file_to_write.write(chipped_file)
                    file_to_write.close()
        except FileNotFoundError as e:
            messages.warning(f"{e}")
            return "failure"
        else:
            if chips_added_amount == 0:
                return "skipped"
            return "success"

    def _insert_chips_into_funcs(self, chipped_file: str):

        updated_file = ""
        lines_list = chipped_file.splitlines()
        lines_iter = iter(lines_list)

        idx = 0
        chips_added_amount = 0

        for line in lines_iter:
            updated_file += line + "\n"
            if "def" in line:
                k = idx

                func_end_found = False
                while not func_end_found:
                    if k != idx:
                        updated_file += lines_list[k] + "\n"

                    if "):" in lines_list[k]:
                        func_end_found = True

                        # check if func is already chipped
                        if self.chip not in lines_list[k+1]:
                            try:
                                nl_spaces_amount = 0

                                for t in range(k+1, k+5):
                                    # check if line contains code to count spaces
                                    if lines_list[t].strip():
                                        nl_spaces_amount = len(lines_list[t]) - len(lines_list[t].lstrip())
                                        break

                                updated_file += " " * nl_spaces_amount + self.chip + "\n"
                                chips_added_amount += 1
                            except IndexError:
                                pass

                        # skip lines in iterator
                        skip_lines = k - idx
                        for _ in range(skip_lines):
                            next(lines_iter)
                            idx += 1

                        break
                    k += 1

            idx += 1

        return updated_file, chips_added_amount

    def _remove_chip_from_file(self, file: str):
        try:
            with open(file, "r") as file_to_read_from:
                file_text = file_to_read_from.read()
                file_to_read_from.close()

            changed_file = ""
            removed_chips_amount = 0
            lines_list = file_text.splitlines()
            for i, line in enumerate(lines_list):
                if self.chip not in line:
                    changed_file += line + "\n"
                else:
                    removed_chips_amount += 1

            if removed_chips_amount:
                with open(file, "w") as file_to_write_to:
                    file_to_write_to.write(changed_file)
                    file_to_write_to.close()
            else:
                return "skipped"
        except FileNotFoundError as e:
            messages.warning(f"{e}")
            return "failure"
        else:
            return "success"
