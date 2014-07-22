#! /usr/bin/env python3

import os.path
import database
import menu

if __name__ == '__main__':

    print('tac')
    print('workflow management')

    homepath = os.path.expanduser('~')
    subpath = ('.local', 'share', 'tac', 'tac.db')
    dbpath = os.path.join(homepath, *subpath)

    db = database.DataBase(dbpath)
    menu.MainMenu(db)

