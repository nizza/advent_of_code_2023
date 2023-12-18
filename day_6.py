import argparse
import math

def parse_lines(lines):
    
    times = lines[0].split(':')[1].strip().split()
    distances = lines[1].split(':')[1].strip().split()
    
    races = []
    for t,d in zip(times, distances):
        race = {'time': int(t),
                'distance': int(d)}
        races.append(race)
    
    return races

def parse_lines_2(lines):
    
    time = lines[0].split(':')[1].replace(' ', '')
    distance = lines[1].split(':')[1].replace(' ', '')
 
    race = {'time': int(time),
            'distance': int(distance)}
    
    return race

def compute_solutions(race):
    
    T = race['time']
    record = race['distance']
    # distance covered when charging for t_charge seconds
    dist_covered = lambda t_charge:  t_charge*T - t_charge**2
    distances = [ dist_covered(t_charge)
                 for t_charge in range(1,T)]
    
    # races breaking the record
    record_breakers = [d for d in distances if d> record ]
    
    return len(record_breakers)
    
def compute_solution(race):
    
    T = race['time']
    record = race['distance']
    
    # Solving 2nd degree inequality
    a = 1
    b = -T
    c = record
    delta = math.sqrt(b**2-4*a*c)
    x1 = (-b - delta) / (2*a)
    x2 = (-b + delta) / (2*a)
    
    # computing the number of int solutions in the range
    return math.floor(x2) - math.ceil(x1) + 1 

        

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
    races = parse_lines(lines)
    # Computing the number of record preakers for each race
    record_breakers = [compute_solutions(race) for race in races]
    # Computing the result
    result = 1
    for x in record_breakers:
        result *= x
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    # parsing the lines
    race = parse_lines_2(lines)
    # computing the solution
    print(compute_solution(race))


