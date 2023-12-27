
import argparse
import math
import sys
sys.setrecursionlimit(5000)

def find_starting_point(data):
    
    # number of rows and columns
    R = len(data)
    C = len(data[0])
    
    for i in range(R):
        for j in range(C):
            if data[i][j] == 'S':
                return i,j


# A dictionary containining for each symbol the transformation
# of directions
MAPPING_DICT = {
                # is a vertical pipe connecting north and south.
                '|' : {'N': lambda x: x['N'],
                    'S': lambda x: x['S'],
                    'W': lambda x: 0,
                    'E': lambda x: 0
                    } ,
                
                # is a horizontal pipe connecting east and west.
                '-' : {'N': lambda x: 0,
                        'S': lambda x: 0,
                        'W': lambda x: x['W'],
                        'E': lambda x: x['E'],
                        },     
                
                # # is a 90-degree bend connecting north and east.
                'L' : {'N': lambda x: x['W'],
                       'S': lambda x: 0,
                       'W': lambda x: 0,
                       'E': lambda x: x['S'],
                      }, 
                
                # is a 90-degree bend connecting north and west. 
                'J' : {'N': lambda x: x['E'],
                       'S': lambda x: 0,
                       'W': lambda x: x['S'],
                       'E': lambda x: 0
                      }, 
                
                # is a 90-degree bend connecting south and west.
                '7' : {'N': lambda x: 0,
                       'S': lambda x: x['E'],
                       'W': lambda x: x['N'],
                       'E': lambda x: 0
                      }, 
                
                # is a 90-degree bend connecting south and east.
                'F' :{'N': lambda x: 0,
                       'S': lambda x: x['W'],
                       'W': lambda x: 0,
                       'E': lambda x: x['N']
                      }
                
}

# A dictionary providing, for each symbol, a dictionary
# providing the transformation of direction for
# the vector pointing inside the loop
INSIDE_LOOP_MAPPING_DICT = {
                # is a vertical pipe connecting north and south.
                '|' : {'N': lambda dir, inner_dir: 0,
                        'S': lambda dir, inner_dir: 0,
                        'W': lambda dir, inner_dir: inner_dir['W'],
                        'E': lambda dir, inner_dir: inner_dir['E']
                        } ,
                
                # is a horizontal pipe connecting east and west.
                '-' : {'N': lambda dir, inner_dir: inner_dir['N'],
                        'S': lambda dir, inner_dir: inner_dir['S'],
                        'W': lambda dir, inner_dir: 0,
                        'E': lambda dir, inner_dir: 0
                        },     
                
                # # is a 90-degree bend connecting north and east.
                'L' : {'N': lambda  dir, inner_dir: ((dir['W'] and inner_dir['N']) or
                                                     (dir['S'] and inner_dir['E'])),
                       'S': lambda dir, inner_dir: ((dir['W'] and inner_dir['S']) or
                                                     (dir['S'] and inner_dir['W'])),
                       'W': lambda dir, inner_dir: ((dir['W'] and inner_dir['S']) or
                                                     (dir['S'] and inner_dir['W'])),
                       'E': lambda dir, inner_dir: ((dir['W'] and inner_dir['N']) or
                                                     (dir['S'] and inner_dir['E'])),
                      }, 
                
                # is a 90-degree bend connecting north and west. 
                'J' : {'N': lambda dir, inner_dir: ((dir['E'] and inner_dir['N']) or
                                                    (dir['S'] and inner_dir['W'])),
                       'S': lambda  dir, inner_dir: ((dir['E'] and inner_dir['S']) or
                                                    (dir['S'] and inner_dir['E'])),
                       'W': lambda  dir, inner_dir: ((dir['E'] and inner_dir['N']) or
                                                     (dir['S'] and inner_dir['W'])),
                       'E': lambda dir, inner_dir: ((dir['E'] and inner_dir['S']) or
                                                    (dir['S'] and inner_dir['E']))
                      }, 
                
                # is a 90-degree bend connecting south and west.
                '7' : {'N': lambda  dir, inner_dir: ((dir['E'] and inner_dir['N']) or
                                                     (dir['N'] and inner_dir['E'])),
                       'S': lambda dir, inner_dir: ((dir['E'] and inner_dir['S']) or
                                                     (dir['N'] and inner_dir['W'])),
                       'W': lambda dir, inner_dir: ((dir['E'] and inner_dir['S']) or
                                                     (dir['N'] and inner_dir['W'])),
                       'E': lambda dir, inner_dir: ((dir['E'] and inner_dir['N']) or
                                                     (dir['N'] and inner_dir['E'])),
                      }, 
                
                # is a 90-degree bend connecting south and east.
                'F' :{'N': lambda  dir, inner_dir: ((dir['W'] and inner_dir['N']) or
                                                     (dir['N'] and inner_dir['W'])),
                       'S': lambda dir, inner_dir: ((dir['W'] and inner_dir['S']) or
                                                     (dir['N'] and inner_dir['E'])),
                       'W': lambda dir, inner_dir: ((dir['W'] and inner_dir['N']) or
                                                     (dir['N'] and inner_dir['W'])),
                       'E': lambda dir, inner_dir: ((dir['W'] and inner_dir['S']) or
                                                     (dir['N'] and inner_dir['E'])),
                      }
}



