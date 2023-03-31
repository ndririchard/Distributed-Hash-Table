import sys
sys.path.append("src")
from utility import *

class Msg:

    def __init__(self, env, sender, receiver):
        self.ttl = 0
        self.env = env
        self.time = time.time()
        self.id = random.randint(1, 100)

        self.sender = sender
        self.receiver = receiver

        logging.info("Msg-{} created at {}".format(self.id, self.env.now))

    def __str__(self):
        return "Message-{}".format(self.id)
    
    def isAlive(self):
        return self.ttl <300
    
    def send(self):
        
        if self.sender.next == self.sender.prev == None:
            pass
        
        else :
            
            # by default, next is the next hope
            next_hope = self.sender.next 
            
            if abs(self.sender.next.id - self.receiver.id) >= \
                abs(self.sender.prev.id - self.receiver.id):

                # choose the prev node as next hope if it's closer than the next
                next_hope = self.sender.prev 
            
            # deliver the message to next_hope
            next_hope.forward(self) 
