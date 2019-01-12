# select id, date_created, expiration_timestamp from c2ip;
#    +----+---------------------+----------------------+
#    | id | date_created        | expiration_timestamp |
#    +----+---------------------+----------------------+
#    |  1 | 2019-01-10 20:03:02 | 2019-01-10 21:03:02  |
#    +----+---------------------+----------------------+
#    1 row in set (0.00 sec)

from datetime import datetime
from sqlalchemy import select

class expirelib():
    def __init__(self,dbusr,dbpass,dbport,dbtable="threatkb",dbhost="127.0.0.1"):
        self.mysql_user = dbusr
        self.mysql_pass = dbpass
        self.mysql_db= dbtable
        self.mysql_host= dbhost
        self.mysql_port= dbport

    def isExpired(self,expired):
        
        expiredDate=datetime.strptime(expired,'%Y-%m-%d %H:%M:%S')
        #print(expiredDate)
        #print(datetime.now())
        if(datetime.now() > expiredDate):
            #print("expired")
            return True
        else:
            #print("not expired")
            return False
        

    def displaySQL(self):
        print(self.mysql_user+"@"+self.mysql_host+":"+self.mysql_port+" ("+self.mysql_db+")")

    def deleteExpired(self):
        return None


test = expirelib("threatkb","P@sswordsRC00l","3307")
test.displaySQL()

test.isExpired("2019-01-10 21:03:02")
