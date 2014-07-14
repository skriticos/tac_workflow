"""
    Functions related to workflow edititing
"""

import re
import textwrap
import util
import prompt

identRegex = re.compile('^[_a-zA-Z][_a-zA-Z0-9]{0,16}$')

def readName(currentName=''):
# ~~~~~~~~~~~~~~~~~~~~~~~
    """
        Read workflow name and validate it

        If currentName is provided, it is printed. Then it reads the workflow
        name from the user. Checks the workflow name and loops until it's valid.
    """
    if currentName:
        print('Current workflow name:', currentName)
    nameOk = False
    while not nameOk:
        name = input('New workflow name: ')
        if identRegex.match(name):
            nameOk = True
        else:
            print('    Invalid name!')
            print('    Only letters, numbers and underscores are allowed.')
            print('    First character must not be a number.')
            print('    Max. 16 charaterss.')
    return name

def Create(db, pid):
# ~~~~~~~~~~~~~
    """
        Create a new workflow. Prompt the user for name and title, let the user
        edit the description in an external editor and send the changes to the
        database.

        in: db - database instance
        in (terminal): name, title, description - workflow properties
        out: pid - workflow id in database
    """
    print('Creating new workflow..')
    name = readName()
    title = input('Workflow title: ')
    description = util.vimEdit()
    pid = db.addRootWorkflow(pid, name, title, description)
    return pid

