# Course: CS261 - Data Structures
# Student Name: Alexander Lubrano
# Assignment: 5 - Part 3: AVL Tree Implementation
# Description: Defines two methods for use with a self-balancing AVL Tree that
#              allow users to add objects to the tree and remove objects
#              from the tree.


import random


class Stack:
    """
    Class implementing STACK ADT.
    Supported methods are: push, pop, top, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """
    def __init__(self):
        """ Initialize empty stack based on Python list """
        self._data = []

    def push(self, value: object) -> None:
        """ Add new element on top of the stack """
        self._data.append(value)

    def pop(self):
        """ Remove element from top of the stack and return its value """
        return self._data.pop()

    def top(self):
        """ Return value of top element without removing from stack """
        return self._data[-1]

    def is_empty(self):
        """ Return True if the stack is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "STACK: { " + ", ".join(data_str) + " }"


class Queue:
    """
    Class implementing QUEUE ADT.
    Supported methods are: enqueue, dequeue, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """
    def __init__(self):
        """ Initialize empty queue based on Python list """
        self._data = []

    def enqueue(self, value: object) -> None:
        """ Add new element to the end of the queue """
        self._data.append(value)

    def dequeue(self):
        """ Remove element from the beginning of the queue and return its value """
        return self._data.pop(0)

    def is_empty(self):
        """ Return True if the queue is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "QUEUE { " + ", ".join(data_str) + " }"


