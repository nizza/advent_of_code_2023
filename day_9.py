import os
import argparse
import re

def parse_line(line):
    
    sequence = [int(x) for x in line.split()]
    return sequence

def diff_sequence(sequence):
    
    if len(sequence) == 1:
        return [0]
    
    res = []
    for i in range(1, len(sequence)):
        diff = sequence[i] - sequence[i-1]
        res.append(diff)
    return res

    
def are_all_zeros(sequence):
    
    # # base case
    # if len(sequence) == 1:
    #     return sequence[0] == 0
    
    res = True
    for i in range(len(sequence)):
        if sequence[i] != 0:
            res = False
            break
    return res

def make_diff_stack(sequence):
    
    sequences_stack = [sequence]
    all_zeros = False
    while not all_zeros:
        sequence = diff_sequence(sequence)
        sequences_stack.append(sequence)
        all_zeros = are_all_zeros(sequence)
        
    return sequences_stack

def predict_next(sequence):
    
    # check if all zeros
    if are_all_zeros(sequence):
     return 0
 
    sequences_stack = make_diff_stack(sequence)
        
    next_value = 0
    N = len(sequences_stack)
    for i in range(N-1, -1, -1):
        sequence =  sequences_stack[i]
        next_value += sequence[-1]
        
    return next_value
  
def predict_prev(sequence):
    
    # check if all zeros
    if are_all_zeros(sequence):
     return 0
 
    sequences_stack = make_diff_stack(sequence)
         
    prev_value = 0
    N = len(sequences_stack)
    for i in range(N-1, -1, -1):
        sequence =  sequences_stack[i]
        prev_value = sequence[0] - prev_value
        
    return prev_value
      

        

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
    sequences = [parse_line(line) for line in lines]
    # Predicting next value for each sequence
    next_values = [predict_next(s) for s in sequences ]
    # computing result
    result = sum(next_values)
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    # Predicting previous value for each sequence
    prev_values = [predict_prev(s) for s in sequences ]
    # computing result
    result = sum(prev_values)
    print(result)
    print()

