import re
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from parsing import *


class Templates:
	def __init__(self):
		self.aux = defaultdict(set)
		self.prep = defaultdict(set)

	def get_template_per_slot(self, templates, slot, n_most_freq=10):
		temp = templates[templates['np_slots'] == slot]
		top_n_temp = pd.value_counts(temp['generaltemplate'])[:n_most_freq].index.values
		temp = temp.query('generaltemplate in @top_n_temp')
		return temp.fillna('')

	def show_plot(self, df, column, xlabel, ylabel, title, n_largest):
		pd.value_counts(df[column])[:n_largest].plot(kind='barh')
		for index, value in enumerate(df[column].value_counts()[:n_largest]):
			label = df[column].value_counts().index.tolist()[index]
			plt.text(value, index, f' {value}', va='center')
		plt.tight_layout() # helps to make long labels fit
		plt.gca().spines['right'].set_color('none') # get rid of right line of box
		plt.gca().spines['top'].set_color('none') # get rid of top line of box
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)
		plt.show()

	def load_templates_to_df(self, template_dir):
		header = ['question', 'generaltemplate', 'template',\
	 			'subj_tags', 'obj_tags', 'verb_tags', 'aux_tags', 'np_slots']
		template_df = pd.read_table(template_dir, sep="\t", names=header)
		return template_df

	def save_templates(self, template_dict, output_file):
		with open(output_file, "wb") as out:
			pickle.dump(template_dict, out)

	def convert_templates_to_dict(self, temp_df):
		template_dict = defaultdict(lambda: defaultdict(set))
		temp_df['np_tags'] = temp_df['subj_tags']+','+temp_df['obj_tags']
		for v_tags,np_tags,temp in zip(temp_df['verb_tags'], temp_df['np_tags'], temp_df['template']):
			verb_key = tuple(tag for tag in v_tags.split(',') if tag)
			# delete entity label
			np_key = tuple(sorted([re.sub(r'.*?/',"",tag) for tag in np_tags.split(',') if tag]))
			template_dict[verb_key][np_key].add(temp)
		return dict(template_dict)

	def replace_verbs(self, doc, template, general_template, verbs):
		verb_tags, aux_tags = [], []
		for token in verbs:
			#if token.dep_ != 'aux':
			template[token.i] = f'<{token.tag_}>_{token.dep_}'
			general_template[token.i] = \
				'VERB' if token.dep_ not in {'aux','prt'} else str(token.dep_).upper()
			if token.dep_ == 'aux':
				self.aux[str(token.tag_)].add(str(token))
				aux_tags.append(str(token.tag_))
			else:
				verb_tags.append(str(token.tag_))
		return template, general_template, verb_tags, aux_tags

	def replace_prep(self, doc, template, general_template, prep_token):
		template[prep_token.i] = f'<{prep_token.tag_}>_{prep_token.dep_}'
		general_template[prep_token.i] = 'PREP'
		self.prep[str(prep_token.tag_)].add(str(prep_token))
		return template, general_template

	def replace_nps(self, doc, template, general_template, nps):
		subj_tags, obj_tags = [], []
		for np in nps:
			head = np.root
			np_start, np_end = head.left_edge.i, head.right_edge.i+1
			try:
				if list(doc[np_start : np_end]) == template[np_start : np_end]:
					entity, tag = head.ent_type_, head.tag_
					label = entity+'/'+tag if entity else tag
					padding = (np_end-np_start) - 1
					np_string = f'<{label}>_NP_{head.dep_}'
					template[np_start : np_end] = [np_string] + padding*['']
					general_template[np_start : np_end] = ['NP'] + padding*['']

					if head.dep_ == 'pobj' and head.head.dep_ == 'prep':
						template, general_template = \
							self.replace_prep(doc, template, general_template, head.head)

					if head.dep_ in SUBJECT_DEPS:
						subj_tags.append(label)
					else:
						obj_tags.append(label)
			except:
				# parts of NP have already been replaced --> most likely parsing error
				return [], [], [], []
		return template, general_template, subj_tags, obj_tags

	def create_templates(self, dataset, output_file):
		parser = Parsing()

		with open(dataset) as data,\
		open(output_file, 'w') as out:
			for line in data:
				question = line.split('\t')[0]
				doc = parser.nlp(question)
				complex_nps = parser.get_complex_nps(doc)
				verbs = parser.get_verbs(doc)
				template, general_template, verb_tags, aux_tags = \
						self.replace_verbs(doc, list(doc), list(doc), verbs)
				template, general_template, subj_tags, obj_tags = \
						self.replace_nps(doc, template, general_template, complex_nps)

				template = ' '.join([str(token) for token in template if token])
				general_template = ' '.join([str(token) for token in general_template if token])
				np_slots = len(subj_tags) + len(obj_tags)

				out.write(f'{question}\t{general_template}\t{template}\t'\
					f'{",".join(subj_tags)}\t{",".join(obj_tags)}\t'\
					f'{",".join(verb_tags)}\t{",".join(aux_tags)}\t{np_slots}\n')


'''
WHYJ = 'why_clean.txt'
temps = Templates()
#temps.create_templates(WHYJ, 'test_templates.txt')
df = temps.load_templates_to_df('test_templates.txt')
one_slot_df = temps.get_template_per_slot(df, 1)
one_slot = temps.convert_templates_to_dict(one_slot_df)
two_slots_df = temps.get_template_per_slot(df, 2)
two_slots = temps.convert_templates_to_dict(two_slots_df)
three_slots_df = temps.get_template_per_slot(df, 3)
three_slots = temps.convert_templates_to_dict(three_slots_df)
temps.save_templates(two_slots, 'two_slots.pkl')
temps.save_templates(three_slots, 'three_slots.pkl')#'''
#temps.show_plot(one_slot_df, 'generaltemplate', 'Frequency', 'Templates', 'Frequency of Templates', 10)












