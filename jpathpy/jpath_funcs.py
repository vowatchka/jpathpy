#!/usr/bin/env python

"""
JPath functions.
"""

# import modules and packages
import re
import jpathpy
from functools import wraps
from jpathpy.exceptions import *

class JPathFunctionsWrapper(object):
	"""
	Base class for implements classes that have methods 
	that can be called as JPath functions.
	"""
	
	def __init__(*args, **kwargs):
		"""
		Initialize an instance.
		"""
		pass
		
	def _jpath_function(func):
		"""
		Decorator.
		"""
		@wraps(func)
		def wrapper(self, *args, **kwargs):
			"""
			First argument must be an instance of JSelection.
			
			:param tuple *args:
			    Function positional arguments.
				
			:param dict **kwargs:
			    Function keyword arguments.
				
			:except JPathFunctionError:
			    If first argument is not an instance of JSelection.
				
			:except Exception:
			    Other exceptions that can be occured when call ``func``.
				
			:return object:
			"""
			if not isinstance(args[0], jpathpy.JSelection):
				raise JPathFunctionError("invalid first argument for JPath function ``%s``: expected an instance of %s" % (func.__name__, jpathpy.JSelection))
			return func(self, *args, **kwargs)
		return wrapper
		
	def _getvalue(self, obj):
		"""
		Return value of ``obj`` or value of ``obj[0]`` if ``obj`` is instance of ``JSelection``.
		
		:param object obj:
		    Object that value will be returned.
			
		:except IndexError:
		    If ``obj`` is instance of ``JSelection`` and has not items.
			
		:return object:
		"""
		return obj[0] if isinstance(obj, jpathpy.JSelection) else obj

