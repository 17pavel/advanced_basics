#!/usr/bin/env python


"""Реализуйте функцию best_hand, которая принимает на вход
покерную "руку" (hand) из 7ми карт и возвращает лучшую
(относительно значения, возвращаемого hand_rank)
"руку" из 5ти карт. У каждой карты есть масть(suit) и
ранг(rank)
Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

Задание со *
Реализуйте функцию best_wild_hand, которая принимает на вход
покерную "руку" (hand) из 7ми карт и возвращает лучшую
(относительно значения, возвращаемого hand_rank)
"руку" из 5ти карт. Кроме прочего в данном варианте "рука"
может включать джокера. Джокеры могут заменить карту любой
масти и ранга того же цвета, в колоде два джокерва.
Черный джокер '?B' может быть использован в качестве треф
или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
любого ранга.

Одна функция уже реализована, сигнатуры и описания других даны.
Вам наверняка пригодится itertools
Можно свободно определять свои функции и т.п."""

import itertools
import random


def create_deck(
        suits=(
                "C",
                "S",
                "H",
                "D",
        ),
        jokers=("?B", "?R"),
):
    ranks = "2 3 4 5 6 7 8 9 T J Q K A".split()
    deck = []
    if jokers is not None:
        deck.extend(jokers)
    for rank in ranks:
        for suit in suits:
            card = rank + suit
            deck.append(card)
    return deck


def deal_cards(num_players=1, num_cards=5):
    deck = create_deck()
    random.shuffle(deck)
    hands = []
    for _ in range(num_players):
        hand = []
        for _ in range(num_cards):
            card = deck.pop()
            hand.append(card)
        hands.append(hand)

    print(*hands)
    return hands


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        #        print(8, max(ranks), hand, "flush-royal")
        return (8, max(ranks), hand, "flush-royal")
    elif kind(4, ranks):
        #        print(7, kind(4, ranks), kind(1, ranks), hand,'kare')
        return (7, kind(4, ranks), kind(1, ranks), hand, "kare")
    elif kind(3, ranks) and kind(2, ranks):
        #        print(6, kind(3, ranks), kind(2, ranks), hand,'full-house')
        return (6, kind(3, ranks), kind(2, ranks), hand, "full-house")
    elif flush(hand):
        #        print(5, ranks, hand,'flush')
        return (5, ranks, hand, "flush")
    elif straight(ranks):
        #        print(4, max(ranks), hand,'straigth')
        return (4, max(ranks), hand, "straigth")
    elif kind(3, ranks):
        #        print(3, kind(3, ranks), ranks, hand, 'set')
        return (3, kind(3, ranks), ranks, hand, "set")
    elif two_pair(ranks):
        #        print(2, two_pair(ranks), hand,'two-pair')
        return (2, two_pair(ranks), hand, "two-pair")
    elif kind(2, ranks):
        #        print(1, kind(2, ranks), ranks, hand,'pair')
        return (1, kind(2, ranks), ranks, hand, "pair")
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    ranks = ["--23456789TJQKA".index(rank) for rank, _ in hand]
    return sorted(ranks, reverse=True)


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    suits = [suit for _, suit in hand]
    return len(set(suits)) == 1


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    return max(ranks) - min(ranks) == 4 and len(set(ranks)) == 5


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    for rank in ranks:
        if ranks.count(rank) == n:
            return rank


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    #    res = set(ranks)
    #    return res if len(res) == 2 else None
    pairs = []
    for rank in set(ranks):
        if ranks.count(rank) == 2:
            pairs.append(rank)
    if len(pairs) == 2:
        return sorted(pairs, reverse=True)


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт"""
    comb = tuple(itertools.combinations(hand, 5))
    best = max(comb, key=hand_rank)
    #    print(hand_rank(best))
    return best


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    wild_hand = []
    cp_wild_hand = []
    hand.sort(key=lambda x: x.replace("?", ""))
    if "?R" in hand and "?B" not in hand:
        black = create_deck(suits=("D", "H"), jokers=None)
        hand.remove("?R")
        for card in black:
            cp_hand = hand[:]
            if card not in cp_hand:
                cp_hand.append(card)
                cp_wild_hand.append(cp_hand)
        wild_hand = cp_wild_hand
    if "?B" in hand:
        black = create_deck(suits=("C", "S"), jokers=None)
        hand.remove("?B")
        for card in black:
            cp_hand = hand[:]
            if card not in cp_hand:
                cp_hand.append(card)
                cp_wild_hand.append(cp_hand)
        wild_hand = cp_wild_hand
        if "?R" in hand:
            res = []
            for hand in wild_hand:
                __wild_hand = []
                red = create_deck(suits=("H", "D"), jokers=None)
                hand.remove("?R")
                for card in red:
                    __hand = hand[:]
                    __hand.append(card)
                    __wild_hand.append(__hand)
                res.extend(__wild_hand)
            wild_hand = res
    best_5 = []
    best = []
    if wild_hand:
        for el in wild_hand:
            best_5.append(best_hand(el))
        best = max(best_5, key=hand_rank)
    else:
        best = best_hand(hand)
    print("best: ", hand_rank(best))
    return best


def test_best_hand():
    print("test_best_hand...")
    assert sorted(best_hand("6C 7C 9C 8C TC 5C JS".split())) == [
        "6C",
        "7C",
        "8C",
        "9C",
        "TC",
    ]
    assert sorted(best_hand("TD TC TH 7C 7D 8C 8S".split())) == [
        "8C",
        "8S",
        "TC",
        "TD",
        "TH",
    ]
    assert sorted(best_hand("JD TC TH 7C 7D 7S 7H".split())) == [
        "7C",
        "7D",
        "7H",
        "7S",
        "JD",
    ]
    print("OK")


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split())) == [
        "7C",
        "7D",
        "7H",
        "7S",
        "JD",
    ]
    print(100 * "*")
    assert sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split())) == [
        "7C",
        "8C",
        "9C",
        "JC",
        "TC",
    ]
    print(100 * "*")
    assert sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split())) == [
        "7C",
        "TC",
        "TD",
        "TH",
        "TS",
    ]

    print("OK")


if __name__ == "__main__":
    #    test_best_hand()
    #    test_best_wild_hand()
    best_wild_hand(*deal_cards(num_cards=7))
    print(50 * "*")
    best_wild_hand(*deal_cards(num_cards=7))
