#! /usr/bin/env python3

import sys
sys.path.insert(0, 'aima')
import copy

import search

class ASARProblem(search.Problem):
     """Airline Scheduling and Routing Problem"""


     def __init__(self):
         """ Define goal state and initialize a problem """

     def load(self,fh):
         "loads input file"

         lines = fh.read().splitlines()

         file = list(filter(None,lines)) # removes blank lines
         a,p,l,c = ({} for i in range(4))

         for string in file:
             if string[0] == "A":
                 ax = string[2:].split()
                 a.update({ax[0]:tuple(ax[1:])})

             elif string[0] == "P" :
                 px = string[2:].split()
                 p.update({px[0]:px[1]})

             elif string[0] == "L":
                 lx = string[2:].split()
                 l.update({tuple(lx[0:2]):tuple(lx[2:])})

             elif string[0] == "C":
                 cx = string[2:].split()
                 c.update({cx[0]:cx[1]})

         self.a = a
         self.p = p
         self.l = l
         self.c = c
         self.nodes = 0


         planes_list = [] #initially we don't have a plane and airport defined. The algorithm takes care of that
         for key in p:
             planes_list.append(key)
         planes = dict(zip(planes_list, [None] * len(planes_list)))
         legs = list(l.keys())

         self.initial = StateDict(legs, planes, 0, self.nodes)

         return self

     def actions(self, state):
         """Return the actions that can be executed in the given
         state. The result would typically be a list, but if there are
         many actions, consider yielding them one at a time in an
         iterator, rather than building them all at once."""

         actions = []

         for (airplane,info) in state.planes.items():
             if info == None:
                 for leg in state.legs:

                     fligh_duration = self.l[leg][0]
                     arrival = state.time_sum(self.a[leg[0]][0],fligh_duration) #check if the arrival time is after the closing time of the airport
                     if arrival <= self.a[leg[1]][1] and arrival >= self.a[leg[1]][0]: # arrival of aircraft > closing time
                        actions.append([airplane, leg[0], leg[1]])

             else:
                 for leg in state.legs:
                     if leg[0] == info[1]: #Check if the leg departure airport is equal to the state airport departure for that aricraft
                         fligh_duration = self.l[leg][0]
                         arrival = state.time_sum(info[0],fligh_duration) #check if the arrival time is after the closing time of the airport
                         if arrival <= self.a[leg[1]][1] and arrival >= self.a[leg[1]][0]: # arrival of aircraft > closing time
                             actions.append([airplane,leg[0],leg[1]])
         return actions

     def result(self, state, action):
         """Return the state that results from executing the given
         action in the given state. The action must be one of
         self.actions(state)."""

         new_state = copy.deepcopy(state)

         if len(new_state.legs) > 0:
             airplane_code = action[0]

             airplane_type = self.p[airplane_code]# class of the airplane. ex: a320
             protation_time = self.c[airplane_type]

             if new_state.planes[action[0]] == None:
                 departure = self.a[action[1]][0]
                 new_state.planes[action[0]] = [None] * 2
                 new_state.planes[action[0]][0] = departure
                 new_state.planes[action[0]][1] = action[1]
             else:
                 departure = new_state.planes[airplane_code][0]



             flight_duration = self.l[tuple(action[1:])][0]

             arrival = state.time_sum(departure,flight_duration)

             new_state.planes[airplane_code] = ["", ""]
             new_state.planes[airplane_code][0] =  new_state.time_sum(arrival, protation_time)# new time of departure, airplane is added to dictionary

             new_state.planes[airplane_code][1] = action[2]#new departure airport

             new_state.legs.remove(tuple(action[1:]))# remove leg already used from list of legs

             leg = tuple(action[1:3])

             index_cost = self.l[leg].index(airplane_type) + 1
             link_cost = self.l[leg][index_cost]

             new_state.profit = new_state.profit + int(link_cost)

             if airplane_code in new_state.schedule: #check if it is the first flight
                 new_state.schedule[airplane_code].append(departure)
                 new_state.schedule[airplane_code].append(action[1])
                 new_state.schedule[airplane_code].append(action[2])

             else:
                 new_state.schedule.update({airplane_code:[departure, action[1], action[2]]})

         self.nodes = self.nodes + 1
         new_state.code = self.nodes

         return new_state


     def goal_test(self, state):

         # estado inicial igual ao estado final e lista de legs vazia
         """Return True if the state is a goal. The default method compares the
         state to self.goal or checks for state in self.goal if it is a
         list, as specified in the constructor. Override this method if
         checking against a single self.goal is not enough."""

         if not state.legs:

             for (airplane,info) in state.planes.items():
                 if info != None:
                     if info[1] != state.schedule[airplane][1]:
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

         cost = c + (1/int(link_cost))

         return cost


     def heuristic(self,n):
         h = 0
         return h

     def save(self,fh,state):
         if state != None:
             for airplane in state.schedule:
                 fh.write("S "+ airplane + " ")
                 sp = str(state.schedule[airplane])
                 sp = sp.replace(',','').replace('[','').replace(']','').replace('\'','')
                 fh.write(sp + "\n")

             fh.write("P "+ str (state.profit))
         else:
             fh.write("Infeasible")

         return


class StateDict(dict):
     """ State Class """
     def __init__(self, legs, planes, profit, code):
         self.legs = legs
         self.profit = 0
         self.planes = planes
         self.schedule = {}
         self.code = code

     def print_state(self):
         print("PLANES INFO " + str(self.planes))
         print("LEGS LEFT " + str(self.legs))
         print("PLANES SCHEDULES " + str(self.schedule))
         print("PROFIT " + str(self.profit))
         print("CODE " + str(self.code))
         return

     def __hash__(self):
         return hash(self.code)

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

##################################### MAIN ###################################

if len(sys.argv)>1:
    with open(sys.argv[1]) as fh:
        pb = ASARProblem()
        pb.load(fh)
        fh.close()

#     print(pb.a)
#     print(pb.p)
#     print(pb.l)
#     print(pb.c)
# #
#     print("##################")
#     #initial state for testing
#     state = pb.initial
#     print("---STATE---")
#     state.print_state()
#     print()
# #
# #
#     actions = pb.actions(state)
#     print("---ACTIONS---")
#     print(actions)
#     print()
# #
#     print("---ACTION---")
#     action = actions[0]
#     print(action)
#     print()
# #
#     print("---NEW STATE----")
#     new_state = pb.result(state,action)
#     new_state.print_state()
# #
# #
# #######
#     print()
#     print("--- TESTE 2 ---")
#     actions = pb.actions(new_state)
#     print(actions)
#     action = actions[0]
#     print(action)
#     new_state = pb.result(state,action)
#     new_state.print_state()
# #
# ######
# ########
#     print()
#     cost = pb.path_cost(0, pb.initial, action, new_state)
#     print("---PATH COST---- " + str(cost))
# #
# #########
#     print("---GOAL TEST--- " + str(pb.goal_test(new_state)))

    test = search.astar_search(pb,pb.heuristic)



#### TESTES
    with open("OUTPUT_TESTE.txt","w+") as fh:
        pb.save(fh,test.state)

else:
    print("Usage: %s <filename>"%(sys.argv[0]))
