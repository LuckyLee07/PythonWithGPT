# -*- coding: utf-8 -*-
from Token import *
from Lexer import Lexer

# 定义语法分析器
class Interpreter(object):
	def __init__(self, lexer:Lexer):
		self.lexer = lexer
		self.curr_token = self.lexer.get_next_token()

	def error(self):
		return Exception('Invalid syntax')

	def eat(self, token_type):
		if self.curr_token.ctype == token_type:
			self.curr_token = self.lexer.get_next_token()
		else:
			self.error()

	def factor(self):
		token = self.curr_token
		self.eat(INTEGER)
		return token.value

	def term(self):
		result = self.factor()

		while self.curr_token.ctype in (MULTIPLY, DIVIDE):
			token = self.curr_token
			if token.ctype == MULTIPLY:
				self.eat(MULTIPLY)
				result = result * self.factor()
			elif token.ctype == DIVIDE:
				self.eat(DIVIDE)
				result = result / self.factor()
		return result

	def expr(self):
		print('%s = '%self.lexer.text, end='')
		result = self.term()

		while self.curr_token.ctype in (PLUS, MINUS):
			token = self.curr_token
			if token.ctype == PLUS:
				self.eat(PLUS)
				result = result + self.term()
			elif token.ctype == MINUS:
				self.eat(MINUS)
				result = result - self.term()
		return result