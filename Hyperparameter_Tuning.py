
import Virtual_World as vw
from Search_Strategies import HeuristicDepthFirstSearch as H_dfs, GreedyBestFirstSearch as GreedyBestFS, RandomSearch
import Measures
import numpy as np
import pandas as pd
import math


# This is the percentage change between the current and its prior adjacent neighbor
# list of EUs for every action in a shedule
def growth_rate(EUs):
    percent_change = pd.Series(EUs).pct_change()
    # first two index are nan and inf
    return percent_change.tolist()[2:]

#is calculated by the standard deviation of the growth rate
def volatility(growth_rate):
    volatility = np.std(growth_rate)
    return volatility

# will be used to determing the min and max values for growth rate percentage and volatlity 
def get_min_max(grid, criteria):
    print(grid.values())                                 # this if only applies to random search as it has unpredicatbale values
    minimum = min(grid.values(), key=lambda sched_evals: math.inf if (math.isinf(sched_evals[criteria]) or \
                                                                      math.isnan(sched_evals[criteria])) else sched_evals[criteria])
    maximum = max(grid.values(), key=lambda sched_evals: -math.inf if (math.isinf(sched_evals[criteria]) or \
                                                                       math.isnan(sched_evals[criteria])) else sched_evals[criteria])
    
    return [minimum[criteria], maximum[criteria]] 
# used for getting the lowest scoring params and the highest scoring params
def get_min_max_values(grid, criteria):
    minimum = min(grid.keys(), key=lambda hyperparams: grid[hyperparams][criteria])
    maximum = max(grid.keys(), key=lambda hyperparams: grid[hyperparams][criteria])
    return [minimum, maximum]
# growth rate percentage and volatility are subject to nrmalization so they can be on the same scale
def normalize(value, min_max, is_volatility = False):
    min = min_max[0]
    max = min_max[1]
  
    #min max normalization 
    normalized = (value - min) / (max - min)
    # we do 1 - normalized for volatility because we actually favor lower valued volatility
    if (is_volatility): normalized = 1 - normalized
    return normalized * 100

# get the criteria evaluation values given a schedule
#fully reliant on the Expected Utility 
def criteria_evaluation(schedule):
    EUs = schedule.get_all_EUs()
    print(EUs)
    growth_rates = growth_rate(EUs)
    return {"final_EU" : EUs[-1], 
            "avg_growth_rate" : np.mean(growth_rates), 
            "volatility" : volatility(growth_rates)}

# since all values are now know, we can finall put it through our metrics equation 
# sched_eval is the return dict from the above function
def metric_evaluation(sched_eval, growth_min_max, volatility_min_max):
    norm_growth_rate = normalize(sched_eval["avg_growth_rate"], growth_min_max)
    norm_volatility = normalize(sched_eval["volatility"], volatility_min_max, True)
    return (0.8 * sched_eval["final_EU"]) + (0.5 * norm_growth_rate) \
                                          + (0.3 * norm_volatility)


# Set up the virtual world
#will require all input files like normal
world = vw.VirtualWord()
world.setup_virtual_World()
print("Setup Completed")

# to allow for overwritting the values in the Measure file
Measures.hyperparameter_on = True 

def grid_search():
    # params to try 
    params_grid = {"x_0": [5], "k" : [0.001, 0.01, 0.5, 1], "gamma" : [0.5, 0.75, 0.9, 1], "C" : [-1]}

    # exhaustive grid search implementation
    grid = {}
    for x_0 in params_grid["x_0"]:
        for k in params_grid["k"]:
            for gamma in params_grid["gamma"]:
                for C in params_grid["C"]:
                    #overwritting values 
                    Measures.X_0 = x_0
                    Measures.K = k
                    Measures.GAMMA = gamma
                    Measures.c = C
                    # focusing only on one country 
                    mexico = world.world_countries["Mexico"]
                    actions = mexico.actions_list
                    depth_bound = mexico.depth_bound
                    frontier_max_size = mexico.max_frontier_size
                    countries = world.world_countries
                    search = mexico.search
                    # Every time you want to evaluate a different search algorithm 
                    #you need to make the change in the configuration.csv and rerun this file
                    if (search == "H_DFS"):
                        schedule = H_dfs.HeuristicDepthFirstSearch(mexico, actions, depth_bound, frontier_max_size, 
                                                                   countries).get_best_schedule()
                    elif (search == "GBFS"):
                        schedule = GreedyBestFS.GreedyBestFirstSearch(mexico, actions, depth_bound, \
                                                                      frontier_max_size, countries).get_best_schedule()
                    elif (search == "RS"):
                        schedule = RandomSearch.RandomSearch(mexico, actions, depth_bound, \
                                                             frontier_max_size, countries).get_best_schedule()
                    
                    hyperparams = "{0},{1},{2},{3}".format(x_0, k, gamma, C)
                    print(hyperparams)
                    print("__________________")
                    grid[hyperparams] = criteria_evaluation(schedule)
                    # print(grid)
    return grid 
# used to print out hyperparameteres 
def print_params(params, label):
    params = params.split(",")
    # print(params)
    print("The {0} parameter values are: \nx_0: {1}\nk: {2}\ngamma: {3}\nC: {4}"\
          .format(label, params[0], params[1], params[2], params[3]))


# when called the grid search will be complete and will have all the info available to 
# do the final metric evaluation 
def evaluate_grid(grid):
    growth_min_max = get_min_max(grid, "avg_growth_rate")
    print(growth_min_max)
    
    volatility_min_max = get_min_max(grid, "volatility")

    print(volatility_min_max)
    metric_eval = "metric_evaluation"
    for key in grid.keys():
        criteria_eval = grid[key]
        grid[key][metric_eval] = metric_evaluation(criteria_eval, growth_min_max, volatility_min_max)

    best_worst_params = get_min_max_values(grid, metric_eval)
    print_params(best_worst_params[0], "worst")
    print_params(best_worst_params[1], "best")

################## GRID SEARCH IS CALLED HERE ##################
hyperparameter_grid = grid_search()
print(hyperparameter_grid)
evaluate_grid(hyperparameter_grid)



    
