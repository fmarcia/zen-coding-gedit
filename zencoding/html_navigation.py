#  Html Navigation for Gedit
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
Parse HTML content to navigate through its nodes

@author Franck Marcia (franck.marcia@gmail.com)
@link http://github.com/fmarcia/zen-coding-gedit
'''

import re

class Node ():

	def __init__(self, type, name = '', start = 0, end = 0, parent = None):
		self.type = type
		self.name = name
		self.start = start
		self.end = end
		self.parent = parent
		self.children = []

	def __str__(self):
		if self.name:
			return '<%s:%s:%d:%d>' % (self.type, self.name, self.start, self.end)
		else:
			return '<%s:%d:%d>' % (self.type, self.start, self.end)

	def append(self, type, start = 0, end = 0, name = ''):
		child = Node(type, name, start, end, self)
		self.children.append(child)
		return child

	def first_child(self):
		if len(self.children) > 0:
			return self.children[0]
		return None

	def last_child(self):
		if len(self.children) > 0:
			return self.children[-1]
		return None

	def next_sibling(self):
		if self.parent:
			siblings = self.parent.children
			index = siblings.index(self)
			if index < len(siblings) - 1:
				return siblings[index + 1]
		return None

	def previous_sibling(self):
		if self.parent:
			siblings = self.parent.children
			index = siblings.index(self)
			if index > 0:
				return siblings[index - 1]
		return None

	def show(self, level = 0):
		children = ''
		for child in self.children:
			children += child.show(level + 1)
		return ('\t' * level) + str(self) + '\n' + children


class HtmlNavigation():

	def __init__(self, content):
		self.content = content
		self.tree = self._parse(content)

	def _parse(self, content, print_and_exit = False):

		empty_tags = ['area','base','basefont','br','col','embed','frame','hr','img','input','isindex','link','meta','param']

		def tokens_feed():
			tokens_re = '(<!--|-->|<\!\[CDATA\[|\]\]>|<\?|\?>|<\!|<[A-Za-z][A-Za-z0-9\-_:\.]*|</[A-Za-z][A-Za-z0-9\-_:\.]*\s*>|/?>|["\'=]|\s+)'
			tokens = filter(lambda s: s, re.split(tokens_re, content))
			for token in tokens:
				yield token

		def get_next_token():
			try:
				return tokens.next()
			except StopIteration:
				return None

		tokens = tokens_feed()
		
		if print_and_exit:
			for token in tokens: print token, '|',
			print
			return None

		root = Node('root')
		node = root.append('text')
		offset = 0
		end = 0
		token = ''

		while True:

			previous_token = token
			offset = end

			token = get_next_token()
			if not token: break
			end = offset + len(token)

			if token == '<!--':
				if node.type == 'text':
					node.end = offset
					node = node.parent
					node = node.append('comment', offset)

			elif token == '-->':
				if node.type == 'comment':
					node.end = end
					node = node.parent.append('text', end)

			elif token == '<![CDATA[':
				if node.type == 'text':
					node.end = offset
					node = node.parent
					node = node.append('cdata', offset)

			elif token == ']]>':
				if node.type == 'cdata':
					node.end = end
					node = node.parent.append('text', end)

			elif token == '<?':
				if node.type != 'question--tag':
					if node.type == 'text':
						node.end = offset
						node = node.parent
					node = node.append('question-tag', offset)

			elif token == '?>':
				if node.type == 'question-tag':
					node.end = end
					previous_sibling = node.previous_sibling()
					if previous_sibling and previous_sibling.type == 'text':
						node = node.parent.append('text', end)
					else:
						node = node.parent

			elif token == '<!':
				if node.type == 'text':
					node.end = offset
					node = node.parent.append('exclam-tag', offset)

			elif token.startswith('</'):

				if node.type == 'text':

					node.end = offset

					name = token[2:-1].rstrip().lower()
					current_node = node
					node = node.parent

					while True:
						if node.type == 'tag':
							if node.name == name:
								node.end = end
								node = node.parent.append('text', end)
								break
							else:
								node.end = end
								node = node.parent
								if node.type == 'root':
									node = current_node
									break
						else:
							break

			elif token.startswith('<'):
				name = token[1:].rstrip().lower()
				if node.type == 'text' and name:
					node.end = offset
					node = node.parent.append('start-tag', offset, 0, name)

			elif token == '/>':
				if node.type == 'start-tag':
					node.type = 'empty-tag'
					node.end = end
					node = node.parent.append('text', end)

			elif token == '>':
				if node.type == 'exclam-tag':
					node.end = end
					node = node.parent.append('text', end)
				elif node.type in ['start-tag', 'attribute']:
					if node.type == 'attribute':
						node.end = offset
						node = node.parent
					if node.name in empty_tags:
						node.type = 'empty-tag'
						node.end = end
						node = node.parent.append('text', end)
					else:
						node.type = 'tag'
						node = node.append('text', end)
				

			elif token == '"':
				if node.type == 'attribute' and previous_token == '=':
					node = node.append('double_quoted_value', end)
				elif node.type == 'double_quoted_value':
					node.end = offset
					node = node.parent
					node.end = end
					node = node.parent

			elif token == "'":
				if node.type == 'attribute' and previous_token == '=':
					node = node.append('single_quoted_value', end)
				elif node.type == 'single_quoted_value':
					node.end = offset
					node = node.parent
					node.end = end
					node = node.parent

			else:
				is_alnum = not re.sub('[A-Za-z][A-Za-z0-9\-_:\.]*', '', token)
				if node.type == 'start-tag':
					if is_alnum:
						node = node.append('attribute', offset, 0, token)

				elif node.type == 'attribute':
					if previous_token == '=' and is_alnum:
						node.append('not_quoted_value', offset, end)
						node.end = end
						node = node.parent
					elif token != '=':
						node.end = offset
						node = node.parent						

		while node.type != 'root':
			node.end = end
			node = node.parent
		node.end = end

		return root

	def current(self, offset_start, offset_end, tree = None):

		if tree is None:
			tree = self.tree

		result = tree
		for child in tree.children:

			if child.start <= offset_start and offset_end <= child.end:
				sibling = child.next_sibling()

				if sibling and sibling.start == offset_start and sibling.end == offset_end:
					return sibling

				sibling = child.previous_sibling()

				if sibling and sibling.start == offset_start and sibling.end == offset_end:
					return sibling

				result = self.current(offset_start, offset_end, child)

		return result

	def _prepare(self, offset_start, offset_end, content):
		if content != self.content:
			self.__init__(content)
		return self.current(offset_start, offset_end)
	
	def previous(self, offset_start, offset_end, content):

		result = None
		current = self._prepare(offset_start, offset_end, content)

		if current:
			result = current.previous_sibling()

			if result:
				test = result.last_child()

				while test:
					result = test
					test = test.last_child()
			else:
				result = current.parent

				if result:
					test = result.last_child()

					while test and test.start < offset_start:
						result = test
						test = test.last_child()
		return result
	
	def next(self, offset_start, offset_end, content):

		current = self._prepare(offset_start, offset_end, content)
		if not current:
			return None

		test = current.first_child()
		if test:
			return test

		test = current.next_sibling()
		if test:
			return test

		while True:
		    current = current.parent
		    if not current:
			    return None
		    test = current.next_sibling()
		    if test:
			    return test

if __name__ == '__main__':

	content = '''
<div id="id<?=$var_id?>" <?=$attr?>><
    ><div class="tab media-genre tab-init" id="tab_media" onclick="toggleTab('media');">Mo<b>v<i>i</b>e</i></div>
    <span id="txt_current_date" style="font-weight:bold;font-size:16px;color:#636363;">Monday, May 17th< 2010</span>
    &nbsp;<a class="link" style="cursor: pointer;" onclick="saveGrid();">Start h>ere</a>
    &nbsp;<a class="link" href="/grid.php?defaut=yes">Default grid</a>
</div><!-- test -->
'''
	test = HtmlNavigation(content)
	if test.tree:
		print test.tree.show()
		test._parse(content, True)

