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
            graph.add_edge(cn.id, cn.next.id)
            if cn.next == self.nodes[0]:
                c = False
            cn = cn.next

        subax1 = plt.subplot(121)
        nx.draw(graph, with_labels=True, font_weight='bold')
        plt.show()  


    def simulator(self, time):
        for loop in range(30):
            t = random.random()
            node = Node(self.env, random.randint(1, 1000))
            print("New node_{} created at {}".format(node.id, self.env.now))
            node.join(random.choice(self.nodes))
            self.nodes.append(node)
            yield self.env.timeout(t)
        
        rdn = random.choice(self.nodes)
        rdn.leave()
        self.nodes.remove(rdn)
        print("Node {} left at {}".format(rdn.id, self.env.now))
        yield self.env.timeout(1)