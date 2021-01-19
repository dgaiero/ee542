import math
import threading

import construct
from commonLibrary.abstract.Sensor.Sensor import Sensor
from commonLibrary.interface.dummy import DummyInterface
from construct import BitsInteger, BitStruct


class DummySensor(Sensor):
   def __init__(self, sensor_id:str, sample_rate: float, config_payload:dict=None):
      super().__init__(sensor_id, sample_rate, config_payload=config_payload)
      self.seed = self.config_payload['seed']
      self.random = None
      if config_payload and "fields" in config_payload:
         fields =  config_payload["fields"]
      else:
         fields = [f"DATA_{i}" for i in range(5)]
      self.inf = DummyInterface(self.seed, config_payload=self.config_payload)
      self.read_bit_size:int = 8 + sum((16 for _ in fields))
      self.structure = BitStruct(
      "DEVICE_ID" / construct.BitsInteger(8),
      *[field / BitsInteger(16) for field in fields])
      

   def sample(self):
      return self.inf.read(self.read_bit_size)

   def open(self):
      self.inf.open()

   def close(self):
      self.inf.close()

   def parse(self, val):
      return self.structure.parse(val)

   def save(self):
      pass

   def push(self):
      pass


def main():
   config_payload = {'seed': 313045}
   test = DummySensor('test', 0.5, config_payload=config_payload)
   test.open()
   val = test.sample()
   print(val)
   parsed_val = test.parse(val)
   print(parsed_val)
   print(parsed_val['DEVICE_ID'])


if __name__ == "__main__":
   main()
