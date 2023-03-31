import sys
sys.path.append("src")
from utility import *
from node.node import *
from message.msg import *


class Network:

    def __init__(self, env, advanced_routing = True):
        # DHT PARAMETERS
        self.env = env
        self.nodes = []
        self.backup = []
        self.advanced_routing = advanced_routing
        
        # LOGGING
        logging.info("OBJECT CREATION - DHT is created at {}".\
                        format(self.env.now))

        # ADD DEFAULT NODE
        self.nodes.append(Node(self.env, 0))
    
    def createGroups(self, sorted_Nodes):
        groups = {}
        i, group_id = 0, 0
        nodes = []
        while i < len(sorted_Nodes):
            if (i % NUMBER_OF_NODES_IN_GROUPS == 0) and (i != 0):
                groups[group_id] = nodes
                nodes = []
                group_id += 1
            else:
                nodes.append(sorted_Nodes[i])
            i += 1
        groups[group_id] = nodes
        return groups

    def updateNodeRoutingTable(self, routing_table):
        for node in self.nodes:
            node.routing_table = routing_table
        logging.info("Nodes routing table have been updated at {}".\
                     format(self.env.now))

    def advancedRoutingSetting(self):
        sorted_nodes = []
        
        node = self.nodes[0]
        capteur = True
        while capteur:
            sorted_nodes.append(node)
            node = node.next
            if node == self.nodes[0]:
                capteur = False
        groups = self.createGroups(sorted_nodes)
        print(groups)
    
    def display(self):

        # CREATE A NETWORK GRAPH ISING NETWORKX
        graph = nx.Graph()

        # ADD NODES
        for node in self.nodes:
            graph.add_node(node.id)
        
        # CREATE EGDES ONLY WHEN THE NODE IS ACTIVE
        cn = self.nodes[0]
        c = True
        while c:
            if cn.isAlive:
                graph.add_edge(cn.id, cn.next.id)
            if cn.next == self.nodes[0]:
                c = False
            cn = cn.next
        
        # DRAW THE GRAPH
        nx.draw(graph, with_labels=True, font_weight='bold')

        # ADD THE METRIX OF PERFORMANCE TO THE PLOT
        plot_metrix(self)
        
        plt.show()
    
    def joinLeaveSimulation(self):

        while True:

            # CHOOSE A RANDOM ACTION BETWEEN JOINNING THE DHT AND LEAVING
            todo = random.random()

            if todo <= TRESHOLD:

                node = Node(self.env, random.randint(MIN_NODE_ID, 
                                                MAX_NODE_ID))
                node.join(random.choice(self.nodes))
                self.nodes.append(node)
                yield self.env.timeout(TIME_TO_JOIN_AND_LEAVE)
            
            else:

                node = random.choice((self.nodes))
                node.leave()
                yield self.env.timeout(TIME_TO_JOIN_AND_LEAVE)
    
    def sendSimulation(self):

        """
            Here, we simulate the fact that several nodes try 
            to deliver message to each other
        """

        while True:

            sender = random.choice(self.nodes)
            receiver = random.choice(self.nodes)

            if (sender.isAlive and receiver.isAlive):
                msg = Msg(self.env, sender, receiver)
                logging.info("Node-{} made a SEND to Node-{} at {}".format(sender.id, receiver.id, self.env.now))
                msg.send()
                self.backup.append(msg)
                yield self.env.timeout(TIME_TO_SEND)

    def putGetSimulation(self):

        put_time = random.random() + 0.5

        while True:
            
            rdn_node = random.choice(self.nodes)
            value = fake.catch_phrase() + " " + fake.word() + " " + fake.word() # generate fake movie name
            key = hash_string(value)

            rdn_node.put(key, value)
            logging.info("Node-{} added new data@<<{}>> at {}".format(rdn_node.id, value, self.env.now))
            rdn_node.replicat(key, value)

            yield self.env.timeout(TIME_TO_SEND)
    
    
    
    def simulation(self):

        self.env.process(self.joinLeaveSimulation())

        self.env.process(self.sendSimulation())

        self.env.process(self.putGetSimulation())
