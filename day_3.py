import os
import argparse
import re

def find_numbers(lines):
    
    # exctracting number of rows and columns
    R = len(lines)
    C = len(lines[0])
    
    numbers_list = list()
    current_number = ''
    for i in range(R):
        for j in range(C):
            x = lines[i][j]
            if x.isdigit():
                current_number += x
                # checking if first digit of the number
                if len(current_number) == 1:
                    current_number_start = (i, j)
            # storing number, if necessary
            elif  len(current_number) > 0:
                numbers_list.append({'number': current_number,
                                     'position': current_number_start})
                current_number = ''
    
    # storing last number, if necessary
    if  len(current_number) > 0:
        numbers_list.append({'number': current_number,
                             'position': current_number_start})

    return numbers_list

def find_part_numbers(numbers, lines):
    
    part_numbers = list()
    for n in numbers:
        
        number = n['number']
        i_start = n['position'][0]
        j_start = n['position'][1]
        
        # getting the coordinates of the neigbors
        neigbors = list()
        # left neighbors
        neigbors.extend([(i_start-1, j_start-1),    
                         (i_start, j_start-1),
                         (i_start+1, j_start-1)
                         ])
        # above and below neighbors
        for j in range(j_start, j_start+len(number)):
            neigbors.extend([(i_start-1, j),
                            (i_start+1, j)
                            ])
        # right neighbors
        j_end = j_start+len(number)
        neigbors.extend([(i_start-1, j_end),    
                         (i_start, j_end),
                         (i_start+1, j_end)
                         ])
        
        # going through the list of neighbors
        is_product = False
        for point in neigbors:
            i,j = point
            try:
                if ((not lines[i][j].isdigit()) and
                    lines[i][j] != '.' ):
                    is_product = True
                    break
            except:
                pass
        
        # keeping number if a product identifier was found
        if is_product:
            part_numbers.append(int(number))
        
    return part_numbers


def find_gears(numbers, lines):
    
    gears_candidates = dict()
    for n in numbers:
        
        number = n['number']
        i_start = n['position'][0]
        j_start = n['position'][1]
        
        # getting the coordinates of the neigbors
        neigbors = list()
        # left neighbors
        neigbors.extend([(i_start-1, j_start-1),    
                         (i_start, j_start-1),
                         (i_start+1, j_start-1)
                         ])
        # above and below neighbors
        for j in range(j_start, j_start+len(number)):
            neigbors.extend([(i_start-1, j),
                            (i_start+1, j)
                            ])
        # right neighbors
        j_end = j_start+len(number)
        neigbors.extend([(i_start-1, j_end),    
                         (i_start, j_end),
                         (i_start+1, j_end)
                         ])
        
        # going through the list of neighbors
        is_product = False
        for point in neigbors:
            i,j = point
            try:
                if lines[i][j] == '*':
                    if point in gears_candidates:
                        gears_candidates[point].append(int(number))
                    else:
                        gears_candidates[point] = [int(number)]
            except:
                pass
        
    # filtering to keep only gears with 2 components
    gears = {k:v for k,v in gears_candidates.items() 
             if len(v)==2}
        
    return gears

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
    numbers = find_numbers(lines)
    # searching for part numbers
    part_numbers = find_part_numbers(numbers, lines)
    result = sum(part_numbers)
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    # finding the gears
    gears = find_gears(numbers, lines) 
    # finding the gears ratio
    gears_ratios = [v[0]*v[1] for v in gears.values()]
    result = sum(gears_ratios)
    print(result)
    #print()

