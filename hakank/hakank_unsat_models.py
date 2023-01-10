# Generation of non-trivial unsatisatisfiable Minizinc models
# inspired by [cite unsat model here] and [2]
# from the Minizinc Challenge [19]
# [1]  
# [2]  Lazaar, N., Gotlieb, A., Lebbah, Y.: A CP framework for testing CP. Constraints 17(2), 123–147 (2012)
# [19] Stuckey, P., Becket, R., Fischer, J.: Philosophy of the MiniZinc challenge. Con- straints 15(3), 307–316 (2010)

## Read Minzinc Model from file 

## Introduce mistakes non-trivially
## Random instance selection
## 1. Swapping arguments to gloabal
## 2. changing relational operators
## 3. Changing indexes ooffsets
## 4. wrong variables in constraints
## 5. Removing negations
## 6. Changig constraints