class TreeNode:
    """
    AVL Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    def __str__(self):
        return 'AVL Node: {}'.format(self.value)


class AVL:
    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.root = None

        # populate AVL with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of AVL in human-readable form using pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self.root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, cur, values):
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if cur:
            values.append(str(cur.value))
            self._str_helper(cur.left, values)
            self._str_helper(cur.right, values)

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        s = Stack()
        s.push(self.root)
        while not s.is_empty():
            node = s.pop()
            if node:
                # check for correct height (relative to children)
                l = node.left.height if node.left else -1
                r = node.right.height if node.right else -1
                if node.height != 1 + max(l, r):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self.root:
                        return False
                s.push(node.right)
                s.push(node.left)
        return True

    # -----------------------------------------------------------------------

    def _contains(self, value):
        """
        Used internally to check for duplicate values.

        Returns True if target value is found.
        Returns False otherwise.
        """
        # Keeps track of a current node being processed
        cur = self.root

        # Iterates until the end of the tree if no object matches the target
        while cur is not None:
            # Returns True if the object was found in the tree
            if cur.value == value:
                return True
            elif value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        # Only executes if the target was not found in the tree
        return False

    def _height(self, node):
        """
        Used internally to get the height of a node in the tree.

        Returns the height of the specified node.
        """
        # If the node is empty, returns -1
        if node is None:
            return -1
        # Otherwise, returns the height of the node
        return node.height

    def _update_height(self, node):
        """
        Used internally to update the height of a node in the tree.
        """
        # The height of the node is the max of its longest subtree plus itself
        node.height = max(self._height(node.left),
                          self._height(node.right)) + 1

    def _rotate_right(self, current):
        """
        Used internally to rotate a node to the right of its left child.

        Returns the rotated subtree.
        """
        # Holds the left child of the rotation node
        left_child = current.left
        # Sets the left child of the rotation node as its left child's right
        # child (either None or a subtree)
        current.left = left_child.right

        # If the new left child of the rotated node is not None, sets the new
        # child's parent to the rotation node
        if current.left is not None:
            current.left.parent = current

        # Sets the old left child's right child as the rotation node
        left_child.right = current
        # Sets the rotation node's parent as the old left child
        current.parent = left_child

        # Updates the height of both nodes moved
        self._update_height(current)
        self._update_height(left_child)

        return left_child

    def _rotate_left(self, current):
        """
        Used internally to rotate a node to the left of its right child.

        Returns the rotated subtree.
        """
        # Holds the right child of the rotation node
        right_child = current.right
        # Sets the right child of the rotation node as its right child's left
        # child (either None or a subtree)
        current.right = right_child.left

        # If the new right child of the rotated node is not None, sets the new
        # child's parent as the rotation node
        if current.right is not None:
            current.right.parent = current

        # Sets the old right child's left child as the rotation node
        right_child.left = current
        # Sets the rotation node's parent as the old right child
        current.parent = right_child

        # Updates the height of both nodes moved
        self._update_height(current)
        self._update_height(right_child)
        return right_child

    def _balance_factor(self, node):
        """
        Used internally to find the balance factor of a node.

        Returns the balance factor.
        """
        # Initializes these at 0 because if both of the node's children are
        # None, the height balance factor will be 0.
        right_height = 0
        left_height = 0

        # Finds the height of each of the children
        if node.right is not None:
            right_height = node.right.height + 1
        if node.left is not None:
            left_height = node.left.height + 1

        # Returns the balance factor as the difference between the height of
        # the right and left child heights
        return right_height - left_height

    def _balance(self, node):
        """
        Used internally to check for re-balancing.

        If necessary, re-balances the AVL Tree.

        Otherwise, if no re-balancing is needed, updates the heights from the
        new node.
        """

        # Holds the original parent of the node being rotated
        original_parent = node.parent
        # Holds the balance factor of the node to be rotated
        balance_factor = self._balance_factor(node)

        # If there is a left imbalance
        if balance_factor < -1:

            # If there is a left imbalance but its left child has a right
            # imbalance (Left-right imbalance)
            if self._balance_factor(node.left) > 0:
                # Rotates the left child node to the left
                node.left = self._rotate_left(node.left)
                node.left.parent = node

            # Calls for a right rotation and holds the resulting new subtree
            new_subtree_root = self._rotate_right(node)

            # Sets the new subtree's parent as the original parent of the
            # rotated node
            new_subtree_root.parent = original_parent

            # If the original parent is None, then the new subtree root node
            # becomes the new root node of the tree
            if original_parent is None:
                self.root = new_subtree_root

            # Else, if the original parent is a node, sets the correct child
            # of the original parent as the new subtree
            elif original_parent.left.value == node.value:
                original_parent.left = new_subtree_root
            elif original_parent.right.value == node.value:
                original_parent.right = new_subtree_root

        # If there is a right imbalance
        elif balance_factor > 1:

            # If the is a right imbalance but its right child has a left
            # imbalance (Right-left imbalance)
            if self._balance_factor(node.right) < 0:
                # Rotates the right child node to the right
                node.right = self._rotate_right(node.right)
                node.right.parent = node

            # Calls for a left rotation and holds the resulting new subtree
            new_subtree_root = self._rotate_left(node)

            # Sets the new subtree's parent as the original parent of the
            # rotated node
            new_subtree_root.parent = original_parent

            # If the original parent is None, then the new subtree root node
            # becomes the new root node of the tree
            if original_parent is None:
                self.root = new_subtree_root

            # Else, if the original parent is a node, sets the correct child
            # of the original parent as the new subtree
            elif original_parent.left.value == node.value:
                original_parent.left = new_subtree_root
            elif original_parent.right.value == node.value:
                original_parent.right = new_subtree_root

        # Otherwise, if there are no imbalances large enough to necessitate a
        # re-balancing, updates the height starting with the node that was
        # passed to this method
        else:
            self._update_height(node)

    def add(self, value: object) -> None:
        """
        Takes an object to add to an AVL Tree.

        Does nothing if the object is a duplicate of one already in the tree.

        Adds it to its correct position in the tree and re-balances the tree
        if necessary.
        """

        # If the object is a duplicate, does nothing
        if self._contains(value) is True:
            return

        # Instantiates a new node with the new object
        new_node = TreeNode(value)

        # If the root node is empty, sets the new node as the root node
        if self.root is None:
            self.root = new_node

        # Otherwise, adds the new node in its correct spot in the tree
        else:
            # Keeps track of the current node
            cur = self.root
            # Keeps track of the current node's parent node
            cur_parent = None

            # Iterates until the correct spot is found in the tree
            while cur is not None:
                # Updates the parent node
                cur_parent = cur
                # If the object being added is less than the current node,
                # advances current to its own left child
                if value < cur.value:
                    cur = cur.left
                # Otherwise if the object being added is greater than or equal
                # to the current node, advances current to its own right child
                else:
                    cur = cur.right

            # If the object being added is less than its parent's object, sets
            # the new node as the left child of its new parent and sets the new
            # node's parent as the current parent
            if value < cur_parent.value:
                cur_parent.left = new_node
                new_node.parent = cur_parent
            # Otherwise, sets the new node as the right child of its new parent
            # and sets the new node's parent as the current parent
            else:
                cur_parent.right = new_node
                new_node.parent = cur_parent

            # Updates the heights of the nodes up the tree from the new node
            cur_parent = new_node.parent
            while cur_parent is not None:
                self._update_height(cur_parent)
                cur_parent = cur_parent.parent

            # Checks at each level from the new node upwards, if the tree
            # needs re-balancing by calling the parents of each node starting
            # from the new node
            balance_parent = new_node.parent
            while balance_parent is not None:
                self._balance(balance_parent)
                balance_parent = balance_parent.parent

    def remove(self, value: object) -> bool:
        """
        Takes an object to remove from the AVL Tree.

        Removes the object if found in the tree and returns True.
        Otherwise, if not found, returns False.
        """

        # If the root is empty, there is nothing to remove
        if self.root is None:
            return False

        # If the object is not in the tree, returns False
        if self._contains(value) is False:
            return False

        # Keep track of the node being removed and its parent
        removing = self.root
        parent = None

        # Iterates until the target object is found
        while removing is not None:
            # When the value is found, breaks out of iteration to preserve the
            # removing and parent pointers
            if removing.value == value:
                break
            elif value < removing.value:
                parent = removing
                removing = removing.left
            else:
                parent = removing
                removing = removing.right

        # Keeps track of which nodes to update the height and balance from
        update_height = parent
        balance_parent = parent

        # If the removal node has no children
        if removing.left is None and removing.right is None:
            # If the removal node is the root node
            if removing.parent is None:
                self.root = None
            # Else, if the removal node is the left child of its parent
            elif removing.value < parent.value:
                parent.left = None
            # Else, if the removal node is the right child of its parent
            else:
                parent.right = None

        # Else, if the removal node only has a right child
        elif removing.left is None:
            # If the removal node is the root node
            if removing.parent is None:
                self.root = removing.right
                self.root.parent = None
            # Else, if the removal node is the left child of its parent
            elif removing.value < parent.value:
                parent.left = removing.right
                parent.left.parent = parent
            # Else, if the removal node is the right child of its parent
            else:
                parent.right = removing.right
                parent.right.parent = parent

        # Else, if the removal node only has a left child
        elif removing.right is None:
            # If the removal node is the root node
            if removing.parent is None:
                self.root = removing.left
                self.root.parent = None
            # Else, if the removal node is the left child of its parent
            elif removing.value < parent.value:
                parent.left = removing.left
                parent.left.parent = parent
            # Else, if the removal node is the right child of its parent
            else:
                parent.right = removing.left
                parent.right.parent = parent

        # Else, if the removal node has two children
        else:

            # Keep track of the in-order successor and its parent
            successor = removing.right
            successor_parent = removing.right

            # Iterates to the in-order successor
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            # If the in-order successor is the removal node's right child
            if removing.right.left is None:
                successor.left = removing.left
                successor.left.parent = successor
                successor.parent = removing.parent
                # If removal node is the root node
                if removing.parent is None:
                    self.root = successor
                # Else if the removal node is its parent's left child
                elif removing.value < parent.value:
                    parent.left = successor
                # Else, if the removal node is the right child of its parent
                else:
                    parent.right = successor

                # Updates the two pointers for updating height and balancing
                update_height = successor_parent
                balance_parent = successor_parent

            # Otherwise, if the in-order successor is not the removal node's
            # right child
            else:
                successor.left = removing.left
                successor.left.parent = successor
                successor_parent.left = successor.right
                # If the successor's parent's left node now holds the
                # successor's right child
                if successor_parent.left is not None:
                    successor_parent.left.parent = successor_parent
                successor.right = removing.right
                successor.right.parent = successor
                successor.parent = removing.parent
                # If removal node is the root node
                if removing.parent is None:
                    self.root = successor
                # Else if the removal node is its parent's left child
                elif removing.value < parent.value:
                    parent.left = successor
                # Else, if the removal node is the right child of its parent
                else:
                    parent.right = successor

                # Updates the pointers for updating height and balancing
                update_height = successor_parent
                balance_parent = successor_parent

        # Updates the height starting from the lowest node modified, moving up
        # its parents in the tree until it reaches the root node
        while update_height is not None:
            self._update_height(update_height)
            update_height = update_height.parent

        # Balances the tree starting from the lowest parent node modified,
        # moving up its parents in the tree until it reaches the root node
        while balance_parent is not None:
            self._balance(balance_parent)
            balance_parent = balance_parent.parent

        return True


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        avl = AVL(case)
        print(avl)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        avl = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', avl)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL()
        for value in case:
            avl.add(value)
        if not avl.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    avl = AVL(case)
    for del_value in case:
        print('INPUT  :', avl, del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    avl = AVL(case)
    for _ in case[:-2]:
        print('INPUT  :', avl, avl.root.value)
        avl.remove(avl.root.value)
        print('RESULT :', avl)
        if not avl.is_valid_avl():
            print("^^^INVALID AVL STRUCTURE^^^")

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL(case)
        for value in case[::2]:
            avl.remove(value)
        if not avl.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')
