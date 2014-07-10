# util.drawMenu(['foo', 'bar', 'xyz'])
#
# ~~~~~~~~~~~~~~~~~~~~~~~~
# [F]OO ~ [B]AR ~ [X]YZ
# ~~~~~~~~~~~~~~~~~~~~~~~~
#
# Draw a menu as shown above.

def drawMenu(optlist):
    print(80*'~')
    optlist2 = []
    for opt in optlist:
        o = opt.upper()
        o = '[' + o[0] + ']' + o[1:]
        optlist2.append(o)
    print(' ~ '.join(optlist2))
    print(80*'~')

