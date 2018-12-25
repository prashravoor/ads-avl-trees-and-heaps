import logging
from argparse import ArgumentParser
import random

log = logging.getLogger()

class TreeNode(object):
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
    
    def __repr__(self):
        return str(self.value)
    
    def __lt__(self, other):
        if not other:
            return False
        return self.value < other.value
    
    def __eq__(self, other):
        if not other:
            return False
        
        return self.value == other.value
    
    def __gt__(self, other):
        if not other:
            return False
        
        return self.value > other.value

class BinaryTree(object):
    def __init__(self):
        self.root = None
        self.height = -1
        self.num_nodes = 0
    
    # Prints the tree on it's side, with the indent set to the level of the node
    # Siblings are on the same level
    # Sample output:
    """
    Tree:
    17
    - None
    - 62
    - - None
    - - 89
    - - - -20
    - - - - None
    - - - - 68
    - - - - - None
    - - - - - 70
    - - - - - - -37
    - - - - - - - -84
    - - - - - - - - None
    - - - - - - - - -38
    - - - - - - - - - -72
    - - - - - - - - - None
    - - - - - - - None
    - - - - - - None
    - - - None
    """
    def _pretty_print(self, node, level=0):
        log.debug("Entered print at node {} at level {}".format(node, level))
        result = ''

        for _ in range(level):
            result += '- ' # Add 2 spaces for each level
        result += str(node) + "\n"
        log.debug("Result at level {} is {}".format(level, result))
        if not node:
            return result
        if not node.left and not node.right:
            return result

        result += self._pretty_print(node.left, level+1)
        result += self._pretty_print(node.right, level+1)

        return result

    def __str__(self):
        # Display the tree as a string
        return self._pretty_print(self.root)
    
    def get_height(self):
        return self.height

    def get_num_nodes(self):
        return self.num_nodes

    def insert(self, value):
        log.debug("Inserting node {} into tree".format(value))
        node = TreeNode(value)
        cur = self.root
        while cur and (cur.left or cur.right):
            if node < cur and cur.left:
                log.debug("Going left from node {}".format(cur))
                cur = cur.left
            elif cur.right:
                log.debug("Going right from node {}".format(cur))
                cur = cur.right
            else:
                log.debug("Breaking!")
                break

        if not cur:
            log.debug("The first node is being inserted")
            self.root = node
        else:
            log.debug("Inserting value {} at {}".format(value, cur))
            if node < cur:
                cur.left = node
            else:
                cur.right = node
            log.debug("After insertion, cur = {}, left = {}, right = {}".format(cur, cur.left, cur.right))

    def delete_node(self, value):
        pass
    
    def find_node(self, value):
        pass

if __name__ == '__main__':
    parser = ArgumentParser()
    logLevel = "DEBUG"
    parser.add_argument('--log')
    args = parser.parse_args()
    logLevel = args.log

    if logLevel != None:
        numLogLevel = getattr(logging, logLevel.upper())
        logging.basicConfig(level=numLogLevel)
        log.setLevel(numLogLevel)    

    tree = BinaryTree()
    for i in range(10):
        tree.insert(random.randint(-100, 100))

    print("Tree: \n", tree)