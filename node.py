class Node:
    def __init__(self, search_state, parent=None, action=''):
        self.state = search_state
        self.parent = parent
        if parent:             #  DFS/BFS
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.action = action    
        self.key = -1           # A*'s f
        self.g = 10000000000    # A*'s g
        self.heap_index = 0     # 
        self.h = -1             # A*'s h

    def __repr__(self):
        return self.state.__repr__()

    def trace(self):
        s = ''
        if self.parent:
            s = self.parent.trace()
            s += '-' + self.action + '->'
        s += str(self.state)
        return s
