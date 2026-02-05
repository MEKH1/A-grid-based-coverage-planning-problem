def Check_Plan(cave, path,filename):
    empty_space = []
    visited = []
    not_visited = []
    directions = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)} 
    starting_row = None
    starting_col = None
    for row_index, row in enumerate(cave):
        if "S" in row:
            starting_row = row_index
            starting_col = row.index('S')
        for col_index, cell in enumerate(row):
            if cell == ' ':
                empty_space.append((row_index, col_index))

    for dir in path:
        displace_row, displace_col = directions[dir] #vaccum directions

        # the new vaccum index 
        if starting_row is not None:
            new_row_index= starting_row + displace_row
            new_col_index = starting_col + displace_col
        else:
            return Check_Plan_without_starting_point(cave,path,filename)

        # check if the new possition of the vaccum is right (not outside the boundary and is not a wall) 
        if 0 <= new_row_index < len(cave) and 0 <= new_col_index < len(cave[0]) and cave[new_row_index][new_col_index] != 'X':
            starting_row, starting_col = new_row_index, new_col_index
            visited.append((new_row_index, new_col_index))
                
        elif new_row_index >= len(cave) and cave[0][new_col_index] != 'X': #out side the map from the bottom  so go to the top
            starting_row, starting_col = 0 , new_col_index
            visited.append((0, new_col_index))
            
        
        elif new_row_index < 0 and cave[len(cave)-1][new_col_index] != 'X': #out side the map from the top so go the bottom 
            starting_row, starting_col = len(cave)-1 , new_col_index
            visited.append((len(cave)-1, new_col_index))


        elif new_col_index >= len(cave[0]) and cave[new_row_index][0] != 'X':  #out side the map from the left so go to the start right
            starting_row, starting_col = new_row_index , 0
            visited.append((new_row_index, 0))


        elif new_col_index < 0 and cave[new_row_index][len(cave[0])-1] != 'X': #out side the map from the right so go to the end left
            starting_row, starting_col = new_row_index , len(cave[0])-1 
            visited.append((new_row_index, len(cave[0])-1))


    # check for the unvisited spots 
    for element in empty_space:
        if element not in visited:
            not_visited.append(element)


    problemname = filename.split('m', )[1]
    with open('solutions/solution'+problemname, 'w') as file:
        if not not_visited:
            file.write('GOOD PLAN')
        else:
            file.write('BAD PLAN\n')
            for element in not_visited:
                file.write(f'{element[1]}, {element[0]}\n')



def Check_Plan_without_starting_point(cave,path,filename):
    empty_space = []
    visited = []
    all_visited=[]
    not_visited_at_all = []
    directions = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)} 

    for row_index, row in enumerate(cave):
        for col_index, cell in enumerate(row):
            if cell == ' ':
                empty_space.append((row_index, col_index))

    for s in empty_space:
        starting_row, starting_col = s
        visited = []
        not_visited = []
        for dir in path:
            displace_row, displace_col = directions[dir] #vaccum directions

            # the new vaccum index 
            new_row_index= starting_row + displace_row
            new_col_index = starting_col + displace_col

            # check if the new possition of the vaccum is right (not outside the boundary and is not a wall) 
            if 0 <= new_row_index < len(cave) and 0 <= new_col_index < len(cave[0]) and cave[new_row_index][new_col_index] != 'X':
                starting_row, starting_col = new_row_index, new_col_index
                visited.append((new_row_index, new_col_index))
                    
            elif new_row_index >= len(cave) and cave[0][new_col_index] != 'X': #out side the map from the bottom  so go to the top
                starting_row, starting_col = 0 , new_col_index
                visited.append((0, new_col_index))
                
            
            elif new_row_index < 0 and cave[len(cave)-1][new_col_index] != 'X': #out side the map from the top so go the bottom 
                starting_row, starting_col = len(cave)-1 , new_col_index
                visited.append((len(cave)-1, new_col_index))


            elif new_col_index >= len(cave[0]) and cave[new_row_index][0] != 'X':  #out side the map from the left so go to the start right
                starting_row, starting_col = new_row_index , 0
                visited.append((new_row_index, 0))


            elif new_col_index < 0 and cave[new_row_index][len(cave[0])-1] != 'X': #out side the map from the right so go to the end left
                starting_row, starting_col = new_row_index , len(cave[0])-1 
                visited.append((new_row_index, len(cave[0])-1))
            else:
                visited.append((starting_row, starting_col))



        all_visited.append(set(visited))
    
    # Find intersection of all visited sets
    visited_by_all = set.intersection(*all_visited)
    not_visited_at_all = set(empty_space) - visited_by_all
    problemname = filename.split('m', )[1]
    with open('solutions/solution'+problemname, 'w') as file:
        if not not_visited_at_all:
            file.write('GOOD PLAN')
        else:
            file.write('BAD PLAN\n')
            for element in not_visited_at_all:
                file.write(f'{element[1]}, {element[0]}\n')

    
