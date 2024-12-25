"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-10 00:13:32
LastEditTime: 2024-12-25 23:51:41
FilePath: \\sagkit\\src\\sagkit\\constructors\\hybrid_constructor.py
Description: Hybrid constructor
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import sys
import math
import traceback
from sagkit.utils import State
from sagkit.constructors import Constructor


class Hybrid_constructor(Constructor):

    # Override read_jobs method of the Constructor class
    def construct_SAG(self):
        # Initialize root state
        self.state_list = []
        SAG_root = State(len(self.state_list), 0, 0, [])
        self.state_list.append(SAG_root)

        # Construct SAG
        shortest_leaf = SAG_root
        while shortest_leaf.depth < len(self.job_list):
            # with tqdm(
            #     total=len(self.job_list),
            #     desc=f"Depth {shortest_leaf.depth+1}/{len(self.job_list)}",
            # ) as pbar:
            try:
                eligible_successors = []
                future_jobs = [
                    j for j in self.job_list if j not in shortest_leaf.job_path
                ]
                for future_job in future_jobs:
                    t_E = max(shortest_leaf.EFT, future_job.BCAT)
                    if future_job.is_priority_eligible(
                        future_jobs, t_E
                    ) and future_job.is_potentially_next(
                        future_jobs, t_E, shortest_leaf.LFT
                    ):
                        eligible_successors.append(future_job)
                if len(eligible_successors) == 0:
                    sys.exit("No eligible successor found during construction!")
                for eligible_successor in eligible_successors:
                    self.expand(
                        leaf=shortest_leaf,
                        job=eligible_successor,
                        to_merge=self.to_merge,
                    )
                    if eligible_successor.is_ET:
                        eligible_successor.set_to_non_triggered()
                        self.expand(
                            leaf=shortest_leaf,
                            job=eligible_successor,
                            to_merge=self.to_merge,
                        )
                        eligible_successor.set_to_triggered()
                shortest_leaf = self.find_shortest_leaf()
                # pbar.n = shortest_leaf.depth
            except Exception as e:
                print(e, traceback.format_exc())

    # Override count_execution_scenarios method of the Constructor class
    def count_execution_scenarios(self):
        actual_es_counter = 1
        for job in self.job_list:
            actual_es_counter *= (
                (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 2)
                if job.is_ET
                else (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 1)
            )
        actual_es_counter = math.log10(actual_es_counter)
        analyzed_es_counter = actual_es_counter
        return actual_es_counter, analyzed_es_counter

    # Override count_idle_time method of the Constructor class
    def count_idle_time(self):
        return 0
