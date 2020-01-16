Overview
========
Package ``jpathpy`` is easy way for selecting items from objects, that can be iterate by keys or indices (such as dictionaries or lists).

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

Simple python ``dict`` is not ordered, so that using ``collections.OrderedDict`` is more right if you work with JSON string. It saves initial order of items if you need it. For example:

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


Stat
----
+----------------------------+---------------------------------+
| Name                       | jpathpy                         |
+----------------------------+---------------------------------+
| Version                    | |pypi-version|                  |
+----------------------------+---------------------------------+
| License                    | |github-license|                |
+----------------------------+---------------------------------+
| Author                     | Vladimir Saltykov               |
|                            | <vowatchka@mail.ru>             |
+----------------------------+---------------------------------+
| Copyright                  | © since 2017                    |
+----------------------------+---------------------------------+
| Dev Status                 | |pypi-dev-status|               |
+----------------------------+---------------------------------+
| Languages                  | |github-language-count|         |
|                            | |github-language-top|           |
+----------------------------+---------------------------------+
| Python version             | |pypi-pyversions|               |
+----------------------------+---------------------------------+
| Wheel                      | |pypi-wheel|                    |
+----------------------------+---------------------------------+
| Downloads from ``pypi``    | |pypi-downloads|                |
+----------------------------+---------------------------------+
| Latest GitHub release      | |github-latest-release|         |
+----------------------------+---------------------------------+
| Release date               | |github-release-date|           |
+----------------------------+---------------------------------+
| Last GitHub commit         | |github-last-commit-date|       |
+----------------------------+---------------------------------+
| Open issues                | |github-open-issues|            |
+----------------------------+---------------------------------+
| Closed issues              | |github-closed-issues|          |
+----------------------------+---------------------------------+
| Open pull requests         | |github-open-pull-requests|     |
+----------------------------+---------------------------------+
| Closed pull requests       | |github-closed-pull-requests|   |
+----------------------------+---------------------------------+

.. |pypi-version| image:: https://img.shields.io/pypi/v/jpathpy
	:target: https://pypi.org/project/jpathpy/
	:alt: PyPI

.. |github-license| image:: https://img.shields.io/github/license/vowatchka/jpathpy
	:target: http://choosealicense.com/licenses/mit/
	:alt: GitHub

.. |pypi-dev-status| image:: https://img.shields.io/pypi/status/jpathpy
	:alt: PyPI - Status

.. |github-language-count| image:: https://img.shields.io/github/languages/count/vowatchka/jpathpy
	:alt: GitHub language count

.. |github-language-top| image:: https://img.shields.io/github/languages/top/vowatchka/jpathpy
	:alt: GitHub top language

.. |pypi-pyversions| image:: https://img.shields.io/pypi/pyversions/jpathpy
	:target: https://www.python.org/downloads/
	:alt: PyPI - Python Version

.. |pypi-wheel| image:: https://img.shields.io/pypi/wheel/jpathpy
	:alt: PyPI - Wheel

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/jpathpy
	:alt: PyPI - Downloads

.. |github-latest-release| image:: https://img.shields.io/github/v/release/vowatchka/jpathpy
	:target: https://github.com/vowatchka/jpathpy/releases
	:alt: GitHub release (latest by date)

.. |github-release-date| image:: https://img.shields.io/github/release-date/vowatchka/jpathpy
	:target: https://github.com/vowatchka/jpathpy/releases
	:alt: GitHub Release Date

.. |github-last-commit-date| image:: https://img.shields.io/github/last-commit/vowatchka/jpathpy
	:alt: GitHub last commit

.. |github-open-issues| image:: https://img.shields.io/github/issues/vowatchka/jpathpy
	:target: https://github.com/vowatchka/jpathpy/issues?q=is%3Aopen+is%3Aissue
	:alt: GitHub issues

.. |github-closed-issues| image:: https://img.shields.io/github/issues-closed/vowatchka/jpathpy
	:target: https://github.com/vowatchka/jpathpy/issues?q=is%3Aissue+is%3Aclosed
	:alt: GitHub closed issues

