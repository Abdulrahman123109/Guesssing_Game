"""CSC108/CSCA08: Fall 2022 -- Assignment 1: Mystery Message Game

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Mario Badr, Jennifer Campbell, Tom Fairgrieve, Diane
Horton, Michael Liut, Jacqueline Smith, Anya Tafliovich and Michelle Craig.
"""

from constants import (CONSONANT_POINTS, VOWEL_COST, CONSONANT_BONUS,
                       PLAYER_ONE, PLAYER_TWO, CONSONANT, VOWEL,
                       SOLVE, QUIT, HUMAN, HUMAN_HUMAN,
                       HUMAN_COMPUTER, EASY, HARD, ALL_CONSONANTS,
                       ALL_VOWELS, PRIORITY_CONSONANTS, HIDDEN)


# We provide this function as an example.
def is_win(view: str, message: str) -> bool:
    """Return True if and only if message and view are a winning
    combination. That is, if and only if message and view are the same.

    >>> is_win('banana', 'banana')
    True
    >>> is_win('a^^le', 'apple')
    False
    >>> is_win('app', 'apple')
    False
    """

    return message == view


def computer_chooses_solve(view: str, difficulty: str,\
                           consonants: str) -> bool:
    """Return true if difficulty is hard and half of the letters
    have been revealed or if there are no more consonants to guess.

    Or if difficulty is easy and there is no more consonants to choose from.
    >>> computer_chooses_solve('b^tt^^', 'H', '(r, t, y, k, l, d, z, x, v)')
    True
    >>> computer_chooses_solve('b^n^n^', 'E', '')
    True
    """
    if difficulty == 'H':
        if (consonants == '') or half_revealed(view):
            return True
        return False
    if consonants == '':
        return True
    return False


def is_bonus_letter(view: str, letter: str, message: str) -> bool:
    """Returns true if and only if the letter is
    consonant and in message and hidden in view.

    >>> is_bouns_letter('ba^a^a', n, 'banana')
    True
    >>> is_bouns_letter('l^^'s g^', o, 'let's go')
    False
    """
    if letter in message:
        if letter in view:
            return False
        return True
    return False


# We provide this function as an example of using a function as a helper.
def is_game_over(view: str, message: str, move: str) -> bool:
    """Return True if and only if message and view are a winning
    combination or move is QUIT.
    >>> is_game_over('a^^le', 'apple', 'V')
    False
    >>> is_game_over('a^^le', 'apple', 'Q')
    True
    >>> is_game_over('apple', 'apple', 'S')
    True
    """
    return move == QUIT or is_win(view, message)


def current_player_score(player_one_score: int, player_two_score: int,
                         current_player: str) -> int:
    """Return player_one_score or player_two_score
    depandeing on the current_player

    >>> current_player_score(4, 7, PLAYER_ONE)
    4
    >>> current_player_score(0, 3, PLAYER_TWO)
    3
    """
    if current_player == PLAYER_ONE:
        return player_one_score
    return player_two_score


# We provide the header and docstring of this function as an example
# of where and how to use constants in the docstring.
def is_human(current_player: str, game_type: str) -> bool:
    """Return True if and only if current_player represents a human in a
    game of type game_type.

    current_player is PLAYER_ONE or PLAYER_TWO.
    game_type is HUMAN, HUMAN_HUMAN,
    or HUMAN_COMPUTER.
    In a HUMAN game or a HUMAN_HUMAN game, a player is always
    human. In a HUMAN_COMPUTER game,
    PLAYER_ONE is human and
    PLAYER_TWO is computer.

    >>> is_human('Player One', 'P1')
    True
    >>> is_human('Player One', 'PVP')
    True
    >>> is_human('Player Two', 'PVP')
    True
    >>> is_human('Player One', 'PVE')
    True
    >>> is_human('Player Two', 'VE')
    False
    """
    if (game_type == 'PVE') and current_player == PLAYER_TWO:
        return False
    else:
        return True


def get_updated_char_view(view: str, message: str,\
                          index: int, guess: str) -> str:
    """Return guess if the guess in the index of message
    or if there is a character in the given index,
    Otherwise is returns '^'.

    >>> get_updated_char_view('b^tt^^', 'better', 5, r)
    'r'
    >>> get_updated_char_view('s^^^ ^n^', 'step one', 3, r)
    '^'
    """
    if guess == message[index]:
        return guess
    if guess != '^':
        return view[index]
    return '^'


def is_one_player_game(game_type: str) -> bool:
    """Return True if and only if game_type is P1

    >>> is_one_player_game('PVP')
    False
    >>> is_one_player_game('P1')
    True
    """
    if game_type == 'P1':
        return True
    return False


def calculate_score(score: int, num_occurrences: int, move: str) -> int:
    """return the updated score based on move and num_occurrences

    >>> calculate_score(3, 2, 'C')
    5
    >>> calculate_score(7, 3, 'V')
    6
    """
    if move == 'V':
        return score - 1
    elif move == 'C':
        return score + num_occurrences
    elif move == 'S':
        return score + (num_occurrences * 2)
    else:
        return score


def erase(message: str, index: int) -> str:
    """Return the message with the character at the index is removed
    if the index greater or less than message length, otherwise returns message

    >>> erase('hello', 2)
    'helo'
    >>> erase('let's get it', 7)
    let's gt it'
    """
    if 0 <= index <= len(message):
        return message[:index] + message[index + 1:]
    return message


def is_fully_hidden(view: str, index: int, message: str) -> bool:
    """Returns True if and only if the character
    at the index of message is not revealed in
    view

    >>> is_fully_hidden('^^ed', 1, 'aced')
    True
    >>> is_fully_hidden('ba^a^a', 2, 'banana')
    False
    """
    if message[index] not in view:
        return True
    elif view[index] == '^':
        return False
    else:
        return False


def next_player(current_player: str, num_occurrences: int,\
                game_type: str) -> str:
    """return the current_player if and only if: 1) the num_occurrences is \
    greater than 0 and the game_type is PVE or PVP, 2) the game_type is P1.

    >>> next_player(PLAYER_ONE, 2, PVP)
    PLAYER_ONE
    >>> next_player(PLAYER_TWO, 0, PVE)
    PLAYER_ONE
    """
    if game_type in ('PVP', 'PVE'):
        return helper_next_player(num_occurrences, current_player)
    else:
        return current_player


def helper_next_player(num_occurrences: int, current_player: str) -> str:
    """return the current_player if the num_occurrences more then 0

    >>> helper_next_player(2, PLAYER_ONE, PVP)
    PLAYER_ONE
    >>> helper_next_player(0, PLAYER_ONE, PVP)
    PLAYER_TWO
    """
    if num_occurrences > 0 and current_player == PLAYER_ONE:
        return PLAYER_ONE
    elif current_player == PLAYER_TWO and num_occurrences > 0:
        return PLAYER_TWO
    elif num_occurrences <= 0 and current_player == PLAYER_ONE:
        return PLAYER_TWO
    else:
        return PLAYER_ONE


# Helper function for computer_chooses_solve
# This function is already complete. You must not modify it.
def half_revealed(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic
    characters in view are revealed.

    >>> half_revealed('')
    True
    >>> half_revealed('x')
    True
    >>> half_revealed('^')
    False
    >>> half_revealed('a^,^c!')
    True
    >>> half_revealed('a^b^^e ^c^d^^d')
    False
    """

    num_hidden = view.count(HIDDEN)
    num_alphabetic = 0
    for char in view:
        if char.isalpha():
            num_alphabetic += 1
    return num_alphabetic >= num_hidden
