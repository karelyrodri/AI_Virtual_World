
# State: Set of current resource levels for all countries 
#Heuristic: The “State 
#Quality” of a country • How you choose to weight a state in terms of its utility/goodness
class State():
    # resources weight added for the case of different countries valuing different resources
    def __init__(self, resourceWeights):
        self.resources = {}
        self.resource_weights = resourceWeights#{"Natural":{}, "Manufactured":{}, "Waste": {}}
        self.quality_evaluation = None

    def states_are_equal(self, other_state):
        # states are equal if their resource counts are equal 
        return self.resources == other_state.resources


    def set_quality_eval(self):
        self.quality_evaluation = self.state_quality()
        # print(self.quality_evaluation)

# ideas drawn from quote in this article 
#https://www.thebalancemoney.com/gdp-per-capita-formula-u-s-compared-to-highest-and-lowest-3305848
#"The countries with the highest economic production per person have thriving economies and few residents."

#ratio between population and amount of natural resources The idea is more workers can increase production of natural resources 
    #dont want too much resources, not enough workers
    #dont want too little resouces, too much population 
    # include timber and metallic elements
    # utility created for ranges because they dont have weights associated  
 
# Manufactured resources / population * their weights . Depicts how many people share access to these resources
    # Ideally looking for a low number of people sharing the same resource 
    # high values will have a negative impact on the country 
    # this will be the most valuable portion so we can advance 
 
# waste * wasteWeights  
    # negative waste evaluation will be added apart from calculation because in the real world we subtly 
    # ignore the accumulated waste and disregard it when viewing how great a country is 
    #ratio of waste compared to resources


    def state_quality(self):
        population = self.resources["Population"] 
        #  sum( Utility value of the (num of natural resources / population) ) 
        #  each production business should be evaluated seperately before summing   
        natural_production_cost = 0
        for resource in self.resource_weights["Natural"].keys():
            if (resource != "Population"):
                ratio = self.resources[resource] / population
                # print("Resource: {0}  -- resource count: {1}   --  pop: {2}".format(resource, self.resources[resource], population))
                natural_production_cost += self.natural_resource_utility(ratio)

        #  + sum(manufactured resources / population * weight)
        manufactured_weighted = self.weighted_Resources("Manufactured", population) * 1000 # because a decimal is returned
        # print("manufactured: {0}".format(manufactured_weighted))
        #  + sum(waste * wasteWeight)
        waste_weighted = self.weighted_Resources("Waste")
        # print("waste: {0}".format(waste_weighted))

        print("{0} + {1} + {2}".format(natural_production_cost, manufactured_weighted, waste_weighted))
        return natural_production_cost + manufactured_weighted + waste_weighted

    def weighted_Resources(self, resource_name, population = None):
        weighted_total = 0
        for resource in self.resource_weights[resource_name].keys():
            resourceAmt = self.resources[resource]
            if (population != None): resourceAmt /= population
            weighted_total += self.resource_weights[resource_name][resource] * resourceAmt
        return weighted_total

    def natural_resource_utility(self, ratio):
        # goal is to exclude extremes
        # print("RATIO (resource/pop): {0}".format(ratio))
        utility_val = 0
        # we are looking for 3 to 8 times the amount of resource to population
        # anything above may accumulated wasted resources or signifies slow production rate 
        # anything under is not enough for the population
        if (ratio >= 3 or ratio <= 8):
            #best result
            utility_val = 10
        elif (ratio > 20):
            # not so great 
            utility_val = -5
        elif (ratio < 1):
            # terrible - not enough resources to continue prospering
            utility_val = -10
        else:
            # barely missed the mark
            utility_val = 5
            
        return utility_val 

