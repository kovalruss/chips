import argparse
from .commands.add import add
from .commands.remove import remove
from .commands.results import results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # main
    parser.add_argument('-a', '--add', help='Add chips', action='store_true')
    parser.add_argument('-r', '--remove', help='Remove chips', action='store_true')
    parser.add_argument('-rs', '--results', help='Generate results to .chipping_results/results.py',
                        action='store_true')

    # optional
    parser.add_argument('--auto', default="off",
                        help='Determines whether to auto generate .chipping_results/results.py',
                        type=str)
    parser.add_argument('-p', '--path', help='Set custom chipping path',
                        type=str)
    parser.add_argument('-rt', '--result_type', default="list_files",
                        help='list_files - list all affected files \n'
                             'blind = no output \n'
                             'count_files - print number of files affected',
                        type=str)

    options = parser.parse_args()
    args = {}
    if options.add:
        if options.auto:
            args = {**args, "auto": options.auto}
        if options.path:
            args = {**args, "path": options.path}
        if options.result_type:
            args = {**args, "result_type": options.result_type}
        add(**args)
    elif options.remove:
        if options.path:
            args = {**args, "path": options.path}
        if options.result_type:
            args = {**args, "result_type": options.result_type}
        remove(**args)
    elif options.results:
        results(**args)
