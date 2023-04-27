from Data_Types import Operators as ops, Actions, PriorityQueue as pq, Schedule as sched
import copy
import time


class HeuristicDepthFirstSearch():

    def __init__(self, country, actions, depth_bound, frontier_max_size, countries):
        self.frontier_max_size = frontier_max_size
        self.depth_bound = depth_bound
        self.country = country      
        self.actions = actions
        self.operator = ops.Operators()
        self.frontier_completed_schedules = pq.PriorityQueue() # each schedule will be of size Depth Bound
        ##### Change ######
        self.timeout = 180 # 3 minutes to reach max_frontier_size if not just return best found at this time 
        self.start_time = time.monotonic()
        ###################
        self.heuristicDFS(copy.deepcopy(country), copy.deepcopy(countries)) 
        
    def heuristicDFS(self, country, countries): # TREE BASED RECURSIVE APPROACH 
        initial_schedule = sched.Schedule() # root node / start of partial schedule
        initial_schedule.add_next_move(country, countries, None) # Initial State
    
        self.search(0, initial_schedule) 
    

    def search(self, current_depth, current_schedule):
        # base cases
        # search ends when we reach frontier max size 
        if (self.frontier_completed_schedules.size() == self.frontier_max_size + 1 or self.is_timed_out()):
            return # we want to backtrack and exit the entire search
        elif (current_depth == self.depth_bound):
            ##### CHANGE #####
            print("\nREACHED\n")
            current_EU = current_schedule.latest_EU()
            best_EU = self.frontier_completed_schedules.best_schedule_EU()
            # if the current EU if not better than the best in the frontier or
            # if the frontier is empty and the scheduel found has an EU that leads us to 
            # a EU value worse than what we started with, then we do nothing and return 
            if ((current_EU < best_EU or current_EU < current_schedule.get_EU(0)) and not self.is_timed_out()): 
                print("----DENIED----")
                return 
            # otherwise we can add it to the frontier 
            print("!!!ADDED!!!!")
            print(self.frontier_completed_schedules.size())
            self.frontier_completed_schedules.push(current_schedule) # add completed schedule to sorting frontier 
            self.start_time = time.monotonic() # reset timeout to give 3 full minutes to find another best schedule 
            ##################
        else:
            # because of the frontier max size we will only get to choose a certain number of branches to explore
            # to make things interesting, all countries will scramble the possible operators so that each country
            # approaches the "development" of their country differently   
            self.actions.shuffle_actions_list()
            for action in self.actions.actions_list:
                # cut the for loop if we already met our frontier max size 
                if (self.frontier_completed_schedules.size() == self.frontier_max_size or self.is_timed_out()): break
                # print(action)
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
                    quantity = self.operator.random_num_of_resource_quantity(transfer, countries)
                    if (quantity > 0): action_node = self.operator.transfer(transfer, quantity, countries) 

                if (action_node != None): # only recurse if action was successful 
                    next_schedule = copy.deepcopy(current_schedule)
                    next_schedule.add_next_move(country, countries, action_node)

                    ##### CHANGE #####
                    frontier = self.frontier_completed_schedules # just to shorten 
                    # pruning 
                    # only if the frontier is empty or schedule has potential/meets the threshold at this point can be explored
                    if (frontier.is_empty() or self.frontier_completed_schedules.meets_threshold(next_schedule)):
                        self.search(current_depth + 1, next_schedule) 
                    ##################
        return
    
    #return best schedule found
    def get_best_schedule(self):
        return self.frontier_completed_schedules.best_schedule()
    
    ##### Change #####
    def is_timed_out(self):
        is_timed_out = time.monotonic() - self.start_time > self.timeout and not self.frontier_completed_schedules.is_empty()
        if (is_timed_out): 
                print("\nTIMED OUT\n")
                print(self.frontier_completed_schedules.size())
        return is_timed_out
    ##################
