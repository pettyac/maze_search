"""
There should only be console printing in main.py. Remember to comment out ALL
debug/test printing in your other python files.
"""

import sys
import random;

import config
from pymaze import *
from Problem import *
from Fringe import *
from ClosedList import *
from Bot import RandomBot
from view import View
from view import EdgeView
from graph_search import *

seed = input("enter random seed: ")
random.seed(seed)

#==============================================================================
# DO NOT CHANGE ANYTHING IN THIS SECTION.
# Create maze
#==============================================================================
ROWS = config.ROWS
COLS = config.COLS
PUNCHES = config.PUNCHES
option = input("0-random maze or 1-stored maze: ")
maze = DFSMazeWithCycles(ROWS, COLS, PUNCHES)
if option == 1:
    maze.restore('maze.json')
rooms = {}
#==============================================================================
# DO NOT CHANGE ANYTHING IN THIS SECTION.
#==============================================================================
NUMBOTS = 1
r0 = int(input("initial row: "))
c0 = int(input("initial column: "))
initial_state = (r0, c0)
r1 = int(input("goal row: "))
c1 = int(input("goal column: "))
goal_state = (r1, c1)
search = raw_input("Search type <bfs | dfs | ucs | iddfs | astar | gbfs> : ")

if search == 'ucs' or search == 'astar':
    rooms = {}
    while 1:
        d_room = input("Enter dangerous room locations in \"x y cost\" format: ")
        if d_room == '': break
        d_room = d_room.split(" ")
        r2, c2, cost = [int(x) for x in d_room]
        rooms[(r2, c2)] = cost
#==============================================================================
# gui == True iff use graphical animation. For now set this to True.
#==============================================================================
#gui = raw_input('graphical animation? (y/n): ')
#if gui in 'yY':
#    gui = True
#else:
#    gui = False
gui = True

#==============================================================================
# Create view of maze and bot
#==============================================================================
if gui:
    from view import CELLWIDTH 
    view0 = View(width=(COLS) * CELLWIDTH,
                 height=(ROWS) * CELLWIDTH,
                 delay=1)
    mazeview = view0.add_maze(maze, name='maze')
    edgeview = view0.add_edges(mazeview, name='edgeview')
    
    bots = []
    for i in range(NUMBOTS):
        bot = RandomBot(maze, start=(r0, c0))
        bots.append(bot)
        name = 'bot%s' % i
        view0.add_bot(bot,
                      mazeview,
                      color=config.BOT_COLOR,
                      name=name)
else:
    view0 = None

#===========================================================
# Select the correct fringe object.
#===========================================================
problem = MazeProblem(maze=maze,
                      initial_state=(r0,c0),
                      goal_states=[(r1,c1)],
                      )
closed_list = SetClosedList()

if search == 'bfs':
    fringe = FSQueue()
    solution = graph_search(problem=problem,
                        fringe=fringe,
                        closed_list=closed_list,
                        view0=view0)
elif search == 'dfs':
    fringe = FSStack()
    solution = graph_search(problem=problem,
                            fringe=fringe,
                            closed_list=closed_list,
                            view0=view0)
elif search == 'ucs':
    fringe = UCSFringe()
    solution = UCS_search(problem=problem,
                        fringe=fringe,
                        closed_list=closed_list,
                        view0=view0,
                        rooms=rooms)
elif search == 'iddfs':
    fringe = IDFSStack()
    solution = iterative_deepening_search(problem=problem,
                        fringe=fringe,
                        closed_list=closed_list,
                        view0=view0)
elif search == 'gbfs':
    fringe = UCSFringe()
    problem = GBFSProblem(problem.maze, problem.initial_state, problem.goal_states)
    solution = GBFS_search(problem=problem,
                        fringe=fringe,
                        closed_list=closed_list,
                        view0=view0)
elif search == 'astar':
    fringe = UCSFringe()
    problem = AStarProblem(problem.maze, problem.initial_state, problem.goal_states)
    solution = AStar_search(problem=problem,
                        fringe=fringe,
                        closed_list=closed_list,
                        view0=view0,
                        rooms=rooms)
else:
    raise Exception('invalid search')
#==============================================================================
# DO NOT CHANGE ANYTHING IN THIS SECTION.
#==============================================================================
print("solution: %s" % solution)
print("len(solution): %s" % len(solution))
print("len(closed_list): %s" % len(closed_list))
print("len(fringe): %s" % len(fringe))

# Compute path from solution for drawing.
maze = problem.maze
(r, c) = initial_state
path = [initial_state]
for action in solution:
    (r, c) = maze.get_adj_tuple((r, c), action)
    path.append((r, c))
print("path: %s" % path)
for bot in bots:
    bot.set_path(path)

if gui:
    while 1:
        view0.run()
