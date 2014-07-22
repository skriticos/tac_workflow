"""
    Counterpart to project.py
"""
import time
import textwrap
import prompt

def CreateRootWorkflow(db, pid):
    print('create root workflow..')
    name = prompt.PromptName()
    title = prompt.PromptTitle()
    description = prompt.PromptDescription()
    status = 'Open'
    timestamp = int(time.time())
    wif = db.insert('tblWorkflow',
            {'ppid': pid,
             'pwif': -1,
             'name': name,
             'title': title,
             'description': description,
             'status': status,
             'created': timestamp,
             'modified': timestamp})
    return wif

def CreateSubWorkflow(db, wif):
    print('create sub workflow..')
    name = prompt.PromptName()
    title = prompt.PromptTitle()
    description = prompt.PromptDescription()
    status = 'Open'
    timestamp = int(time.time())
    ppid = db.getConditionalRow('tblWorkflow', ['ppid'], {'wif': wif})['ppid']
    subwif = db.insert('tblWorkflow',
            {'ppid': ppid,
             'pwif': wif,
             'name': name,
             'title': title,
             'description': description,
             'status': status,
             'created': timestamp,
             'modified': timestamp})
    return subwif

def DeleteWorkflowRecursively(db, wif):
    subwfs = db.getConditionalRows('tblWorkflow', ['wif'], {'pwif': wif})
    for wf in subwfs:
        DeleteWorkflowRecursively(db, wf['wif'])
        db.delete('tblWorkflow', {'wif': wif})

def DeleteRootWorkflow(db, pid):
    print('select root workflow id to delete..')
    wfcount = db.getConditionalRowCount(
            'tblWorkflow', {'ppid': pid, 'pwif': -1})
    if wfcount == 0:
        print('error: project has no workflows, aborting..')
        return
    ListRootWorkflows(db, pid)
    wfrows = db.getConditionalRows(
            'tblWorkflow', ['wif'], {'ppid': pid, 'pwif': -1})
    validchoices = set()
    for wf in wfrows:
        validchoices.add(wf['wif'])
    wif = prompt.PromptInt(validchoices, 'wif')
    DeleteWorkflowRecursively(db, wif)

def DeleteSubWorkflow(db, wif):
    print('select sub workflow id to delete..')
    wfcount = db.getConditionalRowCount('tblWorkflow', {'pwif': wif})
    if wfcount == 0:
        print('error: workflow has no sub workflows, aborting..')
        return
    ListSubWorkflows(db, wif)
    wfrows = db.getConditionalRows('tblWorkflow', ['wif'], {'pwif': wif})
    validchoices = set()
    for wf in wfrows:
        validchoices.add(wf['wif'])
    nwif = prompt.PromptInt(validchoices, 'wif')
    DeleteWorkflowRecursively(wif)

def ListRootWorkflows(db, pid):
    print('listing root workflows..')
    wfcount = db.getConditionalRowCount(
            'tblWorkflow', {'ppid': pid, 'pwif': -1})
    if wfcount == 0:
        print('project has no workflows')
        return
    print('    WIF: NAME - [STATUS] TITLE')
    print('    --------------------------')
    wflist = db.getConditionalRows('tblWorkflow',
            ['wif', 'name', 'status', 'title'], {'ppid': pid, 'pwif': -1})
    for wf in wflist:
        print('    {wif}: {name} - [{status}] {title}'.format(**wf))

def ListSubWorkflows(db, wif):
    print('listing sub workflows..')
    wfcount = db.getConditionalRowCount('tblWorkflow', {'pwif': wif})
    if wfcount == 0:
        print('workflow has no sub workflows')
        return
    print('    WIF: NAME - [STATUS] TITLE')
    print('    --------------------------')
    wflist = db.getConditionalRows('tblWorkflow',
            ['wif', 'name', 'status', 'title'], {'pwif': wif})
    for wf in wflist:
        print('    {wif}: {name} - [{status}] {title}'.format(**wf))