# a dictionary mapping input and output vector to a missing sign
VECTOR_TO_SIGN_MAPPING = {
    (1,1,0,0) : '|',   # north - south 
    (0,0,1,1) : '-',   # east - west
    (1,0,0,1) : 'L',   # north - east
    (1,0,1,0) : 'J',   # north - west
    (0,1,1,0) : '7',   # south - west
    (0,1,0,1) : 'F'    # south - east 
}

def get_next_point(point, current_dir, current_sign):
    
    # updating direction vector
    update_map = MAPPING_DICT[current_sign]
    new_dir = {}
    for d in current_dir:
        new_dir[d] = update_map[d](current_dir)
        
    # updating point
    new_point = (point[0]-new_dir['N']+new_dir['S'],
                 point[1]-new_dir['W']+new_dir['E'])
    
    # returning results
    return new_point, new_dir

def get_loop_length(starting_point, maze):
    
    # number of rows and columns
    R = len(maze)
    C = len(maze[0])
    
    # exploring the 4 possible directions from the starting point
    candidate_dirs = [{'N':1, 'S':0, 'W':0, 'E':0},
                      {'N':0, 'S':1, 'W':0, 'E':0},
                      {'N':0, 'S':0, 'W':1, 'E':0},
                      {'N':1, 'S':0, 'W':0, 'E':1}]
    
    found = False
    i = 0
    while not found and i<len(candidate_dirs):
        
        starting_dir = candidate_dirs[i]
        dir = starting_dir
        # updating point
        point = (starting_point[0]-dir['N']+dir['S'],
                    starting_point[1]-dir['W']+dir['E'])
        sign = maze[point[0]][point[1]]
        loop = [point]
        
        # go to next candidate, if sign is ground
        if sign == '.':
            i += 1
            continue
        
        steps = 1
        while  point != starting_point:
            point, dir = get_next_point(point, dir, sign)
            loop.append(point)
            
            # stopping if the direction vector is 0
            # no further movement is possible
            if sum(dir.values()) == 0:
                break
            
            # check if still inside maze
            if ((point[0] >= R) or (point[0] < 0) or
                (point[1] >= C) or (point[1] < 0)):
                break
            
            sign = maze[point[0]][point[1]]
            # check if the sign is not ground
            if sign == '.':
                break
                
            steps += 1
            
        if point == starting_point:
            found = True
            
        # moving to next candidate
        i += 1 
        
    # Computing the missing symbol
    # Converting the direction dictionary to vector
    # (N,S,W,E)
    end_dir = dir
    starting_dir_vector = [starting_dir[k] for k in ['N','S','W','E']]
    # inverting the direction of the end dir to get the exiting 
    # vector, instead of entering vector
    end_dir_vector = [end_dir[k] for k in ['S','N','E','W']]
    # summing the two vector
    joint_vector = [a+b for a,b in zip(starting_dir_vector, end_dir_vector)]
    # getting the symbol from the dictionary
    missing_symbol = VECTOR_TO_SIGN_MAPPING[tuple(joint_vector)]
    print(f'missing_symbol: {missing_symbol}')
    return steps, loop, starting_dir, missing_symbol


def get_neighbors(pos, n_rows, n_cols):
    
    # creating all neigbors
    neighbors_candidates = []
    for y in [-1, 0, 1]:
        for x in [-1, 0, 1]:
            neighbor = (pos[0]+y, pos[1]+x)
            # excluding the point itself
            if not(x==0 and y==0):
                neighbors_candidates.append(neighbor)
    
    # excluding the neighbours outside the maze
    neighbors = []
    for p in neighbors_candidates:
        if (p[0] >=0 and p[0]< n_rows and
            p[1] >=0 and p[1]< n_cols):
            neighbors.append(p)
    return   neighbors  
    

