#! /usr/bin/env python3

#import sys
#sys.path.insert(0, 'aima')

import search

class ASARProblem(search.Problem):
    """Airline Scheduling and Routing Problem"""


    def __init__(self):
        """ Define goal state and initialize a problem """
        #if len(sys.argv)>1:
          #  with open(sys.argv[1]) as fh:
          #      self.load(fh)
          #      fh.close()

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


        #planes = { "CS-TUA":["0800","LPMA"], "CS-TVA":["0800","LPFR"]} #planes initial state
        planes_list = [] #initially we don't have a plane and airport defined. The algorithm takes care of that
        for key in p:
            planes_list.append(key)
        planes = dict(zip(planes_list, [None] * len(planes_list)))


        legs = list(l.keys())
        #self.initial_state(a, legs, planes)
        self.initial = StateDict(legs, planes, 0)

        return self

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        actions = []

        # if dictionary is empty generate as actions all legs for all airplanes
      #  if not state.planes:
       #     for airplane in self.p:            
        #        for legs in self.l:
         #           actions.append([airplane, legs[0], legs[1]])
       # print("actions_empty =", actions)
         

        for (airplane,info) in state.planes.items():
            if info == None:
                for legs in self.l:
                    actions.append([airplane, legs[0], legs[1]])
                   # print("actions_current = ", actions)
            else:
                for leg in state.legs:
                    if leg[0] == info[1]: #Check if the leg departure airport is equal to the state airport departure for that aricraft
                        fligh_duration = self.l[leg][0]
                        arrival = state.time_sum(info[0],fligh_duration) #check if the arrival time is after the closing time of the airport

                        if arrival <= self.a[leg[1]][1]: # arrival of aircraft > closing time
                            actions.append([airplane,leg[0],leg[1]])
        return actions

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""


        airplane_code = action[0]

        airplane_type = self.p[airplane_code]# class of the airplane. ex: a320
        protation_time = self.c[airplane_type]

        if state.planes[action[0]] == None:
            departure = self.a[action[1]][0]
            state.planes[action[0]] = [None] * 2
            state.planes[action[0]][0] = departure
            state.planes[action[0]][1] = action[1]
        else:
            departure = state.planes[airplane_code][0]

        # fill initial state
      #  if not state.planes:
       #     for airport in self.a:
         #       if airport == action[1]:
         #           departure = self.a.get(airport)[0]
             #       print("DEPARTURE = ", departure)
       # else:
           # departure = state.planes[airplane_code][0]

        flight_duration = self.l[tuple(action[1:])][0]
        #print("FLIGHT DURATION = ",flight_duration)
        arrival = state.time_sum(departure,flight_duration)
       # print("ARRIVAL = ", arrival)
        state.planes[airplane_code] = ["", ""]
        state.planes[airplane_code][0] =  state.time_sum(arrival, protation_time)# new time of departure, airplane is added to dictionary

        state.planes[airplane_code][1] = action[2]#new departure airport

        state.legs.remove(tuple(action[1:]))# remove leg already used from list of legs

        leg = tuple(action[1:3])

        index_cost = self.l[leg].index(airplane_type) + 1
        link_cost = self.l[leg][index_cost]

        state.profit = state.profit + int(link_cost)

        if airplane_code in state.schedule: #check if it is the first flight
            state.schedule[airplane_code].append(departure)
            state.schedule[airplane_code].append(action[1])
            state.schedule[airplane_code].append(action[2])

        else:
            state.schedule.update({airplane_code:[departure, action[1], action[2]]})

        return state


    def goal_test(self, state):

        # estado inicial igual ao estado final e lista de legs vazia
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if not state.legs:
            for (airplane,info) in state.planes.items():
                if info[1] != self.initial.planes[airplane][1]:
                    return False
            return True
        else:
            return False

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
        
        return abs(1 / n.state.profit)

    def save(self,fh,state):

        if state != None:
            for airplane in state.schedule:
                fh.write(airplane + " ")
                sp = str(state.schedule[airplane])
                sp = sp.replace(',','').replace('[','').replace(']','').replace('\'','')
                fh.write(sp + "\n")

                fh.write("P "+ str (state.profit))
        else:
            fh.write("Infeasible")

        return


class StateDict(dict):
    """ State Class """
    def __init__(self, legs, planes, profit):
        self.legs = legs
        self.profit = 0
        self.planes = planes
        self.schedule = {}

    def print_state(self):
        print("PLANES INFO " + str(self.planes))
        print("LEGS LEFT " + str(self.legs))
        print("PLANES SCHEDULES " + str(self.schedule))
        print("PROFIT " + str(self.profit))

    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    def time_sum(self,time1, time2):
        """ Time calculator using string data """
        h = int(time1[0:2]) + int(time2[0:2])
        m = int(time1[2:4]) + int(time2[2:4])

        if m >= 60:
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
