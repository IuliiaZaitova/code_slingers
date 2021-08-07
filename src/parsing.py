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


import spacy
import stanza
import spacy_stanza
from spacy.util import filter_spans
from spacy.matcher import Matcher
from random import sample
from collections import defaultdict
import pickle

# dependency labels
# see https://github.com/clir/clearnlp-guidelines/blob/master/md/specifications/dependency_labels.md
OBJECT_DEPS_SPACY = {'dobj','dative','attr','oprd','pobj'}
OBJECT_DEPS_STANZA = {'obj','obl'}
OBJECT_DEPS = OBJECT_DEPS_SPACY | OBJECT_DEPS_STANZA
SUBJECT_DEPS = {'nsubj', 'nsubjpass', 'ROOT'}
VERB_DEPS = ['ROOT','root','conj','ccomp','xcomp','advcl','aux']
SINGULAR = {'NN', 'NNP'}
PLURAL = {'NNS', 'NNPS'}


class MockToken:
	"""
	Token consisting of its string, pos-tag, dependency label
	and head. If the token is a prepositional object, its head is a
	preposition, otherwise the head is equal to the string (text)
	"""
	def __init__(self, text, tag, dep, head):
		self.text = text
		self.tag_ = tag
		self.dep_ = dep
		self.head = head

	def __repr__(self):
		return self.text

	def __str__(self):
		return self.text

class MockNounPhrase:
	"""Contains NP as string and its root, i.e. head"""
	def __init__(self, text, root):
		self.text = text
		self.root = root

	def __repr__(self):
		return self.text

	def __str__(self):
		return self.text

def check_np_str(noun_phrase_str):
	"""
	Checks if noun_phrase_str contains one
	of the specified characters
	"""
	chars = {'*', '_', '(', ')', '"'}
	for char in chars:
		if char in noun_phrase_str:
			return True
	return False

def convert_obj_dict(obj_dict, dep, output_file):
	"""
	Converts dictionary containing tuples of strings
	to one containing MockNounPhrase and MockToken objects
	"""
	converted_obj_dict = defaultdict(list)
	for verb in obj_dict:
		for obj in obj_dict[verb]:
			if dep == 'pobj':
				if obj and obj[-1][-1] in SINGULAR|PLURAL|{'PRP'}:
					np_root = MockToken(obj[-1][0], obj[-1][-1], dep, obj[0][0])
					# exclude the preposition when creating the NP string
					noun_phrase = MockNounPhrase(" ".join([word[0] for word in obj[1:]]), np_root)
					if not check_np_str(noun_phrase.text):
						converted_obj_dict[verb].append(noun_phrase)
			else:
				# since the dobj_dict is too big, we exclude every NP whose head is
				# not a noun (this includes pronouns)
				# exclude NPs that contain special characters to further reduce the
				# size of the resulting dictionary
				if obj and obj[-1][-1] in SINGULAR|PLURAL:
					np_root = MockToken(obj[-1][0], obj[-1][-1], dep, obj[-1][0])
					noun_phrase = MockNounPhrase(" ".join([word[0] for word in obj]), np_root)
					if not check_np_str(noun_phrase.text):
						converted_obj_dict[verb].append(noun_phrase)
	with open(output_file, "wb") as out:
		pickle.dump(converted_obj_dict, out)

