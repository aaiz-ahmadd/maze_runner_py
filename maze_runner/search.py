"""
search.py
---------
THE MAZE RUNNER — Mini Project 1: Classical Search

This is where you implement the search algorithms (Questions 1–7).

Every algorithm receives a SearchProblem (see problems.py) and must return a
LIST OF ACTIONS that leads from the start state to a goal state, e.g.
['South', 'South', 'East']. Return [] if the start state is already a goal.

Conventions the grader relies on (please read — they matter!):

  * Use the fringe containers from util.py (Stack, Queue, PriorityQueue).
  * Calling problem.getSuccessors(state) counts as EXPANDING that state.
    Call it exactly once per expanded state, and never for a state you only
    generated.
  * Goal test when a state is POPPED from the fringe (just before you would
    expand it), not when it is pushed. (For BFS the grader also accepts
    the "early" goal test done when a state is generated.)
  * Push successors in the order getSuccessors returns them.
  * Q1, Q2, Q5, Q6, Q7 are GRAPH searches: keep a set of already-expanded
    states and never expand the same state twice.
"""

import util
from util import Stack, Queue, PriorityQueue, CUTOFF
from heuristics import nullHeuristic


# ----------------------------------------------------------------------
# Q0 (worked example, not graded): always go right
# ----------------------------------------------------------------------
def alwaysRightSearch(problem):
    """
    Not a real search: the runner keeps stepping right ('East') until he
    reaches the goal. If a wall blocks the way east, he is stuck and gives up
    (returns None). It shows you how to use the problem's methods. Try it:
        python runner.py -l maze_tiny -a right     (escapes)
        python runner.py -l maze_small -a right       (walks into a wall)
    """
    state = problem.getStartState()
    actions = []
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)   # list of (next, action, cost)
        east = [s for s in successors if s[1] == 'East']
        if not east:
            return None   # a wall straight ahead: the doors close with him inside
        nextState, action, stepCost = east[0]
        actions.append(action)
        state = nextState
    return actions


# ----------------------------------------------------------------------
# Q1: Depth-First Search
# ----------------------------------------------------------------------
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first (graph search).

    To get started, try printing:
        print("Start:", problem.getStartState())
        print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
        print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    Hint: a fringe entry can hold more than a state. Storing
    (state, actionsSoFar) is an easy way to remember how you got there.
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    initial_state = problem.getStartState()
    frontier.push((initial_state, []))
    explored_states = set()

    while not frontier.isEmpty():
        current_node, path_history = frontier.pop()

        if problem.isGoalState(current_node):
            return path_history

        if current_node not in explored_states:
            explored_states.add(current_node)

            for next_state, move, cost in problem.getSuccessors(current_node):
                updated_path = path_history + [move]
                frontier.push((next_state, updated_path))

    return None


# ----------------------------------------------------------------------
# Q2: Breadth-First Search
# ----------------------------------------------------------------------
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first (graph search)."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    initial_state = problem.getStartState()
    frontier.push((initial_state, []))
    explored_states = set()

    while not frontier.isEmpty():
        current_node, path_history = frontier.pop()

        if problem.isGoalState(current_node):
            return path_history

        if current_node not in explored_states:
            explored_states.add(current_node)

            for next_state, move, cost in problem.getSuccessors(current_node):
                updated_path = path_history + [move]
                frontier.push((next_state, updated_path))

    return None


# ----------------------------------------------------------------------
# Q3: Depth-Limited Search
# ----------------------------------------------------------------------
def depthLimitedSearch(problem, limit):
    """
    Depth-first search that never goes deeper than 'limit' actions.

    Return value:
      * a list of at most 'limit' actions that reaches a goal, or
      * CUTOFF (from util) if no goal was found but the search was stopped
        by the depth limit somewhere, so a deeper solution may exist, or
      * None if no goal was found and the limit was never reached, which
        proves there is no solution at all.

    The start state is at depth 0. A state at depth == limit may be goal
    tested but must not be expanded.

    Do NOT use a global explored set here (think about why that can make the
    search miss a solution that fits within the limit). Instead, avoid cycles
    by not revisiting a state that is already on the current path.
    """
    "*** YOUR CODE HERE ***"
    nodes_stack = util.Stack()
    start_pos = problem.getStartState()
    nodes_stack.push((start_pos, [], [start_pos]))

    hit_limit = False

    while not nodes_stack.isEmpty():
        curr_state, actions_taken, states_in_path = nodes_stack.pop()

        if problem.isGoalState(curr_state):
            return actions_taken

        if len(actions_taken) == limit:
            hit_limit = True
            continue

        for child_state, direction, move_cost in problem.getSuccessors(curr_state):
            if child_state not in states_in_path:
                new_actions = actions_taken + [direction]
                new_states_path = states_in_path + [child_state]
                nodes_stack.push((child_state, new_actions, new_states_path))

    if hit_limit:
        return util.CUTOFF

    return None


