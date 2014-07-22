"""
    Interactive user input module

    Collection of functions that read and validate user input. This is the only
    module that deals with direct user input and input validation.
"""

import subprocess
import tempfile
import re

def PromptChar(options, path):
    """
        Read a character option from user input

        Loop until the user entered a character that was specified in the
        options argument. Characters the user entered beyond the first one are
        discarded. Return valid character.

        Example:
            opt = prompt.PromptChar('abc', '/foo/bar')
    """
    choice = None
    while choice not in list(options):
        userin = input('[' + path + ']: ')
        if len(userin) == 0:
            print('error: empty user input, try again..')
            continue
        choice = userin[0]
        if choice not in list(options):
            print('error: invalid option, try again..')
    return choice

def PromptInt(validnumbers, path):
    """
        Read number option from user input

        Loop until user enters a valid number from a set specified in the
        validnumbers argument. Valid number is returned.

        Example:
            opt = prompt.PromptInt((1, 3, 4, 5), '/foo/bar')
    """
    choice = 0
    while choice not in validnumbers:
        choice = input('[' + path + ']: ')
        if not choice.isdigit():
            print('error: only digits allowed, try again..')
            continue
        choice = int(choice)
        if choice not in validnumbers:
            print('error: choice not in valid numbers, try again..')
    return choice

identifierregex = re.compile('^[_a-zA-Z][_a-zA-Z0-9]{0,16}$')
def PromptName():
    """
        Read a project or workflow name from user input

        Loop until the user enters a valid name that is defined by the
        identifierregex pattern. Return valid name.

        Example:
            name = prompt.PromptName()
    """
    nameok = False
    while not nameok:
        name = input('name: ')
        if identifierregex.match(name):
            nameok = True
        else:
            print('error: invalid name pattern, try again..')
    return name

def PromptTitle():
    """
        Read project or workflow title from user input

        Example:
            title = prompt.PromptTitle()
    """
    title = input('title: ')
    return title

def _vimedit(content=''):
    """
        Open a temporary file in vim for the user to edit

        Create a temporary file, write content into it, run a subprocess with
        vim and the file and read back the changed content.

        Example:
            newdescription = _vimedit(olddescription)
    """
    tmpfp = tempfile.NamedTemporaryFile()
    tmpfilename = tmpfp.name
    if content:
        tmpfp.write(content.encode('UTF-8'))
        tmpfp.flush()
    subprocess.call(['/usr/bin/vim', tmpfilename])
    tmpfp.seek(0)
    return tmpfp.read().decode('UTF-8')

def PromptDescription(olddescription=''):
    """
        Let the user edit a project or workflow description

        Example:
            newdescription = prompt.PromptDescription(olddescription)
    """
    newdescription = _vimedit(olddescription)
    return newdescription

def PromptStatus():
    """
        Read a workflow status from interactive user input

        Show a list of available status options, let the user select one and
        return it.

        Example:
            status = prompt.PromptStatus()
    """
    validstatuses = ['Open', 'Active', 'Completed', 'Aborted']
    validopts = set()
    for x, status in enumerate(validstatuses):
        print('    {}: {}'.format(x+1, status))
        validopts.add(x+1)
    choice = PromptInt(validopts, 'status')-1
    return validstatuses[choice]

