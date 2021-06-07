import stanza
import pickle
import numpy as np
import random
import fasttext
class Word_parser:
    """Grammar parsing class"""
    def __init__(self):
        self.nlp = stanza.Pipeline(lang='en', processors='tokenize, lemma, pos') # For lemmatization and pos-tagging
        #self.ft = fasttext.load_model('cc.eng.300.bin') # Has to be downloaded
        self.verb_trans = pickle.load(open('data/verb_trans.p', 'rb'))
        self.dobjs = pickle.load(open('data/verb_dict_dobj.p', 'rb'))
        self.pobjs = pickle.load(open('data/verb_dict_pobj.p', 'rb'))


    def get_lemma(self, word):
        # Returns the lemma of English words
        doc = self.nlp(word)
        for sentence in doc.sentences:
            for word in sentence.words:
                lemma = word.lemma
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
        print(trans_type)
        return objs