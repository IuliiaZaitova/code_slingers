#!/usr/bin/python3
# coding=utf-8
# Authors: Sharmila Upadhyaya, Isidora, Kirstin, Lulia
# Emails:  {saup00001}@stud.uni-saarland.de
# Organization: Universität des Saarlandes
# Copyright 2020 Sharmila Upadhyaya
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



"""
this module analyze the captions in coco dataset. It shows how the action related to entity are distributed in the caption text.



"""
#imports
from os import walk

import pandas as pd
import json
import spacy
from textpipeliner import PipelineEngine, Context
from textpipeliner.pipes import *
from get_svo import findSVOs

nlp = spacy.load("en_core_web_sm")

# object and subject constants
OBJECT_DEPS = {"dobj", "dative", "attr", "oprd"}
SUBJECT_DEPS = {"nsubj", "nsubjpass", "csubj", "agent", "expl"}
# tags that define wether the word is wh-
WH_WORDS = {"WP", "WP$", "WRB"}

# extract the subject, object and verb from the input
def extract_svo(doc):
    sub = []
    at = []
    ve = []
    for token in doc:
        # is this a verb?
        if token.pos_ == "VERB":
            ve.append(token.text)
        # is this the object?
        if token.dep_ in OBJECT_DEPS or token.head.dep_ in OBJECT_DEPS:
            at.append(token.text)
        # is this the subject?
        if token.dep_ in SUBJECT_DEPS or token.head.dep_ in SUBJECT_DEPS:
            sub.append(token.text)
    return " ".join(sub).strip().lower(), " ".join(ve).strip().lower(), " ".join(at).strip().lower()

class ImageDataset:

    """


    """

    def __init__(self, datapath):

        self.root_datapath = datapath

    def get_annotations(self):
        pass


    def get_filenames(self, file_type = "annotations", file_extension = None, starts_with = "captions"):
        #TODO generalize the files need according to need
        if file_type == "annotations":
            file_path = self.root_datapath + "annotations/"
            files = []
            for (dirpath, dirnames, filenames) in walk(file_path):
                for filename in filenames:
                    if filename.startswith(starts_with):
                        files.append(file_path + filename)
            return files




class CaptionAnalysis:

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        img_dataset = ImageDataset(dataset_name + "/")
        self.captions_files = img_dataset.get_filenames(file_type = "annotations", starts_with = "captions")
        self.all_captions = []
        self.caption_entities_pair = dict()

    def read_captions(self):


        for f in self.captions_files:
            with open(f, "r") as ff :
                json_data = json.load(ff)
                for each_annotation in json_data["annotations"]:
                    self.all_captions.append(each_annotation["caption"])
    

    def get_entity_action_single(self, doc):
        pipes_structure = [SequencePipe([FindTokensPipe("VERB/nsubj/*"),
                                 NamedEntityFilterPipe(),
                                 NamedEntityExtractorPipe()]),
                   FindTokensPipe("VERB"),
                   AnyPipe([SequencePipe([FindTokensPipe("VBD/dobj/NNP"),
                                          AggregatePipe([NamedEntityFilterPipe("GPE"),
                                                NamedEntityFilterPipe("PERSON")]),
                                          NamedEntityExtractorPipe()]),
                            SequencePipe([FindTokensPipe("VBD/**/*/pobj/NNP"),
                                          AggregatePipe([NamedEntityFilterPipe("LOC"),
                                                NamedEntityFilterPipe("PERSON")]),
                                          NamedEntityExtractorPipe()])])]

        engine = PipelineEngine(pipes_structure, Context(doc), [0,1,2])
        return engine.process()



    def get_entity_action_pairs(self):

        for i, caption in enumerate(self.all_captions):
            result = findSVOs(nlp(caption))
            self.caption_entities_pair[i] = result

            import pdb
            pdb.set_trace()

        

ca = CaptionAnalysis("coco")
ca.read_captions()
import pdb
pdb.set_trace()
ca.get_entity_action_pairs()


