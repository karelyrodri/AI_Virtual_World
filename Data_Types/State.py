
# state class 
class State():
    # resources weight added for the case of different countries valuing different resources
    def __init__(self, resource_weights):
        self.resources = {}
        self.resource_weights = resource_weights#{"Natural":{}, "Manufactured":{}, "Waste": {}}
        self.quality_evaluation = None

    def states_are_equal(self, other_state): # not currently in use
        # states are equal if their resource counts are equal 
        return self.resources == other_state.resources

    # set current state quality 
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
        natural_cost = 0
        for resource in self.resource_weights["Natural"].keys():
            if (resource != "Population"):
                ratio = self.resources[resource] / population
                # print("Resource: {0}  -- resource count: {1}   --  pop: {2}".format(resource, self.resources[resource], population))
                if (resource in ["Timber", "MetallicElements", "PlantsAndFibers"]):
                    natural_cost += self.production_utility(ratio)
                elif (resource in ["Seeds", "Clay" ]):
                    natural_cost += self.organic_utility(ratio)
                elif (resource in ["SolarPower", "Water"]):
                    natural_cost += self.energy_source_utility(ratio)


        #  + sum(manufactured resources / population * weight)
        manufactured_weighted = self.weighted_Resources("Manufactured", population) * 1000 # because a decimal is returned
        # print("manufactured: {0}".format(manufactured_weighted))
        #  + sum(waste * wasteWeight)
        waste_weighted = self.weighted_Resources("Waste") * 0.1
        return natural_cost + manufactured_weighted + waste_weighted

# Inputs: 
#   resource_name: name of current resource
#   population: population count for the country
#Outputs:
#   weighted_total: input resource multiplied by its weight 
    def weighted_Resources(self, resource_name, population = None):
        weighted_total = 0
        for resource in self.resource_weights[resource_name].keys():
            resourceAmt = self.resources[resource]
            if (population != None): resourceAmt /= population # used for manufactured resources
            weighted_total += self.resource_weights[resource_name][resource] * resourceAmt

            #penalize if there way too much food
            if ((resource == "Food" and resourceAmt >= 5) or 
                (resource == "MetallicAlloys" and resourceAmt >= 0.8)):
                # 5 times the population is too much food 
                # 2 times the popultion is too many metallic allots 
                # resourceAmt has already been changed to the ratio of resource per person line 72
                weighted_total -= 100
            if ("Housing" in resource and (resourceAmt > 1 and resourceAmt <= 6)):
                weighted_total += 300
                if ("Eco" in resource): weighted_total += 100

        return weighted_total

# Inputs: 
#   ratio: float value representing natural resource/ population
# Outputs:
#   utility_val: value representing the evaluation of the ratio
    def production_utility(self, ratio): #used for natural resource calculation
        #Timber, MetallicElements, PlantAndFibers 

        # goal is to exclude extremes
        utility_val = 0
        # we are looking for 3 to 8 times the amount of resource to population
        # anything above may accumulated wasted resources or signify slow production rate 
        # anything under is not enough for the population
        if (ratio >= 3 or ratio <= 8):
            #best result, 
            utility_val = 10
        elif (ratio > 12):
            # hoarding is not good
            # we want to encourage a surplus of resource to be used up 
            utility_val = -5
        elif (ratio < 1):
            # terrible - not enough resources to continue prospering
            #forces AI to consider recycling templates
            utility_val = -10
        else:
            # barely missed the mark
            utility_val = 5
        return utility_val 
    
    # Seeds, Clay 
    def organic_utility(self, ratio): #used for natural resource calculation
        # bracket for organics that do not go bad
        if (ratio < 1):
            return -2
        else:
            return 5

    #SolarPower, Water
    def energy_source_utility(self, ratio):
        # the more the merrier
        if (ratio > 1):
            # we never want to have less than the amount of people
            # water is highly important so it gets a 10
            return 10
        else:     
            return -5
        # we need to resort to water waste recyling 

