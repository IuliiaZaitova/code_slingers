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



import re
from parsing import *
from random import sample
from grammar_parsing import *


class QuestionGenerator:
	"""
	Generates a question by extracting verbs and
	NPs from a given string and filling them into
	pre-determined templates
	"""
	def __init__(self, generate_objects=True):
		# initialize parser
		self.parser = Parsing()

		# dictionaries for templates
		self.one_slot = pickle.load(open('data/one_slot.pkl', 'rb'))
		self.two_slots = pickle.load(open('data/two_slots.pkl', 'rb'))
		self.three_slots = pickle.load(open('data/three_slots.pkl', 'rb'))

		# dictionary for auxiliary verbs
		self.aux = pickle.load(open('data/aux_verbs.pkl', 'rb'))

		# dictionary for prepositions
		self.prep = pickle.load(open('data/prep.pkl', 'rb'))
		self.gen_obj = generate_objects

	def parse_caption(self, caption):
		"""
		Extracts verbs and noun phrases from caption
		"""
		doc = self.parser.nlp(caption)
		verbs = self.parser.get_verbs(doc, False)
		nps = self.parser.get_complex_nps(doc)

		if not verbs:
			# find verb in complex NP
			verbs = self.parser.find_verb_in_np(nps)
			if not verbs:
				# get default verb
				verbs = self.parser.get_default_verb()
			else:
				# get NPs before and after verb
				nps = self.parser.find_nps_in_np(nps[0], verbs[0])

		# apply further modifications to nps
		nps = self.parser.modify_nps(nps)

		return verbs, nps


	def get_aux(self, tag, verb_tag=False, np_num=False, neg=False):
		"""
		Finds an auxiliary verb that is compatible with
		tense of main verb, singular/plural information
		of subject NP and possible negation in template
		"""
		# check compatibility with verb and sg/pl
		if verb_tag in {'VBG', 'VBN'}:
			if tag == 'VBZ':
				return 'is'
			elif tag == 'VBP':
				return 'are'
			if np_num == 'sg':
				return 'was'
			else:
				return 'were'

		if verb_tag == 'VB':
			if tag == 'VBZ':
				return 'does'
			elif tag == 'VBP':
				return 'do'
			elif tag == 'VBD':
				return 'did'

		if verb_tag == 'VBD':
			if tag in {'VB', 'VBP'}:
				return 'have'
			elif tag == 'VBZ':
				return 'has'
			elif tag == 'VBD':
				return 'had'

		auxs = self.aux[tag]

		# make auxiliary verbs compatible with negation
		auxs = auxs & self.aux['NEG'] if neg else auxs - {'wo','ca'}
		try:
			if np_num == 'sg':
				auxs.remove('were')
			elif np_num == 'pl':
				auxs.remove('was')
			return sample(auxs, 1)[0]
		except:
			return sample(auxs, 1)[0]

	def get_prep(self, tag, suggestion=False):
		"""
		Checks if suggestion is a preposition,
		otherwise return a random preposition
		"""
		if suggestion:
			if suggestion.dep_ == 'prep':
				return suggestion
		return sample(self.prep[tag], 1)[0]


	def choose_template(self, verbs, nps):
		"""
		Finds a template that matches POS-tag and 
		dependency information of the given verbs and NPs
		"""
		# get template dictionary based on NP slots
		if len(nps) == 1:
			templates = self.one_slot
		elif len(nps) == 2:
			templates = self.two_slots
		else:
			templates = self.three_slots
			# only keep first three NPs since we
			# don't have templates for more NPs
			nps = nps[:3]

		# create dictionary keys
		verb_key = tuple(sorted([verb.tag_ for verb in verbs]))
		if len(nps) == 1:
			np_key = [f'{np.root.tag_}' for np in nps]
		else:
			np_key = [f'{np.root.tag_}_{np.root.dep_}' for np in nps]
		np_key = tuple(sorted(np_key))

		# get template from template dictionary
		if verb_key in templates:
			try:
				matches = templates[verb_key][np_key]
				return sample(matches,1)[0], nps
			except:
				if len(nps) > 1:
					# delete an NP and search for templates again
					nps.pop()
					return self.choose_template(verbs, nps)
				return '', nps
		else:
			# try filter out 'RP'
			if 'RP' in verb_key:
				verbs = [verb for verb in verbs if verb.tag_ != 'RP']
				return self.choose_template(verbs, nps)
			return '', nps

	def fill_template(self, template, verbs, nps):
		"""
		Replaces the placeholder labels in the templates
		with matching verbs, prepositions and NPs
		"""
		filled_template = []
		# is the auxiliary verb negated?
		neg = " n't " in template
		# position of auxiliary verb
		aux_ind = -1

		# default grammatical number of NP
		np_num = 'sg' if nps[0].root.tag_ in SINGULAR else 'pl'

		# default verb tag
		verb_tag = verbs[0].tag_

		for word in template.split():
			if '<' not in word:
				filled_template.append(word)
				continue

			slot_info = word.split('_')

			# POS-tag and dependency label of slot
			tag, dep = slot_info[0][1:-1], slot_info[-1]

			# if length of split label is 2,
			# a verb needs to go into this slot
			if len(slot_info) == 2:
				if dep == 'aux':
					filled_template.append(str(word))

					# update auxiliary verb position
					aux_ind = len(filled_template)-1
				elif dep == 'prep':
					filled_template.append(word)
				else:
					for verb in verbs:
						if verb.dep_ == 'ROOT':

							# update POS-tag of main verb
							verb_tag = verb.tag_
						if str(verb.tag_) == tag:

							# fill in verb in template and
							# remove it from open verb list
							filled_template.append(str(verb))
							verbs.remove(verb)
			elif len(slot_info) == 3:

				# if length of split label is 3,
				# an NP needs to go into this slot
				for np in nps:
					if len(nps) == 1:
						# if we only have one NP, check for matching
						# POS-tag only
						np_match = np.root.tag_ == tag
					else:
						# check for matching POS-tag and dependency
						np_match = np.root.tag_ == tag and np.root.dep_ == dep
					if np_match:
						if np.root.dep_ in SUBJECT_DEPS:
							# update grammatical number of subject NP
							np_num = 'sg' if tag in SINGULAR else 'pl'

						# if we have a prepositional object NP, get matching
						# preposition as well
						if np.root.dep_ == 'pobj' and '_prep' in filled_template[-1]:

							# get POS-tag of preposition
							prep_tag = filled_template[-1].split('_')[0][1:-1]

							# check if it's a complex preposition
							prep = self.parser.check_prep(np.root.head)

							# fill preposition into template
							filled_template = filled_template[:-1] + [prep]

						# fill NP into template
						filled_template.append(str(np))

						# we cannot remove np directly (with e.g. nps.remove(np))
						# because it might not be a spacy span object
						# in this case python would throw an error
						nps = [item for item in nps if item.text != np.text]
						break

		# get auxiliary verb and fill into template
		if aux_ind >= 0:

			# get POS-tag of auxiliary verb
			aux_tag = filled_template[aux_ind].split('_')[0][1:-1]

			# get auxiliary verb
			aux = self.get_aux(aux_tag, verb_tag, np_num, neg)
			filled_template[aux_ind] = aux

		return " ".join(filled_template)

