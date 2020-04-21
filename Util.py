import random

from Config import Config
from Task import Task
from Setting import Setting


def GreedyChooseMachine(task_id):
    max_pheromone = -1.0
    machine_id = 0
    for i in range(Config.MACHINE_NUM): 
        # judge if feasible
        if Config.MACHINE_TIME[i][task_id] == 0:
            continue

        pheromone = Config.PHEROMONE_MATRIX[task_id][i]
        if pheromone > max_pheromone:
            max_pheromone = pheromone
            machine_id = i

    return machine_id


def RandomChooseMachine(task_id):
    feasible_machine_cnt = 0

    for machine_id in range(Config.MACHINE_NUM): 
        # judge if feasible
        if Config.MACHINE_TIME[machine_id][task_id] == 0:
            continue
        feasible_machine_cnt += 1
       
    # random_cnt: 0 ~ feasible_machine_cnt-1
    random_cnt = random.randint(0, feasible_machine_cnt-1)
    # print("random result: ", random_cnt, feasible_machine_cnt)
    feasible_machine_cnt = 0
    for machine_id in range(Config.MACHINE_NUM):
        if Config.MACHINE_TIME[machine_id][task_id] == 0:
            continue
        if random_cnt == feasible_machine_cnt:
            return machine_id
        feasible_machine_cnt += 1
    
    # there doesn't need return because loop segment must return before
    print("Random Method can't find a feasible choice!")
    exit(0)


def assignMachine(ant_id, task_id):
    # For simplicity, here we let the 60% ant be greedy
    if ant_id <= int(Setting.ant_num * 0.3):
        return GreedyChooseMachine(task_id) 
    
    return RandomChooseMachine(task_id)




def calcualteFinalCost():
    machine_time_statistic = [0] * Config.MACHINE_NUM
    component_time_statistic = [0] * Config.TASK_NUM
    # print(machine_time_statistic, component_time_statistic)
    for i in range(Config.PROCESS_NUM):
        for j in range(Config.MACHINE_NUM):
            for task in Config.reorder_policy[j][i]:
                # key point
                start_time = max(machine_time_statistic[j], component_time_statistic[task.component_index])

                machine_time_statistic[j] = start_time + task.cost_time
                component_time_statistic[task.component_index] = start_time + task.cost_time

    this_time = 0
    for t in machine_time_statistic:
        this_time = max(this_time, t)
    
    Config.best_reorder_cost = min(Config.best_reorder_cost, this_time)


def dfs(t, machine_id, priority_id, task_cnt):
    
    task_num = len(t[machine_id][priority_id])
    # handle special case 
    if task_num == 0:
        if (priority_id + 1) >= Config.PROCESS_NUM:
            if (machine_id + 1) >= Config.MACHINE_NUM:
                calcualteFinalCost()
                return
            else:
                dfs(t, machine_id + 1, 0, 0)
        else:
            dfs(t, machine_id, priority_id + 1, 0)
        
        return


    for task_index in range(task_num):
        if Config.vis[machine_id][priority_id][task_index] == 1:
            continue

        chosen_task = t[machine_id][priority_id][task_index]
        Config.reorder_policy[machine_id][priority_id].append(chosen_task)
        Config.vis[machine_id][priority_id][task_index] = 1

        if (task_cnt + 1) >= task_num:
            if (priority_id + 1) >= Config.PROCESS_NUM:
                if (machine_id + 1) >= Config.MACHINE_NUM:
                    calcualteFinalCost()
                else:
                    dfs(t, machine_id + 1, 0, 0)
            else:
                dfs(t, machine_id, priority_id + 1, 0)
        else:
            dfs(t, machine_id, priority_id, task_cnt + 1)
        
        verify = Config.reorder_policy[machine_id][priority_id].pop()
        assert(verify == chosen_task)
        Config.vis[machine_id][priority_id][task_index] = 0


"""
We need to calculate the `perfect order` of the tasks
assigned to one machine.

Observations:
1. Process with high priority must execute before the ones with low priority
"""
def calculateMinTimeCost(temp_policy):
    task_classifier_per_machine = [[[] for _ in range(Config.PROCESS_NUM)] for j in range(Config.MACHINE_NUM)] 


    for task_id in range(Config.TASK_NUM * Config.PROCESS_NUM):
        for machine_id in range(Config.MACHINE_NUM):

            if temp_policy[task_id][machine_id] == 1:

                priority = task_id % Config.PROCESS_NUM
                component_id = task_id // Config.PROCESS_NUM
                cost_time = Config.MACHINE_TIME[machine_id][task_id]
                assert(cost_time != 0)
                assert(component_id < Config.TASK_NUM)
                task_classifier_per_machine[machine_id][priority].append(Task(component_id, cost_time))
        
    """
    We need to be clear that what we should enumerate is 
    the order of the same priority tasks in a machine
    """
    Config.reset()
    dfs(task_classifier_per_machine, 0, 0, 0)
    return Config.best_reorder_cost
    

def updatePheromone(best_policy):
    # print("after updatePheromone: \n", best_policy)
    for i in range(Config.TASK_NUM * Config.PROCESS_NUM):
        for j in range(Config.MACHINE_NUM):
            Config.PHEROMONE_MATRIX[i][j] *= Setting.pheromone_decay_ratio

    for i in range(Config.TASK_NUM * Config.PROCESS_NUM):
        for j in range(Config.MACHINE_NUM):
            if best_policy[i][j] == 1:
                # print(best_policy[i][j], "yes")
                Config.PHEROMONE_MATRIX[i][j] += Setting.pheromone_add_ratio

    # print("after updatePheromone: \n", Config.PHEROMONE_MATRIX)

