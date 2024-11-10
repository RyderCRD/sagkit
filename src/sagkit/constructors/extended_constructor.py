"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 21:09:02
LastEditTime: 2024-11-10 17:52:16
FilePath: \\sagkit\\src\\sagkit\\constructors\\extended_constructor.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

from utils import Job
from constructors import Constructor


class Extended_constructor(Constructor):

    # Read jobs from file
    def read_jobs(self, file_path: str) -> None:
        input_file = open(file_path, "r")
        for job_attr in input_file:
            job_attr = job_attr.split()
            job = Job(
                len(self.job_list),
                int(job_attr[0]),
                int(job_attr[1]),
                int(job_attr[2]),
                int(job_attr[3]),
                int(job_attr[4]),
                int(job_attr[5]),
                int(job_attr[6]),
            )
            if job.is_ET:
                job.BCET = 0
            self.job_list.append(job)
        input_file.close()
