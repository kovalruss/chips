# 👾 Chips

Handsome testing tool. It inserts "chips" to your code, detecting unused fragments. Then shows unused functions in a pretty table.

Visit [chips git](https://github.com/kovalruss/chips) to see the insights

## Installation

**Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Chips**

```bash
pip install python-chips
```

**Setup Chips**

By default chips setups everything for you, after `-s` command. If you are running into problems, use args below.
1) `-v --venv <on/off>` Defaults to `on`. Determine whether you are using virtualenv or not. If set to `on` Chips will search for a virtualenv on a root path. **Note:** if `--venv off`, you should run commands below with `python -m chips` instead of `$chips` 
2) `-p --path <YOUR_VIRTUALENV_PATH>` Specify virtualenv path if venv not found

```bash
python -m chips -s
```
**Open a new tab in terminal or run** ``source <YOUR_VIRTUALENV_PATH>/bin/activate``

## Usage
**BEFORE YOU START:** If you want to fully "chip" a big project (not a single app directory), it's highly recommended
to use `--auto off` with `-a` command, for improving project performance. Learn more about `--auto` option below.

1) Add chips to your project (-a --add)

```bash
$chips -a
```
2) Use your code (trigger functions in a way: make api requests, click website, etc..)

3) Generate results file with `$chips -rs` (only if `--auto off` on `-a`). See the generated results at .chipping_results/results.py in a pretty table

![_pretty_table.png](https://raw.githubusercontent.com/kovalruss/chips/master/README_IMGS/_pretty_table.png)

4) Remove chips (-r --remove)
```bash
$chips -r
```

## Ignore particular dirs and files
To exclude particular dirs and files from chipping (f.e. tests and manage.py in Django) 
Chips generates a .chipsignore file, based on your .gitignore. Syntax is the same.

There's a basic excludes list in .chipsignore. You can modify it any time you want.

![_chipsignore.png](https://raw.githubusercontent.com/kovalruss/chips/master/README_IMGS/_chipsignore.png)
Full ignores list [here](https://github.com/kovalruss/chips/blob/master/chips/common/basic_excludes.py)
## Chipping path
Basically Chips are performing on a root path of your project. You can specify a folder or file **local path**, where you want Chips to perform (add or remove). Use -p --path arg.
```bash
$chips -a -p <DESIRED PATH>
```

## Bad performance
If you struggle from a bad performance after chipping, use --auto off to turn off auto generated results
```bash
$chips -a --auto off
```

Then you'll need to generate results manually (-rs --results)
```bash
$chips -rs
```

## Chips logging
Choose logging type. Can be applied to remove and add (-rt --result_type)
1) list (default for add) - list all affected files, 
2) count (default for remove) - print number of files affected,
3) blind - no output
```bash
$chips -a -rt count
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
[git here](https://github.com/kovalruss/chips)