class JPathFunctions(JPathFunctionsWrapper):
	"""
	Class provides methods that can be called as JPath functions.
	"""
	
	@JPathFunctionsWrapper._jpath_function
	def toint(self, selection):
		"""
		Apply ``int()`` function to item in selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return int:
		"""
		return int(selection[0])
		
	@JPathFunctionsWrapper._jpath_function
	def toflt(self, selection):
		"""
		Apply ``float()`` function to item in selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return float:
		"""
		return float(selection[0])
		
	@JPathFunctionsWrapper._jpath_function
	def tostr(self, selection):
		"""
		Apply ``str()`` function to item in selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return str(selection[0])
	
	@JPathFunctionsWrapper._jpath_function
	def get(self, selection, idx):
		"""
		Return item of selection by index.
		
		:param JSelection selection:
		    Selection.
			
		:param int or JSelection idx:
		    Index.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return object:
		"""
		return selection[self._getvalue(idx)]
	
	@JPathFunctionsWrapper._jpath_function
	def len(self, selection):
		"""
		Apply ``len()`` function to item in selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return int:
		"""
		return len(selection[0])
	
	@JPathFunctionsWrapper._jpath_function
	def isnum(self, selection):
		"""
		Return True if item in selection is int or float 
		and False in otherwise.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		value = selection[0]
		return True if not isinstance(value, bool) and isinstance(value, (int, float)) else False
	
	@JPathFunctionsWrapper._jpath_function
	def isint(self, selection):
		"""
		Return True if item in selection is int 
		and False in otherwise.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		value = selection[0]
		return True if not isinstance(value, bool) and isinstance(value, int) else False
	
	@JPathFunctionsWrapper._jpath_function
	def isflt(self, selection):
		"""
		Return True if item in selection is float 
		and False in otherwise.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return True if isinstance(selection[0], float) else False
	
	@JPathFunctionsWrapper._jpath_function
	def isbool(self, selection):
		"""
		Return True if item in selection is bool 
		and False in otherwise.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return True if isinstance(selection[0], bool) else False
	
	@JPathFunctionsWrapper._jpath_function
	def isstr(self, selection):
		"""
		Return True if item in selection is str 
		and False in otherwise.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return True if isinstance(selection[0], str) else False
	
	@JPathFunctionsWrapper._jpath_function
	def isnull(self, selection):
		"""
		Return True if item in selection is None 
		and False in otherwise.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return True if isinstance(selection[0], type(None)) else False
	
	@JPathFunctionsWrapper._jpath_function
	def isarr(self, selection):
		"""
		Return True if item in selection is list or tuple 
		and False in otherwise.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return True if isinstance(selection[0], (list, tuple)) else False
	
	@JPathFunctionsWrapper._jpath_function
	def isobj(self, selection):
		"""
		Return True if item in selection is dict 
		and False in otherwise.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return True if isinstance(selection[0], dict) else False
	
	@JPathFunctionsWrapper._jpath_function
	def rnd(self, selection, digits):
		"""
		Round value of item in selection to digits count.
		
		:param JSelection selection:
		    Selection.
			
		:param int or JSelection digits:
		    Count of digits for rounding.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return float:
		"""
		return round(selection[0], self._getvalue(digits))
	
	@JPathFunctionsWrapper._jpath_function
	def slice(self, selection, start, stop, step):
		"""
		Return slice of item in selection.
		
		:param JSelection selection:
		    Selection.
			
		:param int or JSelection or None start:
		    Start index of slice.
			
		:param int or JSelection or None stop:
		    Stop index of slice.
			
		:param int or JSelection or None step:
		    Slice step.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return iterable:
		"""
		return selection[0][self._getvalue(start) : self._getvalue(stop) : self._getvalue(step)]
	
	@JPathFunctionsWrapper._jpath_function
	def replace(self, selection, template, replacement):
		"""
		Replace all templates in item of selection by replacement.
		
		:param JSelection selection:
		    Selection.
			
		:param str or JSelection template:
		    Template.
			
		:param str or JSelection replacement:
		    Replacement.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return selection[0].replace(self._getvalue(template), self._getvalue(replacement))
	
	@JPathFunctionsWrapper._jpath_function
	def isdigit(self, selection):
		"""
		Apply method ``.isdigit()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection[0].isdigit()
	
	@JPathFunctionsWrapper._jpath_function
	def isalpha(self, selection):
		"""
		Apply method ``.isalpha()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection[0].isalpha()
	
	@JPathFunctionsWrapper._jpath_function
	def isalnum(self, selection):
		"""
		Apply method ``.isalnum()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection[0].isalnum()
	
	@JPathFunctionsWrapper._jpath_function
	def islower(self, selection):
		"""
		Apply method ``.islower()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection[0].islower()
	
	@JPathFunctionsWrapper._jpath_function
	def isupper(self, selection):
		"""
		Apply method ``.isupper()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection[0].isupper()
	
	@JPathFunctionsWrapper._jpath_function
	def isspace(self, selection):
		"""
		Apply method ``.isspace()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection[0].isspace()
	
	@JPathFunctionsWrapper._jpath_function
	def istitle(self, selection):
		"""
		Apply method ``.istitle()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection[0].istitle()
	
	@JPathFunctionsWrapper._jpath_function
	def lower(self, selection):
		"""
		Apply method ``.lower()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return selection[0].lower()
	
	@JPathFunctionsWrapper._jpath_function
	def upper(self, selection):
		"""
		Apply method ``.upper()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return selection[0].upper()
	
	@JPathFunctionsWrapper._jpath_function
	def startswith(self, selection, template):
		"""
		Apply method ``.startswith()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:param str or JSelection template:
		    Template.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection[0].startswith(self._getvalue(template))
	
	@JPathFunctionsWrapper._jpath_function
	def endswith(self, selection, template):
		"""
		Apply method ``.endswith()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:param str or JSelection template:
		    Template.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection[0].endswith(self._getvalue(template))
	
	@JPathFunctionsWrapper._jpath_function
	def capitalize(self, selection):
		"""
		Apply method ``.capitalize()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return selection[0].capitalize()
	
	@JPathFunctionsWrapper._jpath_function
	def ltrim(self, selection):
		"""
		Apply method ``.lstrip()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return selection[0].lstrip()
	
	@JPathFunctionsWrapper._jpath_function
	def rtrim(self, selection):
		"""
		Apply method ``.rstrip()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return selection[0].rstrip()
	
	@JPathFunctionsWrapper._jpath_function
	def trim(self, selection):
		"""
		Apply method ``.strip()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return selection[0].strip()
	
	@JPathFunctionsWrapper._jpath_function
	def title(self, selection):
		"""
		Apply method ``.title()`` on item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return selection[0].title()
	
	@JPathFunctionsWrapper._jpath_function
	def instr(self, selection, template):
		"""
		Check that template in string value of item of selection.
		
		:param JSelection selection:
		    Selection.
			
		:param str or JSelection template:
		    Template.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return True if selection[0].find(self._getvalue(template)) != -1 else False
	
	@JPathFunctionsWrapper._jpath_function
	def normalize(self, selection):
		"""
		Replace all whitespaces to one space in string value 
		of item of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return str:
		"""
		return re.sub(r"\s+", " ", re.sub(r"[\r\n\t\v\f]+", " ", selection[0], re.I)).strip()
	
	@JPathFunctionsWrapper._jpath_function
	def count(self, selection):
		"""
		Return length of selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return int:
		"""
		return len(selection)
	
	@JPathFunctionsWrapper._jpath_function
	def all(self, selection):
		"""
		Apply function ``all()`` to all items in selection.
		
		Note that method return False if selection is empty.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		if len(selection):
			return all([item for item in selection])
		else:
			return False
	
	@JPathFunctionsWrapper._jpath_function
	def any(self, selection):
		"""
		Apply function ``any()`` to all items in selection.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return any([item for item in selection])
		
	@JPathFunctionsWrapper._jpath_function
	def has(self, selection):
		"""
		Return True if selection has items, i.e not empty.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return True if len(selection) else False
		
	@JPathFunctionsWrapper._jpath_function
	def no(self, selection):
		"""
		Return True if selection has not items, i.e. empty.
		
		:param JSelection selection:
		    Selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return not self.has(selection)
		
	@JPathFunctionsWrapper._jpath_function
	def inval(self, selection, val):
		"""
		Return True if some value contains in 
		value of item of selection.
		
		:param JSelection selection:
		    Selection.
			
		:param object or JSelection val:
		    Some value.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return self._getvalue(val) in selection[0]
		
	@JPathFunctionsWrapper._jpath_function
	def initems(self, selection, item):
		"""
		Return True if some item contains in selection.
		
		:param JSelection selection:
		    Selection.
			
		:param object or JSelection item:
		    Some item.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return self._getvalue(item) in selection
		
	@JPathFunctionsWrapper._jpath_function
	def concat(self, selection, added_selection):
		"""
		Concatenate two selections.
		
		:param JSelection selection:
		    Selection.
			
		:param JSelection added_selection:
		    Additional selection.
		
		:except Exception:
		    Some exceptions that can be occurred.
			
		:return bool:
		"""
		return selection + added_selection
