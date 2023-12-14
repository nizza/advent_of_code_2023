import os
import argparse
import re

def is_game_possible(red, green, blue,  trials):
    
    for trial in trials:
        if (trial['red'] > red or
            trial['green'] > green or
            trial['blue'] > blue ):
            return False
    return True

def get_minimum_set(trials):
    
    minimum_set = {'red':0, 'green':0, 'blue':0}
    for trial in trials:
        for k in trial.keys():
            if trial[k]>minimum_set[k]:
                minimum_set[k] = trial[k] 
    return minimum_set

def power_of_game(minimum_set):
    res = 1
    for v in minimum_set.values():
        res*=v
    return res

def parse_line(line):
    game = int(line.split(':')[0].split()[1])
    trials = line.split(':')[1].split(';')
    make_dict = lambda: {'red':0, 'green':0, 'blue':0}
    res = list()
    for trial in trials:
        trial_dict = make_dict()
        for entry in trial.split(','):
            key = entry.strip().split()[1]
            value = int(entry.strip().split()[0])
            trial_dict[key] = value

        # Adding dictionary for current trial to results list
        res.append(trial_dict)
    
    return {'game': game, 'trials': res}


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
    # parsing the lines
    games = [parse_line(line) for line in lines]
    # founding possible games
    possible_games = [game['game'] for game in games 
                      if is_game_possible(12, 13, 14, game['trials']) ]
    result = sum(possible_games)
    print(result)
    print()
    
    # Computing result for part 2
    print("Part 2:")
    # computing the power of the games
    power_of_games = [power_of_game(get_minimum_set(game['trials']))
                      for game in games]
    result = sum(power_of_games)
    print(result)
    #print()

