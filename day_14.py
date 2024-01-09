
import argparse
import time

def parse_lines(lines):
    
    platform = [[c for c in line]
                for line in lines]
    return platform


def get_wall_positions(platform):
    """
    Computes the positions of the fixed stones, for each row
    and for each column.
    Returns two matices:
     - walls_by_row: for each row, provides the column index of the
                   fixed stones;
     - walls_by_col: for each column, provides the column index of the
                   fixed stones;
    """
    
    R = len(platform)
    C = len(platform[0])
    
    # initializing the results
    walls_by_row = [[] for i in range(R)]
    walls_by_col = [[] for i in range(C)]
    
    for i in range(R):
        for j in range(C):
            
            if platform[i][j] == '#':
                walls_by_row[i].append(j)
                walls_by_col[j].append(i)
     
    return walls_by_row, walls_by_col

def get_stones_positions(platform, walls_by_row, walls_by_col):
    """
    Computes the number of stones on each row, and column segment
    Returns:
        - stones_by_row, a list of lists providing for each row,
          a list containing the count of stones on the corresponding
          segment
        - stones_by_col, a list of lists providing for each column,
          a list containing the count of stones on the corresponding
          segment
        - pos_to_segment, a dictionary providing for each stone position (i,j)
          a dictioanary with two entries: 'row_segment', and 'col_segment'.
          These entries provide information about the index of the row segment 
          and column segment for the element
    """
    
    R = len(platform)
    C = len(platform[0])
    
    # initializing the results
    stones_by_row = []
    stones_by_col = []
    pos_to_segment = {}
    ##############################
    # Going through each column  #
    ##############################
    for j in range(C):
        wall_positions = walls_by_col[j]
        stone_count_list = list()
        # creating list of bounds, by extending the walls list
        bounds = [-1] + wall_positions + [R]

        # going through each segment
        for k in range(len(bounds)-1):
            bound_1 = bounds[k]
            bound_2 = bounds[k+1]
            # counting the stones
            stones_count = sum([1 if platform[i][j]=='O' else 0
                                for i in range(bound_1+1, bound_2)])
            # storing the count
            stone_count_list.append(stones_count)
            # indexing the segment
            for i in range(bound_1+1, bound_2):
                pos_to_segment[(i,j)] = {'col_segment': k}
               
        stones_by_col.append(stone_count_list)
        
    ##############################
    # Going through each row    #
    ##############################
    for i in range(R):
        wall_positions = walls_by_row[i]
        stone_count_list = list()
        # creating list of bounds, by extending the walls list
        bounds = [-1] + wall_positions + [C]

        # going through each segment
        for k in range(len(bounds)-1):
                
            bound_1 = bounds[k]
            bound_2 = bounds[k+1]
            # counting the stones
            stones_count = sum([1 if platform[i][j]=='O' else 0
                                for j in range(bound_1+1, bound_2)])
            # storing the count
            stone_count_list.append(stones_count)
            # indexing the segment
            for j in range(bound_1+1, bound_2):
                #print(i)
                pos_to_segment[(i,j)]['row_segment'] = k 
                pos_dict = pos_to_segment[(i,j)]
                pos_dict['row_segment'] = k 

            
        stones_by_row.append(stone_count_list)
    
    
    return stones_by_row, stones_by_col, pos_to_segment
     
            

        
def tilt_platform_columns(platform, walls_by_col, stone_by_row, stones_by_col,
                  pos_to_segment, north=True):
    
    R = len(platform)
    C = len(platform[0])
    
    stone_sybol = 'O'
    empty_symbol = '.'
    
    # tilting each column
    for j in range(C):
        
        # getting wall positions, and stones count for the current column
        wall_positions = walls_by_col[j]
        stones_counts = stones_by_col[j]
        
        # creating list of bounds, by extending the walls list
        bounds = [-1] + wall_positions + [R]
        # rearranging the stones within each segment
        for k in range(len(bounds)-1):
            
            # getting the bounds of the current segment
            bound_1 = bounds[k]
            bound_2 = bounds[k+1]
            
            # getting the stones count in the current segment
            segment_count = stones_counts[k]
            
            # moving all the stones on one side of the segment
            # and updating the tangent row segment
            if north:
                stones_range = range(bound_1+1, bound_1+1+segment_count)
            else:
                stones_range = range(bound_2-segment_count, bound_2)
            for i in stones_range:
                row_segment_index =  pos_to_segment[(i,j)]['row_segment']
                if platform[i][j] == empty_symbol:
                    stone_by_row[i][row_segment_index] += 1
                platform[i][j] = stone_sybol
            
            # fiiling the remainder of the segment
            # and updating the tangent row segment
            if north:
                empty_range = range(bound_1+1+segment_count, bound_2)
            else:
                empty_range = range(bound_1+1, bound_2-segment_count)
            for i in empty_range:
                row_segment_index =  pos_to_segment[(i,j)]['row_segment']
                if platform[i][j] == stone_sybol:
                    stone_by_row[i][row_segment_index] -= 1
                platform[i][j] = empty_symbol
            
    return stone_by_row, stones_by_col     
                      
