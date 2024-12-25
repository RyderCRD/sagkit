"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 17:59:56
LastEditTime: 2024-12-25 23:55:16
FilePath: \\sagkit\\src\\sagkit\\utils\\job.py
Description: Job class for SAG construction algorithms.
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

from typing import List
from sagkit.schedulers.fp_scheduler import FP_Scheduler


class Job:
    def __init__(
        self,
        id: int,
        BCAT: int,
        WCAT: int,
        BCET: int,
        WCET: int,
        DDL: int,
        priority: int,
        is_ET: int,
    ) -> None:
        self.id = id
        self.BCAT = BCAT
        self.WCAT = WCAT
        self.BCET = BCET
        self.BCET_REC = BCET
        self.WCET = WCET
        self.WCET_REC = WCET
        self.DDL = DDL
        self.priority = priority
        self.is_ET = is_ET

    def set_to_non_triggered(self) -> None:
        self.BCET = 0
        self.WCET = 0

    def set_to_triggered(self) -> None:
        self.BCET = self.BCET_REC
        self.WCET = self.WCET_REC

    # Determine if the job is priority-eligible at a given time
    def is_priority_eligible(self, future_jobs: List, time: int) -> bool:
        for future_job in future_jobs:
            if (future_job.WCAT <= time) and FP_Scheduler.compare(future_job, self):
                return False
        return True

    # Determine if the job is potentially the next job to be scheduled
    def is_potentially_next(self, future_jobs: List, time: int, state_LFT: int) -> bool:
        if self.BCAT <= state_LFT:
            return True
        for future_job in future_jobs:
            if (
                (future_job.WCAT < time)
                and (future_job.id != self.id)
                and future_job.is_priority_eligible(
                    future_jobs, max(future_job.WCAT, state_LFT)
                )
            ):
                return False
        return True

    def __str__(self) -> str:
        return (
            "Job"
            + str(self.id)
            + "["
            + str(self.BCAT)
            + ", "
            + str(self.WCAT)
            + "] ["
            + str(self.BCET)
            + ", "
            + str(self.WCET)
            + "] "
            + str(self.DDL)
            + ", "
            + str(self.priority)
            + ", "
            + str(self.is_ET)
        )
