import os
import argparse
import re

def parse_line(line):
    
    pattern = line.split()[0]
    damages_list = [int(x) for x in line.split()[1].split(',')]
    
    return {'pattern': pattern,
            'damages_list': damages_list}

def parse_line_unfolded(line):
    
    pattern = '?'.join(5*[line.split()[0]])
    damages_list = 5*[int(x) for x in line.split()[1].split(',')]
    
    return {'pattern': pattern,
            'damages_list': damages_list}

def count_solutions(pattern, damages_list, cache={}):
    
    if (pattern, tuple(damages_list)) in cache:
        return cache[(pattern, tuple(damages_list))], cache
    
    #print(pattern,  damages_list)
    
    # if damages_list is empty, no '#' is allowed in the pattern
    if len(damages_list)==0 :
        return 0 if '#' in pattern else 1, cache
    
    # if pattern is empty, but there are still damage item to fit
    # no solution is possible
    if len(pattern)==0 :
        return 0 , cache
    
    ########################################################
    # Looking for solution including the current character #
    ########################################################
    dam_length = damages_list[0]
    #print('[\?\#]{' + str(dam_length) +'}[^\#]?$')
    regex = re.compile('[\?\#]{' + str(dam_length) +'}[^\#]?$')
    if regex.match(pattern[:dam_length+1]):
        #print('yo')
        # if first damage item is matched then looking for solutions
        # using the remainder of the pattern, and damage items
        solutions_1, cache = count_solutions(pattern[dam_length+1:], damages_list[1:], cache)
    else:
        # no solutions starting at the current character
        solutions_1 = 0
        
    ########################################################
    # Looking for solution excluding the current character #
    ########################################################
    if pattern[0] != '#':
        solutions_2, cache = count_solutions(pattern[1:], damages_list, cache)
    else:
        solutions_2 = 0
    
    # updating cache
    cache[(pattern, tuple(damages_list))] = solutions_1 + solutions_2
        
    return solutions_1 + solutions_2, cache

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
    records = [parse_line(line) for line in lines]
    # counting the solutions
    solutions_count = []
    cache = {}
    for record in records:
        sol, cache = count_solutions(record['pattern'],
                                      record['damages_list'],
                                      cache)
        solutions_count.append(sol)
    # computing the result
    result = sum(solutions_count)
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    # parsing the lines
    records = [parse_line_unfolded(line) for line in lines]
    # counting the solutions
    solutions_count = []
    cache = {}
    for record in records:
        sol, cache = count_solutions(record['pattern'],
                                      record['damages_list'],
                                      cache)
        solutions_count.append(sol)
    # computing the result
    result = sum(solutions_count)
    print(result)
    print()

