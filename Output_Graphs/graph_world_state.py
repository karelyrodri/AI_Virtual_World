import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import seaborn as sns
import os
import numpy as np


class Graph_Results():
    def __init__(self, winning_schedules): # lists of type Schedules 
        self.path = os.getcwd() + "\\Output_Graphs\\"
        self.graph_EU(winning_schedules)
        self.inital_final_resource_barplot(winning_schedules)
        self.create_resource_df(winning_schedules)

        
    def graph_EU(self, schedule_data):  # X axis - number of actions take Y axis - EU score    
                         # line plotted dashed per publisher, solid line for overall average
    
        fig, axes = plt.subplots(2, 1, figsize=(8, 6))
        colors = ['b', 'g', 'r', 'c', 'm', 'k']
        for country in schedule_data.keys():
            schedules = schedule_data[country]
            color = colors.pop()
            EUs = []
            state_qualities = []
            prev_growth_EU = 0
            for i in range(len(schedules)):
                cur_schedule = schedules[i]
                cur_EUs = cur_schedule.get_all_EUs()
                cur_EUs = (np.array(cur_EUs) + prev_growth_EU).tolist()
                EUs += cur_EUs
                prev_growth_EU += cur_EUs[-1]

                cur_state_qualities = cur_schedule.get_all_state_qualities_by_country(country)
                state_qualities += cur_state_qualities
                if (i < len(schedules) - 1): 
                    axes[0].axvline(len(EUs))
                    axes[1].axvline(len(EUs))
            x_range = np.arange(len(EUs))
            search_algo = schedules[-1].get_search_strategy_by_country(country)
            label = "{0} ({1}) - ".format(country, search_algo)
            axes[0].plot(x_range, EUs, marker='o', ms = 2, label = label + "EU", color = color)
            axes[1].plot(x_range, state_qualities, marker='o', ms = 2, label = label + "state quality", color = color)


        # plt.xticks(x_range)
        axes[0].title.set_text("Expected Utility Growth After Each Turn")
        axes[1].title.set_text("State Quality Over Time")
        fig.tight_layout()
        axes[0].legend(loc="upper left")
        axes[1].legend(loc="upper left")
        axes[0].set_ylim(bottom=-10)
        axes[1].set_ylim(bottom=-10)
        plt.savefig(self.path + "Growth_Over_Time.jpg")
        # plt.show()


    
    # Still working on getting a bar working 
    # currently prints a dataframe for staring and final states 
    def inital_final_resource_barplot(self, schedule_data): # resources per country at the start and very end
        country_labels = schedule_data.keys()

        # print(list(schedule_data.values())[-1])
        final_world_state = list(schedule_data.values())[-1][-1].latest_world_state()
        country_labels = final_world_state.keys()

        dfs = [pd.DataFrame(), pd.DataFrame()]
        for country in country_labels:
            countryNode = final_world_state[country]
            label = "{0} ({1}) - ".format(country, countryNode.search)

            initial_state = countryNode.initial_state.resources
            initial_state["Country"] = label
            if (len(dfs[0].columns) == 0): dfs[0] = pd.DataFrame(columns=initial_state.keys())
            dfs[0] = pd.concat([dfs[0], pd.DataFrame([initial_state])], axis=0, ignore_index=True)
 
            final_state = countryNode.current_state.resources
            final_state["Country"] = label
            if (len(dfs[1].columns) == 0): dfs[1] = pd.DataFrame(columns=final_state.keys())
            dfs[1] = pd.concat([dfs[1], pd.DataFrame([final_state])], axis=0, ignore_index=True)

        # print(df_start)
        # print(df_final)
        pd.concat(dfs, axis=0, ignore_index=True).to_csv(self.path + "Inital_Final_States.csv", index=False)
        fig, axes = plt.subplots(2, 1, figsize=(20, 12))

        for position in range(2):
            df = dfs[position]
            df.plot(ax = axes[position], kind='bar', rot=0, x = "Country", \
                      title = "{0} State Resources".format("Inital" if (position == 0) else "Final"))
            axes[position].legend_.remove()
    
        # ax.set_title("Resources per turn for {0}".format(country))
        plt.legend(title="Resources", loc='upper left', bbox_to_anchor=(1.02, 1.7))
        plt.savefig(self.path + "Initial_Final_Resources.jpg")
        



    def create_resource_df(self, schedule_data): # resources per country at the start and very end
        
        resource_df = pd.DataFrame()
        labels = {} # country : label 
        for countryNode in list(schedule_data.values())[-1][-1].latest_world_state().values():
            initial_state = countryNode.initial_state.resources
            label = "{0} ({1}) - ".format(countryNode.name, countryNode.search)
            labels[countryNode.name] = label
            initial_state["Country"] = label
            initial_state["Turn"] = 0
            if (len(resource_df.columns) == 0): resource_df = pd.DataFrame(columns=initial_state.keys())
            resource_df = pd.concat([resource_df, pd.DataFrame([initial_state])], axis=0, ignore_index=True)
 
        for country in schedule_data.keys():
            schedules = schedule_data[country]
            schedule_num = 1
            for schedule in schedules:
                final_schedule_world_state = schedule.latest_world_state()
                countryNode = final_schedule_world_state[country]
                state = countryNode.current_state.resources
                state["Country"] = labels[country]
                state["Turn"] = schedule_num
                resource_df = pd.concat([resource_df, pd.DataFrame([state])], axis=0, ignore_index=True)
                schedule_num += 1
        self.barplot_resources_turns(resource_df)

    def barplot_resources_turns(self, resource_df):
        fig, axes = plt.subplots(6, 1, figsize=(22, 42))
        countries = resource_df["Country"].unique()
        position = 0
        for country in countries:#schedule_data.keys():
            country_df =  resource_df.loc[resource_df["Country"].str.startswith(country)]
            country_df = country_df.loc[:, country_df.columns != "Country"]
            # print(country_df)

            country_df.plot(ax = axes[position], kind='bar', rot=0, x = "Turn", \
                            title = "Resources per turn for {0}".format(country))
            axes[position].legend(title="Resources", loc='upper left', bbox_to_anchor=(1.01, 1.02))
            
            position += 1
        plt.savefig(self.path + "Resources_Per_Turn.jpg")
        # plt.show()



