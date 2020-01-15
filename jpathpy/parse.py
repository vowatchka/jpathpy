#!/usr/bin/env python

"""
Rules of parsing JPath.
"""

# import modules and packages
import os
import ply.lex as plex
import ply.yacc as pyacc
from jpathpy.lex import *
from jpathpy.jpath_funcs import JPathFunctions
from jpathpy.exceptions import *

def create_output_dir(path):
	"""
	Create directory for debug info of package ``ply`` classes and functions.
	
	:param str path:
		Path to directory.
		
		Note that if directory does not exist it will be created.
		
	:except Exception:
		Some exceptions that can be occurred while creating directory.
		
	:return None:
	"""
	if not os.path.exists(path):
		os.makedirs(path, exist_ok=True)

def get_str_from_parsing(p):
	"""
	Return string that was be parsed.
	
	:param ply.yacc.YaccProduction p:
	    Contains parts of parsed string.
		
	:return str:
	"""
	return "".join([str(i) for i in p[1:]])

# define precedences
precedence = (
				("left", "UNION"),
				("left", "DELIMPARAMS", "SLICE"),
				("left", "LSQUAREPAREN", "RSQUAREPAREN"),
				("left", "AND", "OR"),
				("left", "EQ", "NE", "LT", "LE", "GT", "GE"),
				("left", "PLUS", "MINUS"),
				("left", "MULT", "DIV", "MOD"),
				("right", "UMINUS"),
			)

