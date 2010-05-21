#  Lorem Ipsum Generator for Gedit
#
#  Copyright (C) 2010 Franck Marcia
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Parse a request and return 'lorem ipsum' string accordingly

Command format:

	c[haracters] [case] [number_of_characters]
	a[lphanumeric] [case] [number_of_characters]
	w[ords] [case] [number_of_words]
	s[entences] [case] [number_of_words_1 [number_of_words_2 [...]]]
	l[ist] [case] [number_of_words_1 [number_of_words_2 [...]]]

	where case is { u[pper] | lo[wer] | t[itle] }
	and number_of_words is an integer or a multiplication (for example '3*6')
	
	commands can be shorten by using initials. For example, "wt 9" is equivalent
	to "words title 9"
	
	see examples at the end of this script

@author Franck Marcia (franck.marcia@gmail.com)
@link http://github.com/fmarcia/zen-coding-gedit
'''

import random

words = [
	'lorem','ipsum','dolor','sit','amet','consectetur','adipisicing','elit',
	'sed','do','eiusmod','tempor','incididunt','ut','labore','et','dolore',
	'magna','aliqua','ut','enim','ad','minim','veniam','quis','nostrud',
	'exercitation','ullamco','laboris','nisi','ut','aliquip','ex','ea',
	'commodo','consequat','duis','aute','irure','dolor','in',
	'reprehenderit','in','voluptate','velit','esse','cillum','dolore','eu',
	'fugiat','nulla','pariatur','excepteur','sint','occaecat','cupidatat',
	'non','proident','sunt','in','culpa','qui','officia','deserunt',
	'mollit','anim','id','est','laborum'
]
words_bound = 68 # number of words minus 1
words_reset = 23 # number of words per excerpt

characters = [
	'a','b','c','d','e','f','g','h','i','j','k','l','m',
	'n','o','p','q','r','s','t','u','v','w','x','y','z'
]
characters_bound = 25

alphanumeric = [
	'a','b','c','d','e','f','g','h','i','j','k','l','m',
	'n','o','p','q','r','s','t','u','v','w','x','y','z',
	'0','1','2','3','4','5','6','7','8','9'
]
alphanumeric_bound = 35

def get_characters(case, params):
	result = ''
	for char in range(0, params[0]):
		char = characters[random.randint(0, characters_bound)]
		if case == 'upper':
			char = char.upper()
		result += char
	if case == 'title':
		return result.title()
	return result

def get_alphanumeric(case, params):
	result = ''
	for char in range(0, params[0]):
		char = alphanumeric[random.randint(0, alphanumeric_bound)]
		if case == 'upper':
			char = char.upper()
		result += char
	if case == 'title':
		return result.title()
	return result

def get_words(case, params):
	size = params[0]
	start = 0
	result = []
	while True:
		end = size if start + words_reset > size else start + words_reset
		start_ex = random.randint(0, words_bound - end + start)
		#print words_bound - end + start
		#start = random.randint(0, words_bound - params[0] + 1)
		end_ex = start_ex + end - start
		for word in words[start_ex:end_ex]:
			if case == 'upper':
				result.append(word.upper())
			elif case == 'lower':
				result.append(word.lower())
			elif case == 'title':
				result.append(word.title())
			else:
				result.append(word)
		if end == size:
			break
		start += words_reset
	return ' '.join(result)

def get_sentences(case, params):
	result = []
	for nbwords in params:
		sentence = get_words(case, [nbwords])
		if case == '':
			sentence = sentence.capitalize()
		result.append(sentence)
	return '. '.join(result) + '.'

def get_list(case, params):
	result = []
	for nbwords in params:
		item = get_words(case, [nbwords])
		if case == '':
			item = item.capitalize()
		result.append(item)
	return '\n'.join(result)

def lorem_ipsum(command):

	args = command.split(' ')
	if args[0] == '':
		return ''

	def parse(args):
		method, case, params = None, '', []
		for arg in args:
			arg = arg.lower()
			if arg == '': pass
			elif arg == 'cu': method = get_characters; case = 'upper'
			elif arg == 'cl': method = get_characters; case = 'lower'
			elif arg == 'ct': method = get_characters; case = 'title'
			elif arg == 'au': method = get_alphanumeric; case = 'upper'
			elif arg == 'al': method = get_alphanumeric; case = 'lower'
			elif arg == 'at': method = get_alphanumeric; case = 'title'
			elif arg == 'wu': method = get_words; case = 'upper'
			elif arg == 'wl': method = get_words; case = 'lower'
			elif arg == 'wt': method = get_words; case = 'title'
			elif arg == 'su': method = get_sentences; case = 'upper'
			elif arg == 'sl': method = get_sentences; case = 'lower'
			elif arg == 'st': method = get_sentences; case = 'title'
			elif arg == 'lu': method = get_list; case = 'upper'
			elif arg == 'll': method = get_list; case = 'lower'
			elif arg == 'lt': method = get_list; case = 'title'
			elif 'characters'.startswith(arg): method = get_characters
			elif 'alphanumeric'.startswith(arg): method = get_alphanumeric
			elif 'words'.startswith(arg): method = get_words
			elif 'sentences'.startswith(arg): method = get_sentences
			elif 'list'.startswith(arg): method = get_list
			elif 'upper'.startswith(arg): case = 'upper'
			elif 'lower'.startswith(arg): case = 'lower'
			elif 'title'.startswith(arg): case = 'title'
			elif arg.isdigit(): params.append(int(arg))
			else:
				try:
					test = arg.split('*')
					if len(test) == 2:
						for x in range(0, int(test[1])):
							params.append(int(test[0]))
				except:
					pass
		if len(params) == 0:
			params = [1]
		return method, case, params
		
	method, case, params = parse(args)
	if method is None:
		method = get_list
	return method(case, params)

if __name__ == '__main__':
	def echo(x):
		print x + ':', '(' + lorem_ipsum(x) + ')'
	echo('')
	echo('characters')
	echo('characters 10')
	echo('characters upper 10')
	echo('characters lower 12')
	echo('characters title 14')
	echo('alphanumeric')
	echo('alphanumeric 10')
	echo('alphanumeric upper 16')
	echo('alphanumeric lower 14')
	echo('alphanumeric title 15')
	echo('word')
	echo('word 7')
	echo('word upper 5')
	echo('word lower 7')
	echo('word title 9')
	echo('sentences')
	echo('sentences 5 3 9')
	echo('sentences upper 5 3 1')
	echo('sentences lower 4 4 7')
	echo('sentences title 7 4 6')
	echo('list')
	echo('list 5')
	echo('list 4 7')
	echo('list upper 3 2')
	echo('list lower 4 1')
	echo('list title 2 4')
	echo('c 10')
	echo('c u 10')
	echo('a 10')
	echo('a t 10')
	echo('w 7')
	echo('w l 7')
	echo('s 5 3 9')
	echo('s t 7 4 6')
	echo('l 4 7')
	echo('l u 3 2 6')
	echo('cu 10')
	echo('au 10')
	echo('wl 7')
	echo('st 7 4 6')
	echo('lu 3 2 6')
	echo('l 7*5')
