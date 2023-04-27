import numpy as np
from Data_Types import Actions

# completed_turns = {}
X_0 = 5
K = 0.001
GAMMA = 1
c = -1    
# will dictact whether the K value will be based off of the global variable or the search algo 
# if this is false, we will use the best values found for k given the search algo 
hyperparameter_on = False

def undiscounted_schedule_reward(country, schedule):
    # if (len(schedule) == 1): return latest_quality
    #R(ci, sj) = Qend(ci, sj) – Qstart(ci, sj), for country ci and schedule sj.
    #difference between the state quality of the end state of the schedule for a 
    #country and the state quality of the start state for the same country.

    # have to lookup the country state from the saved world state because the countryNode passed 
    # only has data about its current state (AKA its state in schedule[-1])

    start_quality = schedule[0]["world_state"][country.name].current_state.quality_evaluation
    # start_quality = country.initial_state.quality_evaluation
    latest_quality = country.current_state.quality_evaluation
    
    return latest_quality - start_quality


def discounted_schedule_reward(country, schedule):
    #DR(ci, sj) = gammaN ∗ (Qend(ci, sj) – Qstart(ci, sj)), where 0 <= gamma < 1
    # is constantly being accessed and changed
    gamma = GAMMA # where 0 <= gamma < 1

    # completed_turns.setdefault(country.name, 0)
    # print("Completed Turns {0}".format(completed_turns))
    N = (len(schedule)) #+ (completed_turns[country.name] * country.depth_bound)
    # print(N)
    
    discounted = (gamma ** N) * undiscounted_schedule_reward(country, schedule)
    return discounted


def country_accepts_probability(country, schedule):
    x_0 = X_0
    
    if (hyperparameter_on):
        k = K
    else:
        search = country.search 
        if (search == "H_DFS"):
            k = 0.01
        elif (search == "GBFS"):
            k = 1
        elif (search == "RS"):
            k = 0.001

    discounted_reward = discounted_schedule_reward(country, schedule) 
    x = -k * (discounted_reward - x_0)
    return 1 / (1 + np.exp(x))


def schedule_success_probability(schedule):
    # return 1 if it is a transform 
    success_prob = 1
    # only countries involed will be part of the calculation
    recent = schedule[-1]["action"]
    if (recent != None and recent.action_type == Actions.Action_Type.TRANSFER):
        success_prob *= country_accepts_probability(recent.acting_country, schedule) \
                     * country_accepts_probability(recent.country_involved, schedule)

    return success_prob


# Choose and justify C which is a negative constant representing
# the cost of creating a failed plan 
def expected_utility(country, schedule):
    C = c
    # print(C)
    schedule_success = schedule_success_probability(schedule)
    discounted_reward = discounted_schedule_reward(country, schedule) 
    # print((schedule_success * discounted_reward) + ((1 - schedule_success) * C))
    return  (schedule_success * discounted_reward) + ((1 - schedule_success) * C)
