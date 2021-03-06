import pygubu
import tkinter as tk
from tkinter import filedialog
import csv
import logging
from avl_tree import AvlTree, AvlTreeNode
from binary_tree import BinaryTree, TreeNode
from bin_heap import BinaryMinHeap
from argparse import ArgumentParser
import time
from random import randint
import tkinter.simpledialog

logger = logging.getLogger()


class Application(pygubu.TkApplication):
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        # master.withdraw()
        builder.add_from_file('GUI.ui')
        self.toplevel = builder.get_object('toplevel', master)
        # Connect Delete event to a toplevel window
        master.withdraw()
        self.toplevel.master.protocol("WM_DELETE_WINDOW", self.on_close_window)
        builder.connect_callbacks(self)
        self.trees = {}
        self.trace_mode = False
        self.selected_tree = None

        self.status_text = builder.get_object("statustext")
        self.num_of_nodes = builder.get_object('numnodes')
        self.num_of_levels = builder.get_object('numlevels')
        self.tree_type = builder.get_object('treetype')
        self.selected_tree_obj = builder.get_object('selectedtree')
        self.set_trace = builder.get_object('tracemode')

        self.delete_min_btn = builder.get_object('deletemin')
        self.find_min_btn = builder.get_object('findmin')

        self.clearAll()

    def quit(self, event=None):
        self.toplevel.quit()

    def run(self):
        self.toplevel.mainloop()

    def appendMessage(self, message):
        self.status_text.configure(state="normal")
        self.status_text.insert(tk.END, "{}\n".format(message))
        self.status_text.see(tk.END)
        self.status_text.configure(state="disabled")

    def clearStatus(self):
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", tk.END)
        self.status_text.configure(state="disabled")

    def clearLabels(self):
        self.num_of_nodes['text'] = ''
        self.num_of_levels['text'] = ''
        self.selected_tree_obj['text'] = ''
        self.tree_type['text'] = ''
        self.selected_tree = None
        self.find_min_btn.configure(state='disabled')
        self.delete_min_btn.configure(state='disabled')

    def clearAll(self):
        self.clearStatus()
        self.clearLabels()

    def on_close_window(self, event=None):
        print('On close window')
        # Call destroy on toplevel to finish program
        self.toplevel.master.destroy()

    def setLabels(self):
        logger.debug("Set Labels called")
        if self.selected_tree:
            self.num_of_nodes['text'] = "{}".format(
                self.selected_tree.length())
            self.num_of_levels['text'] = "{}".format(
                self.selected_tree.height())

    def disable_buttons(self):
        btn_state = 'disabled'
        if self.selected_tree and self.get_type(self.selected_tree) == '(Binary Heap)':
            btn_state = 'enabled'

        self.find_min_btn.configure(state=btn_state)
        self.delete_min_btn.configure(state=btn_state)

    def CreateAvlTree(self):
        result = tk.simpledialog.askstring(
            'AVL Tree Name', 'Enter AVL Tree Name', parent=None)
        if not result:
            self.appendMessage("No AVL Tree was Created")
            return None
        try:
            self.CreateTreeNamed(result)
            self.appendMessage(
                "Successfully created AVL Tree with name {}".format(result))
        except ValueError:
            self.appendMessage(
                "Failed to create AVL Tree {}, it already exists!".format(result))

    def CreateMinHeap(self):
        result = tk.simpledialog.askstring(
            'Binary Min Heap Name', 'Enter Binary Heap Name', parent=None)
        if not result:
            self.appendMessage("No Heap was Created")
            return None
        try:
            self.CreateTreeNamed(result, "heap")
            self.appendMessage(
                "Successfully created heap with name {}".format(result))
        except ValueError:
            self.appendMessage(
                "Failed to create heap {}, it already exists!".format(result))

    def CreateTreeNamed(self, name, type="avltree"):
        try:
            self.trees[name]
            logger.error(
                "There is already a tree with name: {0}".format(name))
        except KeyError:
            logger.info("Created new Tree of type {} linked".format(type))
            if "heap" == type:
                self.trees[name] = BinaryMinHeap(name)
            else:
                self.trees[name] = AvlTree(name)
            return
        raise ValueError

    def get_type(self, tree):
        dummyType = AvlTree("dummy")
        logger.debug("Type of tree: {}, {}".format(
            type(tree), type(dummyType)))
        if type(tree) == type(dummyType):
            del dummyType
            return "(AVL Tree)"
        del dummyType
        return "(Binary Heap)"

    def ListNames(self):
        self.appendMessage(
            "Currently Available Trees: {}"
            .format([
                "Name: {}, Type: {}"
                .format(name, self.get_type(self.trees[name])) for name in list(self.trees.keys())
            ]))

    def DeleteTree(self):
        result = tk.simpledialog.askstring(
            'Delete Tree', 'Enter Tree Name', parent=None)
        if not result:
            self.appendMessage("No Tree was Deleted")
            return None
        try:
            tree = self.trees.pop(result)
            self.appendMessage(
                "Successfully deleted Tree with name {} of type {}".format(result, self.get_type(tree)))
            if self.selected_tree.name == result:
                self.clearLabels()
            del tree
        except KeyError:
            self.appendMessage("Tree {} does not exist".format(result))

    def SelectTree(self):
        result = tk.simpledialog.askstring(
            'Select Tree', 'Enter Tree Name', parent=None)
        if not result:
            self.appendMessage("No Tree was Selected")
            return None
        try:
            self.selected_tree = self.trees[result]
            self.appendMessage("Tree {} of type {} selected".format(
                result, self.get_type(self.selected_tree)))
            self.selected_tree_obj['text'] = result
            self.tree_type['text'] = self.get_type(self.selected_tree)
            self.setLabels()
            self.disable_buttons()
        except KeyError:
            self.appendMessage("Tree {} does not exist".format(result))

    def InsertItem(self):
        if not self.selected_tree:
            self.appendMessage("You need to select a Tree first")
            return

        result = tk.simpledialog.askinteger(
            'Insert into Tree', 'Enter Integer Value', parent=None)
        self.appendMessage("Added item {} into Tree {}".format(
            result, self.selected_tree.name))

        if not result:
            self.appendMessage("No item was added")
            return
        result = int(result)

        t1 = time.perf_counter()
        self.selected_tree.insert(result)
        t2 = time.perf_counter()
        self.setLabels()
        self.appendMessage(
            "Item {} inserted in {} seconds".format(result, (t2 - t1)))
        if self.trace_mode:
            self.appendMessage("{}".format(self.selected_tree))

    def GetTree(self):
        if not self.selected_tree:
            self.appendMessage("You need to select a tree first")
            return

        self.appendMessage(
            "Pretty Print Tree {}".format(self.selected_tree.name))
        self.appendMessage(str(self.selected_tree))

    def CreateData(self):
        dialog = self.builder.get_object('createdatadiag')
        self.builder.get_object('ok').configure(command=self.CreateDataFile)
        dialog.run()

    def ReadFromCsvFile(self):
        if not self.selected_tree:
            self.appendMessage("You need to select a Tree first")
            return
        filename = filedialog.askopenfilename(
            initialdir=".", title="Select File to read from")
        if not filename:
            self.appendMessage("No values read")
            return
        elif ".csv" not in filename:
            self.appendMessage("Only CSV files are allowed")
            return

        f = open(filename, "r")
        reader = csv.reader(f, delimiter=",")
        keys = []

        logger.info("Reading all integers from file {0}".format(filename))
        for key in reader:
            keys.append(key)

        if not keys or len(keys) <= 0:
            self.appendMessage("No Keys found in the file")
            return

        keys = keys[0]

        logger.info("Found {0} keys in file {1}".format(len(keys), filename))
        logger.debug("Keys: {}".format(keys))

        t1 = time.perf_counter()
        for key in keys:
            try:
                key = int(key)
                self.selected_tree.insert(int(key))
                if self.trace_mode:
                    self.appendMessage(
                        "Inserted Key {}, the tree is now {}".format(key, self.selected_tree))
            except:
                logger.error(
                    "Found invalid key {} in file, skipping it".format(key))
        self.setLabels()
        t2 = time.perf_counter()
        self.appendMessage(
            "Total time to insert {} keys: {} seconds".format(len(keys), (t2 - t1)))

    def SetTrace(self):
        self.trace_mode = self.builder.get_variable('set_trace').get()
        print("Set Trace Mode to {}".format(self.trace_mode))

    def CreateDataFile(self):
        logger.info("Creating Data File")
        filename = self.builder.get_variable('create_data_filename').get()
        numKeys = self.builder.get_variable('num_keys_val').get()

        if not filename:
            self.appendMessage("Invalid Filename specified")
            return

        if numKeys < 0:
            self.appendMessage("Invalid integer {}".format(numKeys))
            return

        try:
            f = open(filename, "w", newline="")
            writer = csv.writer(f, delimiter=",")

            logger.info("Creating {0} keys in file {1}".format(
                numKeys, filename))
            keys = []
            i = 0
            while i < numKeys:
                keys.append(randint(1000000000, 9999999999))
                #keys.append(randint(-1000, 999))
                i += 1

            writer.writerow(keys)
            self.appendMessage(
                "Wrote {} keys to file {}".format(numKeys, filename))
        except Exception as ex:
            self.appendMessage(
                "An Exception has occurred while creating the data file: {}".format(ex))

        dialog = self.builder.get_object('createdatadiag')
        dialog.close()

    def DeleteNode(self):
        if not self.selected_tree:
            self.appendMessage("You need to select a Tree first")
            return

        result = tk.simpledialog.askinteger(
            'Delete Node in Tree', 'Enter Integer Value', parent=None)

        if not result:
            self.appendMessage("No item was deleted")
            return
        result = int(result)

        t1 = time.perf_counter()
        try:
            self.selected_tree.delete(result)
            t2 = time.perf_counter()
            self.appendMessage("Deleted item {} from Tree {} in {} seconds".format(
                result, self.selected_tree.name, (t2 - t1)))
            if self.trace_mode:
                self.appendMessage("{}".format(self.selected_tree))
            self.setLabels()
        except ValueError:
            self.appendMessage("Item {} was not found in the Tree {}".format(
                result, self.selected_tree.name))

    def FindNode(self):
        if not self.selected_tree:
            self.appendMessage("You need to select a Tree first")
            return

        result = tk.simpledialog.askinteger(
            'Find Node in Tree', 'Enter Integer Value', parent=None)

        if not result:
            self.appendMessage("No item was found")
            return
        result = int(result)

        try:
            t1 = time.perf_counter()
            node = self.selected_tree.find(result)
            self.appendMessage("Item {} was found in the tree {}, Left Node: {}, Right Node: {}, Parent: {}".format(
                result, self.selected_tree.name, node.left, node.right, node.parent))
        except ValueError:
            self.appendMessage("Item {} was not found Tree {}".format(
                result, self.selected_tree.name))
        t2 = time.perf_counter()
        self.appendMessage(
            "Find Node Completed in {} seconds".format((t2 - t1)))

    def DeleteFromFile(self):
        if not self.selected_tree:
            self.appendMessage("You need to select a Tree first")
            return
        filename = filedialog.askopenfilename(
            initialdir=".", title="Select File to read from")
        if not filename:
            self.appendMessage("No values read")
            return
        elif ".csv" not in filename:
            self.appendMessage("Only CSV files are allowed")
            return

        f = open(filename, "r")
        reader = csv.reader(f, delimiter=",")
        keys = []

        logger.info("Reading all integers from file {0}".format(filename))
        for key in reader:
            keys.append(key)

        if not keys or len(keys) <= 0:
            self.appendMessage("No Keys found in the file")
            return

        keys = keys[0]

        logger.info("Found {0} keys in file {1}".format(len(keys), filename))
        logger.debug("Keys: {}".format(keys))

        t1 = time.perf_counter()
        for key in keys:
            try:
                key = int(key)
                self.selected_tree.delete(int(key))
                if self.trace_mode:
                    self.appendMessage(
                        "Deleted Key {}, the Tree is now\n{}".format(key, self.selected_tree))
            except ValueError:
                self.appendMessage(
                    "Key {} was not found in the tree".format(key))
            except:
                logger.error(
                    "Found invalid key {} in file, skipping it".format(key))
        self.setLabels()
        t2 = time.perf_counter()
        self.appendMessage(
            "Total time to delete {} keys: {} seconds".format(len(keys), (t2 - t1)))

    def FindMin(self):
        t1 = time.perf_counter()
        self.appendMessage('The minimum element in the tree is {}'.format(
            self.selected_tree._find_min()))
        t2 = time.perf_counter()
        self.appendMessage(
            'Total time to find minimal element: {} seconds'.format(t2-t1))

    def DeleteMin(self):
        try:
            t1 = time.perf_counter()
            node = self.selected_tree.delete_min()
            self.appendMessage("Found minimum element: {}, Left Node: {}, Right Node: {}".format(
                node, node.left, node.right))
            if self.trace_mode:
                self.appendMessage(
                    "Deleted Key {}, the Tree is now\n{}".format(node, self.selected_tree))
            self.setLabels()
        except ValueError:
            self.appendMessage('Failed to delete min, the heap is empty')

        t2 = time.perf_counter()
        self.appendMessage(
            'Total time to delete minimal element: {} seconds'.format(t2-t1))


if __name__ == '__main__':
    parser = ArgumentParser()
    logLevel = "DEBUG"
    parser.add_argument('--log')
    args = parser.parse_args()
    logLevel = args.log

    if logLevel != None:
        numLogLevel = getattr(logging, logLevel.upper())
        logging.basicConfig(level=numLogLevel)
        logger.setLevel(numLogLevel)

    root = tk.Tk()
    app = Application(root)
    app.run()
