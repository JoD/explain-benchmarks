import datetime
import random
from pathlib import Path
from instances import ALL_HAKANK_MODELS

def pickle_all_instances(seed=0, output_dir="pickled/"):
    random.seed(seed)
    ### OUTPUT
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    if output_dir:
        output_dir_path = Path(output_dir)
        if not output_dir_path.exists():
            output_dir_path.mkdir(parents=True)

    for id, (model_name, model_fun) in enumerate(ALL_HAKANK_MODELS.items()):
        print(f"Pickling [{id+1}/{len(ALL_HAKANK_MODELS)}]", flush=True, end="\r")
        model = model_fun(seed=seed)
        model_path = output_dir_path / (model_name + today + ".pkl")
        model.to_file(str(model_path))

if __name__== "__main__":
    pickle_all_instances()