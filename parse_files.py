import os
from Data_Types import Operators
import csv 

    # List of transforms created from parsing file
    # Idea for Part 2, different countries can have different transform templates 
def parse_transforms(file_name): # = "\\Initial_Data\\TRANSFORMS.txt"
    file_path = os.getcwd() + file_name
    transforms = []
    with open(file_path, mode = 'r') as file:
        lines = file.readlines()
        transform_data = None
        for line in lines:
            words = line.strip().replace("(", "").replace(")", "").split()
            if (len(words) > 0): # skip new lines
                if (words[1]) == "Template":
                    if (transform_data != None):
                        transforms.append(parse_transforms_helper(transform_data))
                    transform_data = [words[0]]
                else:
                    transform_data.extend(words)
                # print(words)
        transforms.append(parse_transforms_helper(transform_data))
    file.close()
    return transforms

def parse_transforms_helper(transform_data):
    transform = Operators.Transform(transform_data[0])
    # print(transform_data[0])
    output_idx = transform_data.index("OUTPUTS")
    i = transform_data.index("INPUTS") + 1 # could easily be set to 4
    while (i < len(transform_data)):
        if (i == output_idx): i += 1
        name = transform_data[i]
        amt = transform_data[i + 1]
        if (i < output_idx): # part of inputs 
            transform.inputs[name] = int(amt)
        else: # part of outputs
            transform.outputs[name] = int(amt)
        i += 2
    # print(transform.inputs)
    # print(transform.outputs)
    return transform
 

def parse_initial_resources(file_name): # = "\\Initial_Data\\Resources.csv"
    resources = {"Natural":{}, "Manufactured":{}, "Waste": {}}
    file_path = os.getcwd() + file_name
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            resource = row[0] 
            weight = float(row[1])
            if (weight == 0.0):
                resources["Natural"][resource] = int(weight)
            elif ("Waste" in resource):
                resources["Waste"][resource] = weight
            else:
                resources["Manufactured"][resource] = weight
    file.close()
    return resources


# def parse_initial_state(init_file = "\\Initial_Data\\Initial_State.csv", \
#                         resource_weight_file = "\\Initial_Data\\Resources.csv"): # 
#     file_path = os.getcwd() + init_file
#     countries = []
#     with open(file_path, newline='', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         categories = next(reader)
#         for row in reader:
#             name = row[0]
#             init_state = State.State(parse_initial_resources(resource_weight_file))
#             # print(name)
#             for i in range(1, len(categories)):
#                 resource = categories[i]
#                 amt = int(row[i])
#                 init_state.resources[resource] = amt
#                 # print("{0} - {1}".format(resource, amt))
#             # print(init_state.resourceWeights)
#             # add waste to the resources  from the initial resources file
#             for waste in init_state.resourceWeights["Waste"].keys():
#                 init_state.resources[waste] = 0
#             # print(init_state.resources)
#             init_state.set_quality_eval()
#             print(name)
#             countries.append(CountryNode.Country(name, init_state))
#     file.close()
#     return countries 

# parse_initial_state()
# parse_transforms()

def parse_initial_state(init_file = "\\Initial_Data\\Initial_State.csv"):
    file_path = os.getcwd() + init_file
    countries = {} # {country name : {resource : qty}}
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        categories = next(reader)
        for row in reader:
            name = row[0]
            countries[name] = {}
            for i in range(1, len(categories)):
                resource = categories[i]
                amt = int(row[i])
                countries[name][resource] = amt
    file.close()
    return countries

    
# parse_transforms()
# parse_initial_state()