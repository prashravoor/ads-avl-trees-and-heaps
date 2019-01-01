# ads-avl-trees-and-heaps
ADS Assignment 2 - Implementation of AVL Trees and Heaps

## Running the application
Install python 3.6+, and run `python app.py` to open the GUI for the application.

## Supported Operations
Here **Tree** refers to either a Heap or an AVL Tree<br>
* Create AVL Tree
* Create Heap
* Delete Tree
* Insert Node
* Delete Node
* Find Node
* Show Tree
* Insert Nodes from File
* Delete Nodes from File
* Find Min (Heap only)
* Delete Min (Heap Only)

## Implementation
Both the AVL Tree and the Binary Min Heap derive from the "BinaryTree" base class. <br>
Both use a linked list based implementation for the nodes (TreeNode), so traversal / operations like find, delete, insert etc. are performed on the base class interface.
<br>