def WorkflowTree(db, wif, indent=''):
    topwf = db.getConditionalRow('tblWorkflow',
            ['wif', 'name', 'status', 'title'], {'wif': wif})
    topwf['indent'] = indent
    print('{indent}{wif}: {name} - [{status}] {title}'.format(**topwf))
    workflows = db.getConditionalRows(
            'tblWorkflow', ['wif', 'name', 'status', 'title'], {'pwif': wif})
    for wf in workflows:
        indent += '   '
        WorkflowTree(db, wf['wif'], indent)

def RootWorkflowTree(db, pid):
    wifs = db.getConditionalRows('tblWorkflow',
            ['wif'], {'ppid': pid, 'pwif': -1})
    for wif in wifs:
        WorkflowTree(db, wif['wif'])

def SelectRootWorkflow(db, pid):
    print('select root workflow..')
    wfcount = db.getConditionalRowCount(
            'tblWorkflow', {'ppid': pid, 'pwif': -1})
    if wfcount == 0:
        print('error: project has no workflows, aborting..')
        return
    ListRootWorkflows(db, pid)
    wfrows = db.getConditionalRows(
            'tblWorkflow', ['wif'], {'ppid': pid, 'pwif': -1})
    validchoices = set()
    for wf in wfrows:
        validchoices.add(wf['wif'])
    nwif = prompt.PromptInt(validchoices, 'wif')
    return nwif

def SelectSubWorkflow(db, wif):
    print('select sub workflow..')
    wfcount = db.getConditionalRowCount('tblWorkflow', {'pwif': wif})
    if wfcount == 0:
        print('error: workflow has no sub workflows, aborting..')
        return
    ListSubWorkflows(db, wif)
    wfrows = db.getConditionalRows('tblWorkflow', ['wif'], {'pwif': wif})
    validchoices = set()
    for wf in wfrows:
        validchoices.add(wf['wif'])
    nwif = prompt.PromptInt(validchoices, 'wif')
    return nwif

def WorkflowInfo(db, wif):
    print('listing workflow information..')
    record = db.getConditionalRow(
            'tblWorkflow',
            ['name', 'title', 'description', 'status', 'created', 'modified'],
            {'wif': wif})
    out =  'Name:     {name}\n'
    out += 'Title:    {title}\n'
    out += 'Status:   {status}\n'
    out += 'Created:  {created}\n'
    out += 'Modified: {modified}\n'
    out += 'Description:\n{description}'
    record['description'] = textwrap.indent(record['description'], 4*' ')
    print(out.format(**record))

def EditWorkflowName(db, wif):
    print('editing workflow name..')
    currentname = db.getConditionalRow('tblWorkflow', ['name'], {'wif': wif})
    print('    current name: {name}'.format(**currentname))
    newname = prompt.PromptName()
    db.updateRow('tblWorkflow', {'name': newname}, {'wif': wif})

def EditWorkflowTitle(db, wif):
    print('editing workflow title..')
    currenttitle = db.getConditionalRow('tblWorkflow', ['title'], {'wif': wif})
    print('    current title: {title}'.format(**currenttitle))
    newtitle = prompt.PromptTitle()
    db.updateRow('tblWorkflow', {'title': newtitle}, {'wif': wif})

def EditWorkflowDesription(db, wif):
    print('editing workflow description..')
    cdesc = db.getConditionalRow('tblWorkflow', ['description'], {'wif': wif})
    cdesc = cdesc['description']
    ndesc = prompt.PromptDescription(cdesc)
    db.updateRow('tblWorkflow', {'description': ndesc}, {'wif': wif})

def EditWorkflowStatus(db, wif):
    print('editing workflow status..')
    cstatus = db.getConditionalRow('tblWorkflow', ['status'], {'wif': wif})
    print('    current status: {status}'.format(**cstatus))
    nstatus = prompt.PromptStatus()
    db.updateRow('tblWorkflow', {'status'}, {'wif': wif})

