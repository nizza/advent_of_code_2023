import argparse

def expand_lines(lines):
    
    # number of rows and columns
    R = len(lines)
    C = len(lines[0])
    
    rows_to_expand = list()
    cols_to_expand = list()
    
    # finding empty rows
    for i in range(R):
        to_expand = True
        for j in range(C):
            if lines[i][j] != '.':
                to_expand = False
                break
        if to_expand:
            rows_to_expand.append(i)
    
    # finding empty columns
    for j in range(C):
        to_expand = True
        for i in range(R):
            if lines[i][j] != '.':
                to_expand = False
                break
        if to_expand:
            cols_to_expand.append(j)
                    
    return rows_to_expand, cols_to_expand
    #return result

def find_galaxies(lines):
    
    # number of rows and columns
    R = len(lines)
    C = len(lines[0])

    galaxies = list()
    
    for i in range(R):
        for j in range(C):
            if lines[i][j] == '#':
                galaxies.append((i,j))
    
    return galaxies


def make_pairs(points):
    
    L = len(points)
    
    pairs = list()
    for a in range(L-1):
        for b in range(a+1,L):
            pairs.append((points[a], points[b]))
            
    return pairs


def compute_distance(point_a, point_b, expanded_rows_dict, expanded_cols_dict):
      
    # distance along y axis
    y_start = min(point_a[0], point_b[0])
    y_end = max(point_a[0], point_b[0])
    dy = 0
    for i in range(y_start, y_end):
        if i in expanded_rows_dict:
            dy += expanded_rows_dict[i]
        else:
            dy += 1

    # distance along x axis
    x_start = min(point_a[1], point_b[1])
    x_end = max(point_a[1], point_b[1])
    dx = 0
    for j in range(x_start, x_end):
        if j in expanded_cols_dict:
            dx += expanded_cols_dict[j]
        else:
            dx += 1
    
    return dx+dy

        

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
    # Computing empty rows and columns
    rows_to_expand, cols_to_expand = expand_lines(lines)
    # Computing the positions of the galaxies
    galaxies = find_galaxies(lines)
    # Creating pairs of galaxies
    galaxies_pairs = make_pairs(galaxies)
    # Creating distance dictionaries for empty rows and cols
    rows_to_expand_dict = {i:2 for i in rows_to_expand}
    cols_to_expand_dict = {j:2 for j in cols_to_expand}
    # Computing the distances between pairs of galaxies
    galaxies_pairs_dist = {(p1,p2): compute_distance(p1,p2, 
                                                     rows_to_expand_dict,
                                                     cols_to_expand_dict)
                           for (p1,p2) in galaxies_pairs}
    # Computing the result
    result = sum(galaxies_pairs_dist.values())
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    # Creating distance dictionaries for empty rows and cols
    rows_to_expand_dict = {i:10**6 for i in rows_to_expand}
    cols_to_expand_dict = {j:10**6 for j in cols_to_expand}
    galaxies_pairs_dist = {(p1,p2): compute_distance(p1,p2, 
                                                     rows_to_expand_dict,
                                                     cols_to_expand_dict)
                           for (p1,p2) in galaxies_pairs}
    # Computing the result
    result = sum(galaxies_pairs_dist.values())
    print(result)
    print()

