#!/usr/bin/env python

"""
This package is easy way for selecting items from objects, that can be 
iterate by keys or indices (such as dictionaries or lists).

Also you can use syntax of JPath for selecting items by string expression.

For example, it can be usefull for selecting some items from JSON.

Example:
>>> from jpathpy import jselection
>>> d = { "books": [ 
    {"author": "Nigel Rees"}, 
    {"author": "Evelyn Waugh"}, 
    {"author": "Herman Melville"}, 
    {"author": "J. R. R. Tolkien"},
]}
>>> # try to select all authors
>>> jselection(d).one("author", deep=True).tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien')

JPath example:
>>> from jpathpy import jpath, jselection
>>> d = { "books": [ 
    {"author": "Nigel Rees"}, 
    {"author": "Evelyn Waugh"}, 
    {"author": "Herman Melville"}, 
    {"author": "J. R. R. Tolkien"},
]}
>>> # try to select all authors by JPath
>>> jpath(r'$.."author"', jselection(d)).tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien')

You can use multiline JPath expression. For example:
>>> from jpathpy import jpath, jselection
>>> d = { "books": [ 
    {"author": "Nigel Rees"}, 
    {"author": "Evelyn Waugh"}, 
    {"author": "Herman Melville"}, 
    {"author": "J. R. R. Tolkien"},
]}
>>> # try to select all authors by JPath
>>> jpath(r'''$
               .."author"''', jselection(d)).tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien')

Simple python ``dict`` is not ordered, so that using ``collections.OrderedDict`` is more right 
if you work with JSON string. It saves initial order of items if you need it. For example:
>>> import json
>>> from collections import OrderedDict
>>> from jpathpy import jselection
>>> strjson = '{"a":1, "b":2, "c":3, "d":4, "e":5}'
>>> d = json.loads(strjson)
>>> d
{'c': 3, 'a': 1, 'b': 2, 'd': 4, 'e': 5}
>>> # order of keys IS NOT EQUAL of initial order
>>> # in JSON string
>>> jselection(d).all().tuple()
(3, 1, 2, 4, 5)
>>> d = json.loads(strjson, object_pairs_hook=lambda x : OrderedDict(x))
>>> d
OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])
>>> # order of keys IS EQUAL of initial order
>>> # in JSON string
>>> jselection(d).all().tuple()
(1, 2, 3, 4, 5)
"""

# define metadata
__version__     = "2.0.0"
__author__      = "Vladimir Saltykov"
__copyright__   = "Copyright since 2017, %s" % __author__
__email__       = "vowatchka@mail.ru"
__license__     = "MIT"
__date__        = "2020-01-15"

__all__ = [
	"jselection", "JSelection", "jpath", "JPath", 
	"JPathError", "JPathLExicalError", "JPathSyntaxError", "JPathFunctionError", 
	"JPathFunctions"
]

# import modules and packages
from functools import reduce
from collections import Iterable
from jpathpy.parse import parse
from jpathpy.jpath_funcs import JPathFunctions
from jpathpy.exceptions import *


