import Measures
from Data_Types import Actions
import os
class Schedule():
    def __init__(self):
        self.decisions = [] # list of dicts containing            
                                # world_state: countries
                                # action : Action type that was taken
                                # expected_utility  : for the state

    def add_next_move(self, country, countries, action):
            country.current_state.set_quality_eval()
            if (action != None and action.action_type == Actions.Action_Type.TRANSFER):
                action.country_involved.current_state.set_quality_eval()
                # country nodes in the action are the same that are in the countries list since they were assigned by reference 
                # country = action.acting_country
                # update the stateu quality of country involved in TRANSFER
            self.decisions.append({"world_state" : countries, "action" : action})
            self.decisions[-1]["expected_utility"] = Measures.expected_utility(country, self.decisions)


    def output_scheduler(self, filename):
        file_path = os.getcwd() + "\\Output_Schedules\\" + filename
        with open(file_path, 'a') as output:
            output.write("[ ")
            for decision in self.decisions[1:]:
                    action = decision["action"]
                    if (action.action_type == Actions.Action_Type.TRANSORMATION):
                        output.write("(TRANSFORM self (")
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


