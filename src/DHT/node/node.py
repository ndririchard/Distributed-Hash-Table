import sys
sys.path.append("/home/ndririchard/Documents/IDU4/INFO833/Distributed-Hash-Table/src")

from utility import *


class Node:

    def __init__(self, env, id):
        self.id = id
        self.env = env
        self.isAline
        self.data = {}
        self.next = None
        self.prev = None
        self.routing_table = {}
    
    def __str__(self):
        return "id => {}\nnext => {}\nprev => {}".format(self.id, self.next.id, self.prev.id)

    def closestNode(self, rdn_node):
        if abs(self.id - rdn_node.next.id) > abs(self.id - rdn_node.prev.id):
            return rdn_node.prev
        return rdn_node.next
    
    def join(self, rdn_node):
        """
            join the dht by contacting an random node
        """
        print("join the DHT by contacting node {} at {}".format(rdn_node.id, self.env.now))
        if rdn_node.next == rdn_node.prev == None:
            rdn_node.next = rdn_node.prev = self
            self.next = self.prev = rdn_node
        
        elif rdn_node.id < self.id <= rdn_node.next.id:
            self.prev, self.next = rdn_node, rdn_node.next
            rdn_node.next.prev , rdn_node.next = self, self

        else:
            print("Transfert req to node {} at {}".format(rdn_node.next.id, self.env.now))
            self.join(rdn_node.next)
        
    def leave(self):
        if self.next == self.prev == None:
            pass
        else:
            self.next.prev, self.prev.next = self.prev, self.next




"""if __name__ == "__main__":
    node1 = Node(None, 1)
    node2 = Node(None, 2)
    node3 = Node(None, 3)
    node4 = Node(None, 34)

    node2.join(node1)
    node3.join(node1)
    node4.join(node1)
    node2.leave()

    print(node3)"""