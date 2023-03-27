import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import seaborn as sns
import os


class Graph_Results():
    def __init__(self, winning_schedules, schedule_length, num_of_schedules): # lists of type Schedules 
        self.path = os.getcwd() + "\\Output_Graphs\\"
        self.graph_EU(winning_schedules, schedule_length, num_of_schedules)
        self.barplot_resources(winning_schedules)

        
    def graph_EU(self, schedule_data, schedule_length, schedule_nums):  # X axis - number of actions take Y axis - EU score    
                         # line plotted dashed per publisher, solid line for overall average
        plt.rcParams["figure.figsize"] = [8, 5]
        plt.rcParams["figure.autolayout"] = True 
        colors = ['b', 'g', 'r', 'c', 'm', 'k']
        x_range = np.arange(schedule_nums * schedule_length)
        for country in schedule_data.keys():
            schedules = schedule_data[country]
            color = colors.pop()
            EUs = []
            for i in range(len(schedules)):
                schedule = schedules[i].decisions[1:] # excluding initial state 
                for decision in schedule:
                    EUs.append(decision["expected_utility"])
            plt.plot(x_range, EUs, marker='o', ms = 2, label = country, color = color)
        
        plt.xticks(x_range)
        plt.title("EU Scores of Best Schedules")
        plt.legend()
        plt.savefig(self.path + "EU_Scores.jpg")
        plt.show()
    
    # Still working on getting a bar working 
    # currently prints a dataframe for staring and final states 
    def barplot_resources(self, schedule_data,): # resources per country at the start and very end
        country_labels = schedule_data.keys()

        # print(list(schedule_data.values())[-1])
        final_world_state = list(schedule_data.values())[-1][-1].decisions[-1]["world_state"]
        country_labels = final_world_state.keys()

        df_start = pd.DataFrame()
        df_final = pd.DataFrame()
        for country in country_labels:
            countryNode = final_world_state[country]

            initial_state = countryNode.initial_state.resources
            initial_state["Country"] = country
            if (len(df_start.columns) == 0): df_start = pd.DataFrame(columns=initial_state.keys())
            df_start = pd.concat([df_start, pd.DataFrame([initial_state])], axis=0, ignore_index=True)
 
            final_state = countryNode.current_state.resources
            final_state["Country"] = country
            if (len(df_final.columns) == 0): df_final = pd.DataFrame(columns=final_state.keys())
            df_final = pd.concat([df_final, pd.DataFrame([final_state])], axis=0, ignore_index=True)

        print(df_start)
        print(df_final)
