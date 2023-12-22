
import argparse
import copy
from math import lcm

def parse_line(line):
    
    name = line.split('=')[0].strip()
    left = line.split('=')[1].strip().split(',')[0].strip('(').strip()
    right = line.split('=')[1].strip().split(',')[1].strip(')').strip()
    
    return {'name': name,
            'L': left,
            'R': right}

def check_if_end(vector):
    
    found = True
    for node in vector:
        if not node['name'].endswith('Z'):
            found = False
            break
    
    return found
        
# def find_repetitions(seq):

def check_copy_candidate(copy_candidate, commands):
    
    k = 0
    while k < len(copy_candidate):
        for c in commands:
            if c != copy_candidate[k]:
                return False
            k+=1
    return True 
    

def  compute_period(start_node, nodes_dict, commands):
    """
    Computes
     - the phase, after which the commands start showing a repeating pattern
       of nodes
     - the period of this recurring pattern
     NB
     the length of the commands sequence is assumed to be a prime number,
     so the periodicity cannot be a fraction of a command sequence
    """
      
    node = start_node
    found = False
    # list containing end points after each iteration through the commands sequence
    end_points = []
    
    while not found:
        
        for c in commands:
            next_node_name = node[c]
            node = nodes_dict[next_node_name]
        
        # comparing current end point with previous end points
        # starting from the latest
        curr_end_point = node['name']
        L = len(end_points)
        for T in range(L):
            
            if end_points[L-1-T] == curr_end_point:
                found = True
                period = T+1
                phase = L-T-1
                break
        
        # adding current end point to list
        end_points.append(curr_end_point)
            
    return phase, period
    
 
    
def compute_end_points(node, phase_period, nodes_dict, commands): 
    
    # exctracting phase, and period
    phase = phase_period[0]
    period = phase_period[1]

    # skipping the initial non periodic phase
    for k in range(phase):
        for c in commands:
            next_node_name = node[c]
            node = nodes_dict[next_node_name]
    
    # looking for the end points
    end_points = []
    i = 0
    for k in range(period):
        for c in commands:
            i += 1
            next_node_name = node[c]
            node = nodes_dict[next_node_name]
            if node['name'].endswith('Z'):
                end_points.append(i)    
    return end_points
        

        
            
  
        
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()
        # removing trailing spaces
        lines = [line.strip() for line in lines]
    

    # Computing result for part 1
    print("Part 1:")
    # reading the commands
    commands = lines[0]
    #print(commands)
    # parsing the lines
    nodes = [parse_line(line) for line in lines[2:]]
    # creating dictionary with nodes
    nodes_dict = {node['name']:node for node in nodes}
    #navitagiting the nodes following the commands, until 'ZZZ' is reached
    node = nodes_dict['AAA']
    found = False
    steps = 0
    while not found:
        for c in commands:
            if node['name'] == 'ZZZ':
                found = True
                break
            else:
                steps +=1
                next_node_name = node[c]
                node = nodes_dict[next_node_name]
    print(steps)
    print()
    
    
    #computing result for part 2
    print("part 2:")
    L = len(commands)
    # creating starting vector: all nodes ending with A
    vector = [node for node in nodes if node['name'].endswith('A')]
    # computing the periodicity of each vector
    phase_periods = [compute_period(node, nodes_dict, commands)
                    for node in vector] 
    print(phase_periods)
    # computing the potential end point, within the period, for each node
    end_points_list = [compute_end_points(node, phase_period, nodes_dict, commands)
                        for node, phase_period in zip(vector, phase_periods)]
    print(end_points_list)
    # Since the endpoints are at the end of the period for each node
    # the common end point is the least common multiple (LCM) of the endpoints
    common_end = lcm(*[e[0] for e in end_points_list])
    print(common_end)


