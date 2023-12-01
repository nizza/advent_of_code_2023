import os
import argparse
import re

def find_digits_part_1(line):

    for i in range(len(line)):
        try:
            first_digit = int(line[i])
            break
        except:
            continue
        
    for i in range(len(line)-1, -1, -1):
        try:
            last_digit = int(line[i])
            break
        except:
            continue

    code = first_digit*10 + last_digit
    
    # No couple found
    return code

def find_digits_part_2(line):


    tokens = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
              '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
    
    # going through all the tokens
    all_token_pos_tuples = list()
    for token in tokens:
        # getting the position of all token occurrencies
        token_pos = [m.start() for m in re.finditer(token, line)]
        # creating a list of tuples (pos, token)
        token_pos_tuples = [(pos, token) for pos in token_pos]
        # adding tuples of current token to existing list
        all_token_pos_tuples.extend(token_pos_tuples)
    
    # sorting tokens by index
    all_token_pos_tuples = sorted(all_token_pos_tuples, key=lambda x: x[0])
    
    # Getting the first digit
    i, token = all_token_pos_tuples[0]
    # checking if token is a digit
    try:
        first_digit = int(token)
    # converting token to int
    except:
        first_digit = tokens.index(token) +1
        
    # Getting the last digit
    i, token = all_token_pos_tuples[-1]
    # checking if token is a digit
    try:
        last_digit = int(token)
    # converting token to int
    except:
        last_digit = tokens.index(token) +1
    
    code = first_digit*10 + last_digit
        
    return code
    




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()
    
    # Computing result for part 1
    print("Part 1:")
    result = sum([find_digits_part_1(line) for line in lines])
    print(result)
    print()
    
    # Computing result for part 2
    print("Part 2:")
    #find_digits_part_2(lines[0])
    result = sum([find_digits_part_2(line) for line in lines])
    print(result)
    #print()

