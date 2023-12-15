import os
import argparse
import re

def parse_line(line):
    
    card_number = int(line.split(':')[0].split()[1])
    winning_numbers = line.split(':')[1].split('|')[0].split()
    played_numbers = line.split(':')[1].split('|')[1].split()
    
    return {'card_number': card_number,
            'winning_numbers': winning_numbers,
            'played_numbers': played_numbers}


def compute_card_matches(card):
    
    # counting matches
    count = 0
    for number in card['played_numbers']:
        if number in card['winning_numbers']:
            count += 1
    
    return count

def compute_card_value(card):
    
    # counting matches
    count = compute_card_matches(card)
    
    # computing score
    score = 2**(count-1) if count >0 else 0
    
    return score
    
    
def process_cards(cards):
    
    # Cumputing the number of matches for each card
    cards_matches = {card['card_number']:compute_card_matches(card)
                     for card in cards}
    
    # creating a stack from the original cards
    stack = list(cards)
    
    count = 0
    while count < len(stack):
        
        # getting next card
        card = stack[count]
        card_number = card['card_number']
        
        # getting number of matches
        #matches = compute_card_matches(card)
        matches = cards_matches[card_number]
        
        # adding prize cards to the stack
        start_card = card_number +1
        end_card = min(start_card+matches, len(cards)+1)
        for i in range(start_card, end_card):
            prize_card = cards[i-1]
            stack.append(prize_card)
    
        count+=1
    
    return count 
        
        

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
    cards = [parse_line(line) for line in lines]
    # Computing the scores
    scores = [compute_card_value(card) for card in cards]
    result = sum(scores)
    print(result)
    print()
    
    #computing result for part 2
    print("part 2:")
    result = process_cards(cards) 
    print(result)
    #print()

