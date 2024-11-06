
class analyzer:
    
    def __init__(self, job_list):
        # Output SAG as a dot file
        with open("./dot.txt","w") as dot_file:
            dot_file.write('digraph finite_state_machine {\n'+
            'rankdir = LR;\n'+
            'size = "8,5";\n'+
            'node [shape = doublecircle];\n'+
            '"S0\\n[0, 0]";\n'+
            'node [shape = circle];\n')
            for state in state_list:
                for i in range(len(state.next_jobs)):
                    dot_file.write('"S' + str(state.id) + '\\n[' + str(state.EFT) + ', ' + str(state.LFT) + ']" -> "S' + str(state.next_states[i].id) + \
                        '\\n[' + str(state.next_states[i].EFT) + ', ' + str(state.next_states[i].LFT) + ']" [label="J' + str(state.next_jobs[i].id) + '"];\n')
            dot_file.write('}')
            
            
        # Print SAG statistics
        # for state in state_list:
        #     print('State' + str(state.id) + '[' + str(state.EFT), str(state.LFT) + ']')
        #     for i in range(len(state.next_jobs)):
        #         print('    S' + str(state.id) + ' -- J' + str(state.next_jobs[i].id) + ' -> S' + str(state.next_states[i].id))
        print('Number of states:', len(state_list))
        # print('Number of edges:', sum(len(state.next_states) for state in state_list))
        # leaves = []
        # for state in state_list:
        #     if state.is_leaf():
        #         leaves.append(state)
        # print('Minimum Depth:', min(state.depth for state in leaves))
        # width_recorder = [0 for _ in range(len(state_list)+1)]
        # for state in state_list:
        #     width_recorder[state.depth+1] += len(state.next_states)
        # print('Maximum Width:', max(width_recorder))
        # print('Execution time:', time.time()-start_time, 's')