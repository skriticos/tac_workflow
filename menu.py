"""
    Utility functions that are used to compose the navigation menu and query the
    user for navigation commands via a prompt.
"""

def draw(optlist):
# ~~~~~~~~~~~~~~~~
    """
        Take a list of menu options, puts the first characters in between
        brackets to indicate that these are the command keys for this option and
        output menu to the console sandwiched in two horizontal lines.

        in: ['foo', 'bar']
        out (terminal):
            ~~~~~~~~~~~~~~~~~~~
            [F]OO ~ [B]AR
            ~~~~~~~~~~~~~~~~~~~
    """
    print()
    print(80*'~')
    optlist2 = []
    for opt in optlist:
        o = opt.upper()
        o = '[' + o[0] + ']' + o[1:]
        optlist2.append(o)
    print(' ~ '.join(optlist2))
    print(80*'~')

def readinput(wfpath):
# ~~~~~~~~~~~~~~~~~~~~
    """
        Take a path, draw it surrounded with barkets and read user input.

        in: '/foo/bar', user input (terminal)
        out (terminal): '[/foo/bar]: '
        out: (user input)
    """
    return input('[' + wfpath + ']: ')

def Prompt(optlist, wfpath):
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
        Takes an option list of strings and a path. Compiles a list of valid
        options. Draws a menu and queries user input until valid.

        in: ['foo', 'bar'], '/a/b/c'
        out: [f|b]
    """
    optchars = []
    for opt in optlist:
        optchars.append(opt[0].upper())
    char = None
    while char not in optchars:
        draw(optlist)
        char = readinput(wfpath)[0].upper()
        if char not in optchars:
            print('Invalid input! Try again..')
    return char

def PromptProjectId(db):
# ~~~~~~~~~~~~~~~~~~~~~~
    """
        Prompt the user to select a project id.
    """
    validIds = set()
    for row in db.getAllRows('tblProject', ['pid']):
        validIds.add(row['pid'])
    choice = None
    while choice not in validIds:
        try:
            choice = int(input('Enter the Project ID: '))
        except ValueError:
            print('    Project id must be an integer!')
        if choice not in validIds:
            print('    Invalid id. Enter a valid id')
    return choice

