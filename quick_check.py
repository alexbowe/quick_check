# Inspired by http://dan.bravender.us/2009/6/21/Simple_Quickcheck_implementation_for_Python.html
# could be vastly improved, but I want to keep it simple for this project
# in future, I might also like to set up a performance testing framework

import random, functools
import itertools as it
from itertools import repeat, product

def _dethunk_repeat(thunk):
  return (f() for f in repeat(thunk))

def _bounded_generator(bounds, thunk):
  return it.chain(bounds, _dethunk_repeat(thunk))

def integers(low=0, high=100):
  bounds = (low, high)
  int_thunk = lambda: random.randint(low, high)
  return _bounded_generator(bounds, int_thunk)

def lists(items=integers(), size=(0, 100)):
  limits = (items.next(), items.next())
  # cartesian product to get each corner case
  edge_cases = ([v] * l for (v,l) in product(limits, size))
  list_thunk = lambda: [items.next() for _ in xrange(random.randint(*size))]
  return _bounded_generator(edge_cases, list_thunk)

def tuples(*args):
  return it.imap(tuple, lists(*args))

alphabet = lambda sigma: integers(0, sigma - 1)
index    = alphabet
bits     = alphabet(2)
quads    = alphabet(4)
octets   = alphabet(8)
hextets  = alphabet(16)
zeros    = repeat(0)
ones     = repeat(1)

def for_all(tries=1000, **kwargs):
  def wrap(f):
    @functools.wraps(f)
    def run_tries(*inargs, **inkwargs):
      for _ in xrange(tries):
        random_kwargs = (dict((name, gen.next()) for (name, gen) in kwargs.iteritems()))
        random_kwargs.update(**inkwargs)
        f(*inargs, **random_kwargs)
    return run_tries
  return wrap
