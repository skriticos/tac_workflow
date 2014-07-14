"""
    This module contains functions that are related to project editing.
"""

import re
import textwrap
import util
import prompt

identRegex = re.compile('^[_a-zA-Z][_a-zA-Z0-9]{0,16}$')

def readName(currentName=''):
# ~~~~~~~~~~~~~~~~~~~~~~~
    """
        Read project name and validate it

        If currentName is provided, it is printed. Then it reads the project
        name from the user. Checks the project name and loops until it's valid.
    """
    if currentName:
        print('Current name:', currentName)
    nameOk = False
    while not nameOk:
        name = input('Project new name: ')
        if identRegex.match(name):
            nameOk = True
        else:
            print('    Invalid name!')
            print('    Only letters, numbers and underscores are allowed.')
            print('    First character must not be a number.')
            print('    Max. 16 charaterss.')
    return name

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
    name = readName()
    title = input('Project title: ')
    description = util.vimEdit()
    pid = db.addProject(name, title, description)
    return pid

def EditName(db, pid, projectName):
# ~~~~~~~~~~~~~~~~~~~~
    """
        Edit project name
    """
    print('Editing project name..')
    newname = readName(projectName)
    db.updateRow('tblProject', {'name': newname}, {'pid': pid})

def EditTitle(db, pid):
# ~~~~~~~~~~~~~~~~~~~~~
    """
        Edit project title
    """
    print('Editing project title..')
    oldtitle = db.getConditionalRow('tblProject', ['title'], {'pid': pid})
    oldtitle = oldtitle['title']
    print('Current title: ', oldtitle)
    newtitle = input('Enter new title: ')
    db.updateRow('tblProject', {'title': newtitle}, {'pid': pid})

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
    pid = prompt.PromptProjectId(db)
    return pid

def Info(db, pid):
# ~~~~~~~~~~~~~~~~
    """
        Print project name, title and description.
    """
    record = db.getConditionalRow('tblProject',
            ['name', 'title', 'description'], {'pid': pid})
    print()
    print('Project Name:', record['name'])
    print('Project Title:', record['title'])
    print('Project Description:')
    print(textwrap.indent(record['description'], 4*' '))

