import numpy as np
from Data_Types import Actions

def undiscounted_schedule_reward(country, schedule):
    #R(ci, sj) = Qend(ci, sj) – Qstart(ci, sj), for country ci and schedule sj.
    #difference between the state quality of the end state of the schedule for a 
    #country and the state quality of the start state for the same country.

    # have to lookup the country state from the saved world state because the countryNode passed 
    # only has data about its current state (AKA its state in schedule[-1])
    start_quality = schedule[0]["world_state"][country.name].current_state.quality_evaluation
    end_quality = country.current_state.quality_evaluation
    return end_quality - start_quality


def discounted_schedule_reward(country, schedule):
    #DR(ci, sj) = gammaN ∗ (Qend(ci, sj) – Qstart(ci, sj)), where 0 <= gamma < 1
    gamma = 0.75 # where 0 <= gamma < 1
    N = len(schedule) - 1
    discounted = (gamma ** N) * undiscounted_schedule_reward(country, schedule)
    return discounted


def country_accepts_probability(country, schedule):
    x_0 = 5
    k = 0.001
    discounted_reward = discounted_schedule_reward(country, schedule) 
    x = -k * (discounted_reward - x_0)
    # print("K: {0}   -   DS: {1}  -  {2}".format(k, discounted_reward, x_0))
    # print("X: {0}".format(x))
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
    ## OLD
    # countries = schedule[-1]["world_state"].values()
    # for country in countries:
    #     accept_prob = country_accepts_probability(country, schedule)
    #     success_prob *= accept_prob
    # return success_prob


# Choose and justify C which is a negative constant representing
# the cost of creating a failed plan 
def expected_utility(country, schedule):
    # print(country.current_state.quality_evaluation)
    # (P(sj) ∗ DR(ci, sj)) + ((1 −P(sj)) ∗ C), where ci = self
    # probability country accepts * discounted reward of self
    C = -1
    schedule_success = schedule_success_probability(schedule)
    discounted_reward = discounted_schedule_reward(country, schedule) 
    # print("({0} * {1}) + ((1 - {0}) * {2})".format(schedule_success, discounted_reward, C))
    # print("({0}) + (({1}) * {2})".format((schedule_success * discounted_reward), (1 - schedule_success), C))
    return  (schedule_success * discounted_reward) + ((1 - schedule_success) * C)
