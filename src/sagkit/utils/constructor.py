"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 21:09:02
LastEditTime: 2024-11-10 00:17:22
FilePath: \\sagkit\\src\\sagkit\\constructors\\constructor.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import sys
import traceback
from utils import Job, State


class Constructor:

    def __init__(self, header, do_merging, do_spliting, do_extending) -> None:
        self.job_list = []
        self.state_list = []
        self.header = header
        self.do_merging = do_merging
        self.do_spliting = do_spliting
        self.do_extending = do_extending

    # Read jobs from file
    def read_jobs(self, file_path: str) -> None:
        input_file = open(file_path, "r")
        for job in input_file:
            job = job.split()
            if self.do_extending and int(job[6]) == 1:
                self.job_list.append(
                    Job(
                        len(self.job_list),
                        int(job[0]),
                        int(job[1]),
                        0,
                        int(job[3]),
                        int(job[4]),
                        int(job[5]),
                        int(job[6]),
                    )
                )
            else:
                self.job_list.append(
                    Job(
                        len(self.job_list),
                        int(job[0]),
                        int(job[1]),
                        int(job[2]),
                        int(job[3]),
                        int(job[4]),
                        int(job[5]),
                        int(job[6]),
                    )
                )
        input_file.close()

    # Find the shortest leaf
    def find_shortest_leaf(self) -> State:
        leaves = []
        for state in self.state_list:
            if state.is_leaf():
                leaves.append(state)
        shortest_leaf = min(leaves, key=lambda x: x.depth)
        return shortest_leaf

    @staticmethod
    def match(a: State, b: State) -> bool:
        # Match two states
        if a.depth != b.depth:
            return False
        return max(a.EFT, b.EFT) <= min(a.LFT, b.LFT) and sorted(
            a.job_path, key=lambda s: s.id
        ) == sorted(b.job_path, key=lambda s: s.id)

    # Expansion phase with or without merging
    def expand(self, leaf: State, job: Job, do_merge: bool) -> None:
        EFT = max(leaf.EFT, job.BCAT) + job.BCET
        future_jobs = [j for j in self.job_list if j not in leaf.job_path]
        t_H = sys.maxsize
        for future_job in future_jobs:
            if future_job.priority < job.priority:
                t_H = min(future_job.WCAT - 1, t_H)
        # LFT = min(max(leaf.LFT, job.WCAT), t_H) + job.WCET
        LFT = min(max(leaf.LFT, min(job.WCAT for job in future_jobs)), t_H) + job.WCET
        successor_state = State(len(self.state_list), EFT, LFT, leaf.job_path + [job])
        # print('State No.', len(state_list))
        leaf.next_jobs.append(job)
        if do_merge:
            for state in self.state_list:
                if self.match(state, successor_state):
                    # if leaf.next_states.count(state) == 0:
                    leaf.next_states.append(state)
                    state.EFT = min(state.EFT, successor_state.EFT)
                    state.LFT = max(state.LFT, successor_state.LFT)
                    return
        self.state_list.append(successor_state)
        leaf.next_states.append(successor_state)

    def construct_SAG(self, do_merging, do_spliting):
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

                    if do_spliting and eligible_successor.is_ET:
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

        # Print some statistics
        print("Number of states:", len(self.state_list))
        ET_es_counter = 1
        non_ET_es_counter = 1
        for job in self.job_list:
            ET_es_counter *= (
                (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 2)
                if job.is_ET
                else (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 1)
            )
            non_ET_es_counter *= (
                (job.WCAT - job.BCAT + 1) * (job.WCET + 1)
                if job.is_ET
                else (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 1)
            )
        print("Number of execution scenarios:", ET_es_counter)
        print("Number of non-ET execution scenarios:", non_ET_es_counter)
        print("Valid ratio of non-ET SAG:", ET_es_counter / non_ET_es_counter)
        # Maximum width
        width_list = [0 for _ in range(shortest_leaf.depth + 1)]
        for state in self.state_list:
            width_list[state.depth] += 1
        print("Maximum width:", max(width_list))
        # Maximum Waste idle time
        waste_time = 0
        for job in self.job_list:
            waste_time += job.BCET if job.is_ET else 0
        print("Maximum waste idle time:", waste_time)

    # Output the SAG in .dot format
    # https://dreampuf.github.io/GraphvizOnline to visualize the SAG
    # If that doesn't work, try viewing the site in incognito mode
    def save_SAG(self):
        with open("./tests/" + self.header + "_dot.txt", "w") as dot_file:
            dot_file.write(
                "digraph finite_state_machine {\n"
                + "rankdir = LR;\n"
                + 'size = "8,5";\n'
                + "node [shape = doublecircle];\n"
                + '"S1\\n[0, 0]";\n'
                + "node [shape = circle];\n"
            )
            for state in self.state_list:
                for i in range(len(state.next_jobs)):
                    dot_file.write(
                        '"S'
                        + str(state.id + 1)
                        + "\\n["
                        + str(state.EFT)
                        + ", "
                        + str(state.LFT)
                        + ']" -> "S'
                        + str(state.next_states[i].id + 1)
                        + "\\n["
                        + str(state.next_states[i].EFT)
                        + ", "
                        + str(state.next_states[i].LFT)
                        + ']" [label="J'
                        + str(state.next_jobs[i].id + 1)
                        + '"];\n'
                    )
            dot_file.write("}")
