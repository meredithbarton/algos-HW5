import sys


class Wrestler:
    """Represents a wrestler. Information pertaining to rival and
    assigned team is stored here."""
    def __init__(self, name):
        self.name = name
        self.rivals = []
        self.team = -1
        self.visited = -1

    def new_rival(self, rival):
        self.rivals.append(rival)


class UndirectedGraph:
    """Represents an undirected graph, using wrestlers as vertices,
    and rivalries as edges. The graph exists as either bipartite, or not."""
    def __init__(self):
        self.adj_list = {}
        self.is_bipartite = True
        self.first = None

    def add_vertex(self, wrestler):
        """Adds a vertex to Graph. The first wrestler added
        is to be the source of the graph, for ease of testing"""
        # set a "first" wrestler, for ease of testing
        if len(self.adj_list) == 0:
            self.first = wrestler.name
            wrestler.team = "Babyface"
            wrestler.visited = 0

        # this gives a way to get full wrestler object from name
        self.adj_list[wrestler.name] = wrestler

    def add_edge(self, src, dst):
        """Add an edge to represent rivalries"""
        self.adj_list[src].new_rival(dst)
        self.adj_list[dst].new_rival(src)

    def check_bipartite(self):
        """Check for a bipartite graph using a modified BFS"""
        working_queue = []
        first = self.adj_list[self.first]
        working_queue.append(first)

        while working_queue:
            cur = working_queue.pop(0)

            if cur.team == -1:
                cur.team = "Babyface"
                cur.visited = 0

            # check each rival of cur for teams and assign where needed
            for x in range(len(cur.rivals)):
                # get rival
                rival_name = cur.rivals[x]
                rival_object = self.adj_list[rival_name]
                # -1 represents no color assignment
                if rival_object.visited == -1:
                    # 0 marks that a wrestler has been assigned a team
                    rival_object.visited = 0

                    # assign rival opposite team
                    if cur.team == "Babyface":
                        rival_object.team = "Heel"
                    elif cur.team == "Heel":
                        rival_object.team = "Babyface"

                    working_queue.append(rival_object)

                elif rival_object.visited == 0:
                    # rival already has a team
                    if rival_object.team == cur.team:
                            self.is_bipartite = False

            if not working_queue:
                # check for unconnected wrestlers
                for name in self.adj_list:
                    remaining = self.adj_list[name]
                    if remaining.visited == -1:
                        working_queue.append(remaining)


# data given as argument in command line
input_file = sys.argv[1]
sys.stdin = open(input_file, 'r')

# gather input
WWE = UndirectedGraph()
n = int(input())
for i in range(n):
    wrestler_name = input()
    wrestler_object = Wrestler(wrestler_name)
    WWE.add_vertex(wrestler_object)

r = int(input())
for j in range(r):
    rivalry = input()
    rivalry = rivalry.split()
    WWE.add_edge(rivalry[0], rivalry[1])

# Output
WWE.check_bipartite()

if WWE.is_bipartite:
    print("Yes Possible")
    babyfaces = []
    heels = []
    for wrestler in WWE.adj_list:
        if WWE.adj_list[wrestler].team == "Babyface":
            babyfaces.append(WWE.adj_list[wrestler].name)
        elif WWE.adj_list[wrestler].team == "Heel":
            heels.append(WWE.adj_list[wrestler].name)
    print("Babyfaces: ", babyfaces)
    print("Heels: ", heels)
else:
    print("Impossible")

dataOut = open('results.txt', 'w')
dataOut.write("Yes Possible")
dataOut.write("\n")
dataOut.write("Babyfaces: " + str(babyfaces))
dataOut.write("\n")
dataOut.write("Heels: " + str(heels))
dataOut.close()