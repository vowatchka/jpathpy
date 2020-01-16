#!/usr/bin/env python

"""
JPath exceptions.
"""

class JPathError(Exception):
	"""
	Base JPath exception.
	"""
	def __init__(self, message, lineno=None, pos=None):
		"""
		Initialize exception.
			
		:param str message:
		    Description of exception.
			
		:keyword int lineno:
		    Number of line where exception was occurred.
			
		:keyword int pos:
		    Number of char position where exception was occured.
		"""
		if lineno != None and pos != None:
			self._lineno 	= lineno
			self._pos 		= pos
			self._errmsg 	= "%s at line %d (position: %d)" % (message, self._lineno, self._pos)
		else:
			self._errmsg = "%s" % message
		Exception.__init__(self, self._errmsg)
		
	lineno 	= property()
	pos 	= property()
	errmsg 	= property()
	
	@lineno.getter
	def lineno(self):
		"""
		Return line of JPath expression where exception was occured.
		"""
		return self._lineno
		
	@pos.getter
	def pos(self):
		"""
		Return char position of JPath expression where exception was occured.
		"""
		return self._pos
		
	@errmsg.getter
	def errmsg(self):
		"""
		Return description of exception.
		"""
		return self._errmsg
		
class JPathLexicalError(JPathError):
	"""
	JPath lexical exception.
	"""
	pass
	
class JPathSyntaxError(JPathError):
	"""
	JPath syntax exception.
	"""
	pass
	
class JPathFunctionError(JPathError):
	"""
	JPath function exception.
	"""
	pass
