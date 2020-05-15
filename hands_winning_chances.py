import numpy as np
import tqdm
import time
from itertools import combinations


# strongness:
# H, value
# 1P, value
# 2P, values
# T, value
# S, value
# Fl, value
# Fu, values
# Q, value
# SFl, value

# card = value_color: 5_c


def get_value_and_color(card):
    # return int(card.split('_')[0]), card.split('_')[1]

    str_to_value = {
        '1': 14,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '0': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    return str_to_value[card[0]], card[2]

def get_values(cards):
    str_to_value = {
        '1': 14,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '0': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    return [str_to_value[card[0]] for card in cards]

def get_colors(cards):
    return [card[2] for card in cards]

time_keeper = {
    'SFl': 0,
    'Q': 0,
    'Fu': 0,
    'Fl': 0,
    'S': 0,
    'T': 0,
    'P': 0,
}


def get_cards_value_2(cards_set):

    def check_pairs(cards):
        pairs = []
        card_values = get_values(cards)

        for i in range(len(cards)-1):
            if card_values.count(card_values[len(cards)-1-i]) >= 2:
                pairs.append(card_values[len(cards)-1-i])
                card_values.remove(card_values[len(cards)-1-i])
        if len(pairs) > 0:
            card_values = list(set(card_values) - set(pairs))
            return str(min(len(pairs), 2)) + 'P', sorted(pairs[:2], reverse=True), \
                   sorted(card_values+pairs[2:], reverse=True)[:5 - 2 * min(len(pairs), 2)]
        else:
            return None

    def check_triple(cards):
        left_cards = get_values(cards)
        triples = []
        for i in range(len(cards)-2):
            if left_cards.count(left_cards[i]) == 3:
                triples.append(left_cards[i])
        if len(triples) > 0:
            val = sorted(triples)[-1]
            left_cards = list(filter(lambda a: a != val, left_cards))
            return 'T', [val], sorted(left_cards, reverse=True)[:2]
        return None

    def check_straight(cards):
        cards_value = get_values(cards)
        sorted_cards = sorted(list(set(cards_value)))
        if len(sorted_cards) > 4:
            for i in range(len(sorted_cards) - 1, 3, -1):
                val = sorted_cards[i]
                if val - 4 == sorted_cards[i-4] == sorted_cards[i-3] - 1 == sorted_cards[i-2] - 2 \
                        == sorted_cards[i-1] - 3:
                    return 'S', [val, val-1, val-2, val-3, val-4], []
                elif (val - 3 == sorted_cards[i-2] - 1 == sorted_cards[i-1] - 2 \
                        == sorted_cards[i-3] == 2) and 14 in sorted_cards:
                    return 'S', [5, 4, 3, 2, 1], []
            i = 3
            val = sorted_cards[i]
            if (val - 3 == sorted_cards[i - 2] - 1 == sorted_cards[i - 1] - 2 == sorted_cards[i - 3] == 2) \
                    and 14 in sorted_cards:
                return 'S', [5, 4, 3, 2, 1], []
            else:
                return None
        else:
            return None

    def check_flush(cards):
        colors = get_colors(cards)
        values = get_values(cards)
        for i in range(len(cards)-4):
            if colors.count(colors[i]) >= 5:
                color = colors[i]
                values = [values[i] for i in range(len(values)) if colors[i] == color]
                return 'Fl', sorted(values, reverse=True)[:5], []
            else:
                return None

    def check_quads(cards):
        card_values = get_values(cards)

        if len(cards) == 4:
            if card_values.count(card_values[0]) == 4:
                return 'Q', [card_values[0]], []
            else:
                return None
        else:
            for i in range(len(cards) - 4):
                if card_values.count(card_values[i]) == 4:
                    val = card_values[i]
                    return 'Q', [val], [max([card_value for card_value in card_values if card_value != val])]
            return None

    quads = None
    if len(cards_set) >= 4:
        tm = time.time()
        quads = check_quads(cards_set)
        time_keeper['Q'] += (time.time() - tm)

    if quads is None:
        straight = None
        if len(cards_set) >= 5:
            tm = time.time()
            straight = check_straight(cards_set)
            time_keeper['S'] += (time.time() - tm)
        if straight is None:
            tm = time.time()
            flush = check_flush(cards_set)
            time_keeper['Fl'] += (time.time() - tm)

            if flush is None:
                triple = None
                if len(cards_set) > 2:
                    tm = time.time()
                    triple = check_triple(cards_set)
                    time_keeper['T'] += (time.time() - tm)

                if triple is not None and len(cards_set) > 4:
                    left_cards = [card for card in cards_set if get_value_and_color(card)[0] != triple[1][0]]
                    tm = time.time()
                    pairs = check_pairs(left_cards)
                    time_keeper['P'] += (time.time() - tm)
                    if pairs is not None:
                        return 'Fu', [triple[1][0], pairs[1][0]], []
                    else:
                        return triple

                if triple is None:

                    if len(cards_set) > 1:
                        tm = time.time()
                        pairs = check_pairs(cards_set)
                        time_keeper['P'] += (time.time() - tm)
                    else:
                        print('Not enough cards')
                        return None
                    if pairs is not None:
                        return pairs
                    else:
                        card_values = get_values(cards_set)
                        return 'H', sorted(card_values, reverse=True)[:5], []

            else:
                return flush

        elif straight is not None:
            tcc = cards_set[:]
            tcc = [cd for cd in tcc if get_value_and_color(cd)[0] in straight[1]]
            tm = time.time()
            flush = check_flush(tcc)
            time_keeper['Fl'] += (time.time() - tm)
            if flush is None:
                return straight
            else:
                return 'SFl', straight[1], []

    else:
        return quads

def get_cards_value(cards_set):

    def check_pairs(cards):
        pairs = []
        left_cards = get_values(cards)
        card_values = left_cards[:]

        for i in range(len(cards)-1):
            if card_values.count(card_values[4-i]) == 2:
                pairs.append(card_values[4-i])
                card_values.remove(card_values[4-i])
        if len(pairs) > 0:
            return str(len(pairs)) + 'P', pairs, sorted(left_cards, reverse=True)
        else:
            return None


    def check_triple(cards):
        left_cards = get_values(cards)

        for i in range(len(cards)-2):
            if left_cards.count(left_cards[i]) == 3:
                val = left_cards[i]
                for k in range(3):
                    left_cards.remove(val)
                return 'T', [val], sorted(left_cards, reverse=True)
        return None

    def check_straight(cards):
        cards_value = get_values(cards)
        sorted_cards = sorted(cards_value)
        if sorted_cards[0] + 4 == sorted_cards[4] == sorted_cards[3] + 1 == sorted_cards[2] + 2 \
                == sorted_cards[1] + 3:
            return 'S', [sorted_cards[4-j] for j in range(5)], []
        elif sorted_cards[0] + 4 == sorted_cards[4] - 8 == sorted_cards[3] + 1 == sorted_cards[2] + 2 \
                == sorted_cards[1] + 3:
            return 'S', [5, 4, 3, 2, 1], []
        else:
            return None

    def check_flush(cards):
        colors = get_colors(cards)
        values = get_values(cards)
        if colors.count(colors[0]) == 5:
            return 'Fl', sorted(values, reverse=True), []
        else:
            return None

    def check_full(cards):
        triple = check_triple(cards)
        if triple is None:
            return None
        else:
            left_cards = cards[:]
            left_cards = get_values(left_cards)
            for i in range(3):
                left_cards.remove(triple[1][0])
            if left_cards[0] != left_cards[1]:
                return None
            else:
                return 'Fu', [triple[1][0], left_cards[0]], []

    def check_quads(cards):
        card_values = get_values(cards)

        if len(cards) == 5:
            if card_values.count(card_values[0]) == 4:
                return 'Q', [card_values[0]], [card_values[i] for i in range(1, 5) if card_values[i] != card_values[0]]
            elif card_values.count(card_values[1]) == 4:
                return 'Q', [card_values[1]], [card_values[i] for i in range(5) if card_values[i] != card_values[1]]
            else:
                return None

        else:
            if card_values.count(card_values[0]) == 4:
                return 'Q', [card_values[0]], []
            else:
                return None

    quads = None
    if len(cards_set) >= 4:
        quads = check_quads(cards_set)

    if quads is None:
        straight = None
        flush = None
        if len(cards_set) == 5:
            flush = check_flush(cards_set)
            straight = check_straight(cards_set)

        if straight is None and flush is None:

            triple = None
            pairs = None
            if len(cards_set) > 2:
                triple = check_triple(cards_set)
            if len(cards_set) > 1:
                pairs = check_pairs(cards_set)
            else:
                return 'Not enough cards'

            if triple is not None and len(cards_set) > 4:
                full = check_full(cards_set)
                if full is not None:
                    return full
                else:
                    return triple

            if triple is None and pairs is None:
                card_values = get_values(cards_set)
                return 'H', sorted(card_values, reverse=True), []

            elif triple is not None:
                return triple

            else:
                return pairs

        elif straight is not None and flush is None:
            return straight
        elif straight is None and flush is not None:
            return flush
        else:
            return 'SFl', straight[1], []

    else:
        return quads


def compare_hands(hand1, hand2):
    assert hand1 is not None
    assert hand2 is not None
    val1, hc1, lc1 = hand1
    val2, hc2, lc2 = hand2

    val_to_score = {
        'H': 0,
        '1P': 1,
        '2P': 2,
        'T': 3,
        'S': 4,
        'Fl': 5,
        'Fu': 6,
        'Q': 7,
        'SFl': 8
    }

    if val1 == val2:
        assert len(hc1) == len(hc2)
        for k in range(len(hc1)):

            if int(hc1[k]) > int(hc2[k]):
                return 1
            elif int(hc1[k]) < int(hc2[k]):
                return 2

        if len(lc1) == len(lc2) == 0:
            return 0
        else:
            assert len(lc1) == len(lc2)
            for k in range(len(lc1)):
                if int(lc1[k]) > int(lc2[k]):
                    return 1
                elif int(lc1[k]) < int(lc2[k]):
                    return 2

            return 0

    else:
        if val_to_score[val1] > val_to_score[val2]:
            return 1
        elif val_to_score[val1] < val_to_score[val2]:
            return 2
        else:
            print('ISSUE2')
            return None

def get_best_hand(hands):

    best_hand = ''
    for hand in hands:
        if best_hand == '':
            best_hand = hand
        else:
            compare = compare_hands(get_cards_value_3(best_hand), get_cards_value_3(hand))
            best_hand = [best_hand, hand][compare-1]

    return best_hand

def get_ones_hand(hand, board):
    all_cards = board + hand
    best_hand = ''
    hands_possible = []
    for i in combinations(all_cards, 5):
        hands_possible.append(list(i))
    best_hand = get_best_hand(hands_possible)
    return best_hand

def get_ones_hand_2(hand, board):

    all_cards = board + hand
    best_hand = ''
    for i in combinations(all_cards, 5):
        hand = list(i)
        if best_hand == '':
            best_hand = hand
        else:
            best_hand = [best_hand, hand][compare_hands(get_cards_value_3(best_hand), get_cards_value_3(hand))-1]
    return best_hand

def check_cards_appearances(cards):
    cards_appearances = {
        'Q': [],
        'T': [],
        'P': []
    }
    card_values = get_values(cards)

    if len(cards) == 4:
        if card_values.count(card_values[0]) == 4:
            return 'Q', [card_values[0]], []

    for i in range(len(cards) - 1):
        val = card_values[i]
        if card_values.count(val) == 4:
            return 'Q', [val], [max([card_value for card_value in card_values if card_value != val])]
        elif card_values.count(val) == 3:
            cards_appearances['T'].append(val)
        elif card_values.count(val) == 2:
            cards_appearances['P'].append(val)

    cards_appearances['T'] = list(set(cards_appearances['T']))
    cards_appearances['P'] = list(set(cards_appearances['P']))

    if len(cards_appearances['T']) == 0 and len(cards_appearances['P']) == 0:
        return 'H', sorted(card_values, reverse=True)[:5], []
    else:
        if len(cards_appearances['T']) > 1:
            return 'Fu', [max(cards_appearances['T']), min(cards_appearances['T'])], []
        elif len(cards_appearances['T']) > 0 and len(cards_appearances['P']) > 0:
            return 'Fu', [cards_appearances['T'][0], max(cards_appearances['P'])], []
        elif len(cards_appearances['T']) > 0:
            left_cards = [card for card in card_values if card != cards_appearances['T'][0]]
            return 'T', [cards_appearances['T'][0]], sorted(left_cards, reverse=True)[:2]
        elif len(cards_appearances['P']) > 1:
            left_cards = [card for card in card_values if card not in cards_appearances['P'][:2]]
            return '2P', sorted(cards_appearances['P'][:2], reverse=True), sorted(left_cards, reverse=True)[:1]
        else:
        # elif len(cards_appearances['P']) > 0:
            left_cards = [card for card in card_values if card != cards_appearances['P'][0]]
            return '1P', cards_appearances['P'][:1], sorted(left_cards, reverse=True)[:4]


def check_straight(cards):
    cards_value = get_values(cards)
    sorted_cards = sorted(list(set(cards_value)))
    if len(sorted_cards) > 4:
        for i in range(len(sorted_cards) - 1, 3, -1):
            val = sorted_cards[i]
            if val - 4 == sorted_cards[i - 4] == sorted_cards[i - 3] - 1 == sorted_cards[i - 2] - 2 \
                    == sorted_cards[i - 1] - 3:
                return 'S', [val, val - 1, val - 2, val - 3, val - 4], []
            elif (val - 3 == sorted_cards[i - 2] - 1 == sorted_cards[i - 1] - 2 \
                  == sorted_cards[i - 3] == 2) and 14 in sorted_cards:
                return 'S', [5, 4, 3, 2, 1], []

        val = sorted_cards[3]
        if (val - 3 == sorted_cards[1] - 1 == sorted_cards[2] - 2 == sorted_cards[0] == 2) \
                and 14 in sorted_cards:
            return 'S', [5, 4, 3, 2, 1], []
        else:
            return None
    else:
        return None


def check_flush(cards):
    colors = get_colors(cards)
    values = get_values(cards)
    for i in range(len(cards) - 4):
        if colors.count(colors[i]) >= 5:
            color = colors[i]
            values = [values[i] for i in range(len(values)) if colors[i] == color]
            return 'Fl', sorted(values, reverse=True)[:5], []
        else:
            return None

def check_straight_flush(cards):
    colors = get_colors(cards)
    for color in list(set(colors)):
        colors = np.array(colors)
        subset_cards = np.array(cards)[np.where(colors==color)[0]]
        if len(subset_cards) > 4:
            straight = check_straight(subset_cards)
            if straight is not None:
                return 'SFl', straight[1], []
    return None

def check_quads(cards):
    card_values = get_values(cards)

    if len(cards) == 4:
        if card_values.count(card_values[0]) == 4:
            return 'Q', [card_values[0]], []
        else:
            return None
    else:
        for i in range(len(cards) - 4):
            if card_values.count(card_values[i]) == 4:
                val = card_values[i]
                return 'Q', [val], [max([card_value for card_value in card_values if card_value != val])]
        return None


def get_cards_value_3(cards_set):

    straight = None
    flush = None
    if len(cards_set) > 4:
        flush = check_flush(cards_set)
        straight = check_straight(cards_set)

    if straight is None and flush is None:
        return check_cards_appearances(cards_set)
    else:
        if straight is not None and flush is not None:
            straight_flush = check_straight_flush(cards_set)
            if straight_flush is None:
                quads = check_quads(cards_set)
                if quads is None:
                    return flush
                else:
                    return quads
            else:
                return straight_flush
        else:
            quads = check_quads(cards_set)
            if quads is None:
                if straight is not None:
                    return straight
                else:
                    return flush
            else:
                return quads


def get_ones_hand_3(hand, board):
    all_cards = board + hand

    return get_cards_value_3(all_cards)

def get_probabilities(hand1, hand2, board):
    all_cards = []
    for color in ['c', 's', 'd', 'h']:
        for value in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
            all_cards.append(value + '_' + color)

    def get_possible_cards(all_cards, out_cards):
        possible_cards = all_cards[:]
        for cards_list in out_cards:
            for card in cards_list:
                possible_cards.remove(card)

        return possible_cards

    possible_cards = get_possible_cards(all_cards, [hand1, hand2, board])
    wins = [0, 0, 0]
    # equal, 1, 2

    time_keep = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0
    }

    if len(board) == 0:
        for i in tqdm.trange(len(possible_cards)-4):
            # print(time_keep)
            for j in range(i+1, len(possible_cards)-3):
                for k in range(j+1, len(possible_cards)-2):
                    for l in range(k+1, len(possible_cards)-1):
                        for m in range(l+1, len(possible_cards)):
                            t1 = time.time()
                            copied_board = [possible_cards[i], possible_cards[j], possible_cards[k], possible_cards[l],
                                             possible_cards[m]]
                            t2 = time.time()
                            final_hand1 = get_ones_hand_3(hand1, copied_board)
                            t3 = time.time()
                            final_hand2 = get_ones_hand_3(hand2, copied_board)
                            t4 = time.time()
                            winner = compare_hands(final_hand1, final_hand2)
                            t5 = time.time()

                            # if final_hand1 == final_hand2 == winner:
                            #     wins[0] += 1
                            # elif final_hand1 == winner:
                            #     wins[1] += 1
                            # elif final_hand2 == winner:
                            #     wins[2] += 1
                            # else:
                            #     print('ISSSUE')
                            #     return None
                            wins[winner] += 1
                            t6 = time.time()

                            time_keep['1'] += t2-t1
                            time_keep['2'] += t3 - t2
                            time_keep['3'] += t4 - t3
                            time_keep['4'] += t5 - t4
                            time_keep['5'] += t6 - t5

                            # print(t2-t1, t3-t2, t4-t3, t5-t4, t6-t5)
    if len(board) == 3:
        for i in range(len(possible_cards)-1):
            for j in range(i+1, len(possible_cards)):
                copied_board = board[:]
                copied_board.append(possible_cards[i])
                copied_board.append(possible_cards[j])

                final_hand1 = get_ones_hand_3(hand1, copied_board)
                final_hand2 = get_ones_hand_3(hand2, copied_board)

                winner = compare_hands(final_hand1, final_hand2)
                if winner == 1:
                    print('111', final_hand1, final_hand2)

                wins[winner] += 1

    print(wins)
    return wins


# ################## TESTS #####################
#
# print('TESTS')
# print('____________ get cards value _____________')
# cards = ['5_c', '6_c', '7_c', '8_c', '9_c']
# print(cards, get_cards_value(cards))
# cards = ['5_c', '5_h', '5_d', '5_s', '9_c']
# print(cards, get_cards_value(cards))
# cards = ['5_c', '5_h', '5_d', '9_s', '9_c']
# print(cards, get_cards_value(cards))
# cards = ['5_c', '6_h', '7_d', '8_s', '9_c']
# print(cards, get_cards_value(cards))
# cards = ['5_c', '6_c', '7_c', '0_c', '9_c']
# print(cards, get_cards_value(cards))
# cards = ['5_c', '5_c', '5_d', '0_c', '9_c']
# print(cards, get_cards_value(cards))
# cards = ['5_c', '5_c', '0_d', '0_c', '9_c']
# print(cards, get_cards_value(cards))
# cards = ['5_c', '5_c', '2_d', '0_c', '9_c']
# print(cards, get_cards_value(cards))
# cards = ['5_c', '1_c', '7_d', '0_c', '9_c']
# print(cards, get_cards_value(cards))
#
#
# print('____________ special tests _____________')
#
# hand1 = ['5_c', '6_c', '7_c', '4_c', 'K_c']
# hand2 = ['5_c', '6_c', '7_c', '4_c', '8_c']
# print(get_cards_value(hand1))
# print(hand1, hand2, get_best_hand([hand1, hand2]))
# print('%%%%%%%%%% END TESTS %%%%%%%%%%%%%')
#
#
# t1 = time.time()
# hand2 = ['8_c', '9_h']
# hand1 = ['K_s', 'K_d']
# board = ['5_c', '6_c', '7_d']
# u = get_probabilities(hand1, hand2, board)
# print(u)
#
# print('-------')
# cards = ['5_c', '6_c', '7_c', '8_c', '9_h', '13_d', '8_h']
# print(cards, get_cards_value_2(cards))
# print(cards, get_cards_value_2(cards))
# print('________________________')
# t2 = time.time()
# print('TIME', t2-t1)
#
#
# print("//////////////  SPECIAL TEST 2 //////////////////")
# cards = ['5_c', '6_c', '7_c', '8_c', '9_c', 'K_c', 'Q_d']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '6_c', '7_c', '8_c', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_h', '5_d', '5_s', '9_c', '9_d', '9_h']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_h', '5_d', '5_s', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_h', '5_d', '9_s', '9_c', '9_d', '0_d']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_h', '5_d', '9_s', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '6_c', '7_c', '0_c', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '6_c', '7_c', '0_c', '9_c', 'Q_c', 'J_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '6_c', '7_c', '2_d', '3_h', '0_c', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '6_h', '7_d', '8_s', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['A_c', '3_h', '2_d', '5_s', 'J_c', '0_h', '4_h']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_c', '5_d', '0_c', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_c', '5_d', '0_c', '9_c', '2_h', 'K_h']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_c', '0_d', '0_c', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_c', '0_d', '0_c', '9_c', 'K_h', 'K_d']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_c', '2_d', '0_c', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '5_c', '2_d', '0_c', '9_c', 'J_h', 'K_d']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '1_c', '7_d', '0_c', '9_c']
# print(cards, get_cards_value_2(cards))
# cards = ['5_c', '1_c', '7_d', '0_c', '9_c', 'J_h', 'K_d']
# print(cards, get_cards_value_2(cards))
# print("////////////// END SPECIAL TEST 2 //////////////////")


hand2 = ['8_c', '8_h']
hand1 = ['K_c', 'K_d']
board = []
u = get_probabilities(hand1, hand2, board)

print(time_keeper)


tv = time.time()
print("//////////////  SPECIAL TEST 2 //////////////////")
cards = ['5_c', '6_c', '7_c', '8_c', '9_c', 'K_c', 'Q_d']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '6_c', '7_c', '8_c', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_h', '5_d', '5_s', '9_c', '9_d', '9_h']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_h', '5_d', '5_s', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_h', '5_d', '9_s', '9_c', '9_d', '0_d']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_h', '5_d', '9_s', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '6_c', '7_c', '0_c', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '6_c', '7_c', '0_c', '9_c', 'Q_c', 'J_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '6_c', '7_c', '2_d', '3_h', '0_c', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '6_h', '7_d', '8_s', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['A_c', '3_h', '2_d', '5_s', 'J_c', '0_h', '4_h']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_c', '5_d', '0_c', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_c', '5_d', '0_c', '9_c', '2_h', 'K_h']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_c', '0_d', '0_c', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_c', '0_d', '0_c', '9_c', 'K_h', 'K_d']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_c', '2_d', '0_c', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '5_c', '2_d', '0_c', '9_c', 'J_h', 'K_d']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '1_c', '7_d', '0_c', '9_c']
print(cards, get_cards_value_3(cards))
cards = ['5_c', '1_c', '7_d', '0_c', '9_c', 'J_h', 'K_d']
print(cards, get_cards_value_3(cards))
print("////////////// END SPECIAL TEST 2 //////////////////")

print((time.time() - tv)*100000)