def get_inner_points(point, inner_dir):
    
    inner_points = []
    
    # computing the inner point
    inner_point = (point[0]-inner_dir['N']+inner_dir['S'],
                  point[1]-inner_dir['W']+inner_dir['E'])
    inner_points.append(inner_point)
    
    # computing ortigonal directions, if inner direction is diagonal
    if sum(inner_dir.values())>1:
        inner_point = (point[0]-inner_dir['N']+inner_dir['S'], point[1])
        inner_points.append(inner_point)
        inner_point = (point[0], point[1]-inner_dir['W']+inner_dir['E'])
        inner_points.append(inner_point)
        
    # returning results
    return inner_points

def update_inner_dir(current_dir, current_inner_dir, current_sign):
    
    # computing direction vector pointing inside the loop
    update_map = INSIDE_LOOP_MAPPING_DICT[current_sign]
    inner_dir = {}
    for d in ['N', 'S', 'W', 'E']:
        inner_dir[d] = update_map[d](current_dir, current_inner_dir)
    
    # returning results
    return inner_dir

def get_content(starting_point, content, loop, n_rows, n_cols):
    
    # adding the current point to the content
    content.append(starting_point)
    
    # getting the neighbors of the current point
    neighbors = get_neighbors(starting_point, n_rows, n_cols)
    
    # repeating recursively for all the neighbors:
    for pos in neighbors:
        if (pos not in loop) and (pos not in content):
            content = get_content(pos, content, loop, n_rows, n_cols)
        
    return content
    

def get_loop_content(starting_point, starting_dir, maze, loop, missing_symbol):
    
    dir  = starting_dir
    
    # number of rows and columns
    R = len(maze)
    C = len(maze[0])
    
    # Moving through the loop while the current sign 
    # doesn't allow to identify the direction of the interior of the loop
    point = (starting_point[0]-starting_dir['N']+starting_dir['S'],
             starting_point[1]-starting_dir['W']+starting_dir['E'])
    sign = maze[point[0]][point[1]]
    while (sign == '-') or (sign == '|'):
        point, dir = get_next_point(point, dir, sign)
        sign = maze[point[0]][point[1]]
    
    # Getting the vector pointing inside the loop for the 
    # current position
    initial_inside_dir_dict = {
                # # is a 90-degree bend connecting north and east.
                'L' : {'N': 1, 'S': 0, 'W': 0, 'E':1}, 
                # is a 90-degree bend connecting north and west. 
                'J' : {'N': 1, 'S': 0, 'W': 1, 'E':0}, 
                # is a 90-degree bend connecting south and west.
                '7' : {'N': 0, 'S': 1, 'W': 1, 'E':0},
                # is a 90-degree bend connecting south and east.
                'F' :{'N': 0, 'S': 1, 'W': 0, 'E':1}
    }
    inside_dir = initial_inside_dir_dict[sign]
    
    # defining the end point, where we should stop the search
    end_point = point
    
    # going around the loop, ans searching the inner content
    content = []
    while True:
        
        # getting the inner point
        inner_points = get_inner_points(point, inside_dir)
        
        # get content
        for inner_point in inner_points:
            if (inner_point not in loop) and (inner_point not in content):
                content = get_content(inner_point, content, loop, R, C)
        
        # moving to next point
        point, dir = get_next_point(point, dir, sign)
        sign = maze[point[0]][point[1]]
        
        # Replacing 'S' with the missing symbol
        if sign == 'S':
            sign = missing_symbol
        
        # updating the vector pointing inside the loop
        inside_dir = update_inner_dir(dir, inside_dir,  sign)
        
        # stopping if end_point is reached
        if (point == end_point):
            break
    
    # continuing
    
    return content


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input filelo
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()
        # removing trailing spaces
        lines = [line.strip() for line in lines]
    maze = lines
    
    # Computing result for part 1
    print("Part 1:")
    # finding the starting point
    starting_point = find_starting_point(maze)
    # Computing the length of the loop
    steps, loop, starting_dir, missing_symbol = get_loop_length(starting_point, lines)
    # Computing the result
    print(math.ceil(steps/2))
    print()
    
    # Computing result for part 2
    print("part 2:")
    # getting the content
    content = get_loop_content(starting_point, starting_dir, lines, 
                               loop, missing_symbol)
    # computing the size
    res = len(content)
    print(res)