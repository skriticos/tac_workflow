"""
    This module contains functions that are related to project editing.
"""

import re
import util

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

