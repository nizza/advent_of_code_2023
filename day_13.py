
import argparse


def parse_lines(lines):
    
    patterns = list()
    current_pattern = list()
    for line in lines:
        if line == '':
            patterns.append(current_pattern)
            current_pattern = list()
        else:
            current_pattern.append(line)
            
    patterns.append(current_pattern)
    
    return patterns

def compare_columns(pattern, col_1, col_2):

    R = len(pattern)
    
    diffs = 0
    for i in range(R):
        if pattern[i][col_1] != pattern[i][col_2]:
            diffs += 1
    return diffs

def compare_rows(pattern, row_1, row_2):

    C = len(pattern[0])
    
    diffs = 0
    for j in range(C):
        if pattern[row_1][j] != pattern[row_2][j]:
            diffs += 1
    return diffs


def find_center_column(pattern, target_smudges=0):
    
    C = len(pattern[0])
    
    # center column
    for j in range(C-1):
        
        # left and right columns
        l = j 
        r = j + 1
        
        # moving left and right columns in the opposite directions
        # while they contain the same elements (except target smudges)
        diffs = 0
        while l>=0 and r<C:
            
            diffs += compare_columns(pattern, l, r)
            if diffs > target_smudges:
                break
            else:
                l -= 1
                r += 1
        
        if diffs == target_smudges:
            return j+1
    
    # no mirror center column found
    return 0


def find_center_row(pattern, target_smudges=0):
    
    R = len(pattern)
    
    # center row
    for i in range(R-1):
        
        # up and down rows
        u = i 
        d = i + 1
        
        # moving up and down columns in the opposite directions
        # while they contain the same elements  (except target smudges)
        diffs = 0
        while u>=0 and d<R:
            
            diffs += compare_rows(pattern, u, d)
            if diffs > target_smudges:
                break
            else:
                u -= 1
                d += 1
        
        if diffs == target_smudges:
            return i+1
    
    # no mirror center row found
    return 0 
        

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
    patterns = parse_lines(lines)
    # Computing center rows and columns
    centers = [(find_center_column(pattern), find_center_row(pattern))
               for pattern in patterns]
    # Computing the summary score
    result = (sum([center[0] for center in centers]) +
              100*sum([center[1] for center in centers]) 
             )
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    centers = [(find_center_column(pattern, target_smudges=1), 
                find_center_row(pattern, target_smudges=1))
               for pattern in patterns]
    # Computing the summary score
    result = (sum([center[0] for center in centers]) +
              100*sum([center[1] for center in centers]) 
             )
    print(result)
    print()