.. |github-open-pull-requests| image:: https://img.shields.io/github/issues-pr/vowatchka/jpathpy
	:target: https://github.com/vowatchka/jpathpy/pulls?q=is%3Aopen+is%3Apr
	:alt: GitHub pull requests

.. |github-closed-pull-requests| image:: https://img.shields.io/github/issues-pr-closed/vowatchka/jpathpy
	:target: https://github.com/vowatchka/jpathpy/pulls?q=is%3Apr+is%3Aclosed
	:alt: GitHub closed pull requests


Install
-------
::

	pip install jpathpy
	

Usage
-----

>>> from jpathpy import jselection
>>> d = { "books": [ 
            {"author": "Nigel Rees"}, 
            {"author": "Evelyn Waugh"}, 
            {"author": "Herman Melville"}, 
            {"author": "J. R. R. Tolkien"}, 
          ], 
          "paintings": [
            {"author": "Leonardo Da Vinci"}, 
            {"author": "Edvard Munch"}, 
            {"author": "Sistine Chapel by Michelangelo"}, 
            {"author": "Vincent Van Gogh"}, 
          ]
}
>>> s = jselection(d)
>>> s.print()
({'books': [{'author': 'Nigel Rees'}, {'author': 'Evelyn Waugh'}, {'author': 'Herman Melville'}, {'author': 'J. R. R. Tolkien'}], 'paintings': [{'author': 'Leonardo Da Vinci'}, {'author': 'Edvard Munch'}, {'author': 'Sistine Chapel by Michelangelo'}, {'author': 'Vincent Van Gogh'}]},)


Selection by key
^^^^^^^^^^^^^^^^
Use simple selection for select all items with key ``books`` on current level of nesting. If noone items are selected than empty selection will be got.

>>> s.one("books").tuple()
([{'author': 'Nigel Rees'}, {'author': 'Evelyn Waugh'}, {'author': 'Herman Melville'}, {'author': 'J. R. R. Tolkien'}],)
>>> s.one("author").tuple()
()

For select all authors use deep selection.

>>> s.one("author", deep=True).tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien')


Selection all keys
^^^^^^^^^^^^^^^^^^
For select all items on current level of nesting use selection all keys.

>>> s.all().tuple()
([{'author': 'Nigel Rees'}, {'author': 'Evelyn Waugh'}, {'author': 'Herman Melville'}, {'author': 'J. R. R. Tolkien'}], [{'author': 'Leonardo Da Vinci'}, {'author': 'Edvard Munch'}, {'author': 'Sistine Chapel by Michelangelo'}, {'author': 'Vincent Van Gogh'}])

Also you can select all keys from all nested levels.

>>> s.all(deep=True).tuple()
([{'author': 'Nigel Rees'}, {'author': 'Evelyn Waugh'}, {'author': 'Herman Melville'}, {'author': 'J. R. R. Tolkien'}], [{'author': 'Leonardo Da Vinci'}, {'author': 'Edvard Munch'}, {'author': 'Sistine Chapel by Michelangelo'}, {'author': 'Vincent Van Gogh'}], 'Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien', 'Leonardo Da Vinci', 'Edvard Munch', 'Sistine Chapel by Michelangelo', 'Vincent Van Gogh')

Select items by indices
^^^^^^^^^^^^^^^^^^^^^^^
You can select items by indices from selection. If index out of range no exceptions will be occured, but if index is invalid exception will be raised.

>>> authors = s.one("books").one("author")
>>> authors.i(0).tuple()
('Nigel Rees',)
>>> authors.i(slice(None,None,-1)).tuple()
('J. R. R. Tolkien', 'Herman Melville', 'Evelyn Waugh', 'Nigel Rees')
>>> authors.i([1, 0, 3, 2]).tuple()
('Evelyn Waugh', 'Nigel Rees', 'J. R. R. Tolkien', 'Herman Melville')
>>> authors.i(100500).tuple()
()
>>> authors.i("0").tuple()
TypeError: indices must be integers or slices, not str


Selection items from arrays
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can select items by indices from arrays if it exists in selection. If index out of range no exceptions will be occured, but if index is invalid exception will be raised. If item of selection is not array than it will be skiped in new selection.

