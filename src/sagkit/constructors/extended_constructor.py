"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 21:09:02
LastEditTime: 2024-12-22 18:03:32
FilePath: \\sagkit\\src\\sagkit\\constructors\\extended_constructor.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import math
from sagkit.utils import Job
from sagkit.constructors import Constructor


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

    def count_execution_scenarios(self):
        actual_es_counter = 1
        analyzed_es_counter = 1
        for job in self.job_list:
            actual_es_counter *= (
                (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET_REC + 2)
                if job.is_ET
                else (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET_REC + 1)
            )
            analyzed_es_counter *= (
                (job.WCAT - job.BCAT + 1) * (job.WCET + 1)
                if job.is_ET
                else (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 1)
            )
        actual_es_counter = math.log10(actual_es_counter)
        analyzed_es_counter = math.log10(analyzed_es_counter)
        return actual_es_counter, analyzed_es_counter

    def count_idle_time(self):
        return 0
