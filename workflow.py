"""
    Functions related to workflow edititing
"""

import re
import textwrap
import time
import util
import prompt

identRegex = re.compile('^[_a-zA-Z][_a-zA-Z0-9]{0,16}$')

def readName(currentName=''):
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
# ~~~~~~~~~~~~~~~~~~
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

def EditName(db, wif):
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    wfname = db.getConditionalRow('tblWorkflow', ['name'], {'wif':wif})
    wfname = wfname['name']
    print('Editing workflow name..')
    newname = readName(wfname)
    db.updateRow('tblWorkflow', {'name': newname}, {'wif': wif})

def EditTitle(db, wif):
# ~~~~~~~~~~~~~~~~~~~~~
    print('Editing workflow title..')
    oldtitle = db.getConditionalRow('tblWorkflow', ['title'], {'wif': wif})
    oldtitle = oldtitle['title']
    print('Current title: ', oldtitle)
    newtitle = input('Enter new title: ')
    db.updateRow('tblWorkflow', {'title': newtitle}, {'wif': wif})

def EditDescription(db, wif):
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print('Editing workflow description..')
    olddesc = db.getConditionalRow('tblWorkflow', ['description'], {'wif': wif})
    olddesc = olddesc['description']
    newdesc = util.vimEdit(olddesc)
    db.updateRow('tblWorkflow', {'description': newdesc}, {'wif': wif})

def EditStatus(db, wif):
# ~~~~~~~~~~~~~~~~~~~~~~
    print('Editing workflow status..')
    oldstatus = db.getConditionalRow('tblWorkflow', ['status'], {'wif': wif})
    oldstatus = oldstatus['status']
    print('Current status:', oldstatus)
    newstatus = prompt.PromptWorkflowStatus(db, wif)
    db.updateRow('tblWorkflow', {'status': newstatus}, {'wif': wif})

def ListRoot(db, pid):
# ~~~~~~~~~~~~~~~~~~~~
    """
        List the ids, names and titles of all root-workflows
    """
    print()
    print('List of Root-Workflows:')
    workflows = db.getConditionalRows(
            'tblWorkflow',
            ['wif', 'name', 'title'],
            {'ppid': pid, 'pwif': -1})
    for wf in workflows:
        print('    {wif}: {name} - {title}'.format(**wf))

def SelectRoot(db, pid):
# ~~~~~~~~~~~~~~~~~~~~~~
    workflowCount = db.getConditionalRowCount(
            'tblWorkflow', {'ppid': pid, 'pwif': -1})
    if not workflowCount:
        print('This project has no workflows! Aporting select..')
        return None
    print()
    print('Selecting a root-workflow..')
    ListRoot(db, pid)
    pid = prompt.PromptRootWorkflowId(db, pid)
    return pid

def Info(db, wif):
# ~~~~~~~~~~~~~~~~
    record = db.getConditionalRow('tblWorkflow',
            ['name', 'title', 'description', 'status', 'created', 'modified'],
            {'wif': wif})
    print()
    print('Workflow ID:      ', wif)
    print('Workflow Name:    ', record['name'])
    print('Workflow Title:   ', record['title'])
    print('Workflow Status:  ', record['status'])
    print('Workflow Created: ', time.ctime(record['created']))
    print('Workflow Modified:', time.ctime(record['modified']))
    print('Workflow Description:')
    print(textwrap.indent(record['description'], 4*' '))

