#Karely Rodriguez
# CS5260 AI
#Programming Project Part 1

# MAIN FUNCTION FOUND AT THE BOTTOM
from Data_Types import CountryNode, State, Actions
from Search_Strategies import HeuristicDepthFirstSearch as H_dfs, GreedyBestFirstSearch as GreedyBestFS, RandomSearch
import parse_files as pf
from Output_Graphs import graph_world_state as gr
import copy
import os

class VirtualWord ():

    def __init__ (self):
        # self.operators = None
        self.init_state_data = None # {countryName: {resourceName: qty}}
        self.world_countries = {} # full of country nodes
        self.winning_country_schedules = {} #{countryName : [outputschedules]}


    def setup_virtual_World(self):
        self.init_state_data = pf.parse_initial_state()
        countries_params = pf.parse_configurations()
        transforms = pf.parse_transforms()
        allies = {}
        for country in self.init_state_data.keys():
            alliance = self.setup_country_node(country, countries_params[country])
            allies.setdefault(alliance, []).append(country)
        # set up countries action_lists not that we have all the countryNodes created 
        for country in self.world_countries.keys():
            countryNode = self.world_countries[country]
            resources = countryNode.current_state.resources.keys()
            self.world_countries[country].allies = allies[countryNode.allies] #overwritting alliance number with alliance list 
            # print(self.world_countries)
            # for part 2 we can consider alliances in which only those who are allies can be 
            # approached for a transer, for now we just pass in all the countries         
            action_list = Actions.Action_List(transforms, resources, country, countryNode.allies)
            self.world_countries[country].actions_list = action_list
           

    def setup_country_node(self, name, params):
        resource_file = "\\Initial_Data\\Resources{0}.csv".format(params["Resources_File"])
        init_state = State.State(pf.parse_initial_resources(resource_file))
        resource_data = self.init_state_data[name]
        for resource in resource_data.keys():
            amt = resource_data[resource]
            init_state.resources[resource] = amt
        # add waste to the resources  from the initial resources file
        for waste in init_state.resource_weights["Waste"].keys():
            init_state.resources[waste] = 0
        # evaluate state quality for intial resources
        init_state.set_quality_eval()
        allyNum = params["Alliance"]
        country_node = CountryNode.Country(name, init_state, int(params["Depth_Bound"]), 
                                           int(params["Max_Frontier_Size"]), params["Search"], 
                                           allyNum)
        self.world_countries[name] = country_node
        return allyNum


    def country_scheduler(self, country, output_schedule_file, depth_bound, frontier_max_size):
                                               
        print(country.name + " entered scheduler")
     
        action_list =  country.actions_list

        #conduct search
        search_algorithm = country.search
        # previous_best = self.winning_country_schedules.get(country.name) #pick up where we left off if applies 
        # if (previous_best != None): previous_best = previous_best[-1]
            
        if (search_algorithm == "H_DFS"):
            schedule = H_dfs.HeuristicDepthFirstSearch(country, action_list, depth_bound, frontier_max_size, \
                                                       self.world_countries).get_best_schedule()
        elif (search_algorithm == "GBFS"):
            schedule = GreedyBestFS.GreedyBestFirstSearch(country, action_list, depth_bound, frontier_max_size, self.world_countries).get_best_schedule()
        ##### ADDITION #####
        elif (search_algorithm == "RS"):
            schedule = RandomSearch.RandomSearch(country, action_list, depth_bound, frontier_max_size, self.world_countries).get_best_schedule()

        self.world_countries = copy.deepcopy(schedule.latest_world_state())

        # print to text file
        schedule.output_scheduler(output_schedule_file)
        self.winning_country_schedules.setdefault(country.name, []).append(schedule)


    def print_world_country_data(self):
        for country in self.world_countries.values():
            country.print_country_data()
    
def delete_old_output_schedules():
    path = os.getcwd() + "\\Output_Schedules\\"
    for file_name in os.listdir(path):
        os.remove(path + file_name)
###################################
#         Main program
###################################

num_out_schedules = 5

def main ():
    delete_old_output_schedules()
    world = VirtualWord()
    world.setup_virtual_World()
    print("Setup complete")
    
    for i in range(num_out_schedules):
        for country in world.world_countries.values():
            
            output_file = "{0}_{1}_output_schedule.txt".format(country.name, country.search)
            world.country_scheduler(country, output_file, country.depth_bound, country.max_frontier_size)
                                           
    # plot graphs and save
    gr.Graph_Results(world.winning_country_schedules)


if __name__ == "__main__":
    main ()