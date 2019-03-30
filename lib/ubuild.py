# -*- ubuild -*-
"""This library provides a simple framework for creating build menus."""

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import sys
import os
import os.path as op

import auxly
from qprompt import Menu, alert, _guess_name, _guess_desc

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

__version__ = "0.2.1"

#: The main build menu.
_MENU = Menu()

#: Menu names that are reserved.
RESV_NAMES = ["q"]

#: Default script name with extension.
SCRIPTNAME = "_Build.py"

#: Regex used to find alternative script names.
ALTSCRIPTREGEX = "_[A-Z][A-z0-9_-]*\.py$"

#: Line that must be found in a file for it to be an alternative script.
ALTDECLARATION = "# -*- ubuild -*-"

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def _find_script(dpath):
    """Attempts to find a script in the given absolute directory path."""
    if not op.isabs(dpath):
        return
    if SCRIPTNAME in os.listdir(dpath):
        return SCRIPTNAME
    for f in auxly.filesys.walkfiles(dpath, regex=ALTSCRIPTREGEX, recurse=False):
        if ALTDECLARATION in auxly.filesys.File(op.join(dpath, f)).read().splitlines():
            return f

def _taken_names():
    """Returns a list of names already taken by menu entries."""
    return [e.name for e in _MENU.entries] + RESV_NAMES

def menu(*args, **kwargs):
    """Decorator that adds the function to the build menu."""
    args = list(args)
    argfunc = None
    if args and callable(args[0]):
        argfunc = args[0]
        args.pop(0)
    name = args.pop(0) if args else kwargs.get('name')
    desc = args.pop(0) if args else kwargs.get('desc')
    fargs = args.pop(0) if args else kwargs.get('args')
    fkrgs = args.pop(0) if args else kwargs.get('kwargs')
    def decor(func):
        global _MENEU
        nonlocal name, desc, fargs, fkrgs
        if None == desc:
            desc = _guess_desc(func.__name__)
        if None == name:
            name = _guess_name(desc, _taken_names())
        _MENU.add(name, desc, func, fargs, fkrgs)
        return func
    if argfunc:
        decor(argfunc)
        return argfunc
    else:
        return decor

def main(**kwargs):
    """Shows the main build menu. When the menu exits, the system-level exit()
    will be called with the menu return value."""
    global _MENEU
    returns = kwargs.pop('returns', "func")
    header = kwargs.pop('header', "Ubuild")
    loop = kwargs.pop('loop', True)
    sys.exit(_MENU.main(loop=loop, returns=returns, header=header, **kwargs))

def runner(searchdir="."):
    """Attempts to locate a build script by checking the search directory and
    walking up parent directories towards the filesystem root. If found, the
    build script will be run. When the script exits, the system-level exit()
    will be called using the return value from the script."""
    cdir = op.abspath(searchdir)
    scriptname = None
    while True:
        scriptname = _find_script(cdir)
        if scriptname:
            break
        if cdir == op.abspath(os.sep):
            break
        cdir = op.abspath(op.join(cdir, ".."))
    if not scriptname:
        alert("Script not found.")
        return
    path = op.join(cdir, scriptname)
    alert(f"Running `{path}`:")
    with auxly.filesys.Cwd(cdir):
        cmd = f"python {scriptname}"
        args = sys.argv[1:]
        if args:
            cmd += " " + " ".join(args)
        sys.exit(auxly.shell.call(cmd))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    if set(sys.argv).intersection({"--version", "-v"}):
        print(f"ubuild-{__version__}")
        sys.exit(0)
    if set(sys.argv).intersection({"--help", "-h"}):
        print("Ubuild is a utility for running build scripts.")
        sys.exit(0)
    runner()
