#! /usr/bin/env python3

"""
    Main module. Contains the navigation menu and connects the other modules.
"""

import os.path
import util
import prompt
import project
import workflow
import hlp
import database

class menuitems:
    root = [
        'quit', 'select', 'list', 'tree', 'create', 'delete', 'help']
    project = [
        'back', 'select', 'info', 'list', 'tree', 'edit', 'create', 'help']
    projectEdit = [
        'back', 'name', 'title', 'description', 'help']
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
        if char == 'S':
            pid = project.Select(db)
            if pid:
                projectMenu(db, pid)
        if char == 'L':
            project.List(db)
        if char == 'T':
            pass # tree
        if char == 'C':
            pid = project.Create(db)
            projectMenu(db, pid)
        if char == 'D':
            pass # delete a project and all of it's workflows
        if char == 'H':
            hlp.RootHelp()

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
            project.Info(db, pid)
        if char == 'L':
            workflow.ListRoot(db, pid)
        if char == 'T':
            pass # tree
        if char == 'E':
            projectEditMenu(db, pid, projectName)
        if char == 'C':
            workflow.Create(db, pid)
        if char == 'H':
            hlp.ProjectHelp()

def projectEditMenu(db, pid, projectName):
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
        Show project edit menu and prompt.
    """
    char = None
    while char != 'B':
        char = prompt.Prompt(menuitems.projectEdit, '/' + projectName)
        if char == 'N':
            project.EditName(db, pid, projectName)
        if char == 'T':
            project.EditTitle(db, pid)
        if char == 'D':
            project.EditDescription(db, pid)
        if char == 'H':
            hlp.ProjectEditHelp()

mainMenu(setupDatabase())

