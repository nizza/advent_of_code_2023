import argparse


def parse_line(line):
    
    hand = line.split()[0]
    bet = int(line.split()[1])
    
    return {'hand': hand,
            'bet': bet}

def compute_cards_value(hand, card_symbols_sorted):
    
    # value of single cards
    card_val_tuples = zip(card_symbols_sorted, range(len(card_symbols_sorted)))
    card_val_dict = {k:v for (k,v) in card_val_tuples}
    
    # value of hand
    # card at the beginning have higher value
    hand_val = 0
    L = len(hand)
    for i in range(L):
        card_val = card_val_dict[hand[i]]
        hand_val += card_val * len(card_symbols_sorted)**(L-1-i)
    
    return hand_val 

def score_play(play, card_symbols_sorted, handle_jokers=False):
    """
    Compute a score for each hand, composed by  two factors:
     - the type of hand ('Five of a kind', 'Full house',..)
     - the value of the cards
     
     The aggregate score is computed in such a way that, all the hands for 
     a given type of hand (e.g: 'Five of a kind') have a higher total score
     than all the other possible hands with a lower rank type of hand
     (e.g. 'Full house', Three of a kind, ...)
    """
    
    hand = play['hand']
    L = len(hand)
    
    #################
    # value of cards
    #################
    hand_val = compute_cards_value(hand, card_symbols_sorted)
        
        
    #################
    # type of hand
    #################
    
    # computing the cards that are repeated
    count = dict()
    for card in hand:
        if card not in count:
            count[card] = 1
        else:
            count[card] += 1
    
    if handle_jokers:
        # processing the jokers
        # all jokers are will be considered as the most common card 
        if 'J' in count:
            jokers = count['J']
            count['J'] = 0
            sorted_tuples = sorted(count.items(), key=lambda x: x[1], reverse=True)
            most_common_card = sorted_tuples[0][0]
            count[most_common_card] += jokers
            
    # computing a score for each card, appearing more than once
    # the total score should respect the original ranking
    type_score = 0
    b = 3
    for  v in count.values():
        if v > 1:
            type_score += b**v
    # multiplying the type score by the max hand value
    # to guarantee that type score is always more important than
    # hand value     
    type_score *= len(card_symbols_sorted)**L
    
    
    #################
    # merging the scores
    #################
    total_score = type_score + hand_val
    return total_score
        

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
    plays = [parse_line(line) for line in lines]
    # card symbols sorted
    card_symbols_sorted  = ['A', 'K', 'Q', 'J', 'T', '9', '8',
                            '7', '6', '5', '4', '3', '2']
    card_symbols_sorted.reverse()
    # Computing the scores
    for play in plays:
        play['score'] = score_play(play, card_symbols_sorted)
    # computing the wins
    plays = sorted(plays, key=lambda x: x['score'])
    for i in range(len(plays)):
        play = plays[i]
        play['win'] = play['bet'] * (i+1)
    # total win
    total_win = sum([play["win"] for play in plays])
    print(total_win)
    print()
    
    #computing result for part 2
    print("part 2:")
    # card symbols sorted
    card_symbols_sorted  = ['A', 'K', 'Q', 'T', '9', '8', '7',
                            '6', '5', '4', '3', '2', 'J']
    card_symbols_sorted.reverse()
    # Computing the scores
    for play in plays:
        play['score'] = score_play(play, card_symbols_sorted, handle_jokers=True)
    # computing the wins
    plays = sorted(plays, key=lambda x: x['score'])
    for i in range(len(plays)):
        play = plays[i]
        play['win'] = play['bet'] * (i+1)
    # total win
    total_win = sum([play["win"] for play in plays])
    print(total_win)
    print()

