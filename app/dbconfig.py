__author__ = 'rjr862'

import pymysql

__USER_NAME = 'username'
__HOST_NAME = 'hostname'
__PASSWORD = 'password'
__DB = 'database'

#mysql config
mysql = {__HOST_NAME: 'localhost',
         __USER_NAME: 'root',
         __PASSWORD: 'r5n1l5b1m2j2',  # yes, i'm aware you can see this :)
         __DB: 'resttickets'}

db = pymysql.connect(host=mysql.get(__HOST_NAME),  # your host, usually localhost
                     user=mysql.get(__USER_NAME),  # your username
                     passwd=mysql.get(__PASSWORD),  # your password
                     db=mysql.get(__DB))  # name of the data base
