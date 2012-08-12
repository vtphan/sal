'''
	Three-valued EXpressions evaluated to True, False, or None
'''

from top import *

#---------------------------------------------------------------------------

class TEX(object):
	def __init__(self, op, *operands, **kw):
		self.op = op
		self.operands = operands
		self.name = kw.get('name','unnamed_expr')

	def eval(self):
		return self.op(*self.operands)

	def __str__(self):
		return 'TEX %s op=%s operands=%s' % (self.name, self.op.name, self.operands)

	def __invert__(self):
		return Expression(Not(), self)

	def __and__(self, other):
		return Expression(And(), self, other)

	def __or__(self, other):
		return Expression(Or(), self, other)

#---------------------------------------------------------------------------

class Field (TEX):
	def __init__(self, *validators, **kw):
		self.op = Chain(*validators)
		self.operands = (kw.get('value', None), )
		self.name = kw.get('name', 'unnamed_field')

	def get_value(self):
		return self.operands[0]

	def set_value(self, v):
		self.operands = (v, )

	value = property(get_value, set_value)

#---------------------------------------------------------------------------
