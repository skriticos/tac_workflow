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

def ProjectEditHelp():
# ~~~~~~~~~~~~~~~~~~~~
    """
        Show help for edit project menu.
    """
    print()
    print('BACK:        back to project menu')
    print('NAME:        edit project name')
    print('TITLE:       edit project title')
    print('DESCRIPTION: edit project description')
    print('HELP:        show this help')
    print()

def WorkflowHelp():
# ~~~~~~~~~~~~~~~~~
    print()
    print('M:      back to main menu')
    print('B:      one level up')
    print('Q:      quit application')
    print('S:      select a sub-workflow')
    print('INFO:   show workflow details')
    print('LIST:   list sub-workflows')
    print('TREE:   list sub-workflows recursively')
    print('EDIT:   edit workflow')
    print('CREATE: create a sub-workflow')
    print('D:      delete sub-workflow')
    print('H:      show this help')
    print()

