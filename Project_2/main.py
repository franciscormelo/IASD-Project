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
                probability = string[2:]

            elif string[0] == "M":  # A measurement
                self.nb_measurements += 1
                measurements.append(string[2:])

        self.connections = []
        self.sensors = {}
        self.measurements = [[] for i in range(self.nb_measurements)]


        for i in connections:
            aux1 = i.split(",")
            self.connections.append(tuple(aux1))
        for j in sensors:
            aux2 = j.split(":")
            self.sensors.update({aux2[0]: tuple([aux2[1], float(aux2[2]), float(aux2[3])])})

        for idx, k in enumerate(measurements):
            aux2 = k.split()
            for l in aux2:
                aux3 = l.split(":")
                self.measurements[idx].append(tuple(aux3))


        # Saves the problem information in problem attributes
        self.rooms = rooms
        self.connections = tuple(self.connections)
        #self.sensors = tuple(self.sensors)
        self.probability = probability
        self.measurements = tuple(self.measurements)

        self.map = {}

        # Dictionary with rooms connections
        for room in self.rooms:
            self.map.update({room:[]})


        for connect in self.connections:
            self.map[connect[0]].append(connect[1])
            self.map[connect[1]].append(connect[0])

        self.T = self.nb_measurements
        # probability.BayesNet()
        return



    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        # probability.elimination_ask()
        return (room, likelihood)

def solver(input_file):
    return Problem(input_file).solve()


######## MAIN #######
if len(sys.argv)>1:
    with open(sys.argv[1]) as fh:
        print(sys.argv[1])
        pb = Problem(fh)
        print("ROOMS: ",pb.rooms)
        print("CONNECTIONS: ",pb.connections)
        print("SENSORES: ",pb.sensors)
        print("PROBABILITY: ",pb.probability)
        print("MEASUREMENTS: ",pb.measurements)
        print("MAP: ", pb.map)
        #solver(fh)
        fh.close()
else:
    print("Usage: %s <filename>"%(sys.argv[0]))
