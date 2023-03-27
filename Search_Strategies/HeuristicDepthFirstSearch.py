from Data_Types import Operators as ops, Actions, PriorityQueue as pq, Schedule as sched
import copy


class HeuristicDepthFirstSearch():

    def __init__(self, country, actions, depth_bound, frontier_max_size, countries):
        self.frontier_max_size = frontier_max_size
        self.depth_bound = depth_bound
        # self.countries = countries.values()
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
        self.frontier_completed_schedules = pq.PriorityQueue() # each schedule will be of size Depth Bound
        self.heuristicDFS(copy.deepcopy(country), copy.deepcopy(countries)) 
        
    def heuristicDFS(self, country, countries): # TREE BASED RECURSIVE APPROACH 
        initial_schedule = sched.Schedule() # root node / start of partial schedule
        initial_schedule.add_next_move(country, countries, None) # Initial State
        self.search(0, initial_schedule) 
    

    def search(self, current_depth, current_schedule):
        # base cases
        if (self.frontier_completed_schedules.size() == self.frontier_max_size): # search ends when we reach frontier max size 
            return # we want to backtrack and exit the entire search
        elif (current_depth == self.depth_bound):
            self.frontier_completed_schedules.push(current_schedule) # add completed schedule to sorting frontier 
        else:
            self.actions.shuffle_actions_list()
            for action in self.actions.actions_list:
                # print(action)
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
                    self.search(current_depth + 1, next_schedule)
        return

    def get_best_schedule(self):
        return self.frontier_completed_schedules.peek()
    