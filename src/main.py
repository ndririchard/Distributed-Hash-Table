import sys
sys.path.append("src")
from utility import *
from dht.dht import *

if __name__ == "__main__":

    sys.setrecursionlimit(100000000)
    
    dht = Network(ENV)

    dht.simulation()

    ENV.run(until=RUNNING_TIME)

    print("taille = ", len(dht.nodes))

    dht.advancedRoutingSetting()

    dht.display()