def Find_Plan(cave,filename):
    nodes = []
    visited = []
    Path=[]
    start_found = False
    starting_position = None
    for row_index, row in enumerate(cave):
        for col_index, cell in enumerate(row):
            if cell == 'S':
                starting_position = (row_index, col_index)
                start_found = True
            if cell == ' ' or cell == 'S':  # add to the graph empty space and starting position coordinates 
                nodes.append((row_index, col_index))
    if not start_found:
        Find_Plan_without_S(cave,filename)
    else:                        
        graph= get_neighbors(nodes,cave)
       # print(nodes)
        #print(graph)
        df2s=dfs(visited,graph,starting_position)
       # print(df2s)
        final_path=check_for_jump(graph,df2s,nodes,cave)
        #print(final_path)
        encoded_paln=path_to_directions(final_path,cave)

        problemname = filename.split('m', )[1]
        with open('solutions/solution'+problemname, 'w') as file:
            file.write(encoded_paln)


def Find_Plan_without_S(cave,filename):
    nodes = []
    Path=[]
    All_pathes={} # dict has all possible path with their starting point
    starting_position = None
    for row_index, row in enumerate(cave):
        for col_index, cell in enumerate(row):
            if cell == ' ':  # add to the graph empty space and starting position coordinates 
                nodes.append((row_index, col_index))
    graph= get_neighbors(nodes,cave)
    #print(nodes)
    #print(graph)
    for i in nodes:
        visited = []
        starting_position = (i[0], i[1])
        #print("starting",starting_position)
        df2s=dfs(visited,graph,starting_position)
       # print(df2s)
        final_path=check_for_jump(graph,df2s,nodes,cave)
        #print(final_path)
        #print(path_to_directions(final_path,cave))
        All_pathes[starting_position]= path_to_directions(final_path,cave)
        #print(All_pathes)
    Check_Plan_The_founded_PLAN(cave,nodes, All_pathes)
    last_plane_forall=Check_Plan_The_founded_PLAN(cave,nodes, All_pathes)
    problemname = filename.split('m', )[1]
    with open('solutions/solution'+problemname, 'w') as file:
        file.write(last_plane_forall)


    
def Check_Plan_The_founded_PLAN(cave,empty_space, All_pathes):
    visited = []
    #print(empty_space)
    directions = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)} 
    starting_row = None
    starting_col = None
    starting_points=list(All_pathes.keys())
    #print("AllPathes",All_pathes)
    paths=list(All_pathes.values())
    path=paths[0]
    #print(cave)
    for starting_point in starting_points:
        not_visited=[]
        visited=[]
        #print("starting_ Point",starting_point)
        starting_row, starting_col = starting_point
        #print("current",path)
        visited.append(starting_point)
        for dir in path:
            displace_row, displace_col = directions[dir] #vaccum directions

            # the new vaccum index 
            if starting_row is not None:
                new_row_index= starting_row + displace_row
                new_col_index = starting_col + displace_col

            # check if the new possition of the vaccum is right (not outside the boundary and is not a wall) 
            if 0 <= new_row_index < len(cave) and 0 <= new_col_index < len(cave[0]) and cave[new_row_index][new_col_index] != 'X':
                starting_row, starting_col = new_row_index, new_col_index
                visited.append((new_row_index, new_col_index))
                    
            elif new_row_index >= len(cave) and cave[0][new_col_index] != 'X': #out side the map from the bottom  so go to the top
                starting_row, starting_col = 0 , new_col_index
                visited.append((0, new_col_index))
                
            
            elif new_row_index < 0 and cave[len(cave)-1][new_col_index] != 'X': #out side the map from the top so go the bottom 
                starting_row, starting_col = len(cave)-1 , new_col_index
                visited.append((len(cave)-1, new_col_index))


            elif new_col_index >= len(cave[0]) and cave[new_row_index][0] != 'X':  #out side the map from the left so go to the start right
                starting_row, starting_col = new_row_index , 0
                visited.append((new_row_index, 0))


            elif new_col_index < 0 and cave[new_row_index][len(cave[0])-1] != 'X': #out side the map from the right so go to the end left
                starting_row, starting_col = new_row_index , len(cave[0])-1 
                visited.append((new_row_index, len(cave[0])-1))


    # check for the unvisited spots 
        for element in empty_space:
            if element not in visited:
                not_visited.append(element)
                #print("not visited",not_visited)
                #print("when starting point is",(new_row_index,new_col_index))
                
        #print("visited",visited)

        
        if  not_visited:
            path+=(All_pathes[(starting_row,starting_col)])
            #print("updated",path)
       
    #print("last Plan",path)
    return path