class JSelection():
	"""
	Class provides methods for selecting items from objects, that can be iterate 
	by keys or indices (such as dictionaries or lists).
	"""
	def __init__(self, *items, root=None, iters_by_key=None, ex_iters_by_key=None, iters_by_idx=None, ex_iters_by_idx=None, jpath_inst=None):
		"""
		Initialize jselection.
		
		:param Iterable *items:
		    List of items from that will be next selecting.
			
		:keyword JSelection root:
		    Root selection. If it is None, initialized instance will be root.
			
		:keyword tuple iters_by_key:
		    List of types instances of that are iterable by key, 
		    i.e next operation of selecting by key will be executed from all items 
		    that are instance of one of this types.
			
		    Default is (dict,).
			
		:keyword tuple ex_iters_by_key:
		    List of types instances of which are need to exclude 
		    from processing on each operation of selecting by key.
			
		    Default is ().
			
		:keyword tuple iters_by_idx:
		    List of types instances of which are iterable by indices, 
		    i.e next operation of selecting by indices will be executed from all items 
		    that are instance of one of this types.
			
		    Default (Iterable,).
			
		:keyword tuple ex_iters_by_idx:
		    List of types instances of which are need to exclude 
		    from processing on each operation of selecting by indices.
			
		    Default is (dict, str).
			
		:keyword JPath jpath_inst:
		    Instance that implements JPath.
			
		:except TypeError:
		    If root is not an instance of JSelection.
			
		:return None:
		"""
		self.meta = {
			"iters_by_key" : iters_by_key or (dict,), 
			"ex_iters_by_key" : ex_iters_by_key or (), 
			"iters_by_idx" : iters_by_idx or (Iterable,), 
			"ex_iters_by_idx" : ex_iters_by_idx or (dict, str), 
			"jpath_inst": jpath_inst
		}
		self.meta["root"] = root or self
		if not isinstance(self.meta["root"], JSelection):
			raise TypeError("root must be an instance of %s" % JSelection)
		
		self._items = items
		
	def __getitem__(self, idx):
		"""
		Return item by index.
		"""
		try:
			return self._items[idx]
		except IndexError as ex:
			raise IndexError("index %s out of range" % idx)
		except TypeError as ex:
			raise TypeError("indices must be integers or slices, not %s" % idx.__class__.__name__)
	
	def __add__(self, value):
		"""
		Return self + value.
		"""
		return self.__class__(*(self._items + tuple(value)), **self.meta)
		
	def __mul__(self, value):
		"""
		Return self * value.
		"""
		return self.__class__(*(self._items * value), **self.meta)
		
	def __rmul__(self, value):
		"""
		Return value * self.
		"""
		return self.__class__(*(value * self._items), **self.meta)
		
	def __iter__(self):
		"""
		Return iter(self).
		"""
		self._index = -1
		return self
		
	def __next__(self):
		"""
		Return next(self).
		"""
		if self._index < len(self) - 1:
			self._index += 1
			return self[self._index]
		else:
			raise StopIteration
			
	def __len__(self):
		"""
		Return len(self).
		"""
		return len(self._items)
		
	def __str__(self):
		"""
		Return str(next).
		"""
		return str(self._items)
		
	def __call__(self, root, **kwargs):
		"""
		Call self as a function.
		
		Return a new instance of JSelection that has only one root item that also is root selection.
		
		For example:
		>>> from jpathpy import JSelection
		>>> s = JSelection()
		>>> root = s({"a":1, "b":2})
		>>> # it's only one root item
		>>> root.tuple()
		({'a': 1, 'b': 2},)
		>>> # current selection is also root selection
		>>> root.meta["root"].tuple()
		({'a': 1, 'b': 2},)
		>>> root is root.meta["root"]
		True
			
		:except Exception:
		    Other exceptions that can be occurred when initialize a new instance of JSelection.
			
		:return JSelection:
		"""
		if "root" in kwargs:
			del kwargs["root"]
		return self.__class__(root, **kwargs)
		
	def _select(self, *args, deep=False, all=False):
		"""
		Select items from current selection and return new selection.
		
		:param *args:
		    Can contains key by that will be used for selecting items.
		    Key is required if keyword ``all`` is False.
			
		:keyword bool deep:
		    Indicates that deep selectiong is needed, i.e. selecting will be 
		    from all nested levels.
			
		:keyword bool all:
		    If it is True than all key will be selected from each level of nesting.
			
		:except TypeError:
		    If key is missing when keyword ``all`` is False.
			
		:return JSelection:
		"""
		if not all and not len(args):
			raise TypeError("expected some key")
		
		accum_selections = lambda jselection, appended_item : \
			jselection + (
				(appended_item,) \
					if not deep \
					else \
				tuple(self.__class__(appended_item, **self.meta)._select(*args, deep=deep, all=all))
			)
		
		def select(jselection, select_from):
			if isinstance(select_from, self.meta["iters_by_key"]) and not isinstance(select_from, self.meta["ex_iters_by_key"]):
				if not all:
					jselection += (select_from[args[0]],) if args[0] in select_from else ()
				else:
					jselection += tuple(select_from[k] for k in select_from)
				
				if deep:
					jselection = reduce(accum_selections, [select_from[k] for k in select_from] if not all else jselection, jselection)
			elif isinstance(select_from, self.meta["iters_by_idx"]) and not isinstance(select_from, self.meta["ex_iters_by_idx"]):
				jselection = reduce(select, select_from, jselection)
			return jselection
				
		return self.__class__(*reduce(select, self, ()), **self.meta)
		
	def one(self, key, deep=False):
		"""
		Select items by key from current selection and return new selection.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":{"a":1}, "b":2}
		>>> s = JSelection(d)
		>>> # simple jselection
		>>> s.one("a").tuple()
		({'a': 1},)
		>>> # deep jselection
		>>> s.one("a", deep=True).tuple()
		({'a': 1}, 1)
		
		:param object key:
		    Key for selecting.
			
		:keyword bool deep:
		    Indicates that deep selectiong is needed, i.e. selecting will be 
		    from all nested levels.
			
		:return JSelection:
		"""
		return self._select(key, deep=deep, all=False)
		
	def all(self, deep=False):
		"""
		Select items independently of key from current selection and return new selection.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":{"a":1}, "b":2}
		>>> s = JSelection(d)
		>>> # simple jselection
		>>> s.all().tuple()
		({'a': 1}, 2)
		>>> # deep jselection
		>>> s.all(deep=True).tuple()
		({'a': 1}, 2, 1)
		
		:keyword bool deep:
		    Indicates that deep selectiong is needed, i.e. selecting will be 
		    from all nested levels.
			
		:return JSelection:
		"""
		return self._select(deep=deep, all=True)
			
	def el(self, indices):
		"""
		Select elements by indices from items in current selection if item is iterable by indices. 
	    Items that is not iterable will be skipped in new selection.
		
		If selecting by indices can not be executed for some item that item will be 
		skipped and any exceptions are not be occurred.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":[1,2,3], "b":{"a":1}}
		>>> s = JSelection(d)
		>>> # select all items by key 'a'
		>>> items = s.one("a", deep=True)
		>>> items.tuple()
		([1, 2, 3], 1)
		>>> # select second index
		>>> # note that value of second item
		>>> # is missing in new selection because
		>>> # this value is not iterable
		>>> items.el(1).tuple()
		(2,)
		>>> # select slice
		>>> items.el(slice(1,None)).tuple()
		(2, 3)
		>>> # select items in order of the indices
		>>> items.el([3, -1, 2, 1, 0]).tuple()
		(3, 3, 2, 1)
		>>> # IndexError but skip exceptions
		>>> items.el(100).tuple()
		()
		
		:param int or slice or tuple or list indices:
		    Index or indices by that selection will be executed.
			
		    If index is int, element by this index will be selected.
			
		    If index is slice that slice will be selected.
			
		    If index is list or tuple that it is sequence of indices that 
		    must be selected. Note that selected elements will be added to new selection 
		    in order of the indices.
			
		:except TypeError:
		    If index in ``indices`` is not valid.
			
		:return JSelection:
		"""	
		return self.__class__(*reduce(
			lambda jselection, item : \
				jselection + (lambda item, indices : \
					tuple(self.__class__(*item, **self.meta).i(indices)) \
						if isinstance(item, self.meta["iters_by_idx"]) \
						   and \
						   not isinstance(item, self.meta["ex_iters_by_idx"]) \
						else \
					()
				)(item, indices), 
			self, 
			()
		), **self.meta)
		
	def i(self, indices):
		"""
		Select items from current selection by index or indices.
		
		If selecting by indices can not be executed that item will be 
		skipped and any exceptions are not be occurred.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":[1,2,3], "b":{"a":1}}
		>>> s = JSelection(d)
		>>> items = s.all(deep=True)
		>>> items.tuple()
		({'a': 1}, [1, 2, 3], 1)
		>>> # select first item
		>>> items.i(0).tuple()
		({'a': 1},)
		>>> # select slice
		>>> items.i(slice(1,None)).tuple()
		([1, 2, 3], 1)
		>>> # select items in order of the indices
		>>> items.i([3, -1, 2, 1, 0]).tuple()
		(1, 1, [1, 2, 3], {'a': 1})
		>>> # IndexError but skip exceptions
		>>> items.i(100).tuple()
		()
		>>> # IndexError by simple indexing
		>>> items[100]
		Traceback (most recent call last):
		  File "<pyshell#32>", line 1, in <module>
			items[100]
		IndexError: index 100 out of range
		
		:param int or slice or tuple or list index:
		    Index or indices by that selection will be executed.
			
		    If index is int, item by this index will be selected.
			
		    If index is slice that slice will be select.
			
		    If index is list or tuple that it is sequence of indices that 
		    must be selected. Note that items will be added to new selection 
		    in order of the indices.
			
		:except TypeError:
		    If index in ``indices`` is not valid.
			
		:return JSelection:
		"""
		jselection = ()
		if isinstance(indices, (list, tuple)):
			for idx in indices:
				try: jselection += (self[idx],)
				except IndexError: pass
		else:
			try: jselection += (self[indices],) if isinstance(indices, int) else tuple(self[indices])
			except IndexError: pass
		
		return self.__class__(*jselection, **self.meta)
		
	def exp(self):
		"""
		Expand selection by elements of each item in current selection 
		if item is iterable by indices. Other items in current selection 
		will be added to new selection as it is.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":[1,2,3], "b":"abc", "c":{"d":False}}
		>>> s = JSelection(d)
		>>> # select all keys
		>>> items = s.all()
		>>> items.tuple()
		([1, 2, 3], {'d': False}, 'abc')
		>>> items.exp().tuple()
		(1, 2, 3, {'d': False}, 'abc')
		
		:return JSelection:
		"""
		return self.__class__(*reduce(
			lambda jselection, item : \
				jselection + tuple(item) \
					if isinstance(item, self.meta["iters_by_idx"]) \
					   and \
					   not isinstance(item, self.meta["ex_iters_by_idx"]) \
					else \
				jselection + (item,), 
			self, 
			()
		), **self.meta)
		
	def filter(self, func):
		"""
		Filter current selection and return new selection.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":[1,2,3], "b":{"a":1}}
		>>> s = JSelection(d)
		>>> # select all items by key 'a'
		>>> items = s.one("a", deep=True)
		>>> items.tuple()
		([1, 2, 3], 1)
		>>> # filter
		>>> items.filter(lambda idx, cur, root : isinstance(cur[0], list)).tuple()
		([1, 2, 3],)
		
		:param function or lambda func:
		    Function that will be called on each item of current selection 
		    and if it result will be True, item be added to new selection.
			
		    Note that if some exception will be occurred while processing function 
			that noone exceptions be raised and item be skipped in new selection.
			
			Note that function must be take three arguments:
		        :param int idx:
		            Index of current item.
		        :param JSelection cur:
		            The selection with only current item.
		        :param JSelection root:
		            Root selection.
		
		:return JSelection:
		"""		
		def _(args):
			try: return func(args[0], self.__class__(args[1], **self.meta), self.meta["root"])
			except Exception as ex:
				# print("%s(%r)" % (ex.__class__.__name__, str(ex)))
				pass
		
		return self.__class__(*map(lambda x : x[1], filter(_, enumerate(self))), **self.meta)
		
	def call4item(self, idx, func, *args, **kwargs):
		"""
		Call specified function on item of current selection.
		
		If some exception will be occurred while processing function 
		than exception be raised.
		
		This method always return result of specified function, not new selection.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":"abcdef", "b":{"a":1}}
		>>> s = JSelection(d)
		>>> items = s.one("a", deep=True)
		>>> items.tuple()
		('abcdef', 1)
		>>> # call function
		>>> items.i(0).call4item(0, str.startswith, "abc")
		True
		
		:param int idx:
		    Index of item.
			
		:param function or lambda func:
		    Some function that will be called on item of current selection.
		
		:param tuple *args:
		    Function positional arguments.
			
		:param dict **kwargs:
		    Function keyword arguments.
			
		:except IndexError:
		    If ``idx`` out of selection range.
			
		:except TypeError:
		    If ``idx`` is invalid.
			
		:except Exception:
		    Other exceptions that can be occurred while processing 
		    function from argument ``func``.
			
		:return object:
		"""
		return func(self[idx], *args, **kwargs)
		
	def call4items(self, func, *args, **kwargs):
		"""
		Call specified function on all items of current selection.
		
		If some exception will be occurred while processing function 
		than exception be raised.
		
		This method always return result of specified function, not new selection.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":"abcdef", "b":{"a":0}}
		>>> s = JSelection(d)
		>>> items = s.one("a", deep=True)
		>>> items.tuple()
		('abcdef', 0)
		>>> # call function
		>>> items.call4items(all)
		False
		>>> items.call4items(any)
		True
		
		:param function or lambda func:
		    Some function that will be called on all items of current selection.
			
		:param tuple *args:
		    Function positional arguments.
			
		:param dict **kwargs:
		    Function keyword arguments.
			
		:except Exception:
		    Other exceptions that can be occurred while processing 
		    function from argument ``func``.
			
		:return object:
		"""
		return func([item for item in self], *args, **kwargs)
		
	def call4self(self, func, *args, **kwargs):
		"""
		Call specified function on current selection.
		
		If some exception will be occurred while processing function 
		than exception be raised.
		
		This method always return result of specified function, not new selection.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":"abcdef", "b":{"a":0}}
		>>> s = JSelection(d)
		>>> items = s.one("a", deep=True)
		>>> items.tuple()
		('abcdef', 0)
		>>> # return count of items in current jselection
		>>> items.call4self(lambda self : len(self))
		2
		
		:param function or lambda func:
		    Some function that will be called on current selection.
			
		:param tuple *args:
		    Function positional arguments.
			
		:param dict **kwargs:
		    Function keyword arguments.
			
		:except Exception:
		    Other exceptions that can be occurred while processing 
		    function from argument ``func``.
			
		:return object:
		"""
		return func(self, *args, **kwargs)
		
	def call4each(self, func, *args, **kwargs):
		"""
		Call specified function on each item in selection and return new selection.
		
		If some exception will be occurred while processing function 
		exception not be raised.
		
		For example:
		>>> from jpathpy import JSelection
		>>> d = {"a":"abcdef", "b":{"a":0}}
		>>> s = JSelection(d)
		>>> items = s.one("a", deep=True)
		>>> items.tuple()
		('abcdef', 0)
		>>> # convert to string all items
		>>> items.call4each(str).tuple()
		('abcdef', '0')
		
		:param function or lambda func:
		    Some function that will be called on each item in selection.
			
		:param tuple *args:
		    Function positional arguments.
			
		:param dict **kwargs:
		    Function keyword arguments.
			
		:except Exception:
		    Other exceptions that can be occurred while processing 
		    function from argument ``func``.
			
		:return object:
		"""
		results = []
		for item in self:
			try: results.append(func(item, *args, **kwargs))
			except: pass
		return self.__class__(*results, **self.meta)
		
	def byjpath(self, expr):
		"""
		Execute JPath and return result.
		
		For example:
		>>> from jpathpy import jselection, JPath
		>>> d = {"a":1, "b":{"a":2}}
		>>> s = jselection(d, jpath_inst=JPath())
		>>> s.byjpath(r'$.."a"').tuple()
		(1, 2)
		
		:param str expr:
		    JPath expression.
			
		:except Exception:
			See more at jpathpy.parse.parse.
			
		:return JSelection:
		"""
		if not isinstance(self.meta["jpath_inst"], JPath):
			raise ValueError("it seems that %s doesn't implement JPath" % type(self.meta["jpath_inst"]).__name__)
		return self.meta["jpath_inst"](expr, self)
		
	def setroot(self, root):
		"""
		Set root selection.
		
		:param JSelection root:
		    Root selection.
			
		:return None:
		"""
		self.meta["root"] = root
		
	def tuple(self):
		"""
		Return tuple(self).
		
		:return tuple:
		"""
		return tuple(self)
		
	def print(self):
		"""
		Call print(self).
		
		:return None:
		"""
		print(self)


