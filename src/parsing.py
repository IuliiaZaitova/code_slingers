import spacy
import stanza
import spacy_stanza
from spacy.util import filter_spans
from spacy.matcher import Matcher

# dependency labels
# see https://github.com/clir/clearnlp-guidelines/blob/master/md/specifications/dependency_labels.md
OBJECT_DEPS_SPACY = {'dobj','dative','attr','oprd','pobj'}
OBJECT_DEPS_STANZA = {'obj','obl'}
OBJECT_DEPS = OBJECT_DEPS_SPACY | OBJECT_DEPS_STANZA
SUBJECT_DEPS = {'nsubj', 'nsubjpass'}
VERB_DEPS = ['ROOT','root','conj','ccomp','xcomp','advcl','aux']



class MockToken:
	def __init__(self, text, tag, dep):
		self.text = text
		self.tag_ = tag
		self.dep_ = dep

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
			# download with python3 -m spacy download en_core_web_lg
			self.nlp = spacy.load("en_core_web_lg")

	def generate_verb(self, tag):
		#TODO
		return []

	def generate_np(self, tag):
		#TODO
		return []

	def find_verb_in_np(self, nps):
		# return first verb found in nps
		for np in nps:
			for token in np:
				if token.pos_ == 'VERB':
					return [token]
		return []

	def get_default_verb(self):
		return [MockToken('is', 'VBZ', 'ROOT')]

	def get_complex_nps(self, doc):
		complex_nps = []
		for np in doc.noun_chunks:
			#if np.root.dep_ in SUBJECT_DEPS|OBJECT_DEPS:
			complex_nps.append(doc[np.root.left_edge.i : np.root.right_edge.i+1])
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