from Data_Types import Operators as ops, Actions, PriorityQueue as pq, Schedule as sched
import copy


class GreedyBestFirstSearch():

    def __init__(self, country, actions, depth_bound, frontier_max_size, countries):
        self.frontier_max_size = frontier_max_size #this needs to be less than the length of the actions list!
        self.depth_bound = depth_bound
        self.country = country        
        self.actions = actions
        self.operator = ops.Operators()
        self.frontier_completed_schedules = pq.PriorityQueue() # each schedule will be of size Depth Bound

        self.greedyBestFirstSearch(copy.deepcopy(country), copy.deepcopy(countries)) 

    def greedyBestFirstSearch(self, country, countries): # TREE BASED RECURSIVE APPROACH 
        initial_schedule = sched.Schedule() # root node / start of partial schedule
        initial_schedule.add_next_move(country, countries, None) # Initial State
        
        # set up for all partial schedules of depth1 in this frontier
        frontier_depth1_schedules = pq.PriorityQueue() 
        for action in self.actions.actions_list:
                next_schedule = self.perform_action(action, initial_schedule)
                if (next_schedule != None): frontier_depth1_schedules.push(next_schedule)
        # frontier_depth1_schedules.print_Schedule_EUs()
        
        while (self.frontier_completed_schedules.size() < self.frontier_max_size and  
               not frontier_depth1_schedules.is_empty()):
            # we want to restart greedy at depth 1 every time    
            self.search(1, frontier_depth1_schedules.pop()) 
    

    def search(self, current_depth, current_schedule):
        # base case
        if (current_depth == self.depth_bound):
            self.frontier_completed_schedules.push(current_schedule)
            print("ADDED")
        else:
            frontier_partial_schedules = pq.PriorityQueue()  # will be of size actions_list
            # to make things interesting, all countries will scramble the possible operators so that each country
            # approaches the "development" of their country differently 
            self.actions.shuffle_actions_list() # shuffle to give different transfers a chance to be explored
            for action in self.actions.actions_list:
                next_schedule = self.perform_action(action, current_schedule)
                if (next_schedule != None): frontier_partial_schedules.push(next_schedule) # all partial schedules are of size depth bound
           
            # here is the greedy part. we only pursue the best partial scheudle to keep searcing
            best_partial_schedule = frontier_partial_schedules.peek()
            self.search(current_depth + 1, best_partial_schedule)
        return
    

    def perform_action(self, action, current_schedule):
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
            return next_schedule 
        return None

        #return best schedule found
    def get_best_schedule(self):
        print("get best")
        print(self.frontier_completed_schedules.size())
        return self.frontier_completed_schedules.best_schedule()
    