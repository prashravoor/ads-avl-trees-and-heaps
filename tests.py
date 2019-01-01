import time
from random import randint
from timeit import timeit
import numpy
import matplotlib.pyplot as plt

from avl_tree import AvlTree
from bin_heap import BinaryMinHeap

def get_x_y(measure):
    x = []
    y = []
    for elem in measure:
        if len(elem) > 0:
            x.append(elem[0])
            y.append(elem[1])
    return (x,y)

def plot(measure_tree, measure_heap, title, xlabel, ylabel):
    (x, y) = get_x_y(measure_tree)
    (u, v) = get_x_y(measure_heap)
    axes = plt.gca()
    axes.set_ylim([0, max(y[:] + v[:])])
    plt.scatter(x, y, c='red', label="AVL Tree")
    plt.scatter(u, v, c='blue', label="Binary Heap")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best')
    plt.show()

avl = AvlTree("Tree")
heap = BinaryMinHeap("Heap")

measure_insert_tree = []
measure_insert_heap = []
measure_find_tree = []
measure_find_heap = []
measure_deletemin_tree = []
measure_deletemin_heap = []

num_trials = 10000
# Insert Tree
for i in range(1, num_trials):
    t1 = time.perf_counter()
    avl.insert(randint(1000000000, 9999999999))
    t2 = time.perf_counter()
    measure_insert_tree.append([i, t2-t1])

# Insert Heap
for i in range(1, num_trials):
    t1 = time.perf_counter()
    heap.insert(randint(1000000000, 9999999999))
    t2 = time.perf_counter()
    measure_insert_heap.append([i, t2-t1])

# Find Tree
for i in range(1, int(num_trials/100)):
    avl2 = AvlTree("FindTree")
    for _ in range(1, i*100):
        avl2.insert(randint(1000000000, 9999999999))
    t1 = time.perf_counter()
    try:
        avl2.find(randint(1000000000, 9999999999))
    except ValueError:
        pass
    t2 = time.perf_counter()
    del avl2
    measure_find_tree.append([i*100, t2-t1])

# Find Heap
for i in range(1, int(num_trials/100)):
    heap2 = BinaryMinHeap("FindHeap")
    for _ in range(1, i * 100):
        heap2.insert(randint(1000000000, 9999999999))
    t1 = time.perf_counter()
    try:
        heap2.find(randint(1000000000, 9999999999))
    except ValueError:
        pass
    del heap2
    t2 = time.perf_counter()
    measure_find_heap.append([i*100, t2-t1])

# Delete Min Tree
for i in range(1, num_trials):
    t1 = time.perf_counter()
    node = avl._find_min(avl.root)
    avl.delete(node)
    t2 = time.perf_counter()
    measure_deletemin_tree.append([avl.length(), t2-t1])

# Delete Min Heap
for i in range(1, num_trials):
    t1 = time.perf_counter()
    heap.delete_min()
    t2 = time.perf_counter()
    measure_deletemin_heap.append([heap.length(), t2-t1])

plot(measure_insert_tree, measure_insert_heap, 'Insert Time Comparision', 'Inserted Element number', 'Time (seconds)')
plot(measure_find_tree, measure_find_heap, 'Find Time Comparision', 'Number of Elements in Tree', 'Time (seconds)')
plot(measure_deletemin_tree, measure_deletemin_heap, 'DeleteMin Time Comparision', 'Inserted Element number', 'Time (seconds)')