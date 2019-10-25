#! /usr/bin/env python3

import sys
sys.path.insert(0, 'aima')

import search

class ASARProblem(search.Problem):
    """Airline Scheduling and Routing Problem"""


    def __init__(self, fh):
        """ Define goal state and initialize a problem """
        self = self.load(fh)
        #Problem.__init__(self, initial, goal)
        search.Problem.__init__(self, 1,1)

    def load(self,fh):
        "loads input file"

        lines = fh.read().splitlines()

        file = list(filter(None,lines)) # removes blank lines
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
        actions = []
        for x in self.l:
            flag1 = False
            flag2 = True
            for i in x:
                if i == state[2] and x.index(i)==0 : #verificar quais as legs com aeroporto de partidad do estado
                    flag1 = True  #maneira horrivel de fazer mas funciona
                if i == state[1]: #quais as legs que podem ser realizadas com o aviao do estado
                    flag2 = True
            if flag1 and flag2:
                actions.append(x)
        return actions

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        time1 = state[3]
        time2 = action[2]

        h = int(time1[0:2]) + int(time2[0:2])
        m = int(time1[2:4]) + int(time2[2:4])

        if m > 60:
            m = m - 60
            h = h + 1
        if h < 10:
            time = "0" + str(h)
        else:
            time = str(h)
        if m < 10:
            time = time + "0" + str(m)
        else:
            time = time + str(m)

        return state + action[1:2] + [time]


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
    with open(sys.argv[1]) as fh:
        pb = ASARProblem(fh)
    #print(pb.a)
    #print(pb.p)
    #print(pb.l)
    #print(pb.c)
    #print()
    #print(pb.initial)
    #print(pb.goal)
    state = [pb.p[0][0],pb.p[0][1],pb.a[0][0], pb.a[0][1]]

    print(state)
    actions = pb.actions(state)

    print(actions)
    print("#########")

    print(pb.result(state,actions[0]))


else:
    print("Usage: %s <filename>"%(sys.argv[0]))