def tilt_platform_rows(platform, walls_by_row, stone_by_row, stones_by_col,
                       pos_to_segment, west=True):
    
    R = len(platform)
    C = len(platform[0])
    
    stone_sybol = 'O'
    empty_symbol = '.'
    
    # tilting each row
    for i in range(R):
        
        # getting wall positions, and stones count for the current row
        wall_positions = walls_by_row[i]
        stones_counts = stones_by_row[i]
        
        # creating list of bounds, by extending the walls list
        bounds = [-1] + wall_positions + [C]
        # rearranging the stones within each segment
        for k in range(len(bounds)-1):
            
            # getting the bounds of the current segment
            bound_1 = bounds[k]
            bound_2 = bounds[k+1]
            
            # getting the stones count in the current segment
            segment_count = stones_counts[k]
            # moving all the stones on one side of the segment
            # and updating the tangent row segment
            if west:
                stones_range = range(bound_1+1, bound_1+1+segment_count)
            else:
                stones_range = range(bound_2-segment_count, bound_2)
            for j in stones_range:
                col_segment_index =  pos_to_segment[(i,j)]['col_segment']
                if platform[i][j] == empty_symbol:
                    stones_by_col[j][col_segment_index] += 1
                platform[i][j] = stone_sybol
            
            # fiiling the remainder of the segment
            # and updating the tangent row segment
            if west:
                empty_range = range(bound_1+1+segment_count, bound_2)
            else:
                empty_range = range(bound_1+1, bound_2-segment_count)
            for j in empty_range:
                col_segment_index =  pos_to_segment[(i,j)]['col_segment']
                if platform[i][j] == stone_sybol:
                    stones_by_col[j][col_segment_index] -= 1
                platform[i][j] = empty_symbol
            
    return stone_by_row, stones_by_col 
     

def run_cycle(platform, walls_by_row, walls_by_col, pos_to_segment,
              stones_by_row, stones_by_col):
    
    # North
    stones_by_row, stones_by_col  = tilt_platform_columns(platform, walls_by_col, 
                                                            stones_by_row, 
                                                            stones_by_col, 
                                                            pos_to_segment,
                                                            north=True)
        
    # West
    stones_by_row, stones_by_col  = tilt_platform_rows (platform, walls_by_row, 
                                                            stones_by_row, 
                                                            stones_by_col, 
                                                            pos_to_segment,
                                                            west=True)
    
    # South
    stones_by_row, stones_by_col  = tilt_platform_columns(platform, walls_by_col, 
                                                            stones_by_row, 
                                                            stones_by_col, 
                                                            pos_to_segment,
                                                            north=False)
    
    # East
    stones_by_row, stones_by_col  = tilt_platform_rows (platform, walls_by_row, 
                                                            stones_by_row, 
                                                            stones_by_col, 
                                                            pos_to_segment,
                                                            west=False)
    
    return stones_by_row, stones_by_col 

def find_period(platform, walls_by_row, walls_by_col, pos_to_segment,
                stones_by_row, stones_by_col, N=2000):
    
    results = {}
    
    # Running the cycle N times
    for i in range(N):
        
        stones_by_row, stones_by_col  = run_cycle(platform, walls_by_row, walls_by_col,
                                                  pos_to_segment,
                                                  stones_by_row, stones_by_col)
        
        
        
        result = compute_load(platform)
        if result not in results:
            results[result] = []
        results[result].append(i)

    # Computing the highest periodicity among the different values
    periods = {}
    for k, values in results.items():
        diffs = [values[i]-values[i-1] for i in range(1,len(values))]
        if diffs:
            periods[k] = max(diffs)
    period = max(periods.values())
    
    return period


def compute_load(platform):
    R = len(platform)
    C = len(platform[0])
    
    load = 0
    for i in range(R):
        for j in  range(C):
            if platform[i][j] == 'O':
                load += (R -i)
    
    return load
             
        

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
    # parsing the lines
    platform = parse_lines(lines)
    # getting the positions of the fixed rocks
    walls_by_row, walls_by_col = get_wall_positions(platform)
    # getting the positions of the fixed rocks
    stones_by_row, stones_by_col, pos_to_segment = get_stones_positions(platform, 
                                                        walls_by_row , walls_by_col)
    R = len(platform)
    C = len(platform[0])

    # tilting the platform north
    stones_by_row, stones_by_col  = tilt_platform_columns(platform, walls_by_col, 
                                                            stones_by_row, 
                                                            stones_by_col, 
                                                            pos_to_segment,
                                                            north=True)
    # computing the result
    result = compute_load(platform)
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    # Finding the periodicity
    N = 1000
    period = find_period(platform, walls_by_row, walls_by_col, pos_to_segment,
                stones_by_row, stones_by_col, N)
    print(f'period = {period}')
    # running the cycle the required number of times
    total_cycles = 10**9
    remaining_cycles =  (total_cycles - N) % 42
    for i in range(remaining_cycles):
        stones_by_row, stones_by_col  = run_cycle(platform, walls_by_row, walls_by_col,
                                                  pos_to_segment,
                                                  stones_by_row, stones_by_col)   
    # computing the result 
    result = compute_load(platform)
    print(result)

