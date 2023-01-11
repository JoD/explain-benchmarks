# Generation of non-trivial unsatisatisfiable Minizinc models
# inspired by [cite unsat model here] and [2]
# from the Minizinc Challenge [19]
# [1]  
# [2]  Lazaar, N., Gotlieb, A., Lebbah, Y.: A CP framework for testing CP. Constraints 17(2), 123–147 (2012)
# [19] Stuckey, P., Becket, R., Fischer, J.: Philosophy of the MiniZinc challenge. Con- straints 15(3), 307–316 (2010)

## Read Minzinc Model from file 

import argparse

import datetime
import random
import sys
import traceback
from pathlib import Path
import cpmpy as cp
from hakank.utils import make_unsat_model


from instances import ALL_HAKANK_MODELS


def gen_all_instances(n=5, seed=0, p=0.05, output_dir=None, verbose=True):
    random.seed(seed)
    ### OUTPUT
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    if output_dir:
        p = Path(output_dir)
        if not p.exists():
            p.mkdir(parents=True)
    ### Model selection!
    models = []
    all_models = list(ALL_HAKANK_MODELS)
    selected_models = sorted(random.sample(all_models, k=min(n, len(ALL_HAKANK_MODELS))), key=lambda x: str(x))

    for count, model_name in enumerate(selected_models):
        if count >= n:
            break
        if verbose:
            print(f"Model [{count}/{len(selected_models)}]:\t", model_name)
        try:
            ## generate a model
            model = ALL_HAKANK_MODELS[model_name](seed=seed)
            assert isinstance(model, cp.Model), f"type({model}) be an CPMpy Model"

            ## make model unsat with certain probability
            unsat_model = make_unsat_model(model, p)

            ## Write output to file
            if output_dir:
                model_path = p / (model_name + today + ".pkl")
                model_output = str(model_path)
                unsat_model.to_file(model_output)
            models.append(unsat_model)
        except :
            if verbose:
                traceback.print_exception(*sys.exc_info())
                print(f"\n [{count}/{len(ALL_HAKANK_MODELS)}] Failed model:", model_name)

    ## saving model in directory
    return models





def main(args):
    if args.seed == 0:
        print("Defaulting to seed=0")
    ## Random seed
    seed = args.seed
    ## model
    num_models = args.num
    verbose = args.verbose
    output_dir = args.output_directory
    gen_all_instances(
        n=num_models,
        seed=seed,
        output_dir=output_dir,
        verbose=verbose)

if __name__== "__main__":
    parser = argparse.ArgumentParser(
        prog = 'HakankUnsatModels',
        description = 'Generates a specified number of randomized unsat models ',
        usage='%(prog)s [options]')
    parser.add_argument('-d', '--dir', dest="output_directory", help="Output Directory", type=str, default=None)
    parser.add_argument('-s', '--seed', dest="seed", type=int, help="Seed number for random module", default=0)
    # parser.add_argument('-m', '--model', dest="model", type=str, help=f"Select models from [{list(ALL_HAKANK_MODELS)}]", default=None)
    parser.add_argument('-n', '--num', dest="num", type=int, help="NUmber of unsat models to generate", default=300)
    parser.add_argument('-v', dest='verbose', help="verbosity", default=True)
    args = parser.parse_args()
    main(args)