class JPath(object):
	"""
	Class provides methods for selecting items from objects, that can be iterate 
	by keys or indices (such as dictionaries or lists).
	
	JPath syntax is used for selecting. Note, that only string values can be 
	used for selecting by key.
	
	JPath can be usefull for selecting from JSON.
	
	Following table shows how to use JPath.
	+================================+=========================================+====================================+
	|             JPath              |                Python                   |               Comment              |
	+================================+=========================================+====================================+
	| r'$'                           | root                                    | reference to the root selection    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'@'                           | cur                                     | reference to the current selection |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$."key"'                     | root.one("key")                         |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$.."key"'                    | root.one("key", deep=True)              |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$.*'                         | root.all()                              |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$..*'                        | root.all(deep=True)                     |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$.[0]'                       | root.el(0)                              |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$.[0,1,2]'                   | root.el([0,1,2])                        |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$.[0:1]'                     | root.el(slice(0,1))                     |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$[0]'                        | root.i(0)                               |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$[0,1,2]'                    | root.i([0,1,2])                         |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$[0:1]'                      | root.i(slice(0,1))                      |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$[*]'                        | root.exp()                              |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$[@."key"]'                  | root.filter(                            |                                    |
	|                                |     lambda idx, cur, root :             |                                    |
	|                                |     cur.one("key")                      |                                    |
	|                                | )                                       |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$[@."key" = "value"]'        | root.filter(                            | available compare operations:      |
	|                                |       lambda idx, cur, root :           | >, >=, <, <=, =, !=                |
	|                                |       cur.one("key")[0] == "value"      |                                    |
	|                                |   )                                     |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$[@."key" + 1 > 3]'          | root.filter(                            | available math operations:         |
	|                                |       lambda idx, cur, root :           | +, -, /, *, %                      |
	|                                |       cur.one("key")[0] + 1 > 3         |                                    |
	|                                |   )                                     |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$[@."key" and $.."someKey"]' | root.filter(                            | available logic operations:        |
	|                                |     lambda idx, cur, root :             | and, or                            |
	|                                |     cur.one("key") and root.one(        |                                    |
	|                                |         "someKey",                      |                                    |
	|                                |         deep=True                       |                                    |
	|                                |     )                                   |                                    |
	|                                | )                                       |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	| r'$[startswith(@, "value")]'   | root.call4self(                         | jpath_funcs is instance of         |
	|                                |     jpath_funcs.startswith, *("value",) | jpathpy.jpath_funcs.JPathFunctions |
	|                                | )                                       |                                    |
	+--------------------------------+-----------------------------------------+------------------------------------+
	"""
	def __init__(self, output_dir=None, write_output=False, jpath_funcs=JPathFunctions()):
		"""
		Initialize JPath instance.
		
		:keyword str output_dir:
		    See more at jpathpy.parse.parse.
			
		:keyword bool write_output:
		    See more at jpathpy.parse.parse.
			
		:keyword object jpath_funcs:
		    See more at jpathpy.parse.parse.
		"""
		self.outputDir   = output_dir
		self.writeOutput = write_output
		self.jpathFuncs  = jpath_funcs
		
	def __call__(self, expr, root, **kwargs):
		"""
		Call self as a function.
		
		Execute JPath and return selection as JSelection.
		
		For example:
		>>> from jpathpy import jselection, JPath
		>>> d = {"a":[1,2,3], "b":{"a":"abc"}}
		>>> jpath = JPath()
		>>> jpath(r'$.."a"', jselection(d)).tuple()
		([1, 2, 3], 'abc')
		
		:param str expr:
		    See more at jpathpy.JPath.exec_jpath.
			
		:param JSelection root:
		    See more at jpathpy.JPath.exec_jpath.
			
		:param dict **kwargs:
		    See more at jpathpy.JPath.exec_jpath.
			
		:except Exception:
		    See more at jpathpy.JPath.exec_jpath.
			
		:return JSelection:
		"""
		return self.exec_jpath(expr, root, **kwargs)
	
	def _parse_and_exec(self, expr, start, debug_prefix, cur, root, **kwargs):
		"""
		Parse and execute JPath expression.
		
		For example:
		>>> from jpathpy import jselection, JPath
		>>> d = {"a":[1,2,3], "b":{"a":"abc"}}
		>>> jpath = JPath()
		>>> jpath._parse_and_exec(r'$.."a"', "jpath", "example", jselection(d), jselection(d)).tuple()
		([1, 2, 3], 'abc')
		
		:param str expr:
		    JPath expression.
			
		:param str start:
		    See more at jpathpy.parse.parse.
			
		:param str debug_prefix:
		    Prefix that will be used for debug files.
			
			See more at jpathpy.parse.parse.
			
		:param JSelection cur:
		    Current selection.
			
		:param JSelection root:
		    Root selection.
			
		:param dict **kwargs:
		    Keyword arguments.
			
		:except Exception:
		    Some exceptions that can be occurred while parsing JPath 
		    and execute methods of instances of JSelection.
			
		:return JSelection:
		"""
		jpath_funcs = kwargs.get("jpath_funcs", None) or self.jpathFuncs
		# parse JPath
		res = parse(
			expr, 
			start, 
			output_dir=kwargs.get("output_dir", None) or self.outputDir, 
			write_output=kwargs.get("write_output", False) or self.writeOutput, 
			lextab="%s__lextab" % debug_prefix, 
			tabmodule="%s__parsetab" % debug_prefix, 
			debugfile="%s__debugfile.out" % debug_prefix, 
			jpath_funcs=jpath_funcs
		)
		# execute JPath
		return eval(res, {"root": root, "cur": cur, "jpath_functions": jpath_funcs}) 
	
	def exec_jpath(self, expr, cur, output_dir=None, write_output=False, jpath_funcs=None):
		"""
		Execute JPath and return result as JSelection.
		
		For example:
		>>> from jpathpy import jselection, JPath
		>>> d = {"a":[1,2,3], "b":{"a":"abc"}}
		>>> jpath = JPath()
		>>> # select all items by key 'a'
		>>> jpath.exec_jpath(r'$.."a"', jselection(d)).tuple()
		([1, 2, 3], 'abc')
		>>> # JPathLexicalError
		>>> jpath.exec_jpath(r'#.."a"', jselection(d))
		Traceback (most recent call last):
		  File "<pyshell#14>", line 1, in <module>
			jpath.exec_jpath(r'#.."a"', jselection(d))
		jpathpy.exceptions.JPathLexicalError: Invalid syntax at line 1 (position: 0)
		>>> # JPathSyntaxError
		>>> jpath.exec_jpath(r'$..."a"', jselection(d))
		Traceback (most recent call last):
		  File "<pyshell#16>", line 1, in <module>
			jpath.exec_jpath(r'$..."a"', jselection(d))
		jpathpy.exceptions.JPathSyntaxError: Unexpected token '.' at line 1 (position: 3)
		>>> # JPathFunctionError
		>>> jpath.exec_jpath(r'$.."a"[a(@)]', jselection(d))
		Traceback (most recent call last):
		  File "<pyshell#18>", line 1, in <module>
			jpath.exec_jpath(r'$.."a"[a(@)]', jselection(d))
		jpathpy.exceptions.JPathFunctionError: Unknown JPath function a or it is not callable
		
		:param str expr:
		    JPath expression.
			
		:param JSelection cur:
		    Current selection.
			
		:keyword str output_dir:
		    See more at jpathpy.parse.parse.
			
		:keyword bool write_output:
		    See more at jpathpy.parse.parse.
			
		:keyword object jpath_funcs:
		    See more at jpathpy.parse.parse.
			
		:except Exception:
		    Some exceptions that can be occurred while parsing JPath 
		    and execute methods of instances of JSelection.
			
		:return JSelection:
		"""
		return self._parse_and_exec(
			expr, 
			"jpath", 
			self.exec_jpath.__name__, 
			cur, 
			cur, 
			output_dir=output_dir, 
			write_output=write_output, 
			jpath_funcs=jpath_funcs
		)
		
	def exec_jpath_filter(self, expr, cur, root, output_dir=None, write_output=False, jpath_funcs=None):
		"""
		Execute JPath filtering expression and return result.
		
		For example:
		>>> from jpathpy import jselection, JPath
		>>> d = {"a":[1,2,3], "b":{"a":"abc"}}
		>>> jpath = JPath()
		>>> # filter
		>>> jpath.exec_jpath_filter(r'$.."a".[1] = 2', jselection(d), jselection(d))
		True
		
		:param str expr:
		    JPath filtering expression.
			
		:param JSelection cur:
		    Current selections.	
		
		:param JSelection root:
		    Root selection.
			
		:keyword str output_dir:
		    See more at jpathpy.parse.parse.
			
		:keyword bool write_output:
		    See more at jpathpy.parse.parse.
			
		:keyword object jpath_funcs:
		    See more at jpathpy.parse.parse.
			
		:except Exception:
		    Some exceptions that can be occurred while parsing JPath 
		    and execute methods of instances of JSelection.
			
		:return JSelection:
		"""
		return self._parse_and_exec(
			expr, 
			"expressionstr", 
			self.exec_jpath_filter.__name__, 
			cur, 
			root, 
			output_dir=output_dir, 
			write_output=write_output, 
			jpath_funcs=jpath_funcs
		)
		
	def exec_jpath_func(self, expr, cur, root, output_dir=None, write_output=False, jpath_funcs=None):
		"""
		Execute JPath function and return result.
		
		For example:
		>>> from jpathpy import jselection, JPath
		>>> d = {"a":[1,2,3], "b":{"a":"abc"}}
		>>> jpath = JPath()
		>>> jpath.exec_jpath_func(r'startswith($."b"."a", "ab")', jselection(d), jselection(d))
		True
		>>> jpath.exec_jpath_func(r'startswith($."b"."a", 1)', jselection(d), jselection(d))
		Traceback (most recent call last):
		  File "<pyshell#4>", line 1, in <module>
			jpath.exec_jpath_func(r'startswith($."b"."a", 1)', jselection(d), jselection(d))
		jpathpy.exceptions.JPathFunctionError: startswith first arg must be str or a tuple of str, not int
		
		:param str expr:
		    JPath function.
			
		:param JSelection cur:
		    Current selection.	
		
		:param JSelection root:
		    Root selection.
			
		:keyword str output_dir:
		    See more at jpathpy.parse.parse.
			
		:keyword bool write_output:
		    See more at jpathpy.parse.parse.
			
		:keyword object jpath_funcs:
		    See more at jpathpy.parse.parse.
			
		:except Exception:
		    Some exceptions that can be occurred while parsing JPath 
		    and execute methods of instances of JSelection.
			
		:return object:
		"""
		try:
			return self._parse_and_exec(
				expr, 
				"function", 
				self.exec_jpath_func.__name__, 
				cur, 
				root, 
				output_dir=output_dir, 
				write_output=write_output, 
				jpath_funcs=jpath_funcs
			)
		except JPathError as ex:
			raise ex
		except Exception as ex:
			raise JPathFunctionError(str(ex))
		
"""
The empty selection.

You can call it as function, for example:
>>> from jpathpy import jselection
>>> d = {"a":1, "b":2}
>>> jselection(d).tuple()
({'b': 2, 'a': 1},)
"""
jselection = JSelection()

"""
Instance of base JPath.

You can call it as function, for example:
>>> from jpathpy import jpath, jselection
>>> d = {"a":1, "b":2}
>>> jpath(r'$."a"', jselection(d)).tuple()
(1,)
"""
jpath = JPath()