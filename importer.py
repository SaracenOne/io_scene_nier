import os.path
from .stream import Stream
from .mdv import MDV
from .mdp import MDP
from .model_output import ModelOutput
import math

class Importer:
    def __init__(self, filepath, options):
        self.filepath = filepath
        self.options = options
        self.caches = {}

    def parse_files(self, mdv_file, mdp_file):
        split_text = os.path.splitext(self.filepath)
        mdp_file_path = str(split_text[0]) + ".MDP"

        if os.path.isfile(self.filepath):
           mdv_file = open(self.filepath, "rb+")
        else:
            return

        if os.path.isfile(mdp_file_path + ".dec"):
            mdp_file = open(mdp_file_path + ".dec", "rb+")
        else:
            return

        mdv = MDV()
        mdv.parse_mdv_file(mdv_file)

        mdp = MDP()
        mdp.parse_mdp_file(mdp_file, mdv)

        model_output = ModelOutput()
        model_output.create_model(mdv, mdp)

    def do_import(self):
        mdv_file = None
        mdp_file = None

        self.parse_files(mdv_file, mdp_file)

        if mdv_file is not None:
            mdv_file.close()
        if mdp_file is not None:
            mdp_file.close()