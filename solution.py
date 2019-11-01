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

        self.initial = { "CS-TUA":["0600","LPPT"], "CS-TVA":["0800","LPFR"],"LEGS": list(pb.l.keys())}
        return self

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        actions = []

        for (airplane,info) in state.items():

            if airplane != "LEGS":

                for leg in state["LEGS"]:

                    if leg[0] == info[1]: #Check if the leg departure airport is equal to the state airport departure for that aricraft
                        fligh_duration = self.l[leg][0]
                        arrival = time_sum(info[0],fligh_duration) #check if the arrival time is after the closing time of the airport

                        if arrival <= self.a[leg[1]][1]: # arrival of aircraft > closing time
                            actions.append([airplane,leg[0],leg[1]])
        return actions

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        airplane_type = self.p[action[0]]
        protation_time = self.c[airplane_type]

        flight_duration = self.l[tuple(action[1:])][0]
        arrival = time_sum(state[action[0]][0],flight_duration)
        state[action[0]][0] =  time_sum(arrival, protation_time)

        state[action[0]][1] = action[2]

        state["LEGS"].remove(tuple(action[1:]))

        return state


    def goal_test(self, state):

        # estado inicial igual ao estado final e lista de legs vazia
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if not state["LEGS"]:

            for (airplane,info) in state.items():
                if airplane != "LEGS":
                    if info[1] != self.initial[airplane][1]:
                        return False
            return True
        else:
            return False
                    #if isinstance(self.goal, list):
                    #    return is_in(state, self.goal)
                    #else:
            #return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        leg = tuple(action[1:3])
        airplane_type = self.p[action[0]]


        index_cost = self.l[leg].index(airplane_type) + 1
        link_cost = self.l[leg][index_cost]

        return c + (1/int(link_cost))


    def heuristic(self,n):
        self.h = 0
        return self.h

    def save(self,fh,state):
            return


def time_sum(time1, time2):
    """ Time calculator using string data """
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

    return time

##################################### MAIN ###################################

if len(sys.argv)>1:
    with open(sys.argv[1]) as fh:
        pb = ASARProblem()
        pb.load(fh)

    print(pb.a)
    print(pb.p)
    print(pb.l)
    print(pb.c)

    print("##################")
    #initial state for testing
    state = pb.initial
    print("---STATE---")
    print(state)
    print()


    actions = pb.actions(state)
    print("---ACTIONS---")
    print(actions)
    print()

    print("---ACTION---")
    action = actions[0]
    print(action)
    print()

    print("---NEW STATE----")
    new_state = pb.result(state,action)
    print(new_state)


########
    print("---PATH COST----")
    print("Path Cost")
    cost = pb.path_cost(0, pb.initial, action, new_state)
    print(cost)

#########
    print("GOAL TEST")
    print(pb.goal_test(state))
    h =  pb.heuristic

    search.astar_search(pb,h)


else:
    print("Usage: %s <filename>"%(sys.argv[0]))
