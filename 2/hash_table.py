import random, sys, time

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################
NONEED = -1
NUM_CHAR = 131
# Hash function.
#
# |key|: string
# Return value: a hash value
# interpret string as an expression of integer in NUM_CHAR-ary system
def calculate_hash(key):#10桁131種類(素数)を想定
    assert type(key) == str
    hash = 0
    for (i,char) in enumerate(key):
        hash +=  ord(char)*pow(NUM_CHAR,i)
    return hash
    # return int(key)#10種類の数値のみが存在する場合



# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, key, value,next=None):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next

# An item object that represents one key - value - other_prperty pair in the hash table.
# To be used specifically in the hash table

class ItemInHash(Item):
    # |other_prop|:to be used to hold the pointer of the corresponding item in linked list
    def __init__(self, key, value,next = None, other_prop = None):
        super().__init__(key, value,next)
        self.other_prop = other_prop

# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
    def __init__(self,bucket_size = 97):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = bucket_size
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value,other_prop = None, under_reconstruction = False):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = ItemInHash(key, value, next = self.buckets[bucket_index],other_prop= other_prop)#古い連結リストが，新しいアイテムにぶら下がる
        self.buckets[bucket_index] = new_item
        if not under_reconstruction:#under_reconstructionの場合はitem_countがすでにupdateされている
            self.item_count += 1
            self.reconstruct_if_need()
        return True

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key,get_other_prop = False):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                if get_other_prop:
                    return (item.value, item.other_prop,True)
                else:
                    return (item.value, True)
            item = item.next
        if get_other_prop:
            return (None,None,False)
        else:
            return (None, False)

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str
        #------------------------#
        # Write your code here!  #
        bucket_index = calculate_hash(key) % self.bucket_size  
        item = self.buckets[bucket_index]
        pre_item = None
        while item:
            if item.key  == key:
                if pre_item == None:
                    self.buckets[bucket_index] = item.next
                else:
                    pre_item.next = item.next 
                self.item_count -= 1
                self.reconstruct_if_need()
                return True 
            pre_item = item 
            item = item.next
        return False
        #------------------------#

    #print all pairs of bucket-key-value in hash table for the sake of debugging
    def print_table(self):
        for (i,bucket) in enumerate(self.buckets):
            item = bucket
            while item:
                print("bucket:",i,item.key,item.value)
                item = item.next  
        print("printed hashtable")

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert (self.bucket_size < 100 or self.item_count >= self.bucket_size * 0.3)
    
    #reconstruct hash table according to the result of design_new_table function    
    def reconstruct_if_need(self): 
        new_bucket_size = self.design_new_table()
        if  new_bucket_size != NONEED:
            print("under_reconstruction_to" ,new_bucket_size)
            new_table = HashTable(new_bucket_size)
            new_table.item_count =  self.item_count
            for cur_bucket in self.buckets:
                item = cur_bucket 
                while item:
                    new_table.put(item.key,item.value,item.other_prop, under_reconstruction=True)
                    item = item.next
            self.bucket_size = new_bucket_size 
            self.buckets = new_table.buckets 
            self.item_count = new_table.item_count
    
    # if the hash_table is too sparse or too crowded, return new bucket_size
    # else return NONEED flag
    def design_new_table(self):
        new_bucket_size = NONEED
        if self.item_count > self.bucket_size*0.7:
            new_bucket_size = (self.bucket_size)*2+1
        elif self.item_count <  self.bucket_size*0.3:
            new_bucket_size = (self.bucket_size//4)*2+1
        return  new_bucket_size
        


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1
    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4
    
    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6
    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()
