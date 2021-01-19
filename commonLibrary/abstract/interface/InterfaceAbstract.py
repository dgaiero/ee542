from abc import ABCMeta, abstractmethod


class Interface(metaclass=ABCMeta):

   def __init__(self, channel=None, address=None, bus=None, device=None, config_payload=None):
      self.channel = channel
      self.address = address
      self.bus = bus
      self.device = device
      self.config_payload = config_payload

      self.register = None

   @abstractmethod
   def open(self):
      raise NotImplementedError

   @abstractmethod
   def close(self):
      raise NotImplementedError

   @abstractmethod
   def read(self, *args, **kwargs):
      raise NotImplementedError

   @abstractmethod
   def write(self, *args, **kwargs):
      raise NotImplementedError
