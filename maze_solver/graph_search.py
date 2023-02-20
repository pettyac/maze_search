import random
from SearchNode import *

#==============================================================================
# GRAPH_SEARCH
#
# The fringe and closed list must be drawn while the thinking takes place.
# - Draw the closed list blue (255, 0, 0).
# - Draw the fringe in green (0, 255, 0).
# - Supports early and late goal testing
#==============================================================================
def graph_search(problem=None,
                 Node=None,
                 fringe=None,
                 closed_list=None,
                 view0=None,
                 ):

    solution = 0
    start = problem.get_initial_state()
    if problem.goal_test(start): n.solution(problem.initial_state)
    fringe.put(SearchNode(start)) 
    while fringe:   
        maze = problem.maze
        Node = fringe.get()
        closed_list.put(Node.state)
        
        dirs = problem.actions(Node.state)
        for action in dirs:
            tup = problem.result(Node.state, action)
            n = SearchNode(tup, Node, action)

            # Early goal test
            if problem.goal_test(n.state): 
                solution = n.solution(problem.initial_state)
                view0['maze'].background[n.state] = (0,255,0)
                break
       
            if n.state not in closed_list:
                fringe.put(n) 
                
        #======================================================================
        # - Iterates through the fringe and colors the states of the search
        #   nodes with blue
        # - Iterates through the closed list and colors the states with red
        # - Colors the initial state green
        # - if ucs, iterates through 'danger rooms' and colors the state yella
        # - view0.run() draws everything
        #======================================================================
        if view0:
            for state in closed_list.values():
                view0['maze'].background[state] = (255,0,0)
            for i in fringe:
                view0['maze'].background[i.state] = (0,0,255)
            view0['maze'].background[problem.initial_state] = (0,255,0)
            view0.run() 
        
        if solution: return solution    
    
    return "NO SOLUTION"

def GBFS_search(problem=None,
                 Node=None,
                 fringe=None,
                 closed_list=None,
                 view0=None,
                 rooms=None):

    solution = 0
    start = problem.get_initial_state()
    if problem.goal_test(start): return 0
    fringe.put(GBFSSearchNode(start, h_cost=problem.h_cost(start)))
    while fringe:   
        maze = problem.maze
        Node = fringe.get()
        
        # LATE GOAL TEST 
        if problem.goal_test(Node.state):
            solution = Node.solution(problem.initial_state)
            view0['maze'].background[Node.state] = (0,255,0)
            view0.run()
            return solution

        closed_list.put(Node.state)
        dirs = problem.actions(Node.state)
        for action in dirs:
            room = problem.result(Node.state, action) 
            n = GBFSSearchNode(room, Node, action, problem.h_cost(room))
           
            # EARLY GOAL TEST
            '''
            if problem.goal_test(n.state):             
                solution = n.solution(problem.initial_state)
                view0['maze'].background[n.state] = (0,255,0)
                break
            '''
            if n.state not in closed_list:
                fringe.put(n) 
        
        #======================================================================
        # - Iterates through the fringe and colors the states of the search
        #   nodes with blue
        # - Iterates through the closed list and colors the states with red
        # - Colors the initial state green
        # - if ucs, iterates through 'danger rooms' and colors the state yella
        # - view0.run() draws everything
        #======================================================================
        if view0:
            for state in closed_list.values():
                view0['maze'].background[state] = (255,0,0)
            for i in fringe:
                view0['maze'].background[i.state] = (0,0,255)
            view0['maze'].background[problem.initial_state] = (0,255,0)
            view0.run() 
        
        # used only for early goal test
        # if solution: return solution    
    
    return "NO SOLUTION"


def UCS_search(problem=None,
                 Node=None,
                 fringe=None,
                 closed_list=None,
                 view0=None,
                 rooms=None):

    solution = 0
    start = problem.get_initial_state()
    if problem.goal_test(start): return 0
    fringe.put(UCSSearchNode(start))
    while fringe:   
        Node = fringe.get()
        
        # LATE GOAL TEST 
        if problem.goal_test(Node.state):
            solution = Node.solution(problem.initial_state)
            view0['maze'].background[Node.state] = (0,255,0)
            view0.run()
            return solution

        closed_list.put(Node.state)
        dirs = problem.actions(Node.state)
        for action in dirs:
            room = problem.result(Node.state, action) 
            
            if rooms.has_key(room):
                n = UCSSearchNode(room, Node, action, rooms[room])
            else: 
                n = UCSSearchNode(room, Node, action, Node.path_cost + 1)
           
            # EARLY GOAL TEST
            '''
            if problem.goal_test(n.state):             
                solution = n.solution(problem.initial_state)
                view0['maze'].background[n.state] = (0,255,0)
                break
            '''
            if n.state not in closed_list:
                fringe.put(n) 
        
        #======================================================================
        # - Iterates through the fringe and colors the states of the search
        #   nodes with blue
        # - Iterates through the closed list and colors the states with red
        # - Colors the initial state green
        # - if ucs, iterates through 'danger rooms' and colors the state yella
        # - view0.run() draws everything
        #======================================================================
        if view0:
            for state in closed_list.values():
                view0['maze'].background[state] = (255,0,0)
            for i in fringe:
                view0['maze'].background[i.state] = (0,0,255)
            if rooms: 
                for room in rooms: view0['maze'].background[room] = (255,255,0)
            view0['maze'].background[problem.initial_state] = (0,255,0)
            view0.run() 
        
        # used only for early goal test
        # if solution: return solution    
    
    return "NO SOLUTION"


