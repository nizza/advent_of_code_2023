
import argparse

# a dictionary mapping symbol to the corresponding direction vector
# the order of the components is y, x 
DIR_DICT = { '|': (1, 0),
             '-': (0, 1)
}

def scalar_product(a, b):    
    return a[0]*b[0] + a[1]*b[1]

def rotate_90(direction, clockwise=True):
    
    if clockwise:
        A = [(0,1), (-1,0)]
    else:
        A = [(0,-1), (1,0)]
    
    return (scalar_product(direction, A[0]), scalar_product(direction, A[1]))

def rotate_90_clock(direction):
    return rotate_90(direction, clockwise=True)

def rotate_90_anticlock(direction):
    return rotate_90(direction, clockwise=False)

def update_dir(beam_dir, symbol):
    
    # no change of direction
    if symbol == '.':
        return [beam_dir]

    # no change, or beam split
    if symbol in ['-', '|']:
        
        # getting the vector for this symbol
        s_dir = DIR_DICT[symbol]
        
        # computing the scalar product
        sp = scalar_product(beam_dir, s_dir)
        # split, or neutral depending on the result
        if sp == 0:
            #split
            return [rotate_90_clock(beam_dir), rotate_90_anticlock(beam_dir)]
        else:
            # neutral
            return [beam_dir]
    
    # 90 anticlock for vertical beams
    # 90 anticlock for vertical beams
    if symbol == "\\":
        
        if beam_dir[1] == 0:
            return [rotate_90_anticlock(beam_dir)]
        else:
            return [rotate_90_clock(beam_dir)]
        
    # 90 clock for vertical beams
    # 90 anticlock for horizontal beams
    if symbol == "/":
        
        if beam_dir[1] == 0:
            return [rotate_90_clock(beam_dir)]
        else:
            return [rotate_90_anticlock(beam_dir)]
    
def energize_field(field, pos, beam_dir, energy_map={}):
    
    R = len(field)
    C = len(field[0])
    
    # checking if still inside field
    if pos[0]<0 or pos[0]>=R or pos[1]<0 or pos[1]>=C:
        return energy_map
    
    # stopping if the same position has been visited in the same direction
    if pos in energy_map and beam_dir in energy_map[pos]:
        return energy_map
    
    # energizing the starting position
    if pos not in energy_map:
        energy_map[pos] = set()
    energy_map[pos].add(beam_dir)
    
    # updating the direction and position(s)
    symbol = field[pos[0]][pos[1]]
    directions = update_dir(beam_dir, symbol)
    positions = []
    for beam_dir in directions:
        p = (pos[0] + beam_dir[0], pos[1] + beam_dir[1])
        positions.append(p)

    # going through the field while there is no bifurcation
    # calling recursively energize_field in case of bifurcation
    while len(directions) == 1:
        
        beam_dir = directions[0]
        pos = positions[0]
        
        # checking if still inside field
        if pos[0]<0 or pos[0]>=R or pos[1]<0 or pos[1]>=C:
            return energy_map
        
        # stopping if the same position has been visited in the same direction
        if pos in energy_map and beam_dir in energy_map[pos]:
            return energy_map
        
        # energizing the starting position
        if pos not in energy_map:
            energy_map[pos] = set()
        energy_map[pos].add(beam_dir)

        # updating the direction and position(s)
        symbol = field[pos[0]][pos[1]]
        directions = update_dir(beam_dir, symbol)
        positions = []
        for beam_dir in directions:
            p = (pos[0] + beam_dir[0], pos[1] + beam_dir[1])
            positions.append(p)
    
    # exploring the directions that have not be followed yet 
    for beam_dir, pos in zip(directions, positions):
        energy_map = energize_field(field, pos, beam_dir, energy_map)
    
    return energy_map

def compute_max_energy(field):
    
    R = len(field)
    C = len(field[0])
    
    # initializing the results set
    results = []
    
    # going through the first row
    initial_dir = (1, 0)
    for j in range(C):
        initial_pos = (0, j)
        # energizing the field
        energy_map = energize_field(field, initial_pos, initial_dir, energy_map={})
        # computing the total energy
        energy = len(energy_map)
        # storing the result
        results.append(energy)
    
    # going through the last row
    initial_dir = (-1, 0)
    for j in range(C):
        initial_pos = (R-1, j)
        # energizing the field
        energy_map = energize_field(field, initial_pos, initial_dir, energy_map={})
        # computing the total energy
        energy = len(energy_map)
        # storing the result
        results.append(energy)
        
    # going through the first column
    initial_dir = (0, 1)
    for i in range(R):
        initial_pos = (i, 0)
        # energizing the field
        energy_map = energize_field(field, initial_pos, initial_dir, energy_map={})
        # computing the total energy
        energy = len(energy_map)
        # storing the result
        results.append(energy)
        
    # going through the last column
    initial_dir = (0, -1)
    for i in range(R):
        initial_pos = (i, C-1)
        # energizing the field
        energy_map = energize_field(field, initial_pos, initial_dir, energy_map={})
        # computing the total energy
        energy = len(energy_map)
        # storing the result
        results.append(energy)
        
    return max(results)

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
    # energizing the field
    initial_pos = (0, 0)
    initial_dir = (0, 1)
    energy_map = energize_field(lines, initial_pos, initial_dir, energy_map={})
    # computing the result
    result = len(energy_map)
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    result = compute_max_energy(lines)
    print(result)
    print()
            

