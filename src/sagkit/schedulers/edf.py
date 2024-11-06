import sys
from utils.job import Job

class EDF:
    def edf_scheduler(a:Job, b:Job) -> int:
        if a.DDL < b.DDL:
            return -1
        elif a.DDL > b.DDL:
            return 1
        else:
            if a.priority < b.priority:
                return -1
            elif a.priority > b.priority:
                return 1
            else:
                sys.exit('Same DDL and same priority!')