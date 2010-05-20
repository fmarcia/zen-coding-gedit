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
	l[etters] [case] [quantity]
	w[ords] [case] [quantity]
	s[entences] [case] [quantity_1 [quantity_2 [...]]]
	
	where case is { u[pper] | l[ower] | t[itle] }

@author Franck Marcia (franck.marcia@gmail.com)
@link http://github.com/fmarcia/zen-coding-gedit
'''

import random

def lorem_ipsum(command):

	args = command.split(' ')
	if args[0] == '':
		return ''

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

	letters = [
		'a','b','c','d','e','f','g','h','i','j','k','l',
		'm','n','o','p','q','r','s','t','u','v','w','x','y','z'
	]
	letters_bound = 25

	def parse(args):
		case, params = '', []
		for arg in args:
			arg = arg.lower()
			if arg == '': pass
			elif 'upper'.startswith(arg): case = 'upper'
			elif 'lower'.startswith(arg): case = 'lower'
			elif 'title'.startswith(arg): case = 'title'
			elif arg.isdigit(): params.append(int(arg))
		if len(params) == 0: params = [1]
		return case, params
		
	def get_letters(case, params):
		result = ''
		for letter in range(0, params[0]):
			letter = letters[random.randint(0, letters_bound)]
			if case == 'upper':
				letter = letter.upper()
			result += letter
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

	case, params = parse(args[1:])
	method = args[0].lower()
	if 'letters'.startswith(method): return get_letters(case, params)
	elif 'words'.startswith(method): return get_words(case, params)
	elif 'sentences'.startswith(method): return get_sentences(case, params)
	return ''

if __name__ == '__main__':
	def echo(x):
		print x + ':', '(' + lorem_ipsum(x) + ')'
	echo('')
	echo('letters')
	echo('letters 10')
	echo('letters upper 10')
	echo('letters lower 12')
	echo('letters title 14')
	echo('word')
	echo('word 7')
	echo('word upper 5')
	echo('word lower 7')
	echo('word title 9')
	echo('sentence')
	echo('sentence 5 3 9')
	echo('sentence upper 5 3 1')
	echo('sentence lower 4 4 7')
	echo('sentence title 7 4 6')

