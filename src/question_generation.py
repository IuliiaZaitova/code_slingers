import re
from templates import *
from random import sample
from grammar_parsing import *


class QuestionGenerator:
	def __init__(self, generate_objects=True):
		self.parser = Parsing()
		self.one_slot = pickle.load(open('one_slot.pkl', 'rb'))
		self.two_slots = pickle.load(open('two_slots.pkl', 'rb'))
		self.three_slots = pickle.load(open('three_slots.pkl', 'rb'))
		self.aux = pickle.load(open('aux_verbs.pkl', 'rb'))
		self.prep = pickle.load(open('prep.pkl', 'rb'))
		self.gen_obj = True if generate_objects else False


	def parse_caption(self, caption):
		doc = self.parser.nlp(caption)
		verbs = self.parser.get_verbs(doc, False)
		nps = self.parser.get_complex_nps(doc)

		if not verbs:
			verbs = self.parser.find_verb_in_np(nps)
			if not verbs:
				verbs = self.parser.get_default_verb()
			else:
				# get NPs before and after verb
				nps = self.parser.find_nps_in_np(nps[0], verbs[0])
		return verbs, nps


	def get_aux(self, tag, verb_tag=False, np_num=False):
		# check compatibility with verb

		if verb_tag in {'VBG', 'VBN'}:
			if tag == 'VBZ':
				return 'is'
			elif tag == 'VBP':
				return 'are'
			if np_num == 'sg':
				return 'was'
			else:
				return 'were'
		#TODO:
		# if verb.tag_ == 'VB':
		# np_num == 'sg':
		#return 'does' or 'did'

		auxs = self.aux[tag]
		try:
			if np_num == 'sg':
				auxs.remove('were')
			elif np_num == 'pl':
				auxs.remove('was')
			return sample(auxs, 1)[0]

		except:
			return sample(self.aux[tag], 1)[0]

	def get_prep(self, tag, suggestion=False):
		if suggestion:
			if suggestion.dep_ == 'prep':
				#TODO:
				# if head of prep RB advmod get it too?
				# if head of prep not the verb get it too?
				return suggestion
		return sample(self.prep[tag], 1)[0]


	def choose_template(self, verbs, nps):

		# get template dictionary based on NP slots
		if len(nps) == 1:
			templates = self.one_slot
		elif len(nps) == 2:
			templates = self.two_slots
		else:
			templates = self.three_slots
			# only keep first three NPs
			# TODO: choose which NPs to keep? E.g keep subj-NP over obj-NP?
			nps = nps[:3]

		# create dictionary keys
		verb_key = tuple(sorted([verb.tag_ for verb in verbs]))
		if len(nps) == 1:
			np_key = [f'{np.root.tag_}' for np in nps]
		else:
			# change dependency of root NP to nsubj
			# to be able to match a dictionary key
			np_key = [f'{np.root.tag_}_{np.root.dep_}'.replace('ROOT','nsubj') for np in nps]
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
			# TODO: generate different verb?
			# try filter out 'RP'?
			if 'RP' in verb_key:
				verbs = [verb for verb in verbs if verb.tag_ != 'RP']
				return self.choose_template(verbs, nps)
			return '', nps

	def fill_template(self, template, verbs, nps):
		filled_template = []
		aux_ind = -1

		# default number of np and tag of verb
		np_num = 'sg' if nps[0].root.tag_ in SINGULAR else 'pl'
		verb_tag = verbs[0].tag_


		for word in template.split():
			if '<' not in word:
				filled_template.append(word)
				continue

			slot_info = word.split('_')
			tag, dep = slot_info[0][1:-1], slot_info[-1]

			if len(slot_info) == 2:
				if dep == 'aux':
					filled_template.append(str(word))
					aux_ind = len(filled_template)-1
				elif dep == 'prep':
					filled_template.append(word)
				else:
					for verb in verbs:
						if verb.dep_ == 'ROOT':
							verb_tag = verb.tag_
						if str(verb.tag_) == tag:
							filled_template.append(str(verb))
							verbs.remove(verb)
			elif len(slot_info) == 3:
				# fill in NP
				for np in nps:
					if np.root.tag_ == tag:
						if np.root.dep_ in SUBJECT_DEPS:
							np_num = 'sg' if tag in SINGULAR else 'pl'
						if np.root.dep_ == 'pobj' and '_prep' in filled_template[-1]:
								prep_tag = filled_template[-1].split('_')[0][1:-1]
								prep_suggestion = np.root.head
								prep = self.get_prep(prep_tag, prep_suggestion)
								filled_template = filled_template[:-1] + [str(prep)]
						filled_template.append(str(np))
						nps.remove(np)
						break
					else:
						return ''

		# get auxiliary verb
		if aux_ind >= 0:
			aux_tag = filled_template[aux_ind].split('_')[0][1:-1]
			aux = self.get_aux(aux_tag, verb_tag, np_num)
			filled_template[aux_ind] = aux
		return " ".join(filled_template)


#new_question = QuestionGenerator(generate_objects=True)

'''
with open('example_captions.csv', encoding='utf-8') as f:
	for line in f:
		
		caption = line.strip().split(',')[2]
		doc = new_question.parser.nlp(caption)

		verbs, nps = new_question.parse_caption(caption)

		# get subject np
		subj = new_question.parser.get_subj_np(nps)

		if new_question.gen_obj:
			word_parser = Word_parser()
			obj = word_parser.get_objects(verbs[0])
			print('objects', obj, type(obj))
			for obje in obj:
				print('obj', obje, type(obje))
			if obj:
				nps = [subj]+obj

		template, nps = new_question.choose_template(verbs, nps)

		question = new_question.fill_template(template, verbs, nps)
		print('caption: ', caption, 'question: ', question)#'''
