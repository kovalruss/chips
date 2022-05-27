import os
import json
import click
from gitignore_parser import parse_gitignore

from ..common.messages_service import MessagesService
from chips.common.basic_excludes import BASIC_EXCLUDES
from ast2json import ast2json
from prettytable import PrettyTable as pt

messages = MessagesService()


class ChipService:
    CHIPS_IGNORE_PATH = ""
    MODE = "local"
    LIVE = True

    def __init__(self, mode: str = "local", live: bool = True, _setup: bool = True):
        """
        :param mode: choose chipping mode: local, production
        :param live: option if to autogenerate results file (might affect performance if True)
        """

        # TODO: add external mode implementation
        if mode:
            pass

        if live:
            self.LIVE = live

        if _setup:
            setup_result = self._check_setup()
            if setup_result != "success":
                raise Exception("Chips setup failed! Read logs for more info!")

    def add_chips(self,
                  path: str = None,
                  auto: str = "off",
                  result_type: str = "list_files",
                  silent: bool = False) -> (str, list, list):
        """
        Add chips to current project

        :param auto:
        :param silent:
        :param result_type:
        list_files (default) - list all affected files,
        blind = no output,
        count_files - print number of files affected
        :param path: custom path to run, default = project root
        :return:
        arg1: chipping result in str
        arg2: list of failed files
        """
        current_work_dir = path if path else os.getcwd()
        if not silent:
            messages.default(f'Chipping directory == {current_work_dir}')

        chipped_success_files_list = []
        chipped_failure_files_list = []
        chipped_skipped_files_list = []

        # parse chipsignore file
        matches = parse_gitignore(self.CHIPS_IGNORE_PATH)
        file_tree = []

        work_files = []
        work_filenames = []

        for root, dirs, files in os.walk(current_work_dir):
            # TODO: add not only for .py files
            files = [f for f in files if not matches(f) and f.endswith(".py")]
            dirs[:] = [d for d in dirs if not matches(d)]

            work_filenames += files
            for filename in files:
                work_files.append(os.path.join(root, filename))

        triggers_list = json.load(open(os.getcwd() + '/.chipping_results/_sys/triggered'))

        if not silent:
            messages.info(f"Chipping will be performed for files: {', '.join(work_filenames)}")
            if triggers_list:
                messages.warning("Current trigger progress will be lost!")

            if click.confirm('Do you want to continue?', default=True):
                pass
            else:
                return "No files were chipped", [], []

        for i, filepath in enumerate(work_files):
            chipping_result, file_tree = self._add_chip_to_file(filepath, file_tree)

            if chipping_result == "another_chip_session_detected":
                messages.info("Another chipping session detected. Removing old chips..")
                chipping_result, _fl, _sl = \
                    self.remove_chips(result_type="count_files", silent=True)

                if chipping_result:
                    messages.result(chipping_result)

                chipping_result, chipped_failure_files_list, chipped_skipped_files_list = \
                    self.add_chips(result_type="list_files", silent=True)
                if chipping_result:

                    # list skipped files
                    if chipped_skipped_files_list:
                        messages.default("Chipping skipped for next files: %s" % ", ".join(chipped_skipped_files_list))

                    # list failed files
                    if chipped_failure_files_list:
                        messages.warning("Chipping failed for next files: %s" % ", ".join(chipped_failure_files_list))

                    messages.result(chipping_result)
                return "", [], []

            if chipping_result == "success":
                chipped_success_files_list.append(work_filenames[i])
            elif chipping_result == "failure":
                chipped_failure_files_list.append(work_filenames[i])
            elif chipping_result == "skipped":
                chipped_skipped_files_list.append(work_filenames[i])

        # write success files names to stdout
        if chipped_success_files_list:
            # create or update code_tree
            self._update_or_create_code_tree_json(file_tree)
            ChipService(_setup=False).results(silent=True)

            # make sure triggered is cleared
            with open('.chipping_results/_sys/triggered', 'w') as triggered_json_file:
                triggered_json_file.write("[]")
                triggered_json_file.close()

            if result_type == "list_files":
                return "Chipped %s" % ", ".join(chipped_success_files_list), chipped_failure_files_list, \
                       chipped_skipped_files_list
            elif result_type == "count_files":
                return "Chipped %s files" % len(chipped_success_files_list), chipped_failure_files_list, \
                       chipped_skipped_files_list
            elif result_type == "blind":
                return "Chipping completed", chipped_failure_files_list, chipped_skipped_files_list
        else:
            return "No files were chipped", chipped_failure_files_list, chipped_skipped_files_list

    @classmethod
    def remove_chips(cls,
                     folder_path: str = None,
                     result_type: str = "list_files",
                     silent: bool = False) -> (str, list, list):
        """
        Remove chips from current project

        :param silent:
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
        if not silent:
            messages.default(f'Chipping directory == {current_work_dir}')

        success_files_list = []
        failure_files_list = []
        skipped_files_list = []

        # parse chipsignore file
        matches = parse_gitignore(cls.CHIPS_IGNORE_PATH)

        work_files = []
        work_filenames = []

        for root, dirs, files in os.walk(current_work_dir):
            # TODO: add not only for .py files
            files = [f for f in files if not matches(f) and f.endswith(".py")]
            dirs[:] = [d for d in dirs if not matches(d)]

            work_filenames += files
            for filename in files:
                work_files.append(os.path.join(root, filename))

        if not silent:
            messages.info(f"Chips will be removed for files: {', '.join(work_filenames)}")

            if click.confirm('Do you want to continue?', default=True):
                pass
            else:
                return "Chips were removed from 0 files", [], []

        for i, filepath in enumerate(work_files):
            remove_chips_result = cls._remove_chip_from_file(filepath)
            if remove_chips_result == "success":
                success_files_list.append(work_filenames[i])
            elif remove_chips_result == "failure":
                failure_files_list.append(work_filenames[i])
            elif remove_chips_result == "skipped":
                skipped_files_list.append(work_filenames[i])

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

    @classmethod
    def results(cls, silent: bool = False):
        """
        Generate chipping results to results.py file

        :param silent: deside whether to log or not
        """

        if not silent:
            messages.info("Generating results file..")

        trig_path = os.getcwd() + '/.chipping_results/_sys/triggered'
        trig_json = json.load(open(trig_path))

        tree_path = os.getcwd() + '/.chipping_results/_sys/code_tree'
        tree_json = json.load(open(tree_path))

        with open(os.getcwd() + '/.chipping_results/results.py', "w") as results_file:
            results_file_text = cls._results_text(trig_json, tree_json)
            results_file.write(results_file_text)
            results_file.close()

        if not silent:
            messages.result("Results file generated in location .chipping_results/results.py")

    @classmethod
    def _results_text(cls, trig_json: dict, tree_json: dict):
        import datetime
        results_file_text = f"# Generated by 👾 Chips package on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        results_file_text += f"# This file represents the results of refactoring chips trigger.\n"
        results_file_text += f"# More details here.\n\n"

        # CREATE TABLE
        tb = pt(align="l")
        tb.field_names = ["ID", "File", "Method", "Triggered"]
        idx_counter = 0

        def _iterate_tree(_tree_json: dict, _idx_counter: int, first_iter: bool, tab_iter: int):
            for thread in _tree_json:
                _idx_counter += 1
                chip_id = thread["id"]

                tb.add_row([_idx_counter, file['file_path'] if first_iter else "", tab_iter*" " + thread['name'],
                            "✅" if chip_id in trig_json else "❌"])
                first_iter = False

                if thread["body"]:
                    _idx_counter = _iterate_tree(thread["body"], _idx_counter, first_iter, tab_iter+4)

            return _idx_counter

        for file in tree_json:
            idx_counter = _iterate_tree(file["code_tree"], idx_counter, True, 0)

        results_file_text += "\"\"\"\n"
        results_file_text += tb.get_string() + "\n"
        results_file_text += "\"\"\"\n\n"

        results_file_text += "# Don't forget to remove chips after you finish testing!\n"

        return results_file_text

    @classmethod
    def _update_or_create_code_tree_json(cls, file_tree: dict):
        with open('.chipping_results/_sys/code_tree', 'w') as code_tree_json_file:
            json.dump(file_tree, code_tree_json_file)
            code_tree_json_file.close()

    @classmethod
    def _check_setup(cls):
        messages.info("👾 Checking Chips setup...")

        try:
            os.mkdir(".chipping_results")
        except FileExistsError:
            pass

        try:
            os.mkdir(".chipping_results/_sys")
        except FileExistsError:
            pass

        if not os.path.exists('.chipping_results/_sys/triggered'):
            with open('.chipping_results/_sys/triggered', 'w') as triggered_json_file:
                triggered_json_file.write("[]")
                triggered_json_file.close()

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

                    for basic_exclude in BASIC_EXCLUDES:
                        # TODO: add better matching options. for now chips and my_chips are the same
                        # skip matches in basic_exclude and gitignore file
                        if basic_exclude not in gitignore_text:
                            chipsignore_text += "\n" + basic_exclude

                    chipsignore_text += "\n\n# CUSTOM CHIPS EXCLUDES"
                chipsignore_file.write(chipsignore_text)
                chipsignore_file.close()

                cls.CHIPS_IGNORE_PATH = os.path.realpath(chipsignore_file.name)

        except ModuleNotFoundError:
            messages.error(".chipsignore creation error")
            return "failure"
        else:
            messages.info(".chipsignore created successfully in root directory")
            return "success"

    def _add_chip_to_file(self, filepath: str, file_tree: list):
        try:
            with open(filepath, "r") as file_to_read:
                file_code = file_to_read.read()
                file_to_read.close()

            if "trigger(" in file_code:
                return "another_chip_session_detected", []

            # get chipped file code + amount of chips added
            chipped_file, chips_added_amount, file_tree = self._insert_chips_into_funcs(file_code, filepath, file_tree)

            # rewrite file with updated code
            if chips_added_amount != 0:
                with open(filepath, "w") as file_to_write:
                    file_to_write.write(chipped_file)
                    file_to_write.close()
        except FileNotFoundError as e:
            messages.warning(f"{e}")
            return "failure", []
        else:
            if chips_added_amount == 0:
                return "skipped", file_tree
            return "success", file_tree

    @classmethod
    def _create_file_tree(cls, file_code: str, file_tree: list, file_path: str,):
        import ast

        ast_parsed_code = ast.parse(file_code)
        ast_parsed_code_json = ast2json(ast_parsed_code)

        defs_amount = 0
        tree = []

        def _parse_code_for_defs(rec_item: dict, defs_am: int, c_tree: list):

            for body_item in rec_item["body"]:
                c_tree_dict = {}
                if body_item["_type"] == "FunctionDef":
                    if "name" in body_item:
                        defs_am += 1
                        c_tree_dict["name"] = body_item["name"]
                        c_tree_dict["id"] = cls._generate_func_token()
                        # c_tree_dict["triggered"] = False
                        if "body" in body_item:
                            c_tree_dict = {**c_tree_dict, "body": []}
                            _parse_code_for_defs(body_item, defs_am, c_tree_dict["body"])
                if c_tree_dict:
                    c_tree.append(c_tree_dict)

            return c_tree, defs_am

        code_tree, code_defs_amount = _parse_code_for_defs(ast_parsed_code_json, defs_amount, tree)

        if code_defs_amount:
            file_tree.append({"file_path": file_path.replace(os.getcwd() + '/', ''), "code_tree": code_tree})

        return file_tree, code_tree

    @staticmethod
    def _generate_func_token():
        import random
        import string
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        return random_string

    def _insert_chips_into_funcs(self, chipped_file: str, file_path: str, file_tree: list):

        updated_file = ""
        lines_list = chipped_file.splitlines()
        lines_iter = iter(lines_list)

        if "from chips.services.chip import trigger" not in chipped_file:
            updated_file += "from chips.services.chip import trigger\n"

        idx = 0
        chips_added_amount = 0

        try:
            file_tree, code_tree = self._create_file_tree(chipped_file, file_tree, file_path)
        except SyntaxError:
            code_tree = []

        if code_tree:
            for line in lines_iter:
                updated_file += line + "\n"
                if "def" in line:
                    # GET FUNC NAME
                    func_name = line.split("def", 1)[1].partition("(")[0].replace(':', '').strip()

                    # ITERATE UNTIL THE ACTUAL BEGINNING OF THE FUNCTION
                    k = idx
                    func_end_found = False
                    while not func_end_found:
                        if k != idx:
                            updated_file += lines_list[k] + "\n"

                        if "):" in lines_list[k]:
                            func_end_found = True

                            # check if func is already chipped
                            if "trigger(" not in lines_list[k+1]:
                                try:
                                    nl_spaces_amount = 0

                                    for t in range(k+1, k+5):
                                        # check if line contains code to count spaces
                                        if lines_list[t].strip():
                                            nl_spaces_amount = len(lines_list[t]) - len(lines_list[t].lstrip())
                                            break

                                    # GET CHIP ID
                                    chip_id = self._get_chip_id_by_func_name(func_name, code_tree)

                                    # ADD TRIGGER
                                    if chip_id:
                                        chip = f"trigger('{chip_id}')" if self.LIVE \
                                            else f"trigger('{chip_id}', live=False)"
                                        updated_file += " " * nl_spaces_amount + chip + "\n"
                                        chips_added_amount += 1
                                    else:
                                        messages.error("Fatal chips error happened, filename not found in tree. \n"
                                                       "Try one more time!")
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

        return updated_file, chips_added_amount, file_tree

    @classmethod
    def _get_chip_id_by_func_name(cls, func_name: str, tree: list):
        chip_id = None
        for thread in tree:
            if thread["name"] == func_name:
                chip_id = thread["id"]
                break

            if thread["body"]:
                chip_id = cls._get_chip_id_by_func_name(func_name, thread["body"])

        return chip_id

    @staticmethod
    def _remove_chip_from_file(file_path: str):
        try:
            with open(file_path, "r") as file_to_read_from:
                file_text = file_to_read_from.read()
                file_to_read_from.close()

            changed_file = ""
            removed_chips_parts_amount = 0
            lines_list = file_text.splitlines()
            for i, line in enumerate(lines_list):
                if "trigger(" not in line and "from chips.services.chip import trigger" not in line:
                    changed_file += line + "\n"
                else:
                    removed_chips_parts_amount += 1

            if removed_chips_parts_amount:
                with open(file_path, "w") as file_to_write_to:
                    file_to_write_to.write(changed_file)
                    file_to_write_to.close()
            else:
                return "skipped"
        except FileNotFoundError as e:
            messages.warning(f"{e}")
            return "failure"
        else:
            return "success"
