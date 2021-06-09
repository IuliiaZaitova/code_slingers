import re
from templates import *
from random import sample


class QuestionGenerator:
	def __init__(self):
		self.parser = Parsing()
		self.one_slot = pickle.load(open('one_slot.pkl', 'rb'))
		self.two_slots = pickle.load(open('two_slots.pkl', 'rb'))
		self.three_slots = pickle.load(open('three_slots.pkl', 'rb'))

	def parse_caption(self, caption):
		doc = self.parser.nlp(caption)
		verbs = self.parser.get_verbs(doc, False)
		nps = self.parser.get_complex_nps(doc)

		if not verbs:
			verbs = self.parser.find_verb_in_np(nps)
			if not verbs:
				verbs = self.parser.get_default_verb()
			else:
				# get basic NPs instead
				nps = list(doc.noun_chunks)
		return verbs, nps


	def get_aux(self):
		# TODO
		return ''

	def choose_template(self, verbs, nps):

		verb_key = tuple(sorted([verb.tag_ for verb in verbs]))
		np_key = tuple(sorted([np.root.tag_ for np in nps]))

		if len(nps) == 1:
			templates = self.one_slot
		elif len(nps) == 2:
			templates = self.two_slots
		else:
			templates = self.three_slots
			nps = nps[:3]

		if verb_key in templates:
			temp_verb_match = templates[verb_key]
		else:
			# TODO: generate different verb?
			# try filter out 'RP'?
			if 'RP' in verb_key:
				verbs = [verb for verb in verbs if verb.tag_ != 'RP']
				return self.choose_template(verbs, nps)
			else:
				return '', nps

		if temp_verb_match:
			try:
				temp_np_match = temp_verb_match[np_key]
			except KeyError:
				temp_np_match = {}
			if temp_np_match:
				return sample(temp_np_match, 1)[0], nps
			else:
				return '', nps
		else:
			return '', nps

	def fill_template(self, template, verbs, nps):
		filled_template = []
		for word in template.split():
			if '<' not in word:
				filled_template.append(word)
				continue

			word_info = word.split('_')
			tag = word_info[0][1:-1]
			dep = word_info[-1]

			if len(word_info) == 2:
				# fill in a verb
				if dep == 'aux':
					#aux = self.get_aux(tag)
					filled_template.append(word)
				elif dep == 'prep':
					#prep = self.get_prep(tag)
					filled_template.append(word)
				else:
					for verb in verbs:
						if str(verb.tag_) == tag:
							filled_template.append(str(verb))
							verbs.remove(verb)
			elif len(word_info) == 3:
				# fill in NP
				for np in nps:
					if str(np.root.tag_) == tag:
						filled_template.append(str(np))
						nps.remove(np)
						break
		return " ".join(filled_template)

'''
new_question = QuestionGenerator()

with open('example_captions.csv', encoding='utf-8') as f:
	for line in f:
		caption = line.strip().split(',')[2]
		verbs, nps = new_question.parse_caption(caption)
		template, nps = new_question.choose_template(verbs, nps)
		question = new_question.fill_template(template, verbs, nps)
		print('caption:', caption, 'question:', question)#'''
