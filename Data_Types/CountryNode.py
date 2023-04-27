
import copy
# Country node class containing name, inital state, current state, its actions list
class Country():
    def __init__(self, name, init_state, depth_bound, max_frontier_size, search, allyNum):
        self.name = name
        self.initial_state = init_state # kept in order to reset on demand
        self.current_state = copy.deepcopy(init_state) # will continue to change
        self.depth_bound = depth_bound
        self.max_frontier_size = max_frontier_size
        self.search = search
        self.allies = allyNum # will be overwritten with list of country names soon
        self.actions_list = None # list of possible actions
        
        # self.print_country_data()

    def print_country_data(self):
        print(self.name)
        print("Resources:")
        print(self.current_state.resources)
        print("State Quality:")
        print(self.current_state.quality_evaluation)

