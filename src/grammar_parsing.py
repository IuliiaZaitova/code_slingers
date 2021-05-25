import stanza
import pickle

class Word_parser:
    """Grammar parsing class"""
    def __init__(self, word):
        self.nlp = stanza.Pipeline(lang='en', processors='tokenize, lemma, pos') # For lemmalization and pos-tagging
        self.ft = fasttext.load_model('data/cc.eng.300.bin') # Has to be downloaded
        self.verb_trans = pickle.load(open('verb_trans.p', 'rb'))

    def get_lemma(self, word):
        # Returns the lemma of English words
        doc = self.nlp(word)
        for sentence in doc.sentences:
            for word in sentence.words:
                lemma = word.lemma
        return lemma

    def get_transitivity(self, verb):
        # Returns verb transitivity type generated with probabilities from 'https://github.com/wilcoxeg/verb_transitivity'
        v_lemma = get_lemma(verb)
        if v_lemma in self.verb_trans:
            p = np.array(verb_trans[v_lemma]) # Obtain probabilities of transitivity types
            p /= p.sum()  # normalize, ps have to sum up to 1
            trans_type = np.random.choice(['intrans', 'trans', 'ditrans'], p=p)
        else:
            trans_type = 'intrans'
        return trans_type