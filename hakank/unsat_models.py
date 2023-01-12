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
from utils import make_unsat_model
from time import time

TIMELIMIT = 60

def make_unsat_instances(n=5, seed=0, p=0.05, input_dir="pickled/", output_dir="unsat_pickled/", verbose=True):
    random.seed(seed)
    ### OUTPUT
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    if output_dir:
        output_dir_path = Path(output_dir)
        if not output_dir_path.exists():
            output_dir_path.mkdir(parents=True)

    path_input_dir = Path(input_dir)
    assert path_input_dir.exists(), "Path does not exist"

    all_unsat_models = []
    all_files = sorted(
        [path_file for path_file in path_input_dir.iterdir() if (path_file.is_file() and path_file.suffix == ".pkl")],
        key=lambda x: x.stat().st_size
    )

    for count, path_file in enumerate(all_files):
        print("path_file=", path_file, n)
        if not path_file.is_file() or path_file.suffix != ".pkl":
            continue
        if count >=n:
            break

        try:
            model = cp.Model().from_file(str(path_file))
            assert isinstance(model, cp.Model), f"type({model}) be an CPMpy Model"
            
            start_time = time()
            if not model.solve(time_limit=TIMELIMIT):
                elapsed_time = time() - start_time
                if elapsed_time < TIMELIMIT * 0.95:
                    print("Model is UNSAT!")
                    all_unsat_models.append(unsat_model)
                    continue
                else:
                    raise TimeoutError()

            ## make model unsat with certain probability
            unsat_model = make_unsat_model(model, p)

            ## Write output to file
            if output_dir:
                model_path = output_dir_path / (path_file.name +"_" + today + ".pkl")
                model_output = str(model_path)
                unsat_model.to_file(model_output)
            all_unsat_models.append(unsat_model)
        except :
            if verbose:
                traceback.print_exception(*sys.exc_info())
                print(f"\n Failed model:", path_file.name)

    ## saving model in directory
    return all_unsat_models

def main(args):
    if args.seed == 0:
        print("Defaulting to seed=0")
    ## Random seed
    seed = args.seed
    ## model
    num_models = args.num
    verbose = args.verbose
    output_dir = args.output_directory
    input_dir = args.input_directory
    unsat_prob = args.unsat_prob
    make_unsat_instances(
        n=num_models,
        seed=seed,
        p=unsat_prob,
        input_dir=input_dir,
        output_dir=output_dir,
        verbose=verbose)

if __name__== "__main__":
    #### EXAMPLE USAGE!
    #### python3 unsat_models.py --num 300 -p 0.05 -i pickled/ -d pickled_unsat/

    parser = argparse.ArgumentParser(
        prog = 'HakankUnsatModels',
        description = 'Generates a specified number of randomized unsat models ',
        usage='%(prog)s [options]')
    parser.add_argument('-d', '--output', dest="output_directory", help="Output Directory with Pickled models", type=str, default=None)
    parser.add_argument('-i', '--input', dest="input_directory", help="Input Directory with Pickled models", type=str, default=None)
    parser.add_argument('-s', '--seed', dest="seed", type=int, help="Seed number for random module", default=0)
    # parser.add_argument('-m', '--model', dest="model", type=str, help=f"Select models from [{list(ALL_HAKANK_MODELS)}]", default=None)
    parser.add_argument('-n', '--num', dest="num", type=int, help="NUmber of unsat models to generate", default=300)
    parser.add_argument('-p', '--probability', dest="unsat_prob", type=float, help="NUmber of unsat models to generate", default=0.05)
    parser.add_argument('-v', dest='verbose', help="verbosity", default=True)
    args = parser.parse_args()
    main(args)