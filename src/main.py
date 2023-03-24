import sys
sys.path.append("/home/ndririchard/Documents/IDU4/INFO833/Distributed-Hash-Table/src")

from utility import *
from DHT.network.dht import DHT



if __name__ == "__main__":
    
    dht = DHT(ENV, KEY_LEN)
    ENV.process(dht.simulator())
    ENV.run(until=RUNNING_TIME)

    dht.display() # Display the DHTenv

