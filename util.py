"""
    Utility functions for editing, display, etc.
"""

import tempfile
import subprocess

def vimEdit(content=''):
# ~~~~~~~~~~~~~~~~~~~~~~
    """
        Create a temporary file, write content into it, run a subprocess with
        vim and the file and read back the changed content.
    """
    tmpfp = tempfile.NamedTemporaryFile()
    tmpfilename = tmpfp.name
    if content:
        tmpfp.write(content.encode('UTF-8'))
        tmpfp.flush()
    subprocess.call(['/usr/bin/vim', tmpfilename])
    tmpfp.seek(0)
    return tmpfp.read().decode('UTF-8')

