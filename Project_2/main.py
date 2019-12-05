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
        self.prob = prob
        self.measurements = tuple(self.measurements)

        self.map = {} # Map - Adjacent rooms of each room

        # Dictionary with rooms connections
        for room in self.rooms:
            self.map.update({room:[]})

        # Map - Adjacent rooms of each room
        for connect in self.connections:
            self.map[connect[0]].append(connect[1])
            self.map[connect[1]].append(connect[0])


        self.T = self.nb_measurements



        self.nb_sensors = len(self.sensors) #number of sensores
        
        #Create Baysean Network
        self.BNet = probability.BayesNet()

        for sensor in self.sensors:
            room_sensor = self.sensors[sensor][0]
            TPR = self.sensors[sensor][1]
            FPR = self.sensors[sensor][2]
            # Parents --> Rooms with sensors
            self.BNet.add((room_sensor,'',0.5))
            # Childs -> Sensors
            self.BNet.add((sensor,room_sensor,{True: TPR, False: FPR}))






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
        print("PROBABILITY: ",pb.prob)
        print("MEASUREMENTS: ",pb.measurements)
        print("MAP: ", pb.map)
        print("#################################")
        print(pb.BNet)
        print(pb.BNet.variable_node('s3').cpt)
        #solver(fh)
        fh.close()
else:
    print("Usage: %s <filename>"%(sys.argv[0]))
