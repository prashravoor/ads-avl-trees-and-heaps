from binary_tree import TreeNode, BinaryTree
import logging
from argparse import ArgumentParser
import random

log = logging.getLogger()


class AvlTreeNode(TreeNode):
    def __init__(self, value):
        TreeNode.__init__(self, value)
        self.balance_factor = 0
    
    def __repr__(self):
        result = "({}, {}, Parent-".format(self.value, self.balance_factor)
        if not self.parent:
            result += "None)"
        else:
            result += str(self.parent.value) + ")"
        return result
    
    def height(self):
        left = 0
        right = 0 
        if self.left:
            left = self.left.height()
        if self.right:
            right = self.right.height()
        return 1 + max(left, right)

    # Trigger recalculation of the balance factor
    def height_difference(self):
        self.balance_factor = 0
        if self.left:
            self.balance_factor -= (self.left.height())
        if self.right:
            self.balance_factor += (self.right.height())
    
        log.debug("After calculating balance factor: {}".format(self))
        return self.balance_factor

class AvlTree(BinaryTree):
    def __init__(self, name):
        BinaryTree.__init__(self, name)

    def _rotate_with_left_child(self, k2):
        log.debug("Rotating node {} to the right".format(k2))
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
        self._rotate_with_right_child(k3.left)
        return self._rotate_with_left_child(k3)

    def _double_rotate_right_child(self, k1):
        self._rotate_with_left_child(k1.right)
        return self._rotate_with_right_child(k1)

    def _insert_recursive(self, node, cur):
        if not cur:
            # Node is the root
            self.root = node
            return
        if node < cur:
            if cur.left:
                log.debug("Going left at node {}".format(cur))
                self._insert_recursive(node, cur.left)
            else:
                log.debug("Inserting left of node {}".format(cur))
                cur.left = node
                node.parent = cur
            log.debug("Before Rotate: \n{}".format(self))
            # Rotate the tree, if needed
            if cur.height_difference() < -1:
                log.debug("Left Subtree - Current node: {}".format(cur))
                parent = cur.parent
                if not cur.left or cur.left > node:
                    # Zig-Zig rotation
                    temp = self._rotate_with_left_child(cur)
                    log.debug("After Zig-Zig: {}, {}, {}".format(temp, cur, parent))
                    if not parent:
                        # Modify root
                        self.root = temp
                    else:
                        parent.left = temp
                        temp.parent = parent
                else:
                    # Zig-Zag rotation
                    temp = self._double_rotate_left_child(cur)
                    log.debug("After Zig-Zag: {}, {}".format(temp, cur))
                    if not parent:
                        # Modify root
                        self.root = temp
                    else:
                        parent.right = temp
                        temp.parent = parent
                # cur.height_difference()
        else:
            if cur.right:
                log.debug("Going right at node {}".format(cur))
                self._insert_recursive(node, cur.right)
            else:
                log.debug("Inserting right of node {}".format(cur))
                cur.right = node
                node.parent = cur

            log.debug("Before Rotate: \n{}".format(self))
            if cur.height_difference() > 1:
                log.debug("Right Subtree - Current node: {}, Inserted node: {}".format(cur, node))
                parent = cur.parent
                if cur.right < node:
                    # Zag-Zag rotation
                    temp = self._rotate_with_right_child(cur)
                    log.debug("After Zag-Zag: {}, {}".format(temp, cur))
                    if not parent:
                        # Modify root
                        self.root = temp
                    else:
                        parent.right = temp
                        temp.parent = parent
                else:
                    # Zag-Zig rotation
                    temp = self._double_rotate_right_child(cur)
                    log.debug("After Zag-Zig: {}, {}".format(temp, cur))
                    if not parent:
                        # Modify root
                        self.root = temp
                    else:
                        parent.left = temp
                        temp.parent = parent

    def insert(self, node):
        """
        log.debug("Inserting node {} into tree".format(node))
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
                cur.balance_factor -= 1
            else:
                cur.right = node
                cur.balance_factor += 1
            node.parent = cur
            log.debug("After insertion, cur = {}, left = {}, right = {}".format(
                cur, cur.left, cur.right))
        """
        self._insert_recursive(node, self.root)


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
        # tree.insert(AvlTreeNode(random.randint(-100, 100)))
        tree.insert(AvlTreeNode(input("Enter node " + str(i))))
        print(tree)

    print("Tree: \n", tree)