def get_neighbors(nodes, cave):
    directions = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)} 
    graph = {}

    for node in nodes:
        row, col = node
        neighbors = []

        for direction, (dir_row, dir_col) in directions.items(): 
            next_row, next_col = row + dir_row, col + dir_col
            if 0 <= next_row < len(cave) and 0 <= next_col < len(cave[0]) and (next_row, next_col) in nodes:  # Check if the neighbor is a valid node " " or "S" and in the boundary 
                neighbors.append((next_row, next_col))
            elif next_row >= len(cave) and (0,next_col) in nodes: #out side the map from the bottom  so go to the top
                neighbors.append((0,next_col))
            elif next_row < 0 and (len(cave)-1, next_col) in nodes: #out side the map from the top so go the bottom 
                neighbors.append((len(cave)-1, next_col))
            elif next_col >= len(cave[0]) and (next_row,0) in nodes:  #out side the map from the left so go to the start right
                neighbors.append((next_row,0))
            elif next_col < 0 and (next_row, len(cave[0])-1) in nodes: #out side the map from the right so go to the end left
                neighbors.append((next_row, len(cave[0])-1))
        graph[node] = neighbors
 
    return graph



def dfs(visited, graph, node): 
    if node not in visited:
       # print (node)
        visited.append(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)
    return visited

def check_for_jump(graph,dfs_path,empty_nodes,cave):
    len_col=len(cave[0])
    len_row = len(cave)
    i=0
    while i < len(dfs_path): 
       # print("i",i)
       # print(len(dfs_path))
        current_position = dfs_path[i]
        if (i+1) < len(dfs_path):
            next_position = dfs_path[i + 1]
        else: 
            next_position=dfs_path[i]
        
        # Check horizontal movement
        if  next_position[0] == current_position[0] + 1 or ( current_position[0]==0 and next_position[0] == len_row-1):
            vertical_movement = "UP"
        elif next_position[0] == current_position[0] - 1 or( current_position[0]==len_row-1 and next_position[0]==0):
            vertical_movement = "DOWN"
        else:
            vertical_movement = None  # No horizontal movement
        
        # Check vertical movement
        if (next_position[1] == current_position[1] + 1)  or ( current_position[1]== len_col-1 and next_position[0] == 0):
            horizontal_movement = "RIGHT"
        elif next_position[1] == current_position[1] - 1 or(  current_position[1]==0 and next_position[0] == len_col-1):
            horizontal_movement = "LEFT"

        else:
            horizontal_movement = None  # No vertical movement
        
        # Determine the type of movement
        if horizontal_movement and vertical_movement and current_position!=next_position:
           # print(f"Move from {current_position} to {next_position}: DIAGONAL ({vertical_movement}, {horizontal_movement})")
            skipped=bfs_shortest_path(graph,current_position,next_position)
            #print("path",skipped)
            dfs_path = dfs_path[:dfs_path.index(current_position)+1] + skipped + dfs_path[dfs_path.index(current_position)+1:]

          #  print(dfs_path)
            i+=len(skipped)
        elif current_position not in graph[next_position] and current_position != next_position:
         #   print(f"Move from {current_position} to {next_position}: no Direct Path ")
            skipped=bfs_shortest_path(graph,current_position,next_position)
          #  print("path",skipped)
            dfs_path = dfs_path[:dfs_path.index(current_position)+1] + skipped + dfs_path[dfs_path.index(current_position)+1:]

         #   print(dfs_path)
            i+=len(skipped)


            
        elif horizontal_movement:
            pass #  print(f"Move from {current_position} to {next_position}: HORIZONTAL ({horizontal_movement})")
        elif vertical_movement:
            pass # print(f"Move from {current_position} to {next_position}: VERTICAL ({vertical_movement})")
        elif current_position == next_position:
            pass#  print(f"Move from {current_position} to {next_position}: NO MOVEMENT")
        i+=1
    return dfs_path

def bfs_shortest_path(graph, start, goal):
    visited = []
    queue = [(start, [start])]  

    while queue:
        current_node, path = queue.pop(0)  # Pop the first element (like dequeuing)
        if current_node == goal:
            #print(path[1:-1])
            return path[1:-1] # Return the path if goal is reached

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append((neighbor, path + [neighbor]))  # Add to queue with updated path

    return None


def path_to_directions(path,cave):
    row_len=len(cave)
    col_len=len(cave[0])
   # print("COLLEn",col_len)
   # print("row_len",row_len)
    directions_map = {(-1, 0): "N",(1, 0): "S", (0, 1): "E", (0, -1): "W"} # mapping the coordenates to the  S W N E
    final_directions = ""

    for i in range(len(path) - 1):
        current = path[i]
       # print("current",current)
        next_point = path[i + 1]
       #print("next",next_point)
        move = (next_point[0] - current[0], next_point[1] - current[1])
        #print(move)
        if move  not in directions_map:
            if move[0] < 0: # outside the map bottom S
                move=(1,next_point[1] - current[1])

            elif move[0] == row_len-1 : # outside the map top N
                move=(-1,next_point[1] - current[1])

            elif move[1] < 0:
                move=(next_point[0] - current[0],1) #outside the map right E
            
            elif move[1] == col_len-1 : # outside the map 
                move=(next_point[0] - current[0],-1)

        #print(move)
        final_directions += directions_map.get(move,"?")  # Add the direction to the final_firection
    return final_directions

