# draw(['foo', 'bar', 'xyz'])
def draw(optlist):
    print()
    print(80*'~')
    optlist2 = []
    for opt in optlist:
        o = opt.upper()
        o = '[' + o[0] + ']' + o[1:]
        optlist2.append(o)
    print(' ~ '.join(optlist2))
    print(80*'~')

# cmd = readinput('/foo/bar')
def readinput(wfpath):
    return input('[' + wfpath + ']: ')

# opt = menu.Prompt(['foo', 'bar', 'xyz'])
def Prompt(optlist, wfpath):
    optchars = []
    for opt in optlist:
        optchars.append(opt[0])
    char = None
    while char not in optchars:
        draw(optlist)
        char = readinput(wfpath)
        if char not in optchars:
            print('Invalid input! Try again..')
    return char

