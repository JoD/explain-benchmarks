# webpbn.com Puzzle #8098: Domino Logic III (Abstract pattern)
# Copyright 2010 by Josh Greifer
#
def get_instance():
    rows = 19
    row_rule_len = 2
    row_rules = [
        [0, 3],
        [0, 1],
        [3, 1],
        [0, 1],
        [3, 1],
        [0, 1],
        [3, 1],
        [0, 1],
        [3, 1],
        [0, 1],
        [3, 1],
        [0, 1],
        [3, 1],
        [0, 1],
        [3, 1],
        [0, 1],
        [3, 1],
        [0, 1],
        [0, 1],
        ]

    cols = 19
    col_rule_len = 2
    col_rules = [
        [0, 1],
        [0, 1],
        [1, 3],
        [0, 1],
        [1, 3],
        [0, 1],
        [1, 3],
        [0, 1],
        [1, 3],
        [0, 1],
        [1, 3],
        [0, 1],
        [1, 3],
        [0, 1],
        [1, 3],
        [0, 1],
        [1, 3],
        [0, 1],
        [0, 3],
        ]
    return rows, row_rule_len, row_rules, cols, col_rule_len, col_rules