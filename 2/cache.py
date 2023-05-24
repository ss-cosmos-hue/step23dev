import sys
from hash_table import HashTable,Item
# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!

# An item object that represents one key - value pair in the linked list.
# To be used specifically in linked list
class ItemInLinked(Item):
    # |prev|: The previous item in the linked list. 
    # set to be None only if the item is the first one in linked list
    def __init__(self, key, value,prev):
        super().__init__(key, value)
        self.prev = prev

class LinkedList():
    #Intialize the linked list
    def __init__(self):
        #|first|: first item in the linked list
        #|last|: last item in the linked list
        self.first = None 
        self.last = None 
    
    #delete the oldest or last item in the linked list
    #update |self.last| (and |self.first|)accordingly
    def mypop(self):
        if self.last == None:#when the item count is originally 0
            print("linkedlist is empty before deletion")
            return 
        else:
            second_last = self.last.prev
            if second_last == None:#when the item count is originally 1
                self.first = None 
                self.last = None 
            else:#when the item count is originally >= 2
                second_last.next = None
                self.last = second_last
    
    #add new item at the first part of the linked list
    #update |self.first| (and |self.last|) accordingly    
    def mypush(self,key,value):
        new_ItemInLinked = ItemInLinked(key,value,prev = None)
        if self.first != None:
            self.first.prev = new_ItemInLinked
        else:
            #update last
            self.last = new_ItemInLinked
        new_ItemInLinked.next = self.first
        #update first
        self.first = new_ItemInLinked
    
    #delete certain item in the linked list
    #update  |self.first| and |self.last| if necessary
    def mydel(self,item_to_del):
        if item_to_del.next == None:#最後
            self.mypop()
        elif item_to_del.prev == None:#最後ではなく最初
            assert (self.first != None)
            self.first = self.first.next 
        else:#最後でも最初でもない
            item_to_del.next.prev = item_to_del.prev
            item_to_del.prev.next = item_to_del.next
    
    # get all the items in the linked list from first to last
    def get_items(self):
        items = []
        item = self.first
        while item:
            items.append((item.key,item.value))
            item = item.next 
        return items
    
    # get all the items in the linked list from last to first
    def get_items_backwards(self):
        items = []
        item = self.last
        while item:
            items.append((item.key,item.value))
            item = item.prev 
        return items
    
    #print all the items  in the linked list from first to last
    def myprint(self):
        print(self.get_items())
    
    #print all the items in the linked list from last to first
    def myprint_backwards(self):
        print(self.get_items_backwards())
        
        

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        #------------------------#
        self.hash_table = HashTable()
        self.linked_list = LinkedList()
        self.cache_limit = n
        # Write your code here!  #
        #------------------------#

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        #------------------------#
        value,pos_in_linked_list,get_success = self.hash_table.get(url,get_other_prop=True)
        item_in_linked_list = pos_in_linked_list
        if get_success:
            assert(item_in_linked_list!=None),(value,pos_in_linked_list,get_success)#'DDD'の追加時に場所を入れていない?
            #delete
            self.hash_table.delete(item_in_linked_list.key)
            self.linked_list.mydel(item_in_linked_list)
            #push
            self.linked_list.mypush(url,contents)
            self.hash_table.put(url,contents,self.linked_list.first)
        else:
            #push
            self.linked_list.mypush(url,contents)
            self.hash_table.put(url,contents,self.linked_list.first)
            #pop
            if self.hash_table.item_count > self.cache_limit:
                assert(self.linked_list.last != None)
                self.hash_table.delete(self.linked_list.last.key)
                self.linked_list.mypop()
        # Write your code here!  #
        #------------------------#
        pass

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        #------------------------#
        # Write your code here!  #
        pages = []
        item = self.linked_list.first
        while item:
            pages.append(item.key)
            item = item.next
        return pages
        #------------------------#


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []
    # cache.linked_list.myprint()
    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # cache.hash_table.print_table()
    # cache.linked_list.myprint()
    
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]
    # Access "d.com".
    cache.access_page("d.com", "DDD")
    
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]
    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
