import logging
from argparse import ArgumentParser
import random

log = logging.getLogger()

class TreeNode(object):
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
        self.parent = None
    
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
    def __init__(self, name):
        self.root = None
        self.height = -1
        self.num_nodes = 0
        self.name = name
    
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
        # log.debug("Entered print at node {} at level {}".format(node, level))
        result = ''

        for _ in range(level):
            result += '__' # Add 2 spaces for each level
        result += '(' + str(node) + ")\n"
        # log.debug("Result at level {} is {}".format(level, result))
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

    def insert(self, node):
        log.debug("Inserting node {} into tree {}".format(node, self.name))
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
            log.debug("Inserting value {} at {}".format(node, cur))
            if node < cur:
                cur.left = node
            else:
                cur.right = node
            node.parent = cur
            log.debug("After insertion, cur = {}, left = {}, right = {}".format(cur, cur.left, cur.right))

    def delete_node(self, value):
        pass
    
    def find(self, value):
        log.debug("Finding value {} in tree {}".format(value, self.name))
        node = TreeNode(value)
        cur = self.root
        while cur and not node == cur:
            if node < cur:
                cur = cur.left
            else:
                cur = cur.right

        if not cur or cur != node:
            log.info("The value {} was not found".format(node))
            raise ValueError
        log.info("Found value {} at node.parent = {}, left = {}, right = {}".format(value, cur.parent, cur.left, cur.right))
        return cur

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--log')
    args = parser.parse_args()
    logLevel = args.log

    if logLevel == None:
        logLevel = "INFO"

    numLogLevel = getattr(logging, logLevel.upper())
    logging.basicConfig(level=numLogLevel)
    log.setLevel(numLogLevel)

    tree = BinaryTree("Test")
    for i in range(10):
        tree.insert(TreeNode(random.randint(-100, 100)))

    print("Tree: \n", tree)