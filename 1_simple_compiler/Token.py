# -*- coding: utf-8 -*-

#定义token类型
INTEGER = 'INTEGER'
EOF = 'EOF'
PLUS, MINUS = 'PLUS', 'MINUS'
MULTIPLY, DIVIDE = 'MULTIPLY', 'DIVIDE'

#定义token类型
class Token(object):
	def __init__(self, ctype, value):
		self.ctype = ctype
		self.value = value

	def __str__(self):
		ctype_value = {ctype:self.ctype, value:self.value}
		return 'Token({ctype}, {value})'.format(**ctype_value)

	def __repr__(self):
		return self.__str__()