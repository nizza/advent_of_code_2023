import os
import argparse
import re

def print_tuples(tuples):
    res_list = []
    for t in tuples:
        res_list.append('({:.2e}, {:.2e})'.format(t[0], t[1]))
    res = f'[{",".join(res_list)} ]'
    print(res)

def print_dictionaries(dictionaries):
    res_list = []
    for d in dictionaries:
        dict_list = []
        for k,v in d.items():
            dict_list.append('"{}": {:.2e}'.format(k, v))
        res_list.append("{ " + ",".join(dict_list) + " }")

    res = f'[{",".join(res_list)} ]'
    print(res)

def check_overlaps_seed(seeds_list):
    
    checked_list = list()
    for seed in seeds_list:
        for checked_seed in checked_list:
            if ((seed[0] >= checked_seed[0]) and 
                (seed[0] < checked_seed[0]+checked_seed[1])):
                return True 
            if ((seed[0]+seed[1] > checked_seed[0]) and 
                (seed[0]+seed[1] < checked_seed[0]+checked_seed[1])):
                return True   
                
        checked_list.append(seed)
    return False


def parse_seeds(line):
    
    seeds = line.split(':')[1].split()
    seeds = [int(seed) for seed in seeds]
    
    return seeds

def parse_seeds_v2(line):
    
    seeds = parse_seeds(line)
    
    # grouping into tuples
    starts =  seeds[0::2]
    lengths = seeds[1::2]
    range_tuples = list(zip(starts, lengths))
    
    return range_tuples 
    

def parse_dict_lines(lines):
    
    # exctracting name
    name = lines[0].split()[0]
    
    # exctracting the mappings
    mappings = list()
    for line in lines[1:]:
        des_start, source_start, length = map(int, line.split())
        mappings.append({'des_start': des_start,
                         'source_start': source_start, 
                         'length': length})
    
    return {'name': name,
            'mappings': mappings}

def parse_lines(lines):
    
    # parsing the dictionaries
    dictionaries_list = list()
    current_lines = list()
    for line in lines[2:]:
        if len(line.strip()) == 0:
            parsed_dict = parse_dict_lines(current_lines)
            dictionaries_list.append(parsed_dict)
            current_lines = list()
        else:
            current_lines.append(line)
    # parsing the last dictionary
    parsed_dict = parse_dict_lines(current_lines)
    dictionaries_list.append(parsed_dict)
    
    return dictionaries_list
    

def map_values(values, mappings):
    
    result = list()
    for value in values:
        mapped_value = value
        for mapping in mappings:
            if ((value >= mapping['source_start']) and
                (value < (mapping['source_start'])+mapping['length'])) :
                mapped_value = value - mapping['source_start'] + mapping['des_start']
                break
        result.append(mapped_value)

    return result

def map_segment(segment, mappings, result=[]):
    
    # no mapping available, the segment is mapped to itself
    if len(mappings) == 0:
        mapped_segment = (segment[0], segment[1])
        result.append(mapped_segment)
        return mappings, result
    
    mapping_index = 0
    mapping = mappings[mapping_index]
    
    # skipping all the mappings that end before the current segment 
    while (mapping['source_start'] + mapping['length'] ) <= segment[0]:
        mapping_index += 1
        if mapping_index < len(mappings):
            # moving to next mapping
            mapping = mappings[mapping_index]
        else:
            # mappings finished without any overlap
            mapping = None
            break
    
    # No overlapping with mappings; the segment is mapped to itself
    if mapping == None:
        mapped_segment = (segment[0], segment[1])
        result.append(mapped_segment)
        return [], result
    
    # Creating subsegment for the part that preceeds the mapping
    if mapping['source_start'] > segment[0]:
        subsegment_start = segment[0]
        subsegment_end = min(segment[0]+segment[1], 
                             mapping['source_start'])
        mapped_segment = (subsegment_start, subsegment_end-subsegment_start)
        result.append(mapped_segment)
        # returning if the segment is completed
        if subsegment_end == (segment[0]+segment[1]):
            return mappings[mapping_index:], result 
        # updating the segment yet to be mapped
        else:
            segment_end = segment[0] + segment[1]
            segment_start = subsegment_end
            segment =  (segment_start, segment_end - segment_start)
            
    
    # Creating subsegment for the mapping
    # finding the end of the current segment that can go through the current mapping
    if mapping['source_start'] < (segment[0]+segment[1]):
        subsegment_start = max(mapping['source_start'], segment[0])
        subsegment_end = min(segment[0]+segment[1], 
                            (mapping['source_start']+mapping['length']))
        mapped_start =  subsegment_start -mapping['source_start']+ mapping['des_start']
        mapped_length = subsegment_end - subsegment_start
        result.append((mapped_start, mapped_length))
        # Extracting the subsegment yet to be mapped
        if subsegment_end < segment[0]+segment[1]:
            segment = (subsegment_end, segment[0]+segment[1]-subsegment_end)
            return map_segment(segment, mappings[mapping_index+1:], result)
        else:
            return mappings[mapping_index:], result
    else:
         return mappings[mapping_index:], result 
    

def map_segments(segments, mappings):
    
    # sorting the segments
    segments = sorted(segments, key= lambda x:x[0])
    # sorting the mappings
    mappings = sorted(mappings, key= lambda x:x['source_start'])
    
    # print_dictionaries(mappings)
    # print_tuples(segments)
    
    # index of the current mapping
    result=[]
    for segment in segments:
        mappings, result = map_segment(segment, mappings, result)
               
    return result
        

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
    # parsing the seeds
    seeds = parse_seeds(lines[0])
    # parsing the lines
    dictionaries_list = parse_lines(lines[2:])
    # Mapping values
    values = seeds
    for dictionary in dictionaries_list:
        values  = map_values(values, dictionary['mappings'])
    print(min(values))
    
    # Computing result for part 2
    print("Part 2:")
    # parsing the seeds
    seeds = parse_seeds_v2(lines[0])
    #Mapping values
    segments = seeds
    for dictionary in dictionaries_list:
        segments  = map_segments(segments, dictionary['mappings'])
    # sorting the segments
    segments = sorted(segments, key= lambda x:x[0])  
    # extracting the beginning of the 1st segment
    first_location = segments[0][0]
    print(first_location)

