"""
    User menu functions

    When interacting with the user interface menu, the user is moving through
    the functions in this file to trigger view/edit actions and navigate the
    workflow tree.

    A tree can look like this:
    {project a}
      {root workflow a.1}
        {sub workflow a.1.i}
        {sub workflow a.1.ii}
      {root workflow a.2}
    {project b}
      ..

    Sub workflows can be nested without limit.
    The user starts with the main menu. From there he can select a project which
    puts him in the project menu. The selected project is identified by the
    project pid listed in the database. From here the user can select root
    workflows and then sub workflows and navigate up again.
"""


import sys
import prompt
import project
import workflow
import hlp

def MainMenu(db):
    print('input [h] in any menu to see options')
    path = '/'
    choice = None
    while choice != 'q':
        choice = prompt.PromptChar('cdlthuq', path)
        if choice == 'c':
            pid = project.CreateProject(db)
            ProjectMenu(db, pid)
        elif choice == 'd':
            project.DeleteProject(db)
        elif choice == 'l':
            project.ListProjects(db)
        elif choice == 't':
            project.ProjectTree(db)
        elif choice == 'h':
            hlp.MainMenuHelp()
        elif choice == 'u':
            pid = project.SelectProject(db)
            ProjectMenu(db, pid)
        elif choice == 'q':
            sys.exit(0)

def ProjectMenu(db, pid):
    projectName = db.getConditionalRow(
            'tblProject', ['name'], {'pid': pid})['name']
    path = '/' + projectName
    choice = None
    while choice not in ['b', 'm']:
        choice = prompt.PromptChar('cdilthuebmq', path)
        if choice == 'c':
            wif = workflow.CreateRootWorkflow(db, pid)
            WorkflowMenu(db, wif, path)
        elif choice == 'd':
            workflow.DeleteRootWorkflow(db, pid)
        elif choice == 'i':
            project.ProjectInfo(db, pid)
        elif choice == 'l':
            workflow.ListRootWorkflows(db, pid)
        elif choice == 't':
            workflow.RootWorkflowTree(db, pid)
        elif choice == 'h':
            hlp.ProjectHelp()
        elif choice == 'u':
            wif = workflow.SelectRootWorkflow(db, pid)
            choice = WorkflowMenu(db, wif, path)
        elif choice == 'e':
            choice = ProjectEditMenu(db, pid, path)
        elif choice == 'q':
            sys.exit(0)

def WorkflowMenu(db, wif, path):
    workflowName = db.getConditionalRow(
            'tblWorkflow', ['name'], {'wif': wif})['name']
    path = path + '/' + workflowName
    choice = None
    while choice not in ['b', 'm']:
        choice = prompt.PromptChar('cdilthuebmq', path)
        if choice == 'c':
            wif = workflow.CreateSubWorkflow(db, wif)
            choice = WorkflowMenu(db, wif, path)
        elif choice == 'd':
            workflow.DeleteSubWorkflow(db, wif)
        elif choice == 'i':
            workflow.WorkflowInfo(db, wif)
        elif choice == 'l':
            workflow.ListSubWorkflows(db, wif)
        elif choice == 't':
            workflow.WorkflowTree(db, wif)
        elif choice == 'h':
            hlp.WorkflowHelp()
        elif choice == 'u':
            wif = workflow.SelectSubWorkflow(db, wif)
            choice = WorkflowMenu(db, wif, path)
        elif choice == 'e':
            choice = WorkflowEditMenu(db, wif, path)
        elif choice == 'q':
            sys.exit(0)
    # fall through all nested calls when returning to main menu
    if choice == 'm':
        return choice
    else:
        return None

def ProjectEditMenu(db, pid, path):
    choice = None
    while choice != 'b':
        choice = prompt.PromptChar('ntrihbmq', path)
        if choice == 'n':
            project.EditProjectName(db, pid)
        elif choice == 't':
            project.EditProjectTitle(db, pid)
        elif choice == 'r':
            project.EditProjectDescription(db, pid)
        elif choice == 'i':
            project.ProjectInfo(db, pid)
        elif choice == 'h':
            hlp.ProjectEditHelp()
        elif choice == 'm':
            return choice
        elif choice == 'q':
            sys.exit(0)
    return None

def WorkflowEditMenu(db, wif, path):
    choice = None
    while choice != 'b':
        choice = prompt.PromptChar('ntrsihbmq', path)
        if choice == 'n':
            workflow.EditWorkflowName(db, wif)
        elif choice == 't':
            workflow.EditWorkflowTitle(db, wif)
        elif choice == 'r':
            workflow.EditWorkflowDesription(db, wif)
        elif choice == 's':
            workflow.EditWorkflowStatus(db, wif)
        elif choice == 'i':
            workflow.WorkflowInfo(db, wif)
        elif choice == 'h':
            hlp.WorkflowEditHelp()
        elif choice == 'm':
            return choice
        elif choice == 'q':
            sys.exit(0)

