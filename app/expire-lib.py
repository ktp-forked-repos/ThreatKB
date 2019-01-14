# select id, date_created, expiration_timestamp from c2ip;
#    +----+---------------------+----------------------+
#    | id | date_created        | expiration_timestamp |
#    +----+---------------------+----------------------+
#    |  1 | 2019-01-10 20:03:02 | 2019-01-10 21:03:02  |
#    +----+---------------------+----------------------+
#    1 row in set (0.00 sec)
#
#  Action when expired
# UPDATE c2ip SET state = "Expired" WHERE id=1;


from datetime import datetime
from sqlalchemy.sql import text
from app import db
from app.models import c2ip

from datetime import timedelta
import celery 

class expirelib():
    def __init__(self,db):
        self.CELERYBEAT_SCHEDULE = {
                "runs-every-30-seconds":{
                    "task":"tasks.add",
                    "schedule": timedelta(seconds=30),
                    "args":(16,16)
                },
            }


    def isExpired(self,expired):
        expiredDate=datetime.strptime(expired,'%Y-%m-%d %H:%M:%S')
        return datetime.now() > expiredDate

    def _expireC2(self, conn, id):
        #UPDATE c2ip SET state = "Expired" WHERE id=1;
        conn.execute("""UPDATE c2ip SET state = "Retired" WHERE id="""+str(id))

    @celery.task
    def ExpirationDaemon(self):
         #select id, date_created, expiration_timestamp from c2ip;
         connection = db.connect()
         
         result = connection.execute("SELECT id, expiration_timestamp FROM c2ip")
         for row in result:
             if(row["expiration_timestamp"] is not None):
                 if(self.isExpired(row["expiration_timestamp"])):
                     self._expireC2(connection,row["id"])


test = expirelib("threatkb","P@sswordsRC00l","3307")

if(test.isExpired("2019-01-10 21:03:02")):
    print("Expired")
else:
    print("Not Expired")
