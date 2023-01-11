"""
Word square in cpmpy.

From http://en.wikipedia.org/wiki/Word_square
'''
A word square is a special case of acrostic. It consists of a set of words, 
all having the same number of letters as the total number of words (the 
"order" of the square); when the words are written out in a square grid 
horizontally, the same set of words can be read vertically.
'''

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
import sys
import re
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


#
# convert a character to integer
#
def get_dict():
    alpha = "abcdefghijklmnopqrstuvwxyzåäö"
    d = {}
    rev = {}
    count = 1
    for a in alpha:
        d[a] = count
        rev[count] = a
        count += 1
    return d, rev
    

def word_square(words, word_len = 5):
    num_words = len(words)
    n = word_len
    d, rev = get_dict()

    A = intvar(0,29,shape=(num_words, word_len),name="A")
    E = intvar(0, num_words,shape=n,name="E")

    model = Model(
                   AllDifferent(E) 
                   )

    # copy the words to a matrix
    for i in range(num_words):
        for j in range(word_len):
            model += [A[i,j] == d[words[i][j]]]

    # connect the words by character in proper positions
    for i in range(word_len):
        for j in range(word_len):
            model += [A[E[i],j] == A[E[j],i]]


    return model

def read_words(word_list, word_len):
    dict = {}
    all_words = []
    count = 0
    words = open(word_list).readlines()
    for w in words:
        w = w.strip().lower()
        if len(w) == word_len and not w in dict and not re.search("[^a-zåäö]",w):
            dict[w] = 1
            all_words.append(w)
            count += 1
    return all_words


def get_model(seed=0):
    import random
    random.seed(seed)
    word_len = int(round(random.uniform(5, 9)))
    word_dict = "/usr/share/dict/words"
    words = read_words(word_dict, word_len)
    return word_square(words, word_len=word_len)