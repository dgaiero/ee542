import pprint


class Sample():
   def __init__(self, data=None, timestamp=None):
      self.data = data
      self.time_stamp = timestamp

   def __repr__(self):
      return pprint.pformat(self.data)

   def __str__(self):
      return self.__repr__()

   def to_dict(self):
      return {
          'timestamp': str(self.time_stamp),
          **self.data
      }

   def __iter__(self):
      for key in ['data', 'time_stamp']:
         yield (key, getattr(self, key))
