"""
    Collection of project interaction function

    Middle layer between menu and user input. The functions in this module act
    as a controller between user input and the database. They output information
    from the database and apply changes to the data that is read from prompt
    functions. There is no direct user input in this module.
"""
import time
import textwrap
import prompt
import workflow

def ListProjects(db):
    print('listing projects..')
    projectCount = db.getRowCount('tblProject')
    if projectCount == 0:
        print('no projects in database')
        return
    print('    PID: NAME - TITLE')
    print('    -----------------')
    projectRows = db.getAllRows('tblProject', ['pid', 'name', 'title'])
    for row in projectRows:
        print('    {pid}: {name} - {title}'.format(**row))

def CreateProject(db):
    print('creating a new project..')
    name = prompt.PromptName()
    title = prompt.PromptTitle()
    description = prompt.PromptDescription()
    timestamp = int(time.time())
    pid = db.insert('tblProject',
            {'name': name,
             'title': title,
             'description': description,
             'created': timestamp,
             'modified': timestamp})
    return pid

def DeleteProject(db):
    print('select project id to delete..')
    ListProjects(db)
    validids = set()
    for row in db.getAllRows('tblProject', ['pid']):
        validids.add(row['pid'])
    pid = prompt.PromptInt(validids, 'pid')
    pwfs = db.getConditionalRows('tblWorkflow', ['wif'], {'ppid': pid})
    for wf in pwfs:
        db.delete('tblProject', {'wif': wf['wif']})
    db.delete('tblProject', {'pid': pid})

def SelectProject(db):
    print('select a project..')
    if db.getRowCount('tblProject') == 0:
        print('error: no projects existent! Aborting select..')
        return None
    ListProjects(db)
    validids = set()
    for row in db.getAllRows('tblProject', ['pid']):
        validids.add(row['pid'])
    pid = prompt.PromptInt(validids, 'pid')
    return pid

def ProjectInfo(db, pid):
    print('listing project information..')
    record = db.getConditionalRow('tblProject',
            ['name', 'title', 'created', 'modified', 'description'],
            {'pid': pid})
    print('Name:    ', record['name'])
    print('Title:   ', record['title'])
    print('Created: ', time.ctime(record['created']))
    print('Modified:', time.ctime(record['modified']))
    print('Description:')
    print(textwrap.indent(record['description'], 4*' '))

def ProjectTree(db):
    projects = db.getAllRows('tblProject', ['pid', 'name', 'title'])
    for pro in projects:
        print('{pid}: {name} - {title}'.format(**pro))
        rootwfs = db.getConditionalRows(
                'tblWorkflow', ['wif', 'name', 'title', 'status'],
                {'ppid':pro['pid'], 'pwif':-1})
        for wf in rootwfs:
            workflow.WorkflowTree(db, wf['wif'], '   ')

def EditProjectName(db, pid):
    print('editing project name..')
    oldname = db.getConditionalRow('tblProject', ['name'], {'pid': pid})
    print('    current name: {name}'.format(**oldname))
    newname = prompt.PromptName()
    db.updateRow('tblProject', {'name': newname}, {'pid': pid})

def EditProjectTitle(db, pid):
    print('editing project title..')
    oldtitle = db.getConditionalRow('tblProject', ['title'], {'pid': pid})
    print('    current title: {title}'.format(**oldtitle))
    newtitle = prompt.PromptTitle()
    db.updateRow('tblProject', {'title': newtitle}, {'pid': pid})

def EditProjectDescription(db, pid):
    print('editing project description..')
    cdesc = db.getConditionalRow('tblProject', ['description'], {'pid': pid})
    cdesc = cdesc['description']
    ndesc = prompt.PromptDescription(cdesc)
    db.updateRow('tblProject', {'description': ndesc}, {'pid': pid})

