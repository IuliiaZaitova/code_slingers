#!/usr/bin/python3
# coding=utf-8
# Authors: Isidora Jeknic, Iuliia Zaitova, Kirstin Kolmorgen, Sharmila Upadhyaya
# Emails:  {isje00001}@stud.uni-saarland.de, {s8iuzait}@stud.uni-saarland.de,
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


import gpt_2_simple as gpt2
import tensorflow as tf


#checkpoint path
Model_checkpoint = "output/joke_generation/"

def evaluation(test):
    """
    joke inference
    Params:
    test (string): question generated from caption
    returns:
    string: answer to the input question
    """
    
    tf.reset_default_graph()
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name='run2')
    result = gpt2.generate(sess, run_name='run2', prefix='<soq>'+ test + '<eoq>', length=100, temperature=0.9, return_as_list=True)
    return result[0]



