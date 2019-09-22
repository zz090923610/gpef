import json
import os


# all related configuration files should be store in ~/.gpef/*
# basic conf file is ~/.gpef/basic.json
# ### basic.json
# {
#   "current_exp": "exp_name"
# }
# ###

# exp dict is ~/.gpef/experiments.json
# ### experiments.json
# {
#   "exp_name": "exp_path"
# }
# ###

def init_env():
    if not os.path.exists(os.path.expanduser("~/.gpef")):
        os.makedirs(os.path.expanduser("~/.gpef"), exist_ok=True)
    if not os.path.exists(os.path.expanduser("~/.gpef/basic.json")):
        with open(os.path.expanduser("~/.gpef/basic.json"), "w") as f:
            f.write('{\n\"current_exp\": null\n}')
    if not os.path.exists(os.path.expanduser("~/.gpef/experiments.json")):
        with open(os.path.expanduser("~/.gpef/experiments.json"), "w") as f:
            f.write('{}')


class ConfigHDL:
    def __init__(self):
        self.root = os.path.expanduser("~/.gpef")
        self.basic = self.load_cfg("basic.json")
        self.exp_dict = self.load_cfg("experiment.json")

    def load_cfg(self, file_name):
        with open(os.path.join(self.root, file_name)) as json_file:
            data = json.load(json_file)
            return data

    def save_cfg(self):
        with open(os.path.join(self.root, "basic.json"), "w") as f:
            f.write(json.dumps(self.basic))
        with open(os.path.join(self.root, "experiment.json"), "w") as f:
            f.write(json.dumps(self.exp_dict))



