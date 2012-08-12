#---------------------------------------------------------------------------
# Three-valued OPerators
# 	return True, False or None
#   None means "undefined".  This is different from Python's None, which is
#   of type None.
#---------------------------------------------------------------------------
class TOP (object):
	def __init__(self, name='unnamed_top'):
		self.name = name

	def sql(self):
		raise NotImplementedError

	def mongo(self):
		raise NotImplementedError

#---------------------------------------------------------------------------
class Not (TOP):
	def __init__(self):
		super(Not,self).__init__('Not')

	def __call__(self, a):
		if a is None: return None
		return not a

#---------------------------------------------------------------------------
class Or (TOP):
	def __init__(self):
		super(Or,self).__init__('Or')

	def __call__(self, a, b):
		return a or b

#---------------------------------------------------------------------------
class And (TOP):
	def __init__(self):
		super(And,self).__init__('And')

	def __call__(self, a, b):
		return a and b

#---------------------------------------------------------------------------
class Chain (TOP):
	def __init__(self, *op):
		self.op = op if op else lambda v: True
		super(Chain,self).__init__(','.join(o.name for o in op))

	def __call__(self, v):
		for op in self.op:
			result = op(v)
			if (result == False) or (result is None):
				return result
		return result

#---------------------------------------------------------------------------
# print Not()(3), Not()(False), Not()(None)
# print Or()(3,4), Or()(3,None), Or()(None,5), Or()(None,True), Or()(True,None), Or()(False,None), Or()(None,False)
# print And()(3,4), And()(3,None), And()(None,3), And()(False,None), And()(3,True), And()(True,1)
#---------------------------------------------------------------------------

class Required (TOP):
	def __init__(self):
		super(Required,self).__init__('Required')

	def __call__(self, v):
		return v is None

#---------------------------------------------------------------------------

class Eq (TOP):
	def __init__(self, v):
		self.v = v
		super(Eq,self).__init__('Eq')

	def __call__(self, v):
		return None if v is None else v == self.v

#---------------------------------------------------------------------------

class Ne (TOP):
	def __init__(self, v):
		self.v = v
		super(Ne,self).__init__('Ne')

	def __call__(self, v):
		return None if v is None else v != self.v

#---------------------------------------------------------------------------

class Lt (TOP):
	def __init__(self, v):
		self.v = v
		super(Lt,self).__init__('Lt')

	def __call__(self, v):
		return None if v is None else v < self.v

#---------------------------------------------------------------------------

class Le (TOP):
	def __init__(self, v):
		self.v = v
		super(Le,self).__init__('Le')

	def __call__(self, v):
		return None if v is None else v <= self.v

#---------------------------------------------------------------------------

class Gt (TOP):
	def __init__(self, v):
		self.v = v
		super(Gt,self).__init__('Gt')

	def __call__(self, v):
		return None if v is None else v > self.v

#---------------------------------------------------------------------------

class Ge (TOP):
	def __init__(self, v):
		self.v = v
		super(Ge,self).__init__('Ge')

	def __call__(self, v):
		return None if v is None else v >= self.v

#---------------------------------------------------------------------------

class Length (TOP):
	def __init__(self, n):
		self.n = n
		super(Length,self).__init__('Length')

	def __call__(self, v):
		return None if not isinstance(v,basestring) else len(v) == self.n

#---------------------------------------------------------------------------

class LengthAtMost (TOP):
	def __init__(self, n):
		self.n = n
		super(LengthAtMost,self).__init__('LengthAtMost')

	def __call__(self, v):
		return None if not isinstance(v,basestring) else len(v) <= self.n

#---------------------------------------------------------------------------

class LengthAtLeast (TOP):
	def __init__(self, n):
		self.n = n
		super(LengthAtLeast,self).__init__('LengthAtLeast')

	def __call__(self, v):
		return None if not isinstance(v,basestring) else len(v) >= self.n

#---------------------------------------------------------------------------
# c = Chain(LengthAtMost(5), LengthAtLeast(3), Lt('hell'))
# print c(3), c('hello'), c('hallos')

#---------------------------------------------------------------------------
#  Types are three-valued operators
#---------------------------------------------------------------------------
class Type (TOP):
	def __init__(self, name):
		self.v = None
		super(Type,self).__init__(name)

	def set_v(self, v):
		self.v = v

	value = property(lambda: self.v, set_v)

#---------------------------------------------------------------------------
class Int (Type):
	def __init__(self):
		super(Int,self).__init__('Int')

	def __call__(self, v):
		if isinstance(v,int):
			self.v = v
			return True
		if isinstance(v, basestring):
			try:
				self.v = int(v)
				return True
			except:
				pass
		self.v = None
		return None if v is None else False

#---------------------------------------------------------------------------
class Float (Type):
	def __init__(self):
		super(Float,self).__init__('Float')

	def __call__(self, v):
		if isinstance(v,float):
			self.v = v
			return True
		if isinstance(v, basestring):
			try:
				self.v = float(v)
				return True
			except:
				pass
		self.v = None
		return None if v is None else False

#---------------------------------------------------------------------------
class String (Type):
	def __init__(self, m=None, n=None):
		self.validator = None
		if isinstance(m,int):
			if isinstance(n,int):
				self.validator = Chain(LengthAtLeast(m), LengthAtMost(n))
			else:
				self.validator = LengthAtMost(m)

		super(String,self).__init__('String')

	def __call__(self, v):
		if isinstance(v,basestring):
			if self.validator is None or self.validator(v):
				self.v = v
				return True
		self.v = None
		return None if v is None else False

#---------------------------------------------------------------------------
class Boolean (Type):
	def __init__(self):
		super(Boolean,self).__init__('Boolean')

	def __call__(self, v):
		if isinstance(v,boolean):
			self.v = v
			return True
		if v in ('True','true'):
			self.v = True
			return True
		if v in ('False','false'):
			self.v = False
			return True
		self.v = None
		return None if v is None else False

#---------------------------------------------------------------------------
