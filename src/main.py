import sys
sys.path.append("/home/ndririchard/Documents/IDU4/INFO833/Distributed-Hash-Table/src")

from utility import *
from DHT.network.dht import DHT



if __name__ == "__main__":
    env = simpy.Environment()
    key_len = 8
    dht = DHT(env, key_len)
    env.process(dht.simulator(10000))
    env.run(until=1000000000**2)
    dht.display()