class Parsing:
	"""
	Parsing functions used for questions and captions
	"""
	def __init__(self, parser='spacy'):
		# load model
		if parser == 'stanza':
			# download English model (if necessary)
			#stanza.download('en') 
			# initialize the pipeline
			self.nlp = spacy_stanza.load_pipeline("en")
		else:
			self.nlp = spacy.load("en_core_web_lg")

	def find_verb_in_np(self, nps):
		"""
		Returns the last verb found in NP
		"""
		for np in nps:
			for token in list(np)[::-1]:
				if token.pos_ == 'VERB':
					return [token]
		return []

	def find_nps_in_np(self, np, verb):
		"""
		Splits one complex NP into smaller NPs,
		tries to determine subject NP and keep
		this one as is
		"""
		if verb.i > np.root.i:
			# subject NP is everything before the verb
			subj_np = np[np.root.left_edge.i : verb.i]
			new_doc = self.nlp(str(np[verb.i : np.root.right_edge.i+1]))
			
			# split everything after verb into basic NPs
			obj_np = self.get_complex_nps(new_doc)
		else:
			# subject NP is everything after the verb
			subj_np = np[verb.i+1 : np.root.right_edge.i+1]
			new_doc = self.nlp(str(np[np.root.left_edge.i : verb.i]))

			# split everything before the verb into basic NPs
			obj_np = self.get_complex_nps(new_doc)
		return [subj_np]+obj_np

	def get_subj_np(self, nps):
		"""
		Find subject NP in NP-list
		"""
		for np in nps:
			if np.root.dep_ in SUBJECT_DEPS:
				return np
		if nps:
			# if no NP has a subject dependency label
			# make first NP in list the subject
			subj = nps[0]
			subj.root.dep_ = 'nsubj'
			return subj
		return ''

	def get_default_verb(self):
		"""
		Selects and returns a default verb randomly
		"""
		default_verbs = [
			MockToken('ignore','VB','ROOT','ignore'),
			MockToken('destroy','VB','ROOT','destroy'),
			MockToken('become','VB','ROOT','become'),
			MockToken('sell','VB','ROOT','sell'),
			MockToken('watching','VBG','ROOT','watching'),
			MockToken('hating','VBG','ROOT','hating'),
			MockToken('inviting','VBG','ROOT','inviting'),
			MockToken('giving','VBG','ROOT','giving'),
			MockToken('befriended','VBD','ROOT','befriended'),
			MockToken('angered','VBD','ROOT','angered'),
			MockToken('admired','VBD','ROOT','admired'),
			MockToken('bought','VBD','ROOT','bought'),
			MockToken('put','VBD','ROOT','put')
			]
		return sample(default_verbs,1)

	def get_complex_nps(self, doc):
		"""
		Returns list with all complex NPs in spaCy doc
		"""
		complex_nps = []
		for np in doc.noun_chunks:
			complex_np = doc[np.root.left_edge.i : np.root.right_edge.i+1]
			complex_nps.append(complex_np)
		# filter out dublicate nps, only keep longest, dont keep substrings
		return filter_spans(complex_nps)

	def modify_nps(self, nps):
		"""
		Performs various minor modifications to NPs
		to ensure a grammatical question
		"""
		modified_nps = []
		for np in nps:
			# change dependency of root NP to nsubj
			# to be able to match a dictionary key
			if np.root.dep_ == 'ROOT':
				np.root.dep_ = 'nsubj'

			# filter out trailing 'and'
			if str(np)[-4:] == ' and':
				np = np[:-1]
			modified_nps.append(np)
		return modified_nps

	def check_prep(self, prep):
		"""
		Checks if prep is part of a complex
		preposition (e.g. next to) and returns it
		"""
		try:
			# if head of preposition is an adverb and adverbial modifier, include
			# it as part of preposition
			if prep.head.tag_ == 'RB' and prep.head.dep_ == 'advmod' and prep.head.pos_ == 'ADV':
				prep = prep.head.text + ' ' + prep.text
		except: 
			pass
		return str(prep)

	def filter_verbs(self, verb_tokens):
		"""
		Filters out verbs that are not to be
		replaced in the templates
		"""
		return [token for token in verb_tokens if token.head.dep_ in VERB_DEPS]

	def get_verbs(self, doc, aux=True):
		"""
		Extract verbs with specified dependency labels from doc
		if aux=True, extract auxiliary verbs as well
		"""
		matcher = Matcher(self.nlp.vocab)
		# patterns for verbs to be extracted
		verb_patterns = [[{'POS':'VERB', 'DEP': {'IN': VERB_DEPS}}],\
						[{'DEP':'prt'}]]
		if aux:
			# add pattern for auxiliary verbs
			verb_patterns.append([{'POS':'AUX'}])
		matcher.add('VERBS', verb_patterns)
		matches = matcher(doc)
		return self.filter_verbs([doc[start:end][0] for _,start,end in matches])
