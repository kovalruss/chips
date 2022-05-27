# 👾 Chips

Chips is a tool that inserts "chips" to your code, detecting unused fragments. Then shows unused functions in a pretty table. Might be used for developing, refactoring and manual testing purposes

## Installation

**Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Chips**

```bash
pip install python-chips
```

**Setup Chips with a command below**

1) `-v --venv <on/off>` Determine whether you are using virtualenv or not. If on Chips will search for a virtualenv on a root path. Defaults to on. **Note:** if you are not using virtualenv you should run commands below with `python -m chips` instead of `$chips` 
2) `-p --path <YOUR_VIRTUALENV_PATH>` Specify virtualenv path if venv not found

```bash
python -m chips -s
```
**Open a new tab in terminal or run** ``source <YOUR_VIRTUALENV_PATH>/bin/activate``

## Usage

1) Add chips to your project (-a --add)

```bash
$chips -a
```
2) Use your code (trigger functions in a way: make api requests, click website, etc..)

3) See the auto generated results at .chipping_results/results.py in a pretty table

![_pretty_table.png](README_IMGS/_pretty_table.png)

4) Remove chips (-r --remove)
```bash
$chips -r
```

## Ignore particular dirs and files
To exclude particular dirs and files from chipping (f.e. tests and manage.py in Django) 
Chips generate a .chipsignore file, based on your .gitignore. Syntax is the same.

There's a basic excludes list in .chipsignore. You can modify it any time you want.

![_chipsignore.png](README_IMGS/_chipsignore.png)

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
1) list_files (default for add) - list all affected files, 
2) count_files (default for remove) - print number of files affected,
3) blind - no output
```bash
$chips -a -rt count_files
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.