"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-10 00:13:32
LastEditTime: 2024-11-10 11:59:26
FilePath: \\sagkit\\src\\sagkit\\constructors\\hybrid_constructor.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import sys
import traceback
from utils import State
from constructors import Constructor


class Hybrid_constructor(Constructor):

    def construct_SAG(self, do_merging):
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
                        do_merge=do_merging,
                    )
                    if eligible_successor.is_ET:
                        eligible_successor.set_to_non_triggered()
                        self.expand(
                            leaf=shortest_leaf,
                            job=eligible_successor,
                            do_merge=True,
                        )
                        eligible_successor.set_to_triggered()
                shortest_leaf = self.find_shortest_leaf()
                # pbar.n = shortest_leaf.depth
            except Exception as e:
                print(e, traceback.format_exc())
