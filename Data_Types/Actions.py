from enum import Enum 
from Data_Types import Operators as ops
import random


class Action_Type(Enum):
        TRANSORMATION = 0,
        TRANSFER = 1
# used for easy retrieval of information of the taken action
class Action(): # THIS IS NOT USED IN THE ACTION LIST, its returned from calling an operator.transform or operator.transfer

    def __init__(self, action_type, resources_involved, acting_country, country_involved = None, action_name = None):
        self.action_type = action_type
        self.action_name = action_name
        self.acting_country = acting_country
        self.country_involved = country_involved
        self.resources_involved = resources_involved
        
# class used for producing the actions list and shuffling of list
class Action_List(): # Only contains the specs of the operators 
    def __init__(self, transforms, resources, country, countries):
        self.transforms = transforms
        self.actions_list = self.build_actions_list(resources, country, countries)
        self.shuffle_actions_list()
# Inputs: 
#   resources: resource  dict with resource names : resource keys 
#   country: CountryNode to undergo transform analysis
#   countries: dict of country name: countryNode
# Outputs:
#    action: list of every possible actions including all transorms and combination of transfers 
    def build_actions_list(self, resources, country, countries):
        actions = []
        for transform in self.transforms:
            actions.append({"type" : Action_Type.TRANSORMATION, "operator" : transform})

        for other_country in countries: # saving names an not country Nodes 
            if (country != other_country):
                for resource in resources:
                    if not (resource in ["Population", "SolarPower", "Water", "WaterWaste"]):
        # I am only considering transfers from other_countries to the current coutry because it only 
        # benefits the country if others are giving to them not the other way around 
                            transfer = ops.Tranfer(other_country, country, resource) #giving_country, receiving_country, resource
                            actions.append({"type" : Action_Type.TRANSFER, "operator" : transfer})
        # print("len actions list {0}".format(len(actions)))    
        return actions
    
# function to shuffle the actions in the list while keeping the transforms at the front and transfers at the end
    # def shuffle_actions_lists(self):
    #     transform_len = len(self.transforms)
    #     # we always want the transforms at the beginning of the list and transfers at the end
    #     # we break up list of transforms and transfers
    #     actions_transforms = self.actions_list[:transform_len]
    #     actions_tranfers = self.actions_list[transform_len:]
    #     # scramble both lists
    #     random.shuffle(actions_transforms)
    #     random.shuffle(actions_tranfers)
    #     #rejoin them 
    #     self.actions_list = actions_transforms + actions_tranfers


    def shuffle_actions_list(self):
        random.shuffle(self.actions_list)
        


        