def parse(expr, start, output_dir=None, write_output=False, lextab=None, tabmodule=None, debugfile=None, jpath_funcs=JPathFunctions()):
	"""
	Parse JPath and return string as operation of selecting by used JSelection.
	
	For example:
	>>> from jpathpy.parse import parse
	>>> parse(r'$."a".."b"[0].[0][*][startswith(@, "abc")]', "jpath")
	'root.one("a", deep=False).one("b", deep=True).i(0).el(0).exp().filter(lambda idx, cur, root : cur.call4self(jpath_functions.startswith, *(\'abc\',)))'
	
	:param str expr:
		JPath expression.
		
	:param str start:
		First rule from that parsing JPath will be started.
		
	:keyword str output_dir:
	    Directory where classes and functions of package ``ply`` 
	    will be save their debug info.
		
	    Specified directory will be used only in case if keyword 
	    argument ``write_output`` is True.
		
	    Note that if directory does not exist it will be created.
	
	    By default it will be folder with name ``output`` 
	    in work directory of package ``jpathpy``.
		
	:keyword bool write_output:
	    If it is True classes and functions of package ``ply`` will be 
	    save their debug info in directory specified as ``output_dir``.
		
	    Set it as True only for debug JPath, because 
	    parsing of JPath may be relatively long when 
	    write outputs is on.
		
	:keyword str lextab:
		Name of python file that will be created by package ``ply`` 
		if keyword argument ``write_output`` is True.
		
	:keyword str tabmodule:
		Name of python file that will be created by package ``ply`` 
		if keyword argument ``write_output`` is True.
		
	:keyword str debugfile:
		Name of file with debug info that will be created by package ``ply``
		if keyword argument ``write_output`` is True.
		
	:keyword object jpath_funcs:
	    An instance of some class which methods will be called as 
	    JPath functions.
		
	    Note that each method of specified class must takes instance of 
	    JSelection as first positional argument. To change this 
	    default behavior you must change some functions of parsing JPath.
		
	    Default is instance of jpathpy.jpath_funcs.JPathFunctions.
		
	:except JPathLexicalError:
		If invalid lexemes is used.
		
	:except JPathSyntaxError:
		If JPath syntax is invalid.
		
	:except JPathFunctionError:
		If try to use invalid JPath function or in case if 
		called JPath function raises some exception.
		
	:except Exception:
		Some exceptions that can be occurred while parsing JPath.
		
	:return str:
	"""			
	# define grammar rules
	def p_jpath_root(p):
		"""jpath : ROOT
				 | AT"""
		# rule for parsing reference to the selection
		if p[1] == "$":
			p[0] = "root"
		elif p[1] == "@":
			p[0] = "cur"
		else:
			assert False, "unknown token %s" % p[1]
		
	def p_jpath_union(p):
		"""jpath : jpath UNION jpath"""
		# rule for parsing union of selections
		p[0] = "%s + %s" % (p[1], p[3])
			
	def p_jpath_selection(p):
		"""jpath : jpath SIMPLESELECTOR STRING
				 | jpath SIMPLESELECTOR MULT
				 | jpath DEEPSELECTOR STRING
				 | jpath DEEPSELECTOR MULT"""
		# rule for parsing simple or deep selection by keys
		func, key, delimiter = ("all", "", "") if p[3] == "*" else ("one", '"%s"' % p[3], ", ")
		deep = "False" if p[2] == "." else "True"
		p[0] = p[1] + '.%s(%s%sdeep=%s)' % (func, key, delimiter, deep)

	def p_jpath_filterarray(p):
		"""jpath : jpath SIMPLESELECTOR LSQUAREPAREN int RSQUAREPAREN
				 | jpath SIMPLESELECTOR LSQUAREPAREN indices RSQUAREPAREN
				 | jpath SIMPLESELECTOR LSQUAREPAREN slice RSQUAREPAREN"""
		# rule for parsing selection elements from iterable items by indices
		p[0] = p[1] + ".el(%r)" % p[4]
		

	def p_jpath_filteritems(p):
		"""jpath : jpath LSQUAREPAREN indices RSQUAREPAREN
				 | jpath LSQUAREPAREN slice RSQUAREPAREN
				 | jpath LSQUAREPAREN expressionstr RSQUAREPAREN
				 | jpath LSQUAREPAREN MULT RSQUAREPAREN"""
		# rule for
		# 1. parsing selection items from current selection by indices 
		# 2. parsing filtering
		# 3. parsing expand current selection by elements from items 
		#    that iterable by indices
		if p[3] == "*":
			# expand
			p[0] = p[1] + ".exp()"
		elif str(p.slice[3]) == "expressionstr":
			if str(p[3]).isdigit():
				# take member by index
				p[0] = p[1] + ".i(%r)" % p[3]
			else:
				p[0] = p[1] + ".filter(lambda idx, cur, root : %s)" % p[3]
		else:
			# slice or indices
			p[0] = p[1] + ".i(%r)" % p[3]
		
	def p_expressionstr(p):
		"""expressionstr : expression
						 | jpath"""
		# rule for parsing filtering expression
		p[0] = p[1]

	def p_expression(p):
		"""expression : INT
					  | FLOAT
					  | FALSE
					  | TRUE
					  | NULL
					  | STRING
					  | function"""
		# rule for parsing base types that can be used in filtering expression
		if p.slice[1].type == "STRING":
			p[0] = '"%s"' % p[1]
		else:
			p[0] = p[1]

	def p_expression_uminus(p):
		"""expression : MINUS expression %prec UMINUS
					  | MINUS jpath %prec UMINUS"""
		# rule for parsing unary minus
		if str(p.slice[2]) == "expression":
			p[0] = get_str_from_parsing(p)
		else:
			p[0] = p[1] + p[2]+".val()"
		
	def p_expression_math(p):
		"""expression : jpath PLUS jpath
					  | jpath PLUS expression
					  | expression PLUS jpath
					  | expression PLUS expression
					  | jpath MINUS jpath
					  | jpath MINUS expression
					  | expression MINUS jpath
					  | expression MINUS expression
					  | jpath MULT jpath
					  | jpath MULT expression
					  | expression MULT jpath
					  | expression MULT expression
					  | jpath DIV jpath
					  | jpath DIV expression
					  | expression DIV jpath
					  | expression DIV expression
					  | jpath MOD jpath
					  | jpath MOD expression
					  | expression MOD jpath
					  | expression MOD expression"""
		# rule for parsing an arithmetic operations
		if str(p.slice[1]) == "jpath":
			p[0] = "%s %s %s" % (p[1]+".val()", p[2], p[3])
		elif str(p.slice[3]) == "jpath":
			p[0] = "%s %s %s" % (p[1], p[2], p[3]+".val()")
		else:
			p[0] = "%s %s %s" % (p[1], p[2], p[3])
		
	def p_expression_group(p):
		"""expression : LPAREN expressionstr RPAREN"""
		# rule for parsing a grouping by paren
		p[0] = get_str_from_parsing(p)
		
	def p_expression_comp(p):
		"""expression : jpath EQ jpath
					  | jpath EQ expression
					  | expression EQ expression
					  | expression EQ jpath
					  | jpath NE jpath
					  | jpath NE expression
					  | expression NE jpath
					  | expression NE expression
					  | jpath LT jpath
					  | jpath LT expression
					  | expression LT jpath
					  | expression LT expression
					  | jpath LE jpath
					  | jpath LE expression
					  | expression LE jpath
					  | expression LE expression
					  | jpath GT jpath
					  | jpath GT expression
					  | expression GT jpath
					  | expression GT expression
					  | jpath GE jpath
					  | jpath GE expression
					  | expression GE jpath
					  | expression GE expression"""
		# rule for parsing a comparation operations
		if str(p.slice[1]) == "jpath":
			p[0] = "%s %s %s" % (p[1]+".val()", p[2] if p[2] != "=" else "==", p[3])
		elif str(p.slice[3]) == "jpath":
			p[0] = "%s %s %s" % (p[1], p[2] if p[2] != "=" else "==", p[3]+".val()")
		else:
			p[0] = "%s %s %s" % (p[1], p[2] if p[2] != "=" else "==", p[3])
		
	def p_expression_logic(p):
		"""expression : jpath AND jpath
					  | jpath AND expression
					  | expression AND jpath
					  | expression AND expression
					  | jpath OR jpath
					  | jpath OR expression
					  | expression OR jpath
					  | expression OR expression"""
		# rule for parsing a logical operations
		p[0] = "%s %s %s" % (p[1], p[2], p[3])
		
	def p_function(p):
		"""function : FUNCNAME LPAREN parameters RPAREN"""
		# rule for parsing JPath function
		if hasattr(jpath_funcs, p[1]) and callable(eval("jp_funcs.%s" % p[1], {"jp_funcs": jpath_funcs})):
			p[0] = "%s.call4self(jpath_functions.%s, *%s)" % (p[3][0], p[1], p[3][1:])
		else:
			raise JPathFunctionError("Unknown JPath function ``%s`` or it is not callable" % p[1])
		
	def p_parameters_one(p):
		"""parameters : expression
					  | jpath"""
		# rule for parsing single parameter of JPath function
		p1 = str(p[1])
		p[0] = (p1[1:len(p1)-1] if p1.startswith('"') and p1.endswith('"') else p[1],)
			
	def p_parameters_group(p):
		"""parameters : parameters DELIMPARAMS parameters"""
		# rule for parsing parameters of JPath function
		p[0] = p[1] + p[3]

	def p_indices(p):
		"""indices : INT DELIMPARAMS INT
				   | indices DELIMPARAMS INT"""
		# rule for parsing a list of indices
		if str(p.slice[1]) == "indices":
			p[0] = p[1] + [p[3]]
		else:
			p[0] = [p[1], p[3]]

	def p_slice(p):
		"""slice : slicestartstop
				 | slicestartstop slicestep"""
		# rule for parsing a slice expression
		p[0] = slice(*(p[1] if len(p) == 2 else p[1] + p[2]))
		
	def p_slicestartstop(p):
		"""slicestartstop : SLICE
						  | int SLICE
						  | SLICE int
						  | int SLICE int"""
		# rule for parsing start/stop slice params
		if len(p) == 2:
			p[0] = [None, None]
		elif len(p) == 3:
			p[0] = [None, p[2]] if p[1] == ":" else [p[1], None]
		else:
			p[0] = [p[1], p[3]]
			
	def p_slicestep(p):
		"""slicestep : SLICE
					 | SLICE int"""
		# rule for parsing step slice param
		p[0] = [None] if len(p) == 2 else [p[2]]
		
	def p_int(p):
		"""int : INT
			   | MINUS INT"""
		# rule for parsing positive and negative integers
		if len(p) == 2:
			p[0] = p[1]
		else:
			p[0] = -p[2]
		
	# define error rule
	def p_error(t):
		if t == None:
			raise JPathSyntaxError("Unexpected end of JPath")
		else:
			# while True:
				# tok = parser.token()
				# if not tok:
					# break
				# print(tok)
			raise JPathSyntaxError("Unexpected token '%s'" % str(t.value), t.lineno, t.lexpos)
			
	if write_output:
		if not output_dir:
			_output_dir = os.path.join(os.path.dirname(__file__), "output")
		else:
			_output_dir = output_dir
		create_output_dir(_output_dir)
	
	# init lexer
	if write_output:
		lexer = plex.lex(optimize=True, lextab=lextab or "", outputdir=_output_dir)
	else:
		lexer = plex.lex(optimize=False)
	
	# init parser
	if write_output:
		parser = pyacc.yacc(start=start, optimize=True, debug=True, write_tables=True, tabmodule=tabmodule or "", debugfile=debugfile or "", outputdir=_output_dir)
	else:
		parser = pyacc.yacc(start=start, optimize=True, debug=False, write_tables=False)
	
	# parse JPath
	return parser.parse(expr)