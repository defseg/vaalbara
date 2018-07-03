'''A BucketSchema maintains a collection of names associated with tests, and
sorts items into buckets by which bucket is the first to return a truthy
value.
  There are two orders a BucketSchema maintains: a name order and a test
order. 
  The test order determines the order in which the buckets are tested 
against the item. This is determined by the order in which buckets are added.
  The name order determines the order of the returned OrderedDict of buckets.
This is determined by the name_order parameter, which also functions as the ID.'''

from collections import namedtuple, OrderedDict

class BucketSchema:
  def __init__(self):
    self.buckets = OrderedDict()

  def add(self, name, name_order, test):
    '''Adds a bucket to the schema.

    Args:
      name (str): The name of the bucket.
      name_order (int): The order of the bucket within the returned OrderedDict.
      test (function(_ -> bool)): The test that determines whether to add an item
        to this bucket.
    '''
    self.buckets[name_order] = Bucket(name=name, test=test)

  def bucketize(self, items):
    '''Sort items into the defined buckets.

    Args:
      items (list): Items to embucket.

    Returns:
      OrderedDict(name_order: [Maybe item], name_order: [Maybe item])'''
    bucketing = OrderedDict()
    for k in sorted(self.buckets.iterkeys()):
      bucketing[k] = []
    for item in items:
      for k in self.buckets.iterkeys():
        if self.buckets[k].test(item):
          bucketing[k].append(item)
          break
    return bucketing

  def name(self, name_order):
    return self.buckets[name_order].name

Bucket = namedtuple('Bucket', ['name', 'test'])