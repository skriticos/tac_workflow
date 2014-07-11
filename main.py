"""
    Main module. Contains the navigation menu and connects the other modules.
"""

import util
import menu
import project
import hlp

# menus
rootMenu = [
    'quit', 'select', 'list', 'tree', 'create', 'help']
projectMenu = [
    'back', 'select', 'info', 'list', 'tree', 'edit', 'create', 'help']
projectEditMenu = [
    'name', 'title', 'description', 'back', 'help']
workflowMenu = [
    'main', 'back', 'select', 'info', 'list', 'tree', 'edit', 'create', 'h' ]
workflowEditMenu = [
    'name', 'title', 'description', 'status', 'back', 'help']

# menu loop
char = None
while char != 'Q':
    char = menu.Prompt(rootMenu, '/')
    if char == 'H':
        hlp.RootHelp()
    if char == 'C':
        project.Create(None)

