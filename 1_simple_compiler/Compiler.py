# -*- coding: utf-8 -*-
from Lexer import Lexer
from Interpreter import Interpreter

if __name__ == '__main__':
	while True:
		try:
			text = input('calc> ')
		except EOFError:
			break
		if not text: continue

		lexer = Lexer(text)
		interpreter = Interpreter(lexer)
		result = interpreter.expr()

		print(result)