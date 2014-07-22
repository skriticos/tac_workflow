tac\_workflow
=============

Interactive CLI workflow management application.

* add/edit projects
* add/edit root-workflows and sub-workflows
* navigate through tree (up, down)
* navigate with path (project/rootworkflow/subworkflow/..)
* sqlite3 backend
* python3 code

tblProject
----------

* pid, name, title, description, created, modified
* created, modified: unix timestamp

tblWorkflow
-----------

* wif, ppid, pwif, name, title, description, status, created, modified
* status: ['open', 'active', 'completed', 'aborted']
* pwif: -1 signifies root workflow, otherwise it contains the parent wif

Workflow tree is built through the ppid/pwif relations.

Names
-----

Project and workflow names are identifiers that are used to navigate the tree.
They have the following constraint: `'^[_a-zA-Z][_a-zA-Z0-9]*$`.

Navigation
----------

Interactive CLI. A menu is presented with the possible options and shortcuts.

* main menu
  * create project
  * list projects (by modification date)
  * list project tree
  * select project

* project menu
  * back to main menu

  * edit project name
  * edit title
  * edit description

  * list root workflows
  * list workflow tree
  * create root workflow
  * select workflow

* workflow menu
  * back to main menu
  * go up one

  * edit name
  * edit title
  * edit description
  * change status

  * list sub-workflows
  * list workflow tree
  * create sub-workflow
  * select sub-workflow

User Interface
--------------

The user interface is menu driven. A list of available options at the current
locations is presented at before each prompt. The prompts show the full project
and workflow path similar to a filesystem. Each menu has a help option to
describe the available options.

Editing Longer Text
-------------------

Descriptions are edited in an exeternal text editor. For this a temporary file
is created and the current content added. Then the user can edit the content in
the editor and when he exits, the file is read back and the database updated.

