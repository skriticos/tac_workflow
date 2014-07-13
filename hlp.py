"""
    Functions to output help in the various navigation menus.
"""

def RootHelp():
# ~~~~~~~~~~~~~
    """
        Show help for root menu.
    """
    print()
    print('QUIT:   quit application')
    print('SELECT: select a project')
    print('LIST:   list all projects')
    print('TREE:   list all project trees (show all workflows)')
    print('CREATE: create a new project')
    print('HELP:   show this help')
    print()

def ProjectHelp():
# ~~~~~~~~~~~~~~~~
    """
        Show help for project menu.
    """
    print()
    print('BACK:   back to root menu')
    print('SELECT: select workflow')
    print('INFO:   show project info')
    print('LIST:   list workflows')
    print('TREE:   list workflows recursively')
    print('EDIT:   edit project name, title or description')
    print('CREATE: create a new root-workflow')
    print('HELP:   show this help')
    print()
