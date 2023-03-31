#Concrete instantiations of the TRANSFORM and TRANSFER operations
import math
from Data_Types import Actions as a
import random
# class to be utilized for creating different tranform types
# outlines the transform name, the required resource/qty inputs, and the output resource/qty
class Transform():
    def __init__(self, transform_name):
        self.name = transform_name
        self.inputs = {} # resource name : qty
        self.outputs = {} # resource name : qty

# class to be utilized for storing the details of a transfer 
# outlines the giving country, the recieving country, and resource/qty
class Tranfer():
    def __init__(self, giving_country, receiving_country, resource):
        self.gifter = giving_country
        self.receiver = receiving_country
        self.resource = resource


# class consisting of operator {transfom, transfer} functions    
# Contains a list of the different type of transform templates known as transforms
class Operators():    

# Inputs: 
#   country: CountryNode to undergo transform
#   transform: Transform type with specs on transformation quantities
#   num_transforms: Quantity of desired transforms done in one step
# Outputs:
#    boolean succesful or failure of transform
    def transform(self, country, transform, num_transforms = 1):
        sufficient_qty = True # ensures transform is only done if the country has enough resources
        # print(transform.name)
        for resource in transform.inputs.keys():
            qty = transform.inputs[resource]
            if (not self.sufficient_quantity(country, resource, qty * num_transforms)):
                sufficient_qty = False
                break

        if (sufficient_qty):
            gained_resources = {}
            for resource in transform.inputs.keys():
                qty = transform.inputs[resource] * num_transforms
                country.current_state.resources[resource] -= qty
            for resource in transform.outputs.keys():
                qty = transform.outputs[resource] * num_transforms
                if (resource != "Population"): gained_resources[resource] = qty
                country.current_state.resources[resource] += qty 
            return a.Action(a.Action_Type.TRANSORMATION, gained_resources, country)
        else:
            print("Insufficient Resources to complete the Transformation of {0} \
                  for country {1}".format(transform.name, country.name))
            return None
    
# Inputs: 
#   country: CountryNode to undergo transform analysis
#   transform: Transform type with specs on transformation quantities
# Outputs:
#    max_possible: int representing max number of transforms that can be done in one go  
    def max_num_of_transform(self, country, transform):
            max_possible = math.inf
            for resource in transform.inputs.keys():
                current_amt = country.current_state.resources[resource]
                required_amt = transform.inputs[resource]
                # determine max possible transform by how many transforms the lowest qty has to meet the required amt
                max_possible = min(max_possible, current_amt // required_amt)
            return max_possible
          
    
# Inputs: 
#   country: CountryNode to undergo transform analysis
#   transform: Transform type with specs on transformation quantities
# Outputs:
#    random_num_of_transforms: int representing a random valid amount of transforms to be performed 
    def random_num_of_tranforms(self, country, transform):
        max_num_of_transforms = self.max_num_of_transform(country, transform)
        # random done by probability 
        
        return math.floor(random.uniform(0.5, 1) * max_num_of_transforms)

# Inputs: 
#   transfer: Transfer type with specs on those involved and what
#   quantity: amount of specified resource to be transfered
# Outputs:
#    boolean succesful or failure of transfer    
    def transfer(self, transfer, quantity, countries):#transfer from country_i to country_j
        gifter = countries[transfer.gifter]
        receiver = countries[transfer.receiver]
        resource = transfer.resource 
        if (self.sufficient_quantity(gifter, resource, quantity)):
            gifter.current_state.resources[resource] -= quantity
            receiver.current_state.resources[resource] += quantity
            # these nodes in Action are a reference of the current countries list
            return a.Action(a.Action_Type.TRANSFER, {resource : quantity}, receiver, gifter) 
        else:
            print("Insufficient Resources to complete the Transfer of {0} {1} from \
                  {2} to {3}".format(quantity, resource, gifter.name, receiver.name)) 
            return None

# Inputs: 
#   transform: Transfer type with specs on trnsfer quantities
# Outputs:
#    random_num_of_quantity: int representing a random valid quantity of resources to possibly be given up 
    def random_num_of_resource_quantity(self, transfer, countries):
        # resources with high weight have a lower range used for randomly selecting the quantity to be transfered
        # we only are willing to give up a limited amount of high importance resources 
        # vs an item of less value we may not care as much if most of it is gone
        resource = transfer.resource
        gifter = countries[transfer.gifter].current_state

        weights = gifter.resource_weights
        
        for resource_type in weights.keys():
            if (resource in weights[resource_type].keys()):
                resource_weight = abs(weights[resource_type][resource])
                break #abs if for waste negative values. 
        # those with the lowest negative weights will be limited in the amount of quantity that will be transfered

        available_quantity = gifter.resources[resource]
        # random chosen by probability 
        return math.floor(random.uniform(0, 1 - resource_weight) * available_quantity) 

       

# Inputs: 
#   country: CountryNode to be determined upon if they have sufficient resources
#   resource: resource name
#   quantity: amount of specified resource 
# Outputs:
#    boolean indicating if country has at least the specified amount of said resource
    def sufficient_quantity(self, country, resource, quantity):
        return country.current_state.resources[resource] >= quantity
 
 