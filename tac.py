#! /usr/bin/env python3

"""
    Main module. Contains the navigation menu and connects the other modules.
"""

import os.path
import util
import prompt
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

def setupDatabase():
# ~~~~~~~~~~~~~~~~~~
    """
        Establish connection with the database file
    """
    return database.DataBase(os.path.join(
            os.path.expanduser('~'), '.local', 'share', 'tac', 'tac.db'))

def mainMenu(db):
# ~~~~~~~~~
    """
        Start main menu loop.
    """
    char = None
    while char != 'Q':
        char = prompt.Prompt(menuitems.root, '/')
        if char == 'H':
            hlp.RootHelp()
        if char == 'C':
            pid = project.Create(db)
        if char == 'L':
            project.List(db)
        if char == 'S':
            pid = project.Select(db)
            if pid:
                projectMenu(db, pid)
        if char == 'T':
            pass # tree

def projectMenu(db, pid):
# ~~~~~~~~~~~~~~~~~~
    """
        Start project menu loop.
    """
    projectName = db.getConditionalRow(
            'tblProject', ['name'], {'pid': pid})['name']
    char = None
    while char != 'B':
        char = prompt.Prompt(menuitems.project, '/' + projectName)
        if char == 'S':
            pass # select
        if char == 'I':
            pass # info
        if char == 'L':
            pass # list
        if char == 'T':
            pass # tree
        if char == 'E':
            pass # edit
        if char == 'C':
            pass # create
        if char == 'H':
            hlp.ProjectHelp()



mainMenu(setupDatabase())

