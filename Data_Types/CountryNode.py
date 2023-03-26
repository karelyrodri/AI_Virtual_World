
class Country():
    def __init__(self, name, init_state):
        self.name = name
        self.initial_state = init_state # kept in order to reset on demand
        self.current_state = init_state # will continue to change
        self.actions_list = None # list of possible actions
        # self.print_country_data()

    def print_country_data(self):
        print(self.name)
        print("Resources:")
        print(self.current_state.resources)
        print("State Quality:")
        print(self.current_state.quality_evaluation)

