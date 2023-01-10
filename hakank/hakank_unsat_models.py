# Generation of non-trivial unsatisatisfiable Minizinc models
# inspired by [cite unsat model here] and [2]
# from the Minizinc Challenge [19]
# [1]  
# [2]  Lazaar, N., Gotlieb, A., Lebbah, Y.: A CP framework for testing CP. Constraints 17(2), 123–147 (2012)
# [19] Stuckey, P., Becket, R., Fischer, J.: Philosophy of the MiniZinc challenge. Con- straints 15(3), 307–316 (2010)

## Read Minzinc Model from file 

from instances import ALL_HAKANK_MODELS

def gen_all_instances(n=5):
    models = []

    for count, (model_name, model_fun) in enumerate(ALL_HAKANK_MODELS.items()):
        if count >= n:
            break
        try:
            model = model_fun()
            models.append(model)
        except:
            print(f"\n [{count}/{len(ALL_HAKANK_MODELS)}] Failed model:", model_name)

    
## Introduce mistakes non-trivially
## Random instance selection
## 1. Swapping arguments to gloabal
## 2. changing relational operators
## 3. Changing indexes ooffsets
## 4. wrong variables in constraints
## 5. Removing negations
## 6. Changig constraints

if __name__== "__main__":
    all_models = gen_all_instances(300)