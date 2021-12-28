# Course: CS261 - Data Structures
# Student Name: Alexander Lubrano
# Assignment: 5 - Part 2: Min Heap Implementation
# Description: Defines a group of methods for use in a Min Heap ADT that allow
#              users to add objects to the heap, to get the minimum object in
#              it, to remove objects from it, and to build a new heap from a
#              Dynamic Array of objects in any order.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        Takes an object to insert into the Min Heap array.

        Places it in the correct spot in the heap, retaining the heap property
        of the minimum object being at the beginning of the heap and every
        following object is greater than or equal to the minimum.
        """
        # Appends the node to the end of the heap
        self.heap.append(node)

        # Only runs this block if the heap has more than 1 object in it
        if self.heap.length() > 1:

            # Keeps track of the new object's position in the heap
            new_node_pos = self.heap.length() - 1
            # Keeps track of the new object's current parent
            parent = self.heap.get_at_index(int((new_node_pos - 1) / 2))

            # Iterates until the new object is greater than its current parent
            # or the new node has become the minimum in the heap
            while node <= parent and new_node_pos > 0:

                # Swaps the new node's and parent's positions in the heap
                self.heap.swap(new_node_pos, int((new_node_pos - 1) / 2))
                # Updates the new node's position to the old parent's position
                new_node_pos = int((new_node_pos - 1) / 2)
                # Updates the parent using the new position of the new node
                parent = self.heap.get_at_index(int((new_node_pos - 1) / 2))

    def get_min(self) -> object:
        """
        Returns the minimum object in the heap.
        """
        # Cannot return anything if the heap is empty
        if self.is_empty():
            raise MinHeapException

        # Returns the first value of the heap since that is always the
        # minimum object
        return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Removes the minimum object in the heap and updates the heap's new
        minimum object.

        Returns the removed minimum object.
        """

        # Cannot remove something from an empty heap
        if self.is_empty() is True:
            raise MinHeapException

        # Holds the object of the node being removed
        minimum = self.heap.get_at_index(0)

        # If the heap only has one object, clears the heap
        if self.heap.length() == 1:
            self.heap = DynamicArray()

        # Otherwise, if it has more than one object
        else:

            # Pops the last object off the end of the heap
            last_node = self.heap.pop()
            # Places the last object in the first index position of the heap
            self.heap.set_at_index(0, last_node)

            # Keeps track of the last_node's index position
            last_node_pos = 0
            # Keeps track of the last node's current left and right
            # children indices
            child_pos1 = 2 * last_node_pos + 1
            child_pos2 = 2 * last_node_pos + 2

            # Special case where the nodes after removing a 3rd node would not
            # come out correctly with my implementation
            if self.heap.length() == 2:

                # If the last node is greater than its only child, swaps them
                if last_node > self.heap.get_at_index(child_pos1):
                    self.heap.swap(0, 1)
                    return minimum
                # Otherwise, keeps them in the same order
                else:
                    return minimum

            heap_length = self.heap.length()

            # Iterates until the index of the left or right child goes beyond
            # the bounds of the heap indices
            while child_pos1 < self.heap.length():

                # If the left child position is the last in the heap and its
                # value is less than the last node's, swaps their positions
                if child_pos1 == self.heap.length() - 1 and \
                        self.heap.get_at_index(child_pos1) < last_node:
                    self.heap.swap(last_node_pos, child_pos1)

                # Else, if the left child position is the last in the heap but
                # its value is greater than or equal to the last node's value,
                # breaks out of iteration
                elif child_pos1 == self.heap.length() - 1 and \
                        self.heap.get_at_index(child_pos1) >= last_node:
                    break

                # If the both child values are greater than or equal to the
                # last node's value, the last node cannot move further
                elif self.heap.get_at_index(child_pos1) >= last_node and \
                        self.heap.get_at_index(child_pos2) >= last_node:
                    break

                # If the left child is less than or equal to the right child
                elif self.heap.get_at_index(child_pos1) <= \
                        self.heap.get_at_index(child_pos2):

                    # Swaps the last node and its left child in the heap
                    self.heap.swap(last_node_pos, child_pos1)
                    # Updates the current position of the last node and the
                    # positions of its new left and right children
                    last_node_pos = child_pos1
                    child_pos1 = 2 * last_node_pos + 1
                    child_pos2 = 2 * last_node_pos + 2

                # Otherwise, if the right child is less than the left child
                else:
                    # Swaps the last node and its right child in the heap
                    self.heap.swap(last_node_pos, child_pos2)
                    # Updates the current position of the last node and the
                    # positions of its new left and right children
                    last_node_pos = child_pos2
                    child_pos1 = 2 * last_node_pos + 1
                    child_pos2 = 2 * last_node_pos + 2

        return minimum

    def _heapify(self, array, index):
        """
        Used internally to as a helper method for the build_heap method.

        Takes the array to be "heapified" and the index of the first non-leaf
        node of the heap.

        Rearranges the nodes in the array into a proper min heap.
        """
        # Citation: followed similar structure as on the page, "Building Heap
        # from Array" of GeeksforGeeks.org
        # URL: https://www.geeksforgeeks.org/building-heap-from-array/

        # Keeps track of the index of the current minimum value
        cur_min = index
        # Next variables hold the indices of the left and right children
        left_index = (2 * index) + 1
        right_index = (2 * index) + 2

        # If the left index is not out of bounds and the left child's object
        # is less than its parent's object
        if left_index < array.length() and \
                array.get_at_index(left_index) < array.get_at_index(cur_min):
            cur_min = left_index

        # If the right index is not out of bounds and the right child's object
        # is less than its parent's object
        if right_index < array.length() and \
                array.get_at_index(right_index) < array.get_at_index(cur_min):
            cur_min = right_index

        # If the current minimum changed from its initial value
        if cur_min != index:
            # Swaps the two objects at the two indices
            array.swap(index, cur_min)
            # Recursively "heapifies" the modified subtree
            self._heapify(array, cur_min)

    def build_heap(self, da: DynamicArray) -> None:
        """
        Takes a dynamic array with objects in any order.

        Builds a proper Min Heap ADT using its objects.

        The current content of the original heap is lost.
        """
        # Citation: used similar structure from the same article as the
        # heapify method implemented above

        # Finds the index of the first non-leaf node in the array
        start_index = int(da.length() / 2) - 1

        # Iterates down the indices to heapify each non-leaf node in the array
        # thereby turning the array into a proper heap
        for i in range(start_index, -1, -1):
            self._heapify(da, i)

        # Creates a new heap array to become the main heap and copies the
        # objects from the heapified array
        new_heap = DynamicArray()
        for i in range(da.length()):
            new_heap.append(da.get_at_index(i))

        # Sets the main heap's data as the new heap's
        self.heap = new_heap


