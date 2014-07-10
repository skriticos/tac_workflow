import tempfile
import subprocess

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

# cmd = util.prompt('/foo/bar')
#
# Display prompt and read command
# ===============================

def prompt(wfpath):
    return input('[' + wfpath + ']: ')

# newcontent = util.vimEdit('foobar..')
#
# Edit text in vim
# ================
#
# Create a temporary file, write content into it, run a subprocess with vim and
# the file and read back the changed content.

def vimEdit(content=''):
    tmpfp = tempfile.NamedTemporaryFile()
    tmpfilename = tmpfp.name
    if content:
        tmpfp.write(content.encode('UTF-8'))
        tmpfp.flush()
    subprocess.call(['/usr/bin/vim', tmpfilename])
    tmpfp.seek(0)
    return tmpfp.read().decode('UTF-8')

