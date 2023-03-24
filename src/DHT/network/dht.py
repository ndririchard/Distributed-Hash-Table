import sys
sys.path.append("/home/ndririchard/Documents/IDU4/INFO833/Distributed-Hash-Table/src")

from DHT.node.node import Node
from utility import *


class DHT:

    def __init__(self, env, key_len):
        self.env = env
        self.key_len = key_len
        self.nodes = [Node(self.env, 0)] # default node

    def display(self):
        graph = nx.Graph()
        for node in self.nodes:
            graph.add_node(node.id)

        cn = self.nodes[0]
        c = True
        while c:
            if cn.isAlive:
                graph.add_edge(cn.id, cn.next.id)
            if cn.next == self.nodes[0]:
                c = False
            cn = cn.next

        subax1 = plt.subplot(121)
        nx.draw(graph, with_labels=True, font_weight='bold')
        plt.show()  


    def simulator(self):
        
        while True:
            action = random.random() # choose a random action for the DHT

            if action <= TRESHOLD: # create a new node

                node = Node(self.env, random.randint(MIN_NODE_ID, MAX_NODE_ID))
                print("NEW_NODE : Node-{} is created at {}".format(node.id, self.env.now))
                node.join(random.choice(self.nodes)) # join the DHT
                self.nodes.append(node) # Add the node to the DHT 
                yield self.env.timeout(JOIN_TTL)
            
            else:
                node = random.choice((self.nodes))
                node.leave()
                print("LEAVE_EVENT : Node-{} left ".format(node.id))
                yield self.env.timeout(LEAVE_TTL)
           




        