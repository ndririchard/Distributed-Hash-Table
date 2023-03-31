import sys
sys.path.append("src")
from utility import *


class Node:

    def __init__(self, env, id):

        # Node parameter
        self.id = id
        self.env = env
        self.isAlive = True

        # Node Neighbor
        self.next = None
        self.prev = None

        # Node Data
        self.data = {}

        # Routing
        self.routing_table = {}

        # EVENT LOG
        logging.info("OBJECT CREATION - Node-{} is created at {}".\
                     format(self.id, self.env.now))
    
    def __str__(self):
        return "id => {}\nnext => {}\nprev => {}".\
            format(self.id, self.next.id, self.prev.id)
    
    def join(self, rdn_node, ttl = 0):

        if rdn_node.next == rdn_node.prev == None:
            rdn_node.next = rdn_node.prev = self
            self.next = self.prev = rdn_node
            logging.info("Node-{} inserted in the DHT at {}".\
                         format(self.id, self.env.now))
        
        elif (rdn_node.id < self.id <= rdn_node.next.id) or \
            (rdn_node.next.id < rdn_node.id < self.id):
            self.prev, self.next = rdn_node, rdn_node.next
            rdn_node.next.prev , rdn_node.next = self, self
            logging.info("Node-{} inserted in the DHT at {}".\
                         format(self.id, self.env.now))

        else:

            logging.info("JOIN FORWARD - {} Node-{} forward join-req to Node-{} ".\
                         format(ttl+1, rdn_node.id, rdn_node.next.id))
            
            self.join(rdn_node.next)
    
    def leave(self):
        
        if self.next == self.prev == None:
            pass
        
        else:

            self.next.prev, self.prev.next = self.prev, self.next
            self.isAlive = False

            logging.info("LEAVE - Node-{} left ".format(self.id))
    
    def forward(self, msg):

        if msg.isAlive():
            

            msg.ttl += 1 # increase the TTL
            logging.info("MSG FORWARD - {} Node-{} {} μs".format(msg.ttl, self.id, 
                                    (time.time() - msg.time)*10**6))
            
            if self.id == msg.receiver.id:
                self.deliver(msg)
            
            else:
                next_hope = self.next # by default, next is the next hope
                if abs(self.next.id - msg.receiver.id) >= \
                    abs(self.prev.id - msg.receiver.id):
                    next_hope = self.prev
                next_hope.forward(msg)
        else :

            logging.info("FORWARD ERROR - Msg-{} drop cause reach MAX_NUM_HOPES at {}".\
                     format(msg.id, self.env.now))
        
    def deliver(self, msg):

        msg.time = (time.time() - msg.time)*10**6
        logging.info("Msg-{} read by Node-{} at {}".\
                     format(msg.id, self.id, self.env.now))

    def haveCopy(self, key):
        if key in self.data:
            return True
        return False
    
    def replicat(self, key, value, drepl = 3):

        if self.next == self.prev == None:
            pass

        else :
        
            left, right = self.prev, self.next 
            for loop in range(drepl):

                if left.haveCopy(key):
                    logging.info("REPLICAT ERROR - Try to replicate Data on Node-{} but operation failed at {}".\
                                format(left.next.id, self.env.now))
                    
                elif right.haveCopy(key):
                    logging.info("REPLICAT ERROR - Try to replicate Data on Node-{} but operation failed at {}".\
                                format(right.next.id, self.env.now))
                    
                else :
                    left.put(key, value)
                    logging.info("REPLICAT - Data replicated on Node-{} at {}".\
                            format(left.next.id, self.env.now))
                    
                    right.put(key, value)
                    logging.info("REPLICAT - Data replicated on Node-{} at {}".\
                            format(right.next.id, self.env.now))
                
                left, right = left.prev, right.next

    def put(self, key, value):
        self.data[key] = value

    def get(self, key):

        if key in self.data:
            return self.data[key]
        
        else:
            return None
        