# ----------------------------------------------------------------------
# Q4: Iterative Deepening Search
# ----------------------------------------------------------------------
def iterativeDeepeningSearch(problem, maxDepth=10000):
    """
    Run depthLimitedSearch with limit = 0, 1, 2, ... until it finds a
    solution. Return that solution, or None if the problem has no solution
    (or none within maxDepth).
    """
    "*** YOUR CODE HERE ***"
    for i in range(maxDepth + 1):
        result = depthLimitedSearch(problem, i)

        if result is not util.CUTOFF:
            return result

    return None


# ----------------------------------------------------------------------
# Q5: Uniform-Cost Search
# ----------------------------------------------------------------------
def uniformCostSearch(problem):
    """Search the node of least total path cost g(n) first (graph search)."""
    "*** YOUR CODE HERE ***"
    queue = PriorityQueue()
    state = problem.getStartState()
    queue.push((state, [], 0), 0)
    visited = set()

    while not queue.isEmpty():
        state, path, cost = queue.pop()

        if problem.isGoalState(state):
            return path

        if state in visited:
            continue

        visited.add(state)
        successor = problem.getSuccessors(state)

        for s, p, c in successor:
            if s not in visited:
                queue.push((s, path + [p], cost + c), cost + c)

    return None


# ----------------------------------------------------------------------
# Q6: Greedy Best-First Search
# ----------------------------------------------------------------------
def greedyBestFirstSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that SEEMS closest to the goal first, i.e. the one with
    the lowest heuristic(state, problem) value (graph search).
    """
    "*** YOUR CODE HERE ***"
    p_queue = util.PriorityQueue()
    start_pos = problem.getStartState()

    h_val = heuristic(start_pos, problem)
    p_queue.push((start_pos, []), h_val)

    visited_nodes = set()

    while not p_queue.isEmpty():
        curr_state, actions_taken = p_queue.pop()

        if problem.isGoalState(curr_state):
            return actions_taken

        if curr_state not in visited_nodes:
            visited_nodes.add(curr_state)

            for child_state, direction, move_cost in problem.getSuccessors(curr_state):
                new_actions = actions_taken + [direction]
                child_h_val = heuristic(child_state, problem)
                p_queue.push((child_state, new_actions), child_h_val)

    return None


# ----------------------------------------------------------------------
# Q7: A* Search
# ----------------------------------------------------------------------
def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node with the lowest f(n) = g(n) + heuristic(n) first
    (graph search).
    """
    "*** YOUR CODE HERE ***"
    p_queue = util.PriorityQueue()
    start_pos = problem.getStartState()

    start_f_val = heuristic(start_pos, problem)
    p_queue.push((start_pos, [], 0), start_f_val)

    visited_nodes = set()

    while not p_queue.isEmpty():
        curr_state, actions_taken, past_cost = p_queue.pop()

        if problem.isGoalState(curr_state):
            return actions_taken

        if curr_state not in visited_nodes:
            visited_nodes.add(curr_state)

            for child_state, direction, move_cost in problem.getSuccessors(curr_state):
                new_actions = actions_taken + [direction]
                new_past_cost = past_cost + move_cost

                child_f_val = new_past_cost + heuristic(child_state, problem)

                p_queue.push((child_state, new_actions, new_past_cost), child_f_val)

    return None


# Abbreviations
always_right = alwaysRightSearch
dfs = depthFirstSearch
bfs = breadthFirstSearch
dls = depthLimitedSearch
ids = iterativeDeepeningSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch
astar = aStarSearch