"""
    Main module. Contains the navigation menu and connects the other modules.
"""

import os.path
import util
import menu
import project
import hlp
import database

class menuitems:
    root = [
        'quit', 'select', 'list', 'tree', 'create', 'help']
    project = [
        'back', 'select', 'info', 'list', 'tree', 'edit', 'create', 'help']
    projectEdit = [
        'name', 'title', 'description', 'back', 'help']
    workflow = [
        'main', 'back', 'select', 'info', 'list', 'tree', 'edit', 'create', 'h' ]
    workflowEdit = [
        'name', 'title', 'description', 'status', 'back', 'help']

# setup database
db = database.DataBase(os.path.join(
        os.path.expanduser('~'), '.local', 'share', 'tac', 'tac.db'))

# main menu loop
char = None
pid = -1   # currently selected project id
wif = -1   # currently selected workflow id
while char != 'Q':
    char = menu.Prompt(menuitems.root, '/')
    if char == 'H':
        hlp.RootHelp()
    if char == 'C':
        pid = project.Create(db)

