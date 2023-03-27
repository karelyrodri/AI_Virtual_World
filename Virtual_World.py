#Karely Rodriguez
# CS5260 AI
#Programming Project Part 1

# MAIN FUNCTION FOUND AT THE BOTTOM
from Data_Types import CountryNode, State, Actions
from Search_Strategies import HeuristicDepthFirstSearch as H_dfs, GreedyBestFirstSearch as GreedyBestFS
import parse_files as pf
from Output_Graphs import graph_world_state as gr
from enum import Enum

class VirtualWord ():
    class Search_Type(Enum):
        HueristicDFS = 0,
        GreedyBestFirstSearch = 1

    def __init__ (self):
        # self.operators = None
        self.init_state_data = None # {countryName: {resourceName: qty}}
        self.world_countries = {} # full of country nodes
        self.winning_country_schedules = {} #{countryName : [outputschedules]}


    def setup_virtual_World(self):
        country_data = {}
        self.init_state_data = pf.parse_initial_state()
        for country in self.init_state_data.keys():
            # can easily do something like country + "Resources.csv" or country + "Tranforms.txt" 
            transforms = self.setup_country_node(country, "Resources.csv", "TRANSFORMS.txt")
            country_data[country] = transforms
        # set up countries action_lists not that we have all the countryNodes created 
        for country in self.world_countries.keys():
            country_transforms = country_data[country]
            resources = self.world_countries[country].current_state.resources.keys()
            # print(self.world_countries)
            # for part 2 we can consider alliances in which only those who are allies can be 
            # approached for a transer, for now we just pass in all the countries         
            action_list = Actions.Action_List(country_transforms, resources, self.world_countries[country], self.world_countries)
            self.world_countries[country].actions_list = action_list
    
         
           

    def setup_country_node(self, name, resource_file, transform_file):
        init_state = State.State(pf.parse_initial_resources("\\Initial_Data\\" + resource_file))
        resource_data = self.init_state_data[name]
        for resource in resource_data.keys():
            amt = resource_data[resource]
            init_state.resources[resource] = amt

        # add waste to the resources  from the initial resources file
        for waste in init_state.resource_weights["Waste"].keys():
            init_state.resources[waste] = 0
        # evaluate state quality for intial resources
        init_state.set_quality_eval()
        country_node = CountryNode.Country(name, init_state)
        self.world_countries[name] = country_node

        transforms = pf.parse_transforms("\\Initial_Data\\" + transform_file)
        return transforms


    def country_scheduler(self, country_name, resource_file, initial_state_file, \
                                      output_schedule_file, num_output_schedules, \
                                      depth_bound, frontier_max_size, search_algorithm):
                                               
        print(country_name + " entered scheduler")
        country = self.world_countries[country_name]
        action_list =  country.actions_list

        #conduct search
        search_name = ""
        if (search_algorithm == self.Search_Type.HueristicDFS):
            schedule = H_dfs.HeuristicDepthFirstSearch(country, action_list, depth_bound, frontier_max_size, self.world_countries).get_best_schedule()
            search_name = "H_DFS"
        elif (search_algorithm == self.Search_Type.GreedyBestFirstSearch):
            schedule = GreedyBestFS.GreedyBestFirstSearch(country, action_list, depth_bound, frontier_max_size, self.world_countries).get_best_schedule()
            search_name = "GBFS"
        # print(schedule.decisions)
        # self.print_world_country_data()
        #update the world state 
        self.world_countries = schedule.decisions[-1]["world_state"]
        # print to text file
        schedule.output_scheduler("{0}_{1}_{2}".format(country.name, search_name, output_schedule_file))
        self.winning_country_schedules.setdefault(country_name, []).append(schedule)



    def print_world_country_data(self):
        for country in self.world_countries.values():
            country.print_country_data()
    
###################################
#         Main program
###################################
def main ():
    initial_state_file = "\\Initial_Data\\Initial_State.csv"
    world = VirtualWord()
    world.setup_virtual_World()

    num_out_schedules = 3
    for i in range(num_out_schedules):
        for country in world.world_countries.values():
            depth_bound = 5 # how much can they develop in one turn 
            frontier_max_size = 100 # how far can their search get 
            world.country_scheduler(country.name, "\\Initial_Data\\Resources.csv", initial_state_file, \
                                                 "output_schedule.txt", num_out_schedules, depth_bound, \
                                                frontier_max_size, world.Search_Type.HueristicDFS)
                                                        #   world.Search_Type.GreedyBestFirstSearch 
            
    # plot graphs and save
    gr.Graph_Results(world.winning_country_schedules, depth_bound, num_out_schedules)


if __name__ == "__main__":
    main ()