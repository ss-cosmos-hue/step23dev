from collections import deque
def bfs(start,goal,links):
    queue = deque()
    visited = {}#探索中もしくは探索済みのノード集合
    visited[start] = True 
    queue.push(start)#探索中のノード集合
    while not len(queue) == 0:
        node = queue.pop()
        if node == goal:
            return "FOUND"
        for child in links[node]:
            if not child in visited: 
                queue.push(child)#これから探索する
                visited[child] = True#探索中にする
    return "Not FOUND"
        