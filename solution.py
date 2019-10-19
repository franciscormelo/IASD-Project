#! /usr/bin/env python3

import sys
sys.path.insert(0, 'aima')

import search

class ASARProblem(search.Problem):
    """Airline Scheduling and Routing Problem"""


    def __init__(self, filename):
        """ Define goal state and initialize a problem """
        self = self.load(filename)
        #Problem.__init__(self, initial, goal)
        search.Problem.__init__(self, 1,1)

    def load(self,filename):
        "loads input file"
        with open(filename) as fh:
            lines = fh.read().splitlines()

            file = list(filter(None,lines))
            a,p,l,c = ([] for i in range(4))
            for string in file:
                if string[0] == "A":
                    a.append(string[2:].split(" "))
                elif string[0] == "P" :
                    p.append(string[2:].split(" "))
                elif string[0] == "L":
                    l.append(string[2:].split(" "))
                elif string[0] == "C":
                    c.append(string[2:].split(" "))
                    self.a = tuple(a)
                    self.p = tuple(p)
                    self.l = tuple(l)
                    self.c = tuple(c)

                    return self

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError
    def heuristic(self,n):
        return

#####################################

if len(sys.argv)>1:
    solver = ASARProblem(sys.argv[1])
    print(solver.a)
    print(solver.p)
    print(solver.l)
    print(solver.c)
    print(solver.initial)
    print(solver.goal)

else:
    print("Usage: %s <filename>"%(sys.argv[0]))
