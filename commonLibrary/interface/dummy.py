from os import urandom
from random import Random, seed
import logging
from commonLibrary.abstract.interface.InterfaceAbstract import Interface


class DummyInterface(Interface):

   def __init__(self, *args, **kwargs):
      super().__init__(self, *args, **kwargs)
      self.logger = logging.getLogger(__name__)
      self.seed = self.config_payload['seed']

   def open(self):
      self.logger.info(
          f"Opening Dummy Interface with random seed: {self.seed}")
      self.random = Random(self.seed)

   def close(self):
      pass

   def read(self, num_bytes, offset=0):
      return bytearray(self.random.getrandbits(8) for _ in range(num_bytes))

   def write(self, lst, offset=0):
      pass