>>> authors = s.all()
>>> authors.el(0).tuple()
({'author': 'Nigel Rees'}, {'author': 'Leonardo Da Vinci'})
>>> authors.el(slice(None,None,-1)).tuple()
({'author': 'J. R. R. Tolkien'}, {'author': 'Herman Melville'}, {'author': 'Evelyn Waugh'}, {'author': 'Nigel Rees'}, {'author': 'Vincent Van Gogh'}, {'author': 'Sistine Chapel by Michelangelo'}, {'author': 'Edvard Munch'}, {'author': 'Leonardo Da Vinci'})
>>> authors.el([2,1]).tuple()
({'author': 'Herman Melville'}, {'author': 'Evelyn Waugh'}, {'author': 'Sistine Chapel by Michelangelo'}, {'author': 'Edvard Munch'})
>>> authors.el(100500).tuple()
()
>>> authors.el("0").tuple()
TypeError: indices must be integers or slices, not str


Expand selection by array items
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you need to get all items in arrays as new selection you must expand selection. If you do this than all array in selection will be replaced to their items.

>>> books = s.one("books")
>>> books.tuple()
([{'author': 'Nigel Rees'}, {'author': 'Evelyn Waugh'}, {'author': 'Herman Melville'}, {'author': 'J. R. R. Tolkien'}],)
>>> books.exp().tuple()
({'author': 'Nigel Rees'}, {'author': 'Evelyn Waugh'}, {'author': 'Herman Melville'}, {'author': 'J. R. R. Tolkien'})
>>> books.exp().tuple() == books.one("author").tuple()
False

Filter selection
^^^^^^^^^^^^^^^^
If you need you can filter selection by using some function that must return value that can be represent as true or false. If this function return true for item in selection than item will be added to new selection and skipped in other case.

All functions that used for filtering must have 3 positional arguments:

* ``idx``. It will be contains index of current processed selection item.
* ``cur``. It will be contains selection with only one item: current processed selection item.
* ``root``. It will be contains root selection (root seelction can be get as ``selection.meta["root"]``).

If some exception will be occured while processing filtering function than it not be raised and item of selection will be skipped in new selection.

>>> authors = s.one("author", deep=True)
>>> authors.tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien', 'Leonardo Da Vinci', 'Edvard Munch', 'Sistine Chapel by Michelangelo', 'Vincent Van Gogh')
>>> authors.filter(lambda idx, cur, root : cur[0].startswith("E")).tuple()
('Evelyn Waugh', 'Edvard Munch')
>>> # ("Nigel Rees")[12], ("Evelyn Waugh")[12] and ("Edvard Munch")[12] raise IndexError,
>>> # but it will be skipped
>>> authors.filter(lambda idx, cur, root : cur[0][12]).tuple()
('Herman Melville', 'J. R. R. Tolkien', 'Leonardo Da Vinci', 'Sistine Chapel by Michelangelo', 'Vincent Van Gogh')


Call different functions on selection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can call your different functions on selection or on items in selection. Note, if some exception will be occured while processing function than exception be raised. Call of all following methods return value that return function, not selection.

>>> authors = s.one("author", deep=True)
>>> authors.tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien', 'Leonardo Da Vinci', 'Edvard Munch', 'Sistine Chapel by Michelangelo', 'Vincent Van Gogh')
>>> # get first char of first item
>>> authors.i(0).call4item(0, str.__getitem__, 0)
'N'
>>> # get count of items
>>> authors.call4items(list.__len__)
8
>>> # call function on current selection
>>> authors.call4self(jselection.__class__.filter, lambda idx, cur, root : cur[0].startswith("E")).tuple()
('Evelyn Waugh', 'Edvard Munch')

Also you can call function on each item in selection and get new selection. Note, in this case if some exception will be occured while processing function exception not be raised.

>>> authors = s.one("author", deep=True)
>>> authors.tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien', 'Leonardo Da Vinci', 'Edvard Munch', 'Sistine Chapel by Michelangelo', 'Vincent Van Gogh')
>>> # get string length of each items
>>> authors.call4each(str.__len__).tuple()
(17, 12, 30, 16, 10, 12, 15, 16)


