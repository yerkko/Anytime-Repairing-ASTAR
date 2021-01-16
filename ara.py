from binary_heap import BinaryHeap
from node import Node
import time


class Ara:
    def __init__(self, initial_state, heuristic, weight, max_expansions):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.heuristic = heuristic
        self.weight = weight
        self.open = None
        self.cost = None
        self.max_expansions = max_expansions
        self.last_solution = None

    def estimate_suboptimality(self):
        cost = self.cost
        denominator = min(self.open, key=lambda x: x.g + x.h)

        denominator_num = denominator.h + denominator.g

        return cost/denominator_num 

    def fvalue(self, g, h):
        return g + self.weight * h

    def adjust_weight(self):
        denominator = min(self.open, key=lambda x: x.g + x.h)
        denominator_num = denominator.h + denominator.g
        self.weight = self.last_solution.g / denominator_num

    def recalculate_open(self):
        for i in self.open:
            i.key = self.fvalue(i.g, i.h)
        self.open.reorder()


    def search(self):
        
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)
        initial_node.key = self.fvalue(
            0, initial_node.h)  # asignamos el valor f
        self.open.insert(initial_node)
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while self.expansions <= self.max_expansions:

            while not self.open.is_empty():

                if self.expansions >= self.max_expansions:
                    return self.last_solution

                n = self.open.extract()

                if not self.open.is_empty() and self.open.top().key == n.key:
                    tied_node = self.open.top()
                    if tied_node.g < n.g:
                        tied_node = self.open.extract()
                        self.open.insert(n)
                        n = tied_node

                if n.state.is_goal():
                    self.end_time = time.process_time()
                    self.cost = n.g
                    self.last_solution = n
                    self.adjust_weight()
                    self.recalculate_open()
                    #print('aaa')
                    yield n


                if not(self.last_solution is not None and n.g + n.h >= self.last_solution.g):
                    succ = n.state.successors()
                    self.expansions += 1

                    if self.expansions >= self.max_expansions:
                        return self.last_solution

                    for child_state, action, cost in succ:
                        child_node = self.generated.get(child_state)
                        is_new = child_node is None  
                        path_cost = n.g + cost 
                        if is_new or path_cost < child_node.g:
                            if is_new: 
                                child_node = Node(child_state, n)
                                child_node.h = self.heuristic(child_state)
                                self.generated[child_state] = child_node
                            child_node.action = action
                            child_node.parent = n
                            child_node.g = path_cost
                            child_node.key = self.fvalue(child_node.g, child_node.h)
                            self.open.insert(child_node)
            self.end_time = time.process_time()
            if self.open.is_empty():
                #print("empty open")
                return self.last_solution
            #return None
        return self.last_solution
