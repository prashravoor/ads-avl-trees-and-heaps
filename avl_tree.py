from binary_tree import TreeNode, BinaryTree
import logging
from argparse import ArgumentParser
import random

log = logging.getLogger()

class AvlTreeNode(TreeNode):
    def __init__(self, value):
        TreeNode.__init__(self, value)
        self.balance_factor = 0

    # Trigger recalculation of the balance factor
    def height_difference(self):
        self.balance_factor = 0
        if self.left:
            self.balance_factor -= (self.left.height())
        if self.right:
            self.balance_factor += (self.right.height())

        log.debug("After calculating balance factor: {}".format(self.balance_factor))
        return self.balance_factor

class AvlTree(BinaryTree):
    def __init__(self, name):
        BinaryTree.__init__(self, name)

    def _rotate_with_left_child(self, k2):
        log.debug("Rotating node {} to the right, child {}".format(k2, k2.left))
        k1 = k2.left
        if k1:
            k2.left = k1.right
            if k1.right:
                k1.right.parent = k2
            k1.right = k2
            k1.parent = k2.parent
        k2.parent = k1
        return k1

    def _rotate_with_right_child(self, k1):
        log.debug("Rotating node {} to the left, child {}".format(k1, k1.right))
        k2 = k1.right
        if k2:
            k1.right = k2.left
            if k2.left:
                k2.left.parent = k1
            k2.left = k1
            k2.parent = k1.parent
        k1.parent = k2
        return k2

    def _double_rotate_left_child(self, k3):
        temp = self._rotate_with_right_child(k3.left)
        k3.left = temp
        if temp:
            temp.parent = k3
        return self._rotate_with_left_child(k3)

    def _double_rotate_right_child(self, k1):
        temp = self._rotate_with_left_child(k1.right)
        k1.right = temp
        if temp:
            temp.parent = k1
        return self._rotate_with_right_child(k1)

    def insert(self, node):
        log.debug("Inserting node {}".format(node))
        if type(node) == int:
            node = AvlTreeNode(node)
        self.root = self._insert_recursive(self.root, node)
        self.size += 1

    def _insert_recursive(self, root, key):
        if not root:
            return key
        elif key < root:
            log.debug("Going left at node {}".format(root))
            root.left = self._insert_recursive(root.left, key)
            key.parent = root
            log.debug("Parent of key {} is {}".format(key, root))
        else:
            log.debug("Going right at node {}".format(root))
            root.right = self._insert_recursive(root.right, key)
            key.parent = root
            log.debug("Parent of key {} is {}".format(key, root))
        balance = root.height_difference()
        log.debug("Balance for node {} is {}".format(root, balance))

        # Case 1 - Zig-Zig
        if balance < -1 and key < root.left:
            log.debug("Zig-Zig at node {}".format(root))
            return self._rotate_with_left_child(root)

        # Case 2 - Zag-Zag
        if balance > 1 and key > root.right:
            log.debug("Zag-Zag at node {}".format(root))
            return self._rotate_with_right_child(root)

        # Case 3 - Zig-Zag
        if balance < -1 and key > root.left:
            log.debug("Zig-Zag at node {}".format(root))
            return self._double_rotate_left_child(root)

        # Case 4 - Zag-Zig
        if balance > 1 and key < root.right:
            log.debug("Zag-Zig at node {}".format(root))
            return self._double_rotate_right_child(root)

        return root

    def _delete_recursvive(self, root, key):
        if not root:
            return root

        if key < root:
            log.debug("Going left at node {}".format(root))
            root.left = self._delete_recursvive(root.left, key)
        elif key > root:
            log.debug("Going right at node {}".format(root))
            root.right = self._delete_recursvive(root.right, key)
        else:
            log.debug("Found the node at {}".format(root))
            if root.left is None:
                log.debug("Node has no left child")
                temp = root.right
                root = None
                self.size -= 1
                return temp

            elif root.right is None:
                log.debug("Node has no right child")
                temp = root.left
                root = None
                self.size -= 1
                return temp

            log.debug("Node is an internal node")
            temp = self._find_min(root.right)
            root.value = temp.value
            root.right = self._delete_recursvive(root.right,
                                                 temp)

        balance = root.height_difference()
        log.debug("Height difference of node {} is {}".format(root, balance))

        # Case 1 - Zig-Zig
        if balance < -1 and root.left.height_difference() < 0:
            log.debug("Zig-Zig rotation at node {}".format(root))
            return self._rotate_with_left_child(root)

        # Case 2 - Zag-Zag
        if balance > 1 and root.right.height_difference() >= 0:
            log.debug("Zag-Zag rotation at node {}".format(root))
            return self._rotate_with_right_child(root)

        # Case 3 - Zig-Zag
        if balance < -1 and root.left.height_difference() >= 0:
            log.debug("Zig-Zag rotation at node {}".format(root))
            return self._double_rotate_left_child(root)

        # Case 4 - Zag-Zig
        if balance > 1 and root.right.height_difference() <= 0:
            log.debug("Zag-Zig rotation at node {}".format(root))
            return self._double_rotate_right_child(root)

        return root

    def delete(self, node):
        log.debug('Deleting node {} in Tree {}'.format(node, self.name))
        if type(node) == int:
            node = AvlTreeNode(node)

        self.root = self._delete_recursvive(self.root, node)


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

    tree = AvlTree("Test")
    for i in range(10):
        tree.insert(AvlTreeNode(random.randint(-100, 100)))
        # tree.insert(AvlTreeNode(int(input("Value " + str(i)))))
        # print(tree)

    for i in range(4):
        value = int(input("To Delete: "))
        tree.delete(AvlTreeNode(value))
        print("Tree:\n", tree)
