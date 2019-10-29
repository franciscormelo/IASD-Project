#! /usr/bin/env python3

import sys
sys.path.insert(0, 'aima')

import search

class ASARProblem(search.Problem):
    """Airline Scheduling and Routing Problem"""


    def __init__(self):
        """ Define goal state and initialize a problem """

        #Problem.__init__(self, initial, goal)
        #search.Problem.__init__(self, 1,1)

    def load(self,fh):
        "loads input file"

        lines = fh.read().splitlines()

        file = list(filter(None,lines)) # removes blank lines
        a,p,l,c = ({} for i in range(4))

        for string in file:
            if string[0] == "A":
                ax = string[2:].split(" ")
                a.update({ax[0]:tuple(ax[1:])})

            elif string[0] == "P" :
                px = string[2:].split(" ")
                p.update({px[0]:px[1]})

            elif string[0] == "L":
                lx = string[2:].split(" ")
                l.update({tuple(lx[0:2]):tuple(lx[2:])})

            elif string[0] == "C":
                cx = string[2:].split(" ")
                c.update({cx[0]:cx[1]})

        self.a = a
        self.p = p
        self.l = l
        self.c = c

        return self

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        actions = {}

        for (airplane,info) in state.items():
            airplane_type = self.p[airplane]
            rotation_time = self.c[airplane_type]

            actions.update({ airplane: []})

            for (leg,details) in self.l.items():
                if leg[0] == info[1]: #legs that departure from the same airport of the state
                    fligh_duration = details[0]
                    #check if the arrival time is after the closing time of the airport
                    arrival = time_sum(info[0],fligh_duration)
                    print(arrival)
                    actions[airplane].append(leg)

        return actions

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        time1 = state[3]
        time2 = action[2]

        h = int(time1[0:2]) + int(time2[0:2])
        m = int(time1[2:4]) + int(time2[2:4])

        #time calculator using string data
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


    def heuristic(self,n):
        return

    def save(self,fh,state):
            return


def time_sum(time1, time2):
    h = int(time1[0:2]) + int(time2[0:2])
    m = int(time1[2:4]) + int(time2[2:4])

    #time calculator using string data
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

    return time

#####################################

if len(sys.argv)>1:
    with open(sys.argv[1]) as fh:
        pb = ASARProblem()
        pb.load(fh)


    print(pb.a)
    print(pb.p)
    print(pb.l)
    print(pb.c)

    print("##################")
    state = { "CS-TUA":("0600","LPPT"), "CS-TVA":("0800","LPFR")}

    print(state)


    actions = pb.actions(state)
    print(actions)



else:
    print("Usage: %s <filename>"%(sys.argv[0]))