# BASIC TESTING
if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([211, 214, 220, 221, 222, 233, 226, 223, 224, 242, 266, 364, 256, 264, 320, 228, 375, 281, 238, 285, 283, 368, 285, 371, 387, 282, 268, 385, 270, 358, 325, 283, 234, 390, 447, 311, 455, 343, 353, 304, 753, 545, 295, 390, 436, 363, 350, 378, 395, 459, 476, 588, 343, 305, 352, 506, 489, 380, 439, 392, 412, 334, 345, 331, 449, 298, 247, 416, 536, 464, 573, 483, 331, 557, 562, 528, 702, 365, 436, 333, 389, 827, 795, 648, 729, 640, 475, 520, 517, 487, 576, 636, 486, 423, 458, 448, 569, 457, 646, 536, 809, 528, 519, 835, 651, 528, 412, 624, 519, 573, 450, 556, 753, 670, 745, 458, 673, 680, 800, 707, 647, 522, 494, 414, 421, 354, 394, 484, 537, 548, 523, 688, 478, 276, 643, 758, 512, 769, 813, 628, 931, 600, 590, 508, 710, 640, 495, 631, 795, 971, 701, 735, 630, 824, 822, 445, 894, 580, 626, 735, 974, 653, 707, 883, 882, 972, 799, 944, 672, 885, 978, 952, 878, 566, 488, 585, 745, 722, 647, 578, 534, 646, 965, 821, 997, 502, 526, 616, 746, 979, 949, 915, 885, 618, 589, 724, 492, 660, 811, 913, 558, 829, 929, 895, 913, 602, 919, 887, 979, 731, 826, 658, 605, 968, 499, 904, 778, 930, 727, 829, 720, 617, 623, 708, 556, 909, 859, 861, 713, 848, 948, 967, 726, 930, 954, 997, 717, 831, 906, 767, 816, 899, 857, 837, 559, 860, 870, 718, 786, 453, 702, 607, 914, 938, 902, 703, 627, 990, 674, 935, 773, 828, 890, 786, 976, 788, 964, 283, 674])
    # while not h.is_empty():
    print(h, end=' ')
    print(h.remove_min())
    print(h)

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)
