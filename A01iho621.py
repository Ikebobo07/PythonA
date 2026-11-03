import heapq

# Define the graph based on Figure 1
graph = {
    'S': [('A', 2), ('B', 1), ('D', 1)],
    'A': [('B', 1), ('C', 3), ('D', 1)],
    'B': [('S', 1), ('D', 5)],
    'C': [('A', 3), ('G', 4)],
    'D': [('A', 1), ('G', 7)],
    'G': [('C', 4)]
}

def dfs_traversal(graph, start_node):
    visited = []
    
    def dfs(node):
        visited.append(node)
        neighbors = sorted([neighbor for neighbor, cost in graph.get(node, [])])
        for neighbor in neighbors:
            if neighbor not in visited:
                dfs(neighbor)
                
    dfs(start_node)
    return "".join(visited)

def bfs_traversal(graph, start_node):
    visited = []
    queue = [start_node]
    visited.append(start_node)
    
    while queue:
        current = queue.pop(0)
        neighbors = sorted([neighbor for neighbor, cost in graph.get(current, [])])
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                
    return "".join(visited)

def dfs_path(graph, start_node, goal_node):
    stack = [(start_node, [start_node])]
    visited = set()
    
    while stack:
        current, path = stack.pop()
        
        if current == goal_node:
            return "".join(path)
            
        if current not in visited:
            visited.add(current)
            neighbors = sorted([neighbor for neighbor, cost in graph.get(current, [])], reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
                    
    return ""

def bfs_path(graph, start_node, goal_node):
    queue = [(start_node, [start_node])]
    visited = {start_node}
    
    while queue:
        current, path = queue.pop(0)
        
        if current == goal_node:
            return "".join(path)
            
        neighbors = sorted([neighbor for neighbor, cost in graph.get(current, [])])
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                
    return ""

def ucs_path(graph, start_node, goal_node):
    pq = [(0, start_node, [start_node])]
    visited_costs = {}
    
    while pq:
        cost, current, path = heapq.heappop(pq)
        
        if current == goal_node:
            return "".join(path)
            
        if current not in visited_costs or cost < visited_costs[current]:
            visited_costs[current] = cost
            
            neighbors = sorted(graph.get(current, []))
            for neighbor, edge_cost in neighbors:
                new_cost = cost + edge_cost
                if neighbor not in visited_costs or new_cost < visited_costs[neighbor]:
                    heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))
                    
    return ""

def main():
    print("Welcome to the DFS, BFS and UCS search demo!")
    
    start_node = input("Enter a start node (S, A, B, C, D, G):\n").strip().upper()
    goal_node = input("Enter a goal node (S, A, B, C, D, G):\n").strip().upper()
    
    print(f"The Depth First Search Traversal (starting from node {start_node}) is")7]
    print(dfs_traversal(graph, start_node))
    
    print(f"The Breadth First Search Traversal (starting from node {start_node}) is")
    print(bfs_traversal(graph, start_node))
    
    print("The path found by Depth First Search is")
    print(dfs_path(graph, start_node, goal_node))
    
    print("The path found by Breadth First Search is")
    print(bfs_path(graph, start_node, goal_node))
    
    print("The path found by Uniform Cost Search is")
    print(ucs_path(graph, start_node, goal_node))

if __name__ == "__main__":
    main()
 