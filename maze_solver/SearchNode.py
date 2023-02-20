class SearchNode(object):

    def __init__(self,
                 state,
                 parent=None,
                 parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action

    def __str__(self):
        return '<SearchNode %s %s %s %s>' % (id(self),
                                                self.state,
                                                id(self.parent),
                                                id(self.parent_action))

    def solution(self, initial_state):
        solution = []
        Node = self
        while Node.state != initial_state:
            solution.append(Node.parent_action)
            Node = Node.parent
        solution = solution[::-1]
        return solution

class IDDFSSearchNode(SearchNode):
    def __init__(self, state, parent=None, parent_action=None, depth=0):
        super(IDDFSSearchNode, self).__init__(state, parent, parent_action)
        self.depth = depth
    
    def priority(self):
        return self.depth

class GBFSSearchNode(SearchNode):
    def __init__(self, state, parent=None, parent_action=None, h_cost=0):
        super(GBFSSearchNode, self).__init__(state, parent, parent_action)
        self.h_cost = h_cost

    def priority(self):
        return self.h_cost

class UCSSearchNode(SearchNode):
    def __init__(self, state, parent=None, parent_action=None, path_cost=0):
        super(UCSSearchNode, self).__init__(state, parent, parent_action)
        self.path_cost = path_cost

    def priority(self):
        return self.path_cost

class AStarSearchNode(UCSSearchNode):
    def __init__(self, state, parent=None, parent_action=None, path_cost=0, f_cost=0):
        super(AStarSearchNode, self).__init__(state, parent, parent_action, path_cost)
        self.f_cost = f_cost

    def priority(self):
        return self.f_cost

if __name__ == '__main__':
    print ("Testing (0,0) -> (1,0) -> (1,1) by actions ['E', 'S']")
    state00 = (0, 0)
    node00 = SearchNode(state00)
    state01 = (0, 1)
    node01 = SearchNode(state01, node00, 'E', 1)
    state11 = (1, 1)
    node11 = SearchNode(state11, node01, 'S', 1)
    print(node00)
    print(node01)
    print(node11)
    print(node11.solution())
    print("Expected: ['E', 'S']")
