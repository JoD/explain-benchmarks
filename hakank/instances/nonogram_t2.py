# Copyright 2010 Hakan Kjellerstrand hakank@bonetmail.com
#
# Licensed under the Apache License, Version 2.0 (the 'License'); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#
#     http://www.apache.org/licenses/LICENSE-2.0 
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an 'AS IS' BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 
#
# http:#www.cs.mu.oz.au/433/tenpenki.html
# Note: This problem has 2 solutions.
#
def get_instance():
    rows = 6
    row_rule_len = 6
    row_rules  = [
        [0, 0, 0, 2, 2, 3],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 3],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 0, 2, 2, 1]]

    cols = 14
    col_rule_len = 3
    col_rules = [
        [0, 0, 4],
        [0, 1, 1],
        [0, 1, 1],
        [0, 1, 1],
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [0, 1, 1],
        [0, 0, 0],
        [0, 0, 6],
        [0, 1, 1],
        [0, 1, 1],
        [0, 0, 2]]
    return rows, row_rule_len, row_rules, cols, col_rule_len, col_rules