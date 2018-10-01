import copy

class b_node():
    
    def __init__(self, prev_node, coord):
        self.loc = copy.deepcopy(coord)
        self.h_val = heuristic(self.loc)
        if self.loc == [coordinates[0],coordinates[1]]:
            self.path = [self.loc]
        elif self.loc == [-1,-1]:
            self.path = []
        else:
            self.path = copy.deepcopy(prev_node.path)
            self.path.append(self.loc)

    def __gt__(self, p2):
        return self.h_val > p2.h_val

class h_node():
    #constructor for general nodes
    def __init__(self, prev_node, coord):
        self.loc = copy.deepcopy(coord)
        self.h_val = heuristic(self.loc)
        if self.loc == [coordinates[0],coordinates[1]]:
            self.cost = 0
            self.path = [self.loc]
        elif self.loc == [-1,-1]:
            self.cost = -1
            self.path = []
        else:
            self.cost = prev_node.cost + 1 + abs(maps[prev_node.loc[0]][prev_node.loc[1]] - maps[coord[0]][coord[1]])
            self.path = copy.deepcopy(prev_node.path)
            self.path.append(self.loc)

    # overload greater than operator
    def __gt__(self, p2):
        return (self.cost + self.h_val) > (p2.cost + p2.h_val) 

def heuristic(curr):
    return abs(curr[0] - coordinates[2]) + abs(curr[1] - coordinates[3])

def search_func(type):
    def notCliff(current, prev):
        if abs(maps[current[0]][current[1]] - maps[prev[0]][prev[1]]) < 4:
            return True
        return False

    def create_node(prev, coord, type):
         if type == 0:
            return b_node(prev,coord)
         else:
            return h_node(prev,coord)

    curr = create_node(0, [coordinates[0],coordinates[1]], type)
    visited = [curr.loc]
    possible_move = []
    expanded = 1
    moved = False

    while 1:
        #add all possible moves to the node list
        #top
        if(curr.loc[0] > 0 and ([curr.loc[0]-1,curr.loc[1]] not in visited) and notCliff([curr.loc[0]-1,curr.loc[1]], curr.loc)):
            left_cell = create_node(curr, [curr.loc[0]-1,curr.loc[1]], type)
            possible_move.append(left_cell)
        #down
        if(curr.loc[0] < (size-1) and ([curr.loc[0]+1,curr.loc[1]] not in visited) and notCliff([curr.loc[0]+1,curr.loc[1]], curr.loc)):
            right_cell = create_node(curr, [curr.loc[0]+1,curr.loc[1]], type)
            possible_move.append(right_cell)
        #left
        if(curr.loc[1] > 0 and ([curr.loc[0]-1,curr.loc[1]-1] not in visited) and notCliff([curr.loc[0],curr.loc[1]-1], curr.loc)):
            top_cell = create_node(curr, [curr.loc[0],curr.loc[1]-1], type)
            possible_move.append(top_cell)
        #right
        if(curr.loc[1] < (size-1) and ([curr.loc[0],curr.loc[1]+1] not in visited) and notCliff([curr.loc[0],curr.loc[1]+1], curr.loc)):
            bot_cell = create_node(curr, [curr.loc[0],curr.loc[1]+1], type)
            possible_move.append(bot_cell)

        possible_move.sort(reverse = True)

        # update location
        while moved == False:
            if len(possible_move) is not 0:
                minimum = possible_move.pop()
            else:
                return [create_node(0, [-1,-1], type), -1]

            # check if visited
            if(minimum.loc not in visited):
                expanded += 1
                visited.append(minimum.loc)
                curr = copy.deepcopy(minimum)
                #check if reach goal
                if(curr.loc[0] == coordinates[2] and curr.loc[1] == coordinates[3]):
                    return [curr, expanded]
                moved = True
        moved = False

def extract(str, delim):
    data = []
    for i in str:
        if i in delim:
            continue
        data.append(int(i))
    return data

# read specification from file
coordinates = []
maps = []
file_name = input("Please enter the name of the file for extraction: ")
with open(file_name) as f:
    size = int(f.readline())
    delim = "[], \n"

    # read start & goal
    coor = f.readline()
    coordinates = extract(coor, delim)
    
    #read map
    for y in range(size):
        field = f.readline()
        row = extract(field,delim)
        maps.append(row)
    f.close()

print(size)
print(coordinates)
for i in range(size):
    print(maps[i])

b_result = search_func(0)
if b_result[1] == -1:
    print("no shortest path found for Best First Search.")
else:
    print("Best First Search reached target location: {0} with".format(b_result[0].loc))
    print("# of expanded nodes: {0}".format(b_result[1]))
    print("path: {0}\n".format(b_result[0].path))


a_result = search_func(1)
if a_result[1] == -1:
    print("no shortest path found for A* Search.")
else:
    print("A* Search reached target location: {0} with".format(a_result[0].loc))
    print("# of expanded nodes: {0}".format(a_result[1]))
    print("cost: {0}".format(a_result[0].cost))
    print("path: {0}".format(a_result[0].path))