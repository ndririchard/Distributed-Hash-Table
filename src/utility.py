
# IMPORTS
import sys
import time
import faker
import simpy
import random
import logging
import hashlib
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from simpy.events import AnyOf, AllOf, Event

# CONFIG
logging.basicConfig(filename="dht.log", level=logging.INFO, filemode="w",  
                        format='%(name)s - %(levelname)s - %(message)s')

# GLOBALS VARIABLES

TRESHOLD = 0.9
MAX_NUM_HOPES = 300

NUMBER_OF_NODES_IN_GROUPS = 17

RUNNING_TIME = 2
ENV = simpy.Environment()

MIN_NODE_ID = 1
MAX_NODE_ID = 1000000

TIME_TO_SEND = 0.2
TIME_TO_CREATE_OBJECT = 0.1
TIME_TO_JOIN_AND_LEAVE = 0.15


# GLOBALS FUNCTIONS

fake = faker.Faker() # SIMULATE FAKE DATA

def hash_string(string: str, algorithm: str = 'sha256') -> str:
    """
    Hashes a string using the specified algorithm.

    Args:
        string (str): the string to be hashed.
        algorithm (str): the hashing algorithm to use (default: 'sha256').

    Returns:
        str: the hashed value of the input string.
    """
    hash_object = hashlib.new(algorithm)
    hash_object.update(string.encode())
    return hash_object.hexdigest()

def plot_metrix(dht):

    x , y, z = [], [], []
    for msg in dht.backup:
        x.append(msg.ttl)
        y.append(msg.time)

    fig, ax = plt.subplots()

    ax.scatter(x, y, color="blue")

    ax.set_title("node number = {}".format(len(dht.nodes)))

    # Adding trendline
    z1 = np.polyfit(x, y, 1)
    p1 = np.poly1d(z1)
    ax.plot(x,p1(x),"r--")
