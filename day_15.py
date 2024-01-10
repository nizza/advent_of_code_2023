import os
import argparse
import re

def parse_line(line):
    
    steps = line.split(',')
    
    return steps

def compute_hash(sequence):
    
    val = 0
    for c in sequence:
        asc_val = ord(c)
        val += asc_val
        val *= 17
        val = val % 256
    
    return val

def perform_steps(steps):
    
    # initializing the lens boxes
    boxes = [{} for i in range(256)]
    
    # performing all the steps
    for step in steps:
        
        # remove command
        if '-' in step:
            label = step.split('-')[0]
            # getting the current box
            index = compute_hash(label)
            box = boxes[index]
            if label in box:
                # getting the details of the lens
                lens = box[label]
                pos = lens['pos']
                # removing the lens
                box.pop(label)
                # adjusting the positions of the remaining lenses
                for lens_i in box.values():
                    if lens_i['pos'] >= pos:
                        lens_i['pos'] -= 1
            
        # add command 
        else:
            label = step.split('=')[0]
            focal_length = int(step.split('=')[1])
            # getting the current box
            index = compute_hash(label)
            box = boxes[index]
            # replacing the lens
            if label in box:
                lens = box[label]
                lens['focal_length'] = focal_length
            # adding the lens
            else:
                lens = {'focal_length': focal_length,
                        'pos': len(box)+1}
                box[label] = lens
    
    return boxes

def compute_focusing_power(boxes):
    
    fp = 0
    for i in range(len(boxes)):   
        box = boxes[i]
        for lens in box.values():
            fp += (i+1) * lens['pos'] * lens['focal_length']
    
    return fp
    
              
        

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
    # parsing the line
    steps = parse_line(lines[0])
    # Computing the hash codes
    hash_codes = [compute_hash(step) for step in steps]
    # Computing the results
    result = sum(hash_codes)
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    # performing the steps
    boxes = perform_steps(steps)
    #print(boxes)
    # computing the result
    focusing_power = compute_focusing_power(boxes)
    print(focusing_power)
    print()

