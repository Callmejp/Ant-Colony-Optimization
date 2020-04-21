

class Config:
    SETTING_FILE_PATH = "config.json"
    
    MACHINE_NUM = 6
    TASK_NUM = 4
    PROCESS_NUM = 3

    PHEROMONE_MATRIX = []
    # 0 indicates infeasible
    MACHINE_TIME = [
        [2, 0, 1, 3, 4, 0, 5, 0, 0, 9, 0, 1],
        [3, 3, 4, 0, 3, 0, 6, 4, 0, 0, 6, 0],
        [4, 0, 5, 5, 0, 4, 0, 0, 13, 7, 0, 3],
        [0, 2, 0, 0, 6, 0, 0, 3, 0, 9, 4, 0],
        [0, 4, 0, 2, 0, 7, 0, 5, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 11, 0, 0, 12, 0, 5, 3]
    ]


    # reorder_policy & vis are the global forms that used in the Util.py
    reorder_policy = []
    vis = []
    best_reorder_cost = 0

    def __init__(self):
        small_task_num = Config.TASK_NUM * Config.PROCESS_NUM
        Config.PHEROMONE_MATRIX = [[1.0 for i in range(Config.MACHINE_NUM)] for j in range(small_task_num)]
        # print(Config.PHEROMONE_MATRIX)


    @staticmethod
    def reset():
        Config.best_reorder_cost = 1000000000

        Config.reorder_policy =  [[[] for _ in range(Config.PROCESS_NUM)] for j in range(Config.MACHINE_NUM)] 
        Config.vis = [[[] for _ in range(Config.PROCESS_NUM)] for j in range(Config.MACHINE_NUM)] 
        
        for i in range(Config.MACHINE_NUM):
            for j in range(Config.PROCESS_NUM):
                for k in range(Config.PROCESS_NUM * Config.TASK_NUM):
                    Config.vis[i][j].append(0)
        
        # print(Config.vis)
