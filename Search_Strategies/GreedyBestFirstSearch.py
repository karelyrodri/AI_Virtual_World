from Data_Types import Operators as ops, Actions, PriorityQueue as pq, Schedule as sched
import copy


class GreedyBestFirstSearch():

    def __init__(self, country, actions, depth_bound, frontier_max_size, countries):
        self.frontier_max_size = frontier_max_size #this needs to be less than the length of the actions list!
        self.depth_bound = depth_bound
        self.country = country

        # to save computational power, state.resources (dict) will be turned into a str and be used as a the key in 
        # a expanded states dict with the value as a partial schedule to representing as soon as that state was reached, how did the rest play out
        # after schedule is considered we can look though and add states with partial schedules 
        # this will allow or branches in our search space to get these instead of producing the same
        # schedules and thus saving in computational power at the expense of space
        self.search_cache = {}

        # because of the frontier max size we will only get to choose a certain number of branches to explore
        # to make things interesting, all countries will scramble the possible operators so that each country
        # approaches the "development" of their country differently         
        self.actions = actions
        self.operator = ops.Operators()
        self.best_schedule = None
        self.greedyBestFirstSearch(copy.deepcopy(country), copy.deepcopy(countries)) 

    def greedyBestFirstSearch(self, country, countries): # TREE BASED RECURSIVE APPROACH 
        initial_schedule = sched.Schedule() # root node / start of partial schedule
        initial_schedule.add_next_move(country, countries, None) # Initial State
        self.search(0, initial_schedule) 
    

    def search(self, current_depth, current_schedule):
        # base cases
        # if (self.frontier_completed_schedules.size() == self.frontier_max_size): # search ends when we reach frontier max size 
        #     return # we want to backtrack and exit the entire search
        if (current_depth == self.depth_bound):
            self.best_schedule = current_schedule 
        else:
            frontier_partial_schedules = pq.PriorityQueue() 
            self.actions.shuffle_actions_list()
            while (frontier_partial_schedules.size() < self.frontier_max_size):  # only considering max frontier size amount of partial schedules
                for action in self.actions.actions_list: # size 43
                    action_node = None
                    # we start with a fresh copy of the last world state in the schedule
                    # because we are gonna impose actions on it and add it to the schedule
                    countries = copy.deepcopy(current_schedule.decisions[-1]["world_state"]) # avoiding pass by reference
                    country = countries[self.country.name]
                    if (action["type"] == Actions.Action_Type.TRANSORMATION):
                        transform = action["operator"]
                        transform_num = self.operator.random_num_of_tranforms(country, transform)
                        action_node = self.operator.transform(country, transform, transform_num)
                    elif (action["type"] == Actions.Action_Type.TRANSFER):
                        transfer = action["operator"]
                        quantity = self.operator.random_num_of_resource_quantity(transfer, countries)
                        if (quantity > 0): action_node = self.operator.transfer(transfer, quantity, countries) 

                    if (action_node != None): 
                        next_schedule = copy.deepcopy(current_schedule)
                        next_schedule.add_next_move(country, countries, action_node)
                        frontier_partial_schedules.push(next_schedule) # all partial schedules are of size depth bound
            # here is the greedy part. we only pursue the best partial scheudle to keep searcing
            best_partial_schedule = frontier_partial_schedules.peek()
            self.search(current_depth + 1, best_partial_schedule)
        return

    def get_best_schedule(self):
        return self.best_schedule
    