
import Measures

class PriorityQueue():  

    def __init__(self):
        self.frontier = []

    def put(self, country, schedule): 
        EU = Measures.expected_utility(country, schedule)
        pass


    def is_empty(self):
        return len(self.frontier) == 0


    def pop(self):
        return self.frontier.pop(0)