import math

class PriorityQueue(): # PriorityQueue
    def __init__(self): # helps pick up where we left off the last turn for that country
                                       # needed to allow pruning right away for the new turn 
      
        self.frontier = []

    def push(self, country_schedule): # sorted lowest to highest EU
        size = len(self.frontier)
        EU = country_schedule.latest_EU()
        index = size # if index doesnt update then we can assume it is the largest value 

        for i in range(size):
            if (EU <= self.frontier[i].latest_EU()):
                index = i
                break
        self.frontier.insert(index, country_schedule)
        

    def is_empty(self):
        return len(self.frontier) == 0

    def pop(self):
        return self.frontier.pop()
    
    def peek(self):
        return self.frontier[-1]
    
    def best_schedule(self):
        return self.peek()
    

    def meets_threshold(self, schedule):
        current_EU = schedule.latest_EU()
        EU = 0
        for schedule in self.frontier:
            EU += schedule.get_EU(schedule.length() - 1)
        average_EU = EU / self.size()
        return current_EU >= average_EU


    def size(self):
        return len(self.frontier)
    
    def best_schedule_EU(self):
        return -math.inf if (self.size() == 0) else self.peek().latest_EU()
    
    def print_Schedule_EUs(self):
        EUs = []
        for schedule in self.frontier:
            EUs.append(schedule.latest_EU())
        print(EUs)
