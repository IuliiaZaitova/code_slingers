import spacy
import stanza
import spacy_stanza
from spacy.util import filter_spans
from spacy.matcher import Matcher
from random import sample

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
	def __init__(self, text, root):
		self.text = text
		self.root = root

	def __repr__(self):
		return self.text

	def __str__(self):
		return self.text


class Parsing:
	def __init__(self, parser='spacy'):
		# load model
		if parser == 'stanza':
			# download English model (if necessary)
			#stanza.download('en') 
			# initialize the pipeline
			self.nlp = spacy_stanza.load_pipeline("en")
		else:
			self.nlp = spacy.load("en_core_web_lg")

	def generate_verb(self, tag):
		#TODO
		return []

	def find_verb_in_np(self, nps):
		# return first verb found in nps
		for np in nps:
			for token in np:
				if token.pos_ == 'VERB':
					return [token]
		return []

	def find_nps_in_np(self, np, verb):
		if verb.i > np.root.i:
			subj_np = np[np.root.left_edge.i : verb.i]
			new_doc = self.nlp(str(np[verb.i : np.root.right_edge.i+1]))
			obj_np = self.get_complex_nps(new_doc)
		else:
			subj_np = np[verb.i+1 : np.root.right_edge.i+1]
			new_doc = self.nlp(str(np[np.root.left_edge.i : verb.i]))
			obj_np = self.get_complex_nps(new_doc)
		return [subj_np]+obj_np

	def get_subj_np(self, nps):
		for np in nps:
			if np.root.dep_ in SUBJECT_DEPS:
				return np
		if nps:
			return nps[0]
		return '' #TODO: return default subj np?

	def get_default_verb(self):
		#[MockToken('is', 'VBZ', 'ROOT', 'is')]
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
		complex_nps = []
		for np in doc.noun_chunks:
			complex_np = doc[np.root.left_edge.i : np.root.right_edge.i+1]
			# get rid of 'trailing and'; a common problem
			if str(complex_np)[-4:] == ' and':
				complex_np = complex_np[:-1]
			complex_nps.append(complex_np)
		# filter out dublicate nps -> only keep longest, dont keep substrings
		return filter_spans(complex_nps)

	def filter_verbs(self, verb_tokens):
		return [token for token in verb_tokens if token.head.dep_ in VERB_DEPS]


	def get_verbs(self, doc, aux=True):
		matcher = Matcher(self.nlp.vocab)
		verb_patterns = [[{'POS':'VERB', 'DEP': {'IN': VERB_DEPS}}],\
						[{'DEP':'prt'}]]
		if aux:
			verb_patterns.append([{'POS':'AUX'}])
		matcher.add('VERBS', verb_patterns)
		matches = matcher(doc)
		return self.filter_verbs([doc[start:end][0] for _,start,end in matches])