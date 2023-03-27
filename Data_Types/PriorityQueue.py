class PriorityQueue(): # PriorityQueue
    def __init__(self):
        self.frontier = []

    def push(self, country_schedule): # sorted lowest to highest EU
        size = len(self.frontier)
        latest_schedule = country_schedule.decisions[-1]
        EU = latest_schedule["expected_utility"]
        index = size - 1 if size > 0 else 0 # if index doesnt update then we can assume it is the largest value 
        for i in range(size):
            if (EU <= self.frontier[i].decisions[-1]["expected_utility"]): 
                index = i
                break
        self.frontier.insert(index, country_schedule)

    def is_empty(self):
        return len(self.frontier) == 0

    def pop(self):
        return self.frontier.pop()
    
    def peek(self):
        return self.frontier[-1]
    
    def size(self):
        return len(self.frontier)
