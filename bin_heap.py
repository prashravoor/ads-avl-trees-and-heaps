from binary_tree import BinaryTree, TreeNode
import logging
from argparse import ArgumentParser
import random
log = logging.getLogger()

class BinaryMinHeap(BinaryTree):
    def __init__(self, name):
        BinaryTree.__init__(self, name)

    def _heapify(self, root):
        while root and root.parent:
            if root < root.parent:
                # Swap
                (root.parent.value, root.value) = (
                    root.value, root.parent.value)
            root = root.parent

    def _insert(self, root, node):
        if not root:
            return node

        queue = list([root])

        while len(queue):
            cur = queue.pop(0)
            # Insert node in first open position while doing a BFS
            if not cur.left:
                log.debug("Found empty position at left of node {}".format(cur))
                cur.left = node
                node.parent = cur
                break
            elif not cur.right:
                log.debug("Found empty position at right of node {}".format(cur))
                cur.right = node
                node.parent = cur
                break
            else:
                queue.append(cur.left)
                queue.append(cur.right)

        log.debug("Heapifying from node {}".format(node))
        self._heapify(node)
        self.size += 1

    def insert(self, value):
        log.debug("Inserting value {} into Binary Heap {}".format(
            value, self.name))
        if type(value) == int:
            value = TreeNode(value)
        if not self.root:
            self.root = value
            self.size += 1
            return
        self._insert(self.root, value)

    def find(self, node):
        log.debug("Finding value {} into Binary Heap {}".format(node, self.name))
        if type(node) == int:
            node = TreeNode(node)
        if not self.root:
            raise ValueError

        # Entire tree needs to be searched, try a BFS to find it
        queue = list([self.root])
        while len(queue):
            cur = queue.pop(0)
            if cur == node:
                log.debug("Value found!")
                return cur
            if cur.left:
                queue.append(cur.left)
            if cur.right:
                queue.append(cur.right)
        raise ValueError

    def _find_min(self):
        log.debug("Finding min element in heap {}".format(self.name))
        return self.root

    def _find_last(self):
        # To find the last element, do a BFS. The last element popped from the queue is the last element in the heap
        if not self.root:
            return None

        queue = list([self.root])
        last = None
        while len(queue):
            last = queue.pop(0)
            if last.left:
                queue.append(last.left)
            if last.right:
                queue.append(last.right)

        log.debug("The last element is {}".format(last))
        return last

    def delete(self, node):
        log.debug("Deleting node {} in Heap {}".format(node, self.name))
        if type(node) == int:
            node = TreeNode(node)

        found = self.find(node)
        last = self._find_last()
        (found.value, last.value) = (last.value, found.value)

        if not last.parent:
            # Root is the only element
            log.debug("Deleting the root element")
            del last
            self.root = None
            return

        # Reset pointers of last
        if last == last.parent.left:
            log.debug("The last node is it's parent's left child")
            last.parent.left = None
        else:
            log.debug("The last node is it's parent's right child")
            last.parent.right = None
        del last
        self.size -= 1
        if not found.parent:
            self.root = found
        self._heapify_down(found)

    def _heapify_down(self, node):
        cur = node
        while cur and (cur.left or cur.right):
            if cur == min(cur, cur.left, cur.right):
                break

            if not cur.right:
                # Only left exists
                (cur.value, cur.left.value) = (cur.left.value, cur.value)
                cur = cur.left
            elif not cur.left:
                # Only right exists
                (cur.value, cur.right.value) = (cur.right.value, cur.value)
                cur = cur.right
            else:
                if cur.left < cur.right:
                    (cur.value, cur.left.value) = (cur.left.value, cur.value)
                    cur = cur.left
                else:
                    (cur.value, cur.right.value) = (cur.right.value, cur.value)
                    cur = cur.right
    
    def delete_min(self):
        log.debug("ExtractMin for heap {}".format(self.name))
        if not self.root:
            raise ValueError
        node = TreeNode(self._find_min().value)
        self.delete(node)
        return node

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

    heap = BinaryMinHeap("Test")
    for _ in range(10):
        heap.insert(TreeNode(random.randint(-100, 100)))
        print(heap)
    """
    for i in range(2):
        value = int(input("To Find: "))
        try:
            heap.find(TreeNode(value))
            print("Tree:\n", heap)
        except ValueError:
            print("Not Found!")
    """

    for i in range(4):
        #value = int(input("To Delete: "))
        try:
            heap.delete_min()
            print("Tree:\n", heap)
        except ValueError:
            print("Not Found!")