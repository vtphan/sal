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
		p=[o.eval() if isinstance(o, TEX) else o for o in self.operands]
		return self.op(*p)

	def __str__(self):
		return 'TEX %s op=%s operands=%s' % (self.name, self.op.name, self.operands)

	def __invert__(self):
		return TEX(Not(), self)

	def __and__(self, other):
		return TEX(And(), self, other)

	def __or__(self, other):
		return TEX(Or(), self, other)

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

	def __lt__(self, other):
		return TEX(Lt(other), self.value)

	def __le__(self, other):
		return TEX(Le(other), self.value)

	def __gt__(self, other):
		return TEX(Gt(other), self.value)

	def __ge__(self, other):
		return TEX(Ge(other), self.value)

	def __eq__(self, other):
		return TEX(Eq(other), self.value)

	def __ne__(self, other):
		return TEX(Ne(other), self.value)


#---------------------------------------------------------------------------
