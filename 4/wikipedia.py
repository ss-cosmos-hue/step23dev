import sys
import collections
import numpy as np

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}
        
        # A mapping from a page title to the page ID.
        self.ids = {}
        

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.ids[title] = id
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start_title, goal_title):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        # 趣旨：最短経路を見つけるにはBFSで初めに見つかったところ考えれば良い
        start = self.ids[start_title]
        goal = self.ids[goal_title]
        # A mapping from an ID (integer) of node A to the ID of the previous node B in the shortest path from start to A.
        # For example, if the shortest path from start to B is start -> C -> B,
        # prev_nodes[ID of B] returns the ID of C
        prev_nodes = {}
        queue = collections.deque() #探索中のノードの集合
        visited = {} # 探索中あるいは探索済みのノードの集合
                    # 探索済み：当該ノードからゴールに行けるかどうかの判定済み
        visited[start] = True 
        queue.append(start)
        while not len(queue) == 0:
            node = queue.popleft()
            if node == goal:
                #goalからstartまで逆順に，prev_nodesを用いながら辿る
                backward_path = []
                cur_node = goal 
                while cur_node in prev_nodes.keys():
                    backward_path.append(cur_node)
                    cur_node = prev_nodes[cur_node]
                backward_path.reverse()
                forward_path = backward_path
                forward_path.insert(0,start)
                #print out
                print("FOUND PATH")
                for node in forward_path:
                    print(node,self.titles[node])
                return 
            for child in self.links[node]:
                if not child in visited:
                    #childは探索中
                    queue.append(child) 
                    visited[child] = True 
                    #start---->node->childのようなので。
                    prev_nodes[child] = node
        print("NOT FOUND")
        return


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #numpy でやると並列計算ができてはやいかもしれないが，隣接行列にすると，メモリの寮が増えるだろうのでやめておく
        # 辞書でなく配列で扱いたいけど
        # なんで? 配列の場合アクセスがO(1)だから¥¥¥¥¥¥¥
        #pagerankを計算する
        
        #pagerankを辞書でなくリストで管理するための，IDとlist indexの対応
        id_to_list_idx = {}
        list_idx_to_id = {}
        list_idx = 0
        for id in self.titles.keys():
            id_to_list_idx[id] = list_idx 
            list_idx_to_id[list_idx] = id 
            list_idx += 1
            
        N = len(list(self.titles.keys()))
        #初期化
        page_rank = [1]*N #このうち15%は毎回配分される
        sum_rank = N 
        while True:
            #15%の振り分け
            new_page_rank = [0.15]*N
            #85%の振り分け
            for i in range(N):#全てのノードに対して
                id = list_idx_to_id[i]
                dsts = list(self.links[id])
                
                #隣接ノードがないので全員に振り分ける
                if len(dsts) == 0:
                    
                    edge_val = 0.85*page_rank[i]/N
                    for i in range(len(new_page_rank)):
                        new_page_rank[i]+=edge_val
                #隣接ノードがあるので，隣接ノーどのみに振り分ける
                else:
                    edge_val = 0.85*page_rank[i]/len(dsts)
                    for dst in dsts:
                        dst_list_idx = id_to_list_idx[dst]
                        new_page_rank[dst_list_idx] += edge_val
                        
            tolerance = 1e-8
            assert(abs(sum(new_page_rank)-sum(page_rank))<tolerance)        
            #更新されているかどうか判定
            updated = False
            for i in range(N):
                if abs(page_rank[i]-new_page_rank[i]) > tolerance:
                    updated = True 
                    page_rank = new_page_rank
                    break#for文を抜ける
            if not updated:
                break#while文を抜ける   
        # pageIDとpagerankをtupleにしてsortする
        # pagerankが最大な順にpageIDを算出する
        kNum = 5
        assert(kNum <= N)
        page_rank_listidx_tuples = [(page_rank[i],i) for i in range(N)]
        page_rank_listidx_tuples.sort(reverse=True)
        for i in range(kNum):
            rank,listidx = page_rank_listidx_tuples[i]
            id = list_idx_to_id[listidx]
            print(f'page_rank:{rank}, id: {id}, title:{self.titles[id]}')
        return


    # Do something more interesting!!
    def find_something_more_interesting(self):#しりとり
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    # wikipedia.find_shortest_path("A","C")
    wikipedia.find_most_popular_pages()