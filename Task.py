
class Task:
    component_index = 0
    cost_time = 0

    def __init__(self, c_i, c_t):
        self.component_index = c_i
        self.cost_time = c_t


    def __str__(self):
        return "------------Task------------\n" + \
               "component_index: " + str(self.component_index) + "  cost_time: " + str(self.cost_time) + "\n"