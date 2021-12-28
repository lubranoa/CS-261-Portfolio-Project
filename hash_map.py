# Course: CS261 - Data Structures
# Student Name: Alexander Lubrano
# Assignment: 5 - Part 1: Hash Map Implementation
# Description: Defines a group of methods for use with a Hash Map ADT that
#              allow users to clear the contents of a hash map, to get a key's
#              associated value from the hash map using that key, to put
#              key/object pairs into and remove them from a hash map, to see if
#              the hash map contains a key, to find the number of empty buckets
#              in the hash map and the map's load factor, to resize the hash
#              map to a specified capacity, and to get an array of all the keys
#              contained in the hash map.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the contents of a hash map.

        Does not change capacity.
        """
        # Iterates through the capacity of the hash map's array and replaces
        # the lists at each position in the array with a new empty linked list
        for i in range(self.capacity):
            self.buckets.set_at_index(i, LinkedList())
        # Resets size of the hash map
        self.size = 0

    def get(self, key: str) -> object:
        """
        Takes a key to search for in a hash map.

        Returns the object associated with the specified key.

        Otherwise, if the key is not in the hash map, returns None.
        """
        # If the hash map is empty
        if self.size == 0:
            return None

        # Finds and holds the index to be checked
        check_index = self.hash_function(key) % self.capacity
        # Finds the bucket to be checked
        check_bucket = self.buckets.get_at_index(check_index)

        # If the bucket is empty, there is no value to return
        if check_bucket.head is None:
            return None

        # Else, if the key of the head of the bucket is the same as the target
        elif check_bucket.head.key == key:
            # Returns the associated object of the key
            return check_bucket.head.value

        # Otherwise
        else:
            # Keeps track of the current link in the linked list
            check_link = check_bucket.head
            # Iterates down the linked list
            while check_link is not None:
                # If the current link's key is the same as the target
                if check_link.key == key:
                    # Returns the associated object of the key
                    return check_link.value
                # Moves pointer down the linked list
                check_link = check_link.next

            # Only executes if the key was not found in the hash map
            return None

    def put(self, key: str, value: object) -> None:
        """
        Takes a key and an object to pair with the key and puts it in a hash
        map.

        If the key is already associated with a paired object, it replaces the
        key's current object with the new object.

        Otherwise, inserts the key/object pair into the hash map.
        """

        # If the hash map's capacity is 0, resizes the hash map
        if self.capacity == 0:
            self.resize_table(1)

        # Finds an index using the remainder of the hashed key divided by the
        # hash map's capacity
        new_index = self.hash_function(key) % self.capacity
        # Finds and hold the correct bucket in the hash map
        put_in_bucket = self.buckets.get_at_index(new_index)

        # If the bucket's linked list is empty, inserts the key/value pair
        # into the bucket's list and increments the hash map's size
        if put_in_bucket.head is None:
            put_in_bucket.insert(key, value)
            self.size += 1

        # Else, if the bucket's head link has the same key as the new key/value
        # pair, replaces the key's old value with the new value
        elif put_in_bucket.head.key == key:
            put_in_bucket.head.value = value

        # Otherwise
        else:
            # Keeps track of the current link
            chain_link = put_in_bucket.head
            # Iterates down the linked list
            while chain_link is not None:
                # If one of the links down the chain has the same key as the
                # new key/value pair, replaces the key's old value with the
                # new value and breaks out of the main function
                if chain_link.key == key:
                    chain_link.value = value
                    return
                # Moves the pointer down the linked list
                chain_link = chain_link.next

            # Only executes if a link with the same key was not found
            # Inserts the new key/value pair at the front of the linked list
            # and increments the hash map's size
            put_in_bucket.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes the specified key and its associated value from the hash map.

        If the specified key is not in the hash map, this does nothing.
        """

        # If the hash map is empty, does nothing
        if self.size == 0:
            return

        # Finds and holds the bucket index to check
        check_index = self.hash_function(key) % self.capacity
        # Finds and holds the bucket's linked list to check
        check_bucket = self.buckets.get_at_index(check_index)

        # If the bucket is empty, does nothing
        if check_bucket.head is None:
            return

        # Calls the linked lists remove method that looks for the key, then
        # either does nothing or removes the link containing the key/value pair
        removal = check_bucket.remove(key)

        # If a link was removed, decrements the size of the hash map
        if removal is True:
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Checks the hash map for a specified key.

        Returns True if the key is in the hash map.
        Otherwise, returns False.
        """
        # If the hash map is empty
        if self.size == 0:
            return False

        # Finds and holds the index to be checked
        check_index = self.hash_function(key) % self.capacity
        # Finds the bucket to be checked
        check_bucket = self.buckets.get_at_index(check_index)

        # If the bucket is empty
        if check_bucket.head is None:
            return False

        # Else, if the key of the head of the bucket is the same as the target
        elif check_bucket.head.key == key:
            return True

        # Otherwise
        else:
            # Keeps track of the current link in the linked list
            check_link = check_bucket.head
            # Iterates down the linked list
            while check_link is not None:
                # If the current link's key is the same as the target
                if check_link.key == key:
                    return True
                # Moves pointer down the linked list
                check_link = check_link.next

            return False

    def empty_buckets(self) -> int:
        """
        Counts the number of empty buckets in a hash map.

        Returns the total count.
        """
        counter = 0

        # Iterates through the capacity of the hash map's array
        for i in range(self.capacity):
            # Keeps track of the current bucket
            bucket = self.buckets.get_at_index(i)

            # If the linked list of each position in the array is empty, the
            # bucket is empty, so this increments the counter
            if bucket.head is None:
                counter += 1

        return counter

    def table_load(self) -> float:
        """
        Calculates the load factor of a hash map, which is the average
        number of elements in each bucket.

        Calculated by dividing the total number of elements in the hash map by
        the hash map's capacity.

        Returns the load factor of the hash map.
        """
        return self.size/self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes a hash table to a new specified capacity.

        If the specified capacity is less than 1, does nothing.

        Otherwise, creates a new hash map of the specified capacity and
        transfers all key/object pairs to the new hash map, rehashing all
        map links along the way.
        """

        # If the new capacity is less than 1, does nothing
        if new_capacity < 1:
            return

        # Creates a new hash map of the specified capacity
        new_map = HashMap(new_capacity, self.hash_function)

        # Iterates down the length of the hash map's array
        for i in range(self.capacity):
            # Keeps track of the current bucket
            bucket = self.buckets.get_at_index(i)

            # If the bucket is empty, continues iteration
            if bucket.head is None:
                continue

            # Otherwise
            else:
                # Keeps track of the links to be transferred
                transfer_link = bucket.head

                # Iterates down the bucket's linked list
                while transfer_link is not None:
                    # Adds the key/value pair of the link to the new hash map
                    # The put() method rehashes key/value pair
                    new_map.put(transfer_link.key, transfer_link.value)
                    # Moves the pointer down the linked list
                    transfer_link = transfer_link.next

        # Sets the main hash map's bucket pointer to the new hash map's buckets
        self.buckets = new_map.buckets
        # Updates the main hash map's capacity to the new capacity
        self.capacity = new_map.capacity

    def get_keys(self) -> DynamicArray:
        """
        Returns a Dynamic Array containing all keys stored in a hash map.
        """
        # Initializes a new array
        key_array = DynamicArray()

        # If the hash map is not empty, there are keys in it
        if self.size > 0:

            # Iterates through the capacity of the hash map's array
            for i in range(self.capacity):
                # Keeps track of the current bucket
                bucket = self.buckets.get_at_index(i)
                # If the bucket is empty, continues to the next iteration
                if bucket.head is None:
                    continue
                # Otherwise
                else:
                    # Keeps track of the current link
                    cur_link = bucket.head
                    # Iterates down the length of the
                    while cur_link is not None:
                        # Appends the current link's key to the array
                        key_array.append(cur_link.key)
                        # Moves the pointer to the next link
                        cur_link = cur_link.next

        return key_array


# BASIC TESTING
if __name__ == "__main__":

    """
    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    """

    """
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    """
    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

