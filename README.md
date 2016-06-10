# PyCo - The Python Console

**TL;DR** I was looking for a customizable, portable, open source and cross-platform console, a place where would possible to easily write and compose commands: this is PyCo! Feel free to contribute!

At the very beginning of all of this, I was trying to write a console specific for Data Science, I used to write a lot of Python scripting in order to do common Data Science tasks like cleaning or reshaping data, dumping on file and many more. So I told myself that would be nice to have everything in one place where I can run my own "commands". Later I figured out that Python versatility can allow easily to write whatever commands we want, so here we are: PyCo was born! As far as you keep your commands cross-platform and open source, you may want to share them with us!

# Contents

- [The `pyco` Module](pyco/README.md)
- [The `pyco.core` Module](pyco/core/README.md)
- [The `pyco.utils` Module](pyco/utils/README.md)
- [The `pyco.commands` Module](pyco/commands/README.md)

# Examples

`tic && ls > output.txt && head output.txt && toc` this will reverse on the file `output.txt` the list of files in the current folder. `tic` and `toc` are aliases defined in the file `.aliases` and are used to compute the execution file, finally `head` show the first 10 lines of `output.txt`.

`ls || echo` just a really complex way to `ls`.

`plot -x 1,2,3 -y 3.4, 1.7, 0.65` will use pygal (http://www.pygal.org/) to plot the data.

`stats 3.4, 1.7, 0.65, 0.77, 13 3.4` will return the basic statistics for the provided list of values.

# What Is Supported in PyCo?

PyCo support several things, among the others the most important are:
- aliases: take a look to the file `.aliases` and `pyco.commands.base.Alias`
- stdout redirect: PyCo support `>` to append on file and `>>` to write on a new file, you can find details about the implementation in `pyco.core.parser.CommandParser`
- conditional execution: `&` and `&&` for chaining commands
- pipe and conditional pipe: `|` and `||` for piping outputs

# How To Create Commands?

You can easily take a look to `pyco.commands` that is the module that implements all the available commands. The idea is to create a class derived from `pyco.core.base_commands`:

    class MyCommand(BaseCommand):
        ...

there are three class properties:

    class MyCommand(BaseCommand):
        __cmd_name__ = 'mycommand'
        __cmd_ver__ = '0.0.0'
        __cmd_tags__ = ['tag1', 'tag2']
        ... 

namely: `__cmd_name__` the command name as should used from the command line; `__cmd_ver__` the current version for this command; and `__cmd_tags__` a list of tags to categorized the command. Now, there are mainly 3 function to be implemented:

    class MyCommand(BaseCommand):
        __cmd_name__ = 'mycommand'
        __cmd_ver__ = '0.0.0'
        __cmd_tags__ = ['tag1', 'tag2']
        
        def __init__(self, options):
            super(MyCommand, self).__init__(options=options)
        
        def add_args(self):
                parser = argparse.ArgumentParser(prog=self.name,
                                                 description='Description of mycommand')
                parser.add_argument('-a', '--argument',
                                    dest='argument',
                                    help='An argument, (default=%(default)r).')
                ...
                return parser
        
        def impl(self):
            opts = self.get_options()
            ...
            return 0

the `__init__` is needed in order to let the base class to process the options (aka arguments or args); the `add_args` define the arguments expected by the command, this is very `argparse` so you can make it as complex as `argparse` permits; `impl` is the actual implementation of you command, from here you can access to the options with `self.get_options()` remember: you should return 0 if everything goes fine and an integer different than 0 if there was some error.

Last step. In order to make your commands available you need to import them inside `pyco.commands.__init__`.

I strongly suggest you to take a look to the existing commands to get inspiration!

# What Is Still Missing?

There are several open points and things todo, I'll try to summarize here the most relevant at the current moment (IMHO).

## PyCo GUI
It would be really great to have PyCo running in its own window making it independent from running inside others shells. Several libraries can be useful for this purpose, the one that I'm considering is `wxPython` (http://www.wxpython.org/) also because this should help us in solving also the **Key Detection** aspect.

## Key Detection
I really like the idea of using additional key combination to better interact with PyCo. It would be great if it would be able to detect key combination like `ctrl+r` for searching in the history or arrows for move in the history up to `tab` for autocomplete. This is not an easy task particularly because I want to keep PyCo open source and cross-platform.

## Comments
I'm not really good in commenting and describing the code, so feel free to clarify and extend comments and descriptions.

## Guide and/or Help
If you read the previous section you know that I'm not really good in writing, so if you want to contribute explaining how to use PyCo with guides, tutorial and help, you are very welcome. If decide to contribute, please keep also updated `pyco.commands.base.Help`.

## Numpy and Other not Easily Manageble Packages
In order to maintain the cross-platform capability I did not included packages like: `numpy`, `scipy` or `scikit-learn` it would be amazing if someone much more skilled than me will find a way for integrate them properly.

# Create a PEX or Windows Executable

This is easy like:

`pex -r requirements.txt -e pyco.pyconsole:main -o pyco.pex`

or:

`python setup.py py2exe`
