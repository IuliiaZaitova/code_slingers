#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

DATASET = 'shortjokes.csv'
WHYJ = 'why_jokes.txt'
WHATJ = 'what_jokes.txt'
HOWJ = 'how_jokes.txt'

WHYJ_PARSED = 'why_jokes_parsed.txt'
WHATJ_PARSED = 'what_jokes_parsed.txt'
HOWJ_PARSED = 'how_jokes_parsed.txt'

WHY_REGEX = r',"\s*(\[.+?\])?(q:)?\s*why.*?(?<!\?")$'
WHAT_REGEX = r',"\s*(\[.+?\])?(q:)?\s*what.*?(?<!\?")$'
HOW_REGEX = r',"\s*(\[.+?\])?(q:)?\s*how.*?(?<!\?")$'

def split_jokes(joke):
	q, a = joke.split('?',1)
	q = re.split('\d,"', q)[-1].strip()
	a = a.strip('" \n')
	return q, a

def split_why_jokes(joke):
	if '?' in joke:
		q, a = joke.split('?',1)
	elif 'because' in joke:
		q, a = joke.split('because',1)
		a = 'because'+ a
	elif 'Because' in joke:
		q, a = joke.split('Because',1)
		a = 'Because'+ a
	elif '.' in joke:
		q, a = joke.split('.',1)
	else:
		return '', ''
	q = re.split('\d,"', q)[-1].strip()
	a = a.strip('" \n')
	return q, a



with open(DATASET, encoding='utf-8') as f,\
	open(WHYJ, 'w', encoding='utf-8') as why,\
	open(WHATJ, 'w', encoding='utf-8') as what,\
	open(HOWJ, 'w', encoding='utf-8') as how:
	for line in f:
		if re.search(WHY_REGEX, line.lower()):
			q, a = split_why_jokes(line)
			if q and a:
				why.write(f'{q}\t{a}\n')
		elif '?' in line:
			if re.search(HOW_REGEX, line.lower()):
				q, a = split_jokes(line)
				how.write(f'{q}\t{a}\n')
			elif re.search(WHAT_REGEX, line.lower()):
				q, a = split_jokes(line)
				what.write(f'{q}\t{a}\n')

# Adds tags <soq> <eoq> <eoa> <eoj>
with open(DATASET, encoding='utf-8') as f, \
	open(WHYJ_PARSED, 'w', encoding='utf-8') as why_parsed,\
	open(WHATJ_PARSED, 'w', encoding='utf-8') as what_parsed,\
	open(HOWJ_PARSED, 'w', encoding='utf-8') as how_parsed:
	for line in f:
		if re.search(WHY_REGEX, line.lower()):
			q, a = split_why_jokes(line)
			if q and a:
				why_parsed.write(f'<soq>{q}<eoq>{a}<eoa><eoj>\n')
		elif '?' in line:
			if re.search(HOW_REGEX, line.lower()):
				q, a = split_jokes(line)
				how_parsed.write(f'<soq>{q}<eoq>{a}<eoa><eoj>\n')
			elif re.search(WHAT_REGEX, line.lower()):
				q, a = split_jokes(line)
				what_parsed.write(f'<soq>{q}<eoq>{a}<eoa><eoj>\n')