# -*- coding: utf-8 -*-
from Token import *

# 定义词法分析器
class Lexer(object):
	def __init__(self, text):
		self.pos = 0
		self.text = text
		self.curr_char = self.text[self.pos]

	def error(self):
		raise Exception('Invalid character')

	def advance(self):
		self.pos += 1
		if self.pos > len(self.text)-1:
			self.curr_char = None
		else:
			self.curr_char = self.text[self.pos]

	def skip_whitespace(self):
		while self.curr_char is not None and self.curr_char.isspace():
			self.advance()

	def integer(self):
		result = ''
		while self.curr_char is not None and self.curr_char.isdigit():
			result += self.curr_char
			self.advance()
		return int(result)

	def get_next_token(self):
		while self.curr_char is not None:
			if self.curr_char.isspace():
				self.skip_whitespace()
				continue

			if self.curr_char.isdigit():
				return Token(INTEGER, self.integer())

			if self.curr_char == '+':
				self.advance()
				return Token(PLUS, '+')

			if self.curr_char == '-':
				self.advance()
				return Token(MINUS, '-')

			if self.curr_char == '*':
				self.advance()
				return Token(MULTIPLY, '*')

			if self.curr_char == '/':
				self.advance()
				return Token(DIVIDE, '/')

			self.error()
		return Token(EOF, None)