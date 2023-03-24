import sys
import unittest

sys.path.append("/home/ndririchard/Documents/IDU4/INFO833/Distributed-Hash-Table/src")

from DHT.node.node import DHTNode

class NodeTest(unittest.TestCase):

    def setUp(self):
        self.node = DHTNode(None, 89)
        self.rdn = DHTNode(None, 4)
    
    def testIsAlone(self):
        self.assertTrue(self.node.isAlone(self.rdn))
    
    def testJoin(self):
        self.node.join(self.rdn)
        
        self.assertEqual(self.node.previous_node, self.rdn)
        self.assertEqual(self.node.next_node, self.rdn)

        self.assertEqual(self.rdn.previous_node, self.node)
        self.assertEqual(self.rdn.next_node, self.node)

    


if __name__ == '__main__':
    unittest.main()