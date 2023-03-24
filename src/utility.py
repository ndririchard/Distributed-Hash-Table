
# imports
import simpy
import random
import hashlib
import networkx as nx
import matplotlib.pyplot as plt



# GLOBALS VARIABLES

ENV = simpy.Environment()
RUNNING_TIME = 10
KEY_LEN = 8

TRESHOLD = 0.9

JOIN_TTL = random.random()
LEAVE_TTL = random.random()

MIN_NODE_ID = 1
MAX_NODE_ID = 1000000


