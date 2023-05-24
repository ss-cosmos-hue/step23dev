from cache import LinkedList 

ll = LinkedList()
ll.mypush("a","b")
ll.myprint()
ll.myprint_backwards()

ll.mypush("c","d")
ll.myprint()
ll.myprint_backwards()


ll.mypush("d","e")
ll.myprint()
ll.myprint_backwards()

ll.mypop()
ll.myprint()
ll.myprint_backwards()

ll.mypush("E","F")
ll.myprint()
ll.myprint_backwards()

# ll.mydel("c")mydelの引数はnodeのポインタ
ll.myprint()