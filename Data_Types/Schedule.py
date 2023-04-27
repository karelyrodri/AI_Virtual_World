import Measures
from Data_Types import Actions
import os
# class representing a schedule 
# atrribute decisions refers to actions already taken that have altered the world state
class Schedule():
    def __init__(self):
        self.decisions = [] # list of dicts containing            
                                # world_state: countries
                                # action : Action type that was taken
                                # expected_utility  : for the state
    ##### CHANGE #####
    def latest_EU(self):
        return self.decisions[-1]["expected_utility"]
    
    def length(self):
        return len(self.decisions)
    
    def get_EU(self, index):
        return self.decisions[index]["expected_utility"]
    
    def latest_world_state(self):
        return self.decisions[-1]["world_state"]
    
    def get_all_EUs(self):
        EUs = []
        for i in range(self.length()):
            EUs.append(self.get_EU(i))
        return EUs
    
    def get_all_state_qualities_by_country(self, country):
        state_qualities = []
        for i in range(self.length()):
            state_quality = self.decisions[i]["world_state"][country].current_state.quality_evaluation
            state_qualities.append(state_quality)
        return state_qualities
    
    def get_search_strategy_by_country(self, country):
        return self.latest_world_state()[country].search
    ###################
    
# Inputs: 
#   country: CountryNode to undergo transform analysis
#   countries: dict of country name: countryNode
#   action: type action that has been taken 
    def add_next_move(self, country, countries, action): #adds to the schedule
            country.current_state.set_quality_eval() # update country eval
            
            if (action != None and action.action_type == Actions.Action_Type.TRANSFER):
                # update the state quality of the country involved in TRANSFER
                action.country_involved.current_state.set_quality_eval()
                # country nodes in the action are the same that are in the countries list since they were assigned by reference 
                # country = action.acting_country
            self.decisions.append({"world_state" : countries, "action" : action})
            self.decisions[-1]["expected_utility"] = Measures.expected_utility(country, self.decisions) # EU val calculation

# Inputs: 
#   filename: used as output file name  
    def output_scheduler(self, filename):
        file_path = os.getcwd() + "\\Output_Schedules\\" + filename
        with open(file_path, 'a') as output:
            output.write("[ ")
            for decision in self.decisions[1:]:
                    action = decision["action"]
                    if (action.action_type == Actions.Action_Type.TRANSORMATION):
                        output.write("(TRANSFORM self {0} (".format(action.action_name))
                    elif (action.action_type == Actions.Action_Type.TRANSFER):
                        output.write("(TRANSFER {0} self ".format(action.country_involved.name))
                    self.output_helper(output, decision)

            output.write("]\n")  
        output.close()
    
    def output_helper(self, output, decision):
        action = decision["action"]
        gained_resources = action.resources_involved
        for resource in gained_resources.keys():
            output.write("({0} {1})".format(resource, gained_resources[resource]))
        output.write(") " if len(gained_resources) == 1 else ")) ")
        output.write("EU: {0}\n".format(decision["expected_utility"]))


