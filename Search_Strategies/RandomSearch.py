from Data_Types import Operators as ops, Actions, PriorityQueue as pq, Schedule as sched
import copy
import random


class RandomSearch():

    def __init__(self, country, actions, depth_bound, frontier_max_size, countries):
        self.frontier_max_size = frontier_max_size #this needs to be less than the length of the actions list!
        self.depth_bound = depth_bound
        self.country = country        
        self.actions = actions
        self.subset_len = len(self.actions.actions_list) // 4 # roughly 25%
        self.operator = ops.Operators()
        self.frontier_completed_schedules = pq.PriorityQueue() # each schedule will be of size Depth Bound

        self.randomSearch(copy.deepcopy(country), copy.deepcopy(countries)) 

    def randomSearch(self, country, countries): # TREE BASED RECURSIVE APPROACH 
        initial_schedule = sched.Schedule() # root node / start of partial schedule
        initial_schedule.add_next_move(country, countries, None) # Initial State

        while (self.frontier_completed_schedules.size() < self.frontier_max_size):
            # we want to restart the search until we have met the max frontier size   
            self.search(0, initial_schedule) 

    

    def search(self, current_depth, current_schedule):
        # base case
        if (current_depth == self.depth_bound):
            self.frontier_completed_schedules.push(current_schedule)
            print("ADDED")
        else:
            frontier_partial_schedules = pq.PriorityQueue()  # will be of size actions_list
            # random subset of 25% of the actions_list
            action_subset = random.sample(self.actions.actions_list, self.subset_len) 
            for action in action_subset:
                action_node = None
                # we start with a fresh copy of the last world state in the schedule
                # because we are gonna impose actions on it and add it to the schedule
                countries = copy.deepcopy(current_schedule.latest_world_state()) # avoiding pass by reference
                country = countries[self.country.name]
                if (action["type"] == Actions.Action_Type.TRANSORMATION):
                    transform = action["operator"]
                    transform_num = self.operator.random_num_of_tranforms(country, transform)
                    if (transform_num > 0): action_node = self.operator.transform(country, transform, transform_num)
                elif (action["type"] == Actions.Action_Type.TRANSFER): 
                    transfer = action["operator"]
                    quantity = self.operator.random_num_of_resource_quantity(transfer, countries) # random number of resources to transfer
                    if (quantity > 0): action_node = self.operator.transfer(transfer, quantity, countries) 
                
                # we wont count actions that did not occur
                if (action_node != None):
                    next_schedule = copy.deepcopy(current_schedule)
                    next_schedule.add_next_move(country, countries, action_node)
                    frontier_partial_schedules.push(next_schedule) # all partial schedules are of size depth bound
            #all partial schedules will be expanded 
            while (self.frontier_completed_schedules.size() < self.frontier_max_size and  
                                               not frontier_partial_schedules.is_empty()):
                self.search(current_depth + 1, frontier_partial_schedules.pop())
        return
    

        #return best schedule found
    def get_best_schedule(self):
        print("get best")
        print(self.frontier_completed_schedules.size())
        return self.frontier_completed_schedules.best_schedule()
    