import sys
sys.path.insert(0, 'aima')
import probability

class Problem:

    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network

        # split the file into lines
        lines = fh.read().splitlines()

        # removes blank lines
        file = list(filter(None, lines))

        rooms, connections = (() for i in range(2))
        sensors, measurements = ([] for i in range(2))

        self.nb_measurements = 0

        # Separates the file information according to the first letter in each line
        for string in file:
            if string[0] == "R":  # Set of Rooms R
                rooms = tuple(string[2:].split())

            elif string[0] == "C":  # The set of connection
                connections = tuple(string[2:].split(" "))

            elif string[0] == "S":  # The set of sensors
                sensors = string[2:].split()

            elif string[0] == "P":  #  The propagation probability
                prob = string[2:]

            elif string[0] == "M":  # A measurement
                self.nb_measurements += 1
                measurements.append(string[2:])

        self.connections = []
        self.sensors = {}
        self.measurements = [[] for i in range(self.nb_measurements)]

        # split connection by ,
        for i in connections:
            aux1 = i.split(",")
            self.connections.append(tuple(aux1))
            # split sensor info  by :
        for j in sensors:
            aux2 = j.split(":")
            self.sensors.update({aux2[0]: tuple([aux2[1], float(aux2[2]), float(aux2[3])])})

        # split measurements info
        for idx, k in enumerate(measurements):
            aux2 = k.split()
            for l in aux2:
                aux3 = l.split(":")
                self.measurements[idx].append(tuple(aux3))


        # Saves the problem information in problem attributes
        self.rooms = rooms
        self.connections = tuple(self.connections)
        self.prob = float(prob)
        self.measurements = tuple(self.measurements)

        self.map = {} # Map - Adjacent rooms of each room

        # Dictionary with rooms connections
        for room in self.rooms:
            self.map.update({room:[]})

        # Map - Adjacent rooms of each room
        if not self.connections:
            # No connections ---> Empty map
            pass
        else:
            for connect in self.connections:
                self.map[connect[0]].append(connect[1])
                self.map[connect[1]].append(connect[0])


        self.T = self.nb_measurements



        self.nb_sensors = len(self.sensors) #number of sensores

        #Create Baysean Network
        self.BNet = probability.BayesNet()

        # Creates the Baysean Network taking into account each timestamp
        for time in range(self.T):

            time = time + 1 # Time starts at 1

            if time == 1: # in T = 1, rooms don't have parents
                for room in self.map: # add rooms as parent nodes
                    roomT = None
                    roomT = room + '_t' + str(time)
                    self.BNet.add((roomT,'',0.5)) # Initially all rooms are parents

            else: #if time > 1 -> rooms have parents -> rooms in the previous time and adjacent rooms
                for room in self.map:
                    roomT = None
                    nb_parents = 0
                    room_parents = None
                    roomT = room + '_t' + str(time)
                    room_parents = room + '_t' + str(time-1)
                    nb_parents += 1

                    for adjacents in self.map[room]:
                        if adjacents != []:
                            room_adjacent = adjacents
                            room_parents = room_parents +" " + room_adjacent + '_t' + str(time-1)
                            nb_parents +=1


                    if nb_parents == 1:
                        self.BNet.add((roomT, room_parents, {True:1.0, False:0.0}))
                    elif nb_parents == 2:
                        self.BNet.add((roomT, room_parents, {(True, True): 1.0, (True, False): 1.0, (False, True): self.prob, (False, False): 0.0}))
            # *****Falta melhorar quando sao mais do que 2 pais, tnetar fazer uma tabela de probabilidades automatica******

            for meas in self.measurements[time-1]: # add sensor nodes as childs of the room where the sensor is located in the current timestamp
                sensor = meas[0]
                parent_room = self.sensors[sensor][0] # Parent node of the sensor
                TPR = self.sensors[sensor][1] # True Positive Rate
                FPR = self.sensors[sensor][2] # False Positive Rate
                self.BNet.add((sensor+'_t'+str(time),parent_room + '_t'+ str(time),{True: TPR, False: FPR}))

    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference

        time = 1
        # Evidence String
        evidence = {}
        for measurements in self.measurements:
            for measurement in measurements:
                if measurement[1] == "F":
                    evidence.update({measurement[0]+"_t"+ str(time): False})

                else:
                    evidence.update({measurement[0]+"_t"+ str(time): True})
            time +=1

        room = ""
        likelihood = 0
        # Finds the room with the highest likelihood given the evidence
        for room_search in self.rooms:
            room_query = room_search + "_t" + str(self.T)

            prob = probability.elimination_ask(room_query, evidence, self.BNet)

            if prob[True] > likelihood:
                likelihood = prob[True]
                room = room_search

        return (room, likelihood)

def solver(input_file):
    return Problem(input_file).solve()


######## MAIN #######
if len(sys.argv)>1:
    with open(sys.argv[1]) as fh:
        #print(sys.argv[1])
        #pb = Problem(fh)
        #print("ROOMS: ",pb.rooms)
        #print("CONNECTIONS: ",pb.connections)
        #print("SENSORES: ",pb.sensors)
        #print("PROBABILITY: ",pb.prob)
        #print("MEASUREMENTS: ",pb.measurements)
        #print("MAP: ", pb.map)
        #print("#################################")
        #print(pb.BNet)

        solution = solver(fh)
        print(solution)

        fh.close()
else:
    print("Usage: %s <filename>"%(sys.argv[0]))
