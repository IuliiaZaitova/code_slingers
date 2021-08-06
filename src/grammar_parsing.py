#!/usr/bin/python3
# coding=utf-8
# Authors: Isidora Jeknic, Iuliia Zaitova, Kirstin Kolmorgen, Sharmila Upadhyaya
# Emails:  {shup00001}@stud.uni-saarland.de, {s8iuzait}@stud.uni-saarland.de,
# {s8kikolm}@stud.uni-saarland.de,  {shup00001}@stud.uni-saarland.de
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


import pickle
import numpy as np
import random
class Word_parser:

    """Grammar parsing class"""
    def __init__(self, nlp):
        self.nlp = nlp # For lemmatization and pos-tagging
        self.verb_trans = pickle.load(open('data/verb_trans.p', 'rb'))
        #self.dobjs = pickle.load(open('data/verb_dict_dobj.p', 'rb'))
        #self.pobjs = pickle.load(open('data/verb_dict_pobj.p', 'rb'))
        self.dobjs = pickle.load(open('data/dobj_dict_classes.p', 'rb'))
        self.pobjs = pickle.load(open('data/pobj_dict_classes.p', 'rb'))

    def get_lemma(self, word):
        # Returns the lemma of English words
        doc = self.nlp(word)
        for word in doc:
            lemma = word.lemma_
        return lemma

    def get_transitivity(self, verb):
        # Returns verb transitivity type generated with probabilities from 'https://github.com/wilcoxeg/verb_transitivity'
        #v_lemma = self.get_lemma(verb)
        if verb in self.verb_trans:
            p = np.array(self.verb_trans[verb]) # Obtain probabilities of transitivity types
            p /= p.sum()  # normalize, ps have to sum up to 1
            trans_type = np.random.choice(['intrans', 'trans', 'ditrans'], p=p)
        else:
            trans_type = 'intrans'
        return trans_type

    def get_objects(self, verb):
        # prints the trans type, returns the verb objects if they are available
        # if the verb is not in the obj dictionary, but is (di)transitive,
        # direct object would be generated randomly
        verb = self.get_lemma(verb)
        trans_type = self.get_transitivity(verb)
        objs = []
        if trans_type == 'trans' or trans_type == 'ditrans':
            try:
                objs.append(random.choice(self.dobjs[verb]))
            except:
                objs.append(random.choice(random.choice(list(self.dobjs.values()))))
        if trans_type == 'ditrans':
            try:
                objs.append(random.choice(self.pobjs[verb]))
            except:
                pass
        return objs
