from datetime import datetime
from app import db
from app.models import c2ip

from datetime import timedelta
import celery 

class expirelib:

    def __init__(self):
        self.CELERYBEAT_SCHEDULE = {
                "runs-every-30-seconds":{
                    "task":"tasks.add",
                    "schedule": timedelta(seconds=30),
                    "args":(16,16)
                },
            }

    def log_to_c2_comment(self, c2):
        result = db.session.query(c2ip.C2ip).all()

    #@celery.task
    def expiration_daemon(self):
        result = db.session.query(c2ip.C2ip).all()
        for row in result:
            if(row.expiration_timestamp is not None):
                if(row.state != "Retired"):
                    if(row.expiration_timestamp < datetime.now()):
                        db.session.execute("""UPDATE c2ip SET state = "Retired" WHERE id="""+str(row.id))
        db.session.commit()
            



#test = expirelib()
#test.expiration_daemon()
#if(test.isExpired("2019-01-10 21:03:02")):
#    print("Expired")
#else:
#    print("Not Expired")
