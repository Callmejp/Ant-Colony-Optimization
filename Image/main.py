import numpy as np
import matplotlib.pyplot as plt

from Setting import Setting
from Config import Config
from Util import assignMachine, calculateMinTimeCost, updatePheromone


if __name__ == "__main__":
    # Initialize
    setting = Setting()
    config = Config()
    print(setting)
    # print(Config.PHEROMONE_MATRIX)

    x = np.arange(60)
    y = []
    task_num = Config.TASK_NUM * Config.PROCESS_NUM
    for i in range(setting.iterate_num):
        min_time_cost = 10000000
        best_ant_id = 0
        best_policy = list()

        for ant_id in range(setting.ant_num):
            ant_policy = [[0 for i in range(Config.MACHINE_NUM)] for j in range(task_num)]
        
            for task_id in range(task_num):
                machine_id = assignMachine(ant_id, task_id)
                ant_policy[task_id][machine_id] = 1
        
            current_ant_time_cost = calculateMinTimeCost(ant_policy)
            if current_ant_time_cost < min_time_cost:
                min_time_cost = current_ant_time_cost
                best_ant_id = ant_id
                best_policy = ant_policy
            # print(ant_policy, best_policy)
        updatePheromone(best_policy)
        y.append(min_time_cost)

    y = np.array(y)
    plt.plot(x, y)
    plt.title('Ant Algorithm')
    plt.xlabel('Iteration')
    plt.ylabel('Time')
 
    plt.show()
        


