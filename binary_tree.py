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

    def height(self):
        left = 0
        right = 0
        if self.left:
            left = self.left.height()
        if self.right:
            right = self.right.height()
        return 1 + max(left, right)


class BinaryTree(object):
    def __init__(self, name):
        self.root = None
        self.height = -1
        self.num_nodes = 0
        self.name = name
        self.size = 0

    def length(self):
        return self.size

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
            result += '__'  # Add 2 spaces for each level
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
            log.debug("After insertion, cur = {}, left = {}, right = {}".format(
                cur, cur.left, cur.right))
        self.size += 1

    def _find_min(self, startNode):
        cur = startNode
        while cur and cur.left:
            cur = cur.left
        return cur

    # Replace node u by the subtree rooted at v
    def _transplant(self, u, v):
        log.debug(
            "Transplanting node {} with subtree rooted at node {}".format(u, v))
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _delete(self, node):
        log.debug("Deleting node {}".format(node))
        if not node:
            raise ValueError("Invalid node specified for delete")
        if not node.left:
            self._transplant(node, node.right)
        elif not node.right:
            self._transplant(node, node.left)
        else:
            successor = self._find_min(node.right)
            if not successor.parent == node:
                # Swap the successor with it's right child
                self._transplant(successor, successor.right)
                if successor:
                    successor.right = node.right
                    successor.right.parent = successor
            # Replace the node to be deleted with the subtree of the successor
            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
        del node
        self.size -= 1

    def delete(self, value):
        log.debug("Finding value {} in tree {}".format(value, self.name))
        node = self.find(value)
        if not node:
            log.error("The value {} was not found in the tree {}".format(
                value, self.name))
            return
        log.debug("Found node {}, parent is {}".format(node, node.parent))
        self._delete(node)

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
        log.info("Found value {} at node.parent = {}, left = {}, right = {}".format(
            value, cur.parent, cur.left, cur.right))
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
    value = input("To delete: ")
    tree.delete(int(value))
    print("Tree: \n", tree)
