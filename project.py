"""
    This module contains functions that are related to project editing.
"""

import re
import util
import menu

identRegex = re.compile('^[_a-zA-Z][_a-zA-Z0-9]{0,16}$')

def Create(db):
# ~~~~~~~~~~~~~
    """
        Create a new project. Prompt the user for name and title, let the user
        edit the description in an external editor and send the changes to the
        database.

        in: db - database instance
        in (terminal): name, title, description - project properties
        out: pid - project id in database
    """
    print('Creating new project..')
    nameOk = False
    while not nameOk:
        name = input('Project name: ')
        if identRegex.match(name):
            nameOk = True
        else:
            print('    Invalid name!')
            print('    Only letters, numbers and underscores are allowed.')
            print('    First character must not be a number.')
            print('    Max. 16 charaterss.')
    title = input('Project title: ')
    description = util.vimEdit()
    pid = db.addProject(name, title, description)
    return pid

def List(db):
# ~~~~~~~~~~~
    """
        List existing project names and titles.
    """
    print()
    print('List of Projects:')
    for project in db.getAllRows('tblProject', ['pid', 'name', 'title']):
        print('    {}: {} - {}'.format(
            project['pid'], project['name'], project['title']))

def Select(db):
# ~~~~~~~~~~~~~
    """
        List all projects and ask the user to select one (by id).
    """
    if db.getRowCount('tblProject') == 0:
        print('No projects existent! Aborting select..')
        return None
    print()
    print('Selecting a project..')
    List(db)
    pid = menu.PromptProjectId(db)
    return pid