def AStar_search(problem=None,
                 Node=None,
                 fringe=None,
                 closed_list=None,
                 view0=None,
                 rooms=None):

    solution = 0
    start = problem.get_initial_state()
    if problem.goal_test(start): return 0
    fringe.put(AStarSearchNode(start, f_cost=problem.f_cost(start, 0)))
    while fringe:   
        Node = fringe.get()
        
        # LATE GOAL TEST 
        if problem.goal_test(Node.state):
            solution = Node.solution(problem.initial_state)
            view0['maze'].background[Node.state] = (0,255,0)
            view0.run()
            return solution

        closed_list.put(Node.state)
        dirs = problem.actions(Node.state)
        for action in dirs:
            room = problem.result(Node.state, action) 

            if rooms.has_key(room):
                n = AStarSearchNode(room, Node, action, rooms[room],
                                problem.f_cost(room, rooms[room]))
            else: 
                n = AStarSearchNode(room, Node, action, Node.path_cost + 1,
                                problem.f_cost((room, Node.path_cost + 1)))
           
            # EARLY GOAL TEST
            '''
            if problem.goal_test(n.state):             
                solution = n.solution(problem.initial_state)
                view0['maze'].background[n.state] = (0,255,0)
                break
            '''
            if n.state not in closed_list:
                fringe.put(n) 
        
        #======================================================================
        # - Iterates through the fringe and colors the states of the search
        #   nodes with blue
        # - Iterates through the closed list and colors the states with red
        # - Colors the initial state green
        # - if ucs, iterates through 'danger rooms' and colors the state yella
        # - view0.run() draws everything
        #======================================================================
        if view0:
            for state in closed_list.values():
                view0['maze'].background[state] = (255,0,0)
            for i in fringe:
                view0['maze'].background[i.state] = (0,0,255)
            if rooms: 
                for room in rooms: view0['maze'].background[room] = (255,255,0)
            view0['maze'].background[problem.initial_state] = (0,255,0)
            view0.run() 
        
        # used only for early goal test
        # if solution: return solution    
    
    return "NO SOLUTION"


def iterative_deepening_search(problem=None,
                 Node=None,
                 fringe=None,
                 closed_list=None,
                 limit=0,
                 view0=None):
    

    solution = 0
    fringe.set_limit(limit)
    start = problem.get_initial_state()
    if problem.goal_test(start): return 0
    fringe.put(IDDFSSearchNode(start)) 
    while fringe:   
        Node = fringe.get()
                                                         #LATE GOAL TEST 
        if problem.goal_test(Node.state):
            solution = Node.solution(problem.initial_state)
            view0['maze'].background[Node.state] = (0,255,0)
            view0.run()
            return solution
        
        closed_list.put(Node.state)
        dirs = problem.actions(Node.state)
        for action in dirs:
            (r, c) = problem.result(Node.state, action)
            n = IDDFSSearchNode((r,c), Node, action, Node.depth + 1)
            
            '''
            if problem.goal_test(n.state):                  #EARLY GOAL TEST
                solution = n.solution(problem.initial_state)
                view0['maze'].background[n.state] = (0,255,0)
                break
            '''
            if n.state not in closed_list:
                fringe.put(n) 
        
        
        if view0:
            for state in closed_list.values():
                view0['maze'].background[state] = (255,0,0)
            for i in fringe:
                view0['maze'].background[i.state] = (0,0,255)
            view0.run() # Draw everything
        
        if solution: return solution
    
    if fringe.deeper_limit():
        #print "Restarting... depth = " + str(limit+1)
        if view0:
            for state in closed_list.values():
                view0['maze'].background[state] = (0,0,0)
         
        limit += 1
        closed_list.clear()
        return iterative_deepening_search(problem=problem, fringe=fringe,
                                   closed_list=closed_list,
                                   limit=limit, view0=view0)
    
    else: return "NO SOLUTION"