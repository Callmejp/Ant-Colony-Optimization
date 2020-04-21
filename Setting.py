import json

from Config import Config

class Setting:
    pheromone_decay_ratio = 0.1
    pheromone_add_ratio = 0.1
    ant_num = 20
    iterate_num = 100


    def __init__(self):
        with open(Config.SETTING_FILE_PATH,'r') as load_f:
            load_dict = json.load(load_f)
            # print(load_dict)
            try:
                Setting.pheromone_decay_ratio = float(load_dict["pheromone_decay_ratio"])
                Setting.pheromone_add_ratio = float(load_dict["pheromone_add_ratio"])
                Setting.ant_num = int(load_dict["ant_num"])
                Setting.iterate_num = int(load_dict["iterate_num"])
            except Exception as e:
                print(e)
                print("Please prepare all the needed parameters in config.json!")
    
    
    def __str__(self):
	    return "------------Setting------------\n" + \
               "pheromone_decay_ratio: " + str(self.pheromone_decay_ratio) + "\n" \
               "pheromone_add_ratio: " + str(self.pheromone_add_ratio) + "\n" \
               "ant_num: " + str(self.ant_num) + "\n" \
               "iterate_num: " + str(self.iterate_num) + "\n" 
