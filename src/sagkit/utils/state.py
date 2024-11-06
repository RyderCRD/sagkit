
from typing import List

class State:
    def __init__(self, id:int, EFT:int, LFT:int, job_path:List) -> None:
        self.id = id
        self.EFT = EFT
        self.LFT = LFT
        self.depth = len(job_path)
        self.job_path = job_path
        self.next_jobs = []
        self.next_states = []
        
    def is_leaf(self) -> bool:
        return len(self.next_states) == 0