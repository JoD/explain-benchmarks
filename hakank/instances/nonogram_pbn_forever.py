# webpbn.com Puzzle #6574: Lasts Forever
# Copyright 2009 by Gator
#
def get_instance():
    rows = 25
    row_rule_len = 8
    row_rules = [
        [0, 1, 2, 2, 2, 2, 2, 1],
        [1, 2, 2, 2, 2, 2, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 3, 1],
        [0, 0, 0, 0, 0, 1, 13, 1],
        [0, 0, 0, 0, 0, 1, 13, 1],
        [0, 0, 0, 0, 0, 1, 13, 1],
        [0, 0, 0, 0, 1, 4, 4, 1],
        [0, 0, 0, 1, 4, 3, 4, 1],
        [0, 0, 0, 1, 4, 5, 4, 1],
        [0, 0, 0, 0, 0, 1, 7, 1],
        [0, 0, 0, 0, 0, 1, 7, 1],
        [0, 0, 0, 0, 0, 1, 7, 1],
        [0, 0, 0, 0, 0, 1, 7, 1],
        [0, 0, 0, 0, 1, 1, 5, 1],
        [0, 0, 0, 0, 1, 2, 6, 1],
        [0, 0, 0, 0, 1, 4, 6, 1],
        [0, 0, 0, 0, 1, 6, 6, 1],
        [0, 0, 0, 0, 0, 1, 3, 1],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 2, 2, 2, 2, 2, 1],
        [0, 1, 2, 2, 2, 2, 2, 1]
        ]

    cols = 25
    col_rule_len = 8
    col_rules = [
        [0, 1, 2, 2, 2, 2, 2, 1],
        [1, 1, 2, 2, 2, 2, 2, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 2, 1],
        [0, 0, 0, 0, 1, 6, 1, 1],
        [0, 0, 0, 0, 1, 6, 2, 1],
        [0, 0, 0, 0, 1, 6, 3, 1],
        [0, 0, 0, 0, 1, 4, 8, 1],
        [0, 0, 0, 1, 3, 5, 2, 1],
        [0, 0, 0, 1, 4, 8, 2, 1],
        [0, 0, 0, 1, 4, 9, 2, 1],
        [0, 0, 0, 0, 1, 4, 11, 1],
        [0, 0, 0, 0, 1, 3, 9, 1],
        [0, 0, 0, 0, 1, 4, 8, 1],
        [0, 0, 0, 0, 1, 6, 3, 1],
        [0, 0, 0, 0, 1, 6, 2, 1],
        [0, 0, 0, 0, 1, 6, 1, 1],
        [0, 0, 0, 0, 0, 1, 2, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [1, 2, 2, 2, 2, 2, 1, 1],
        [0, 1, 2, 2, 2, 2, 2, 1]
        ]
    return rows, row_rule_len, row_rules, cols, col_rule_len, col_rules