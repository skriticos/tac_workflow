"""
    Functions to output help in the various navigation menus.
"""

def MainMenuHelp():
    print('main menu help..')
    print('[*]: change data, [i]: display data, [@]: navigate')
    print('c - [*] create project')
    print('d - [*] delete project')
    print('l - [i] list projects')
    print('t - [i] list project tree')
    print('h - [i] show this help')
    print('u - [@] select project')
    print('q - [@] quit application')

def ProjectHelp():
    print('project menu help..')
    print('[*]: change data, [i]: display data, [@]: navigate')
    print('c - [*] create root workflow')
    print('d - [*] delete root workflow')
    print('i - [i] show project information')
    print('l - [i] list root workflows')
    print('t - [i] list root workflow tree')
    print('h - [i] show this help')
    print('u - [@] select root workflow')
    print('e - [@] project edit menu')
    print('b - [@] back to main menu')
    print('m - [@] back to main menu')
    print('q - [@] quit application')

def WorkflowHelp():
    print('workflow menu help..')
    print('[*]: change data, [i]: display data, [@]: navigate')
    print('c - [*] create sub workflow')
    print('d - [*] delete sub workflow')
    print('i - [i] show workflow information')
    print('l - [i] list sub workflows')
    print('t - [i] list sub workflow tree')
    print('h - [i] show this help')
    print('u - [@] select sub workflow')
    print('e - [@] wokflow edit menu')
    print('b - [@] back to parent workflow or project')
    print('m - [@] back to main menu')
    print('q - [@] quit application')

def ProjectEditHelp():
    print('project edit menu help..')
    print('[*]: change data, [i]: display data, [@]: navigate')
    print('n - [*] change name')
    print('t - [*] change title')
    print('r - [*] edit description')
    print('i - [i] show project information')
    print('h - [i] show this help')
    print('b - [@] back to project menu')
    print('m - [@] back to main menu')
    print('q - [@] quit application')

def WorkflowEditHelp():
    print('workflow edit menu help..')
    print('[*]: change data, [i]: display data, [@]: navigate')
    print('n - [*] change name')
    print('t - [*] change title')
    print('r - [*] edit description')
    print('s - [*] change status')
    print('i - [i] show workflow information')
    print('h - [i] show this help')
    print('b - [@] back to workflow menu')
    print('m - [@] back to main menu')
    print('q - [@] quit application')

