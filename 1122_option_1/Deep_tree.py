### Depth TREE
def dfs_tree(graph_to_search, initial_state, goal_state, verbose=False):
    frontiers = [[0, initial_state]]  # the frontier list only has the initial state, with a cost of 0.
    visited = []
    ver = 0 # to
    while len(frontiers) > 0:   # use while loop to iteratively perform search
        if verbose:  # print out detailed information in each iteration
            print('Frontiers (paths):')
            for x in frontiers:
                print('  -', x)
            print('Visited:', visited)
            print('\n')
        path = frontiers.pop(-1)  # Get the last element in the list
        node = path[-1]  # Get the last node in this path
        
        if node in visited:  # check if we have expanded this node, if yes then skip this
            continue
            
        actions = graph_to_search[node] # get the possible actions
        
        if len(actions) == 0:#If next actions is empty, then pass this node,discard visited nodes
            visited = copy.deepcopy(frontiers[-1])# Cover the old visited with the frontiers
            del visited[0]# delate the cost information
            del visited[-1]# delate the unvisited node
            continue
            
        for next_node, next_cost in actions:
            new_path = path.copy()
            new_path.append(next_node)
            new_path[0] = new_path[0] + next_cost
            
            if next_node in visited or new_path in frontiers:
                continue  # skip this node if it is already in the frontiers or the visited list.
            
            # check if we reached the goal state or not
            if next_node == goal_state:
                goal_path = new_path[1:]
                goal_cost = new_path[0]
                return goal_path, goal_cost  # if yes, we can return this path and its cost
            else:
                frontiers.append(new_path)  # add to the frontiers
        
        # after exploring all actions, we add this node to the visited list
        visited.append(node)
        ver += 1
    return None