Selection by JPath
^^^^^^^^^^^^^^^^^^
You can use JPath syntax for select items.

>>> from jpathpy import jpath
>>> s1 = jselection(d, jpath_inst=jpath)
>>> s1.byjpath(r'$.."author"').tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien', 'Leonardo Da Vinci', 'Edvard Munch', 'Sistine Chapel by Michelangelo', 'Vincent Van Gogh')


Other capabilities
^^^^^^^^^^^^^^^^^^
* Iterate.

>>> authors = s.one("books").one("author")
>>> authors.tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien')
>>> for a in authors:
	    print(a)
Nigel Rees
Evelyn Waugh
Herman Melville
J. R. R. Tolkien

* Get item by index.

>>> authors[0]
'Nigel Rees'

* Add item.

>>> (authors + ("Joan Rowling",)).tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien', 'Joan Rowling')

* Repeat items.

>>> (authors.i(0) * 3).tuple()
('Nigel Rees', 'Nigel Rees', 'Nigel Rees')

* Get length of selection.

>>> len(authors)
4

* As tuple.

>>> authors.tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien')

* Print.

>>> authors.print()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien')

* Meta data.

>>> authors.meta
{'iters_by_idx': (<class 'collections.abc.Iterable'>,), 'root': <jpathpy.JSelection object at 0x02FF2670>, 'jpath_inst': None, 'iters_by_key': (<class 'dict'>,), 'ex_iters_by_idx': (<class 'dict'>, <class 'str'>), 'ex_iters_by_key': ()}

* Configurate process of selection.

>>> s.one("author", deep=True).tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien', 'Leonardo Da Vinci', 'Edvard Munch', 'Sistine Chapel by Michelangelo', 'Vincent Van Gogh')
>>> d1 = { "books": [ 
            {"author": "Nigel Rees"}, 
            {"author": "Evelyn Waugh"}, 
            {"author": "Herman Melville"}, 
            {"author": "J. R. R. Tolkien"}, 
          ], 
          "paintings": (
            OrderedDict({"author": "Leonardo Da Vinci"}), 
            OrderedDict({"author": "Edvard Munch"}), 
            OrderedDict({"author": "Sistine Chapel by Michelangelo"}), 
            OrderedDict({"author": "Vincent Van Gogh"}), 
          )
}
>>> # configurate selection
>>> s1 = jselection(d1, iters_by_idx=(list,), ex_iters_by_idx=(tuple,), iters_by_key=(dict,), ex_iters_by_key=(OrderedDict,))
>>> s1.one("author", deep=True).tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien')
>>> 


Use JPath
---------
JPath is string expression that has easy syntax and used for selecting items from objects, that can be iterate by keys or indices (such as dictionaries or lists).

>>> from jpathpy import jpath, jselection
>>> d = { "books": [ 
            {"author": "Nigel Rees"}, 
            {"author": "Evelyn Waugh"}, 
            {"author": "Herman Melville"}, 
            {"author": "J. R. R. Tolkien"}, 
          ], 
          "paintings": [
            {"author": "Leonardo Da Vinci"}, 
            {"author": "Edvard Munch"}, 
            {"author": "Sistine Chapel by Michelangelo"}, 
            {"author": "Vincent Van Gogh"}, 
          ]
}
>>> jpath(r'$.."author"', jselection(d)).tuple()
('Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien', 'Leonardo Da Vinci', 'Edvard Munch', 'Sistine Chapel by Michelangelo', 'Vincent Van Gogh')

JPath <-> JSelection
^^^^^^^^^^^^^^^^^^^^
Follow table show how JPath expressions equal to ``jpathpy.JSelection`` methods.

================================ ============================================= ======================================
JPath expression                 Python                                        Comment
================================ ============================================= ======================================
r'$'                             >>> root                                      root selection
r'@'                             >>> cur                                       current selection
r'$."key"'                       >>> root.one("key")
r'$.."key"'                      >>> root.one("key", deep=True)
r'$.*'                           >>> root.all()
r'$..*'                          >>> root.all(deep=True)
r'$.[0]'                         >>> root.el(0)
r'$.[0,1,2]'                     >>> root.el([0,1,2])
r'$.[0:1]'                       >>> root.el(slice(0,1))
r'$[0]'                          >>> root.i(0)
r'$[0,1,2]'                      >>> root.i([0,1,2])
r'$[0:1]'                        >>> root.i(slice(0,1))
r'$[*]'                          >>> root.exp()
r'$[@."key"]'                    >>> root.filter(                                
                                 >>>     lambda idx, cur, root :                 
                                 >>>         cur.one("key")                      
                                 >>> )                                           
