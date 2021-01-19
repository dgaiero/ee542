from abc import ABCMeta, abstractmethod


class Sensor(metaclass=ABCMeta):

   def __init__(self, sensor_id:str, sample_rate:float, config_payload:dict=None):
      self.name = sensor_id
      self.inf = None
      self.sample_rate = sample_rate
      self.id = sensor_id
      self.config_payload = config_payload

   @abstractmethod
   def open(self):
      pass

   @abstractmethod
   def close(self):
      pass

   @abstractmethod
   def sample(self):
      pass

   @abstractmethod
   def parse(self, val) -> dict:
      pass
