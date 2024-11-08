"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 21:09:02
LastEditTime: 2024-11-08 14:55:37
FilePath: \sagkit\src\sagkit\sag_constructor.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import sys, time
from utils import Job, State

do_merging = True
spliting_condition_list = [False, True]

for do_spliting in spliting_condition_list:
    print("do_spliting:", do_spliting)

    start_time = time.time()

    # Read jobs from file
    job_list = []
    # input_file = open('./input/HQYRealTimeJobs_2.txt', 'r')
    input_file = open("./tests/generate_result.txt", "r")
    for job in input_file:
        job = job.split()
        if not do_spliting and int(job[6]) == 1:
            job_list.append(
                Job(
                    len(job_list),
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
            job_list.append(
                Job(
                    len(job_list),
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

    # ET_es_counter = 1
    # non_ET_es_counter = 1
    # for job in job_list:
    #     ET_es_counter *= (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 2) if job.is_ET else (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 1)
    #     non_ET_es_counter *= (job.WCAT - job.BCAT + 1) * (job.WCET + 1) if job.is_ET else (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 1)
    # print('Number of execution scenarios:', ET_es_counter)
    # print('Number of non-ET execution scenarios:', non_ET_es_counter)
    # print('Valid ratio of non-ET SAG:', ET_es_counter/non_ET_es_counter)

    # Initialize root state
    state_list = []
    SAG_root = State(len(state_list), 0, 0, [])
    state_list.append(SAG_root)

    # find the shortest leaf
    def find_shortest_leaf() -> State:
        leaves = []
        for state in state_list:
            if state.is_leaf():
                leaves.append(state)
        shortest_leaf = min(leaves, key=lambda x: x.depth)
        return shortest_leaf

    # Match two states
    def match(a: State, b: State) -> bool:
        if a.depth != b.depth:
            return False
        return max(a.EFT, b.EFT) <= min(a.LFT, b.LFT) and sorted(
            a.job_path, key=lambda s: s.id
        ) == sorted(b.job_path, key=lambda s: s.id)

    # Expansion phase with or without merging
    def expand(leaf: State, job: Job, do_merge: bool) -> None:
        EFT = max(leaf.EFT, job.BCAT) + job.BCET
        future_jobs = [j for j in job_list if j not in leaf.job_path]
        t_H = sys.maxsize
        for future_job in future_jobs:
            if future_job.priority < job.priority:
                t_H = min(future_job.WCAT - 1, t_H)
        # LFT = min(max(leaf.LFT, job.WCAT), t_H) + job.WCET
        LFT = min(max(leaf.LFT, min(job.WCAT for job in future_jobs)), t_H) + job.WCET
        successor_state = State(len(state_list), EFT, LFT, leaf.job_path + [job])
        # print('State No.', len(state_list))
        leaf.next_jobs.append(job)
        if do_merge:
            for state in state_list:
                if match(state, successor_state):
                    # if leaf.next_states.count(state) == 0:
                    leaf.next_states.append(state)
                    state.EFT = min(state.EFT, successor_state.EFT)
                    state.LFT = max(state.LFT, successor_state.LFT)
                    return
        state_list.append(successor_state)
        leaf.next_states.append(successor_state)

    # construct SAG
    shortest_leaf = SAG_root
    while shortest_leaf.depth < len(job_list):
        eligible_successors = []
        future_jobs = [j for j in job_list if j not in shortest_leaf.job_path]
        for future_job in future_jobs:
            t_E = max(shortest_leaf.EFT, future_job.BCAT)
            if future_job.is_priority_eligible(
                future_jobs, t_E
            ) and future_job.is_potentially_next(future_jobs, t_E, shortest_leaf.LFT):
                eligible_successors.append(future_job)
        if len(eligible_successors) == 0:
            sys.exit("No eligible successor found during construction!")
        for eligible_successor in eligible_successors:
            expand(leaf=shortest_leaf, job=eligible_successor, do_merge=do_merging)

            if do_spliting and eligible_successor.is_ET:
                eligible_successor.set_to_non_triggered()
                expand(leaf=shortest_leaf, job=eligible_successor, do_merge=True)
                eligible_successor.set_to_triggered()

        shortest_leaf = find_shortest_leaf()

    # Print the time it takes to construct the SAG
    print("Construction time:", time.time() - start_time, "s")

    # Output the SAG in .dot format
    # https://dreampuf.github.io/GraphvizOnline to visualize the SAG
    # If that doesn't work, try viewing the site in incognito mode
    with open("./tests/dot.txt", "w") as dot_file:
        dot_file.write(
            "digraph finite_state_machine {\n"
            + "rankdir = LR;\n"
            + 'size = "8,5";\n'
            + "node [shape = doublecircle];\n"
            + '"S1\\n[0, 0]";\n'
            + "node [shape = circle];\n"
        )
        for state in state_list:
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

    print("Number of states:", len(state_list))