r'$[@."key" = "value"]'          >>> root.filter(                              available compare operations:
                                 >>>     lambda idx, cur, root :               ``>``, ``>=``, ``<``, ``<=``,
                                 >>>         cur.one("key")[0] == "value"      ``=``, ``!=``
                                 >>> )
r'$[@."key" + 1 > 3]'            >>> root.filter(                              available math operations:
                                 >>>     lambda idx, cur, root :               ``+``, ``-``, ``/``, ``*``,
                                 >>>         cur.one("key")[0] + 1 > 3         ``%``
                                 >>> )
r'$[@."key" and $.."someKey"]'   >>> root.filter(                              available logic operations:
                                 >>>     lambda idx, cur, root :               ``and``, ``or``
                                 >>>         cur.one("key") and root.one(
                                 >>>             "someKey",
                                 >>>             deep=True
                                 >>>     )
                                 >>> )
r'$[startswith(@, "value")]'     >>> root.call4self(                           jpath_funcs is instance of
                                 >>>     jpath_funcs.startswith, *("value",)   ``jpathpy.jpath_funcs.JPathFunctions``
								 >>> )
================================ ============================================= ======================================


Use JPath functions
-------------------
You can call different functions from JPath expression. By default all new instances of ``jpathpy.JPath`` use instance of ``jpathpy.jpath_funcs.JPathFunctions``. This class provides methods that can be call as JPath function. For example:

>>> jpath(r'$.."author"[startswith(@, "E")]', jselection(d)).tuple()
('Evelyn Waugh', 'Edvard Munch')

You can define your classes, methods of which will be used as JPath functions. All that you need it is inherit from class ``jpathpy.jpath_funcs.JPathFunctionsWrapper``. This class provides two protected methods:

* ``_jpath_function(func)``
   It is decorator for decorate your methods as JPath function.
   
   First argument of JPath function must be an instance of ``jpathpy.JSelection``.
   
* ``_getvalue(self, obj)``
   Return value of ``obj`` or value of ``obj[0]`` if ``obj`` is instance of ``JSelection``.
   
Follow example show how define yourself JPath functions:

>>> from jpathpy.jpath_funcs import JPathFunctionsWrapper
>>>
>>> class MyJPathFuncs(JPathFunctionsWrapper):
        @JPathFunctionsWrapper._jpath_function
        def firstchar(self, selection):
            return self._getvalue(selection)[0]
        @JPathFunctionsWrapper._jpath_function
        def lastchar(self, selection):
            return self._getvalue(selection)[-1]
>>>
>>>
>>> d = { "books": [ 
            {"author": "Nigel Rees"}, 
            {"author": "Evelyn Waugh"}, 
            {"author": "Herman Melville"}, 
            {"author": "J. R. R. Tolkien"}, 
          ], 
          "paintings": [
            {"author": "Leonardo Da Vinci"}, 
            {"author": "Edvard Munch"}, 
            {"author": "Sistine Chapel by Michelangelo"}, 
            {"author": "Vincent Van Gogh"}, 
          ]
}
>>> jpath = JPath(jpath_funcs=MyJPathFuncs())
>>> s = jselection(d)
>>> author = jselection(d).one("author", deep=True).i(0)
>>> author.tuple()
('Leonardo Da Vinci',)
>>> jpath.exec_jpath_func(r'firstchar(@)', author, author)
'L'
>>> jpath.exec_jpath_func(r'lastchar(@)', author, author)
'i'
>>> jpath(r'$.."author"[firstchar(@) = "L" and lastchar(@) = "i"]', s).tuple()
('Leonardo Da Vinci',)

Also you can inherit from ``jpathpy.jpath_funcs.JPathFunctions`` for expand its functionality.