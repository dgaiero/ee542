import datetime
import importlib
import logging
from typing import List

from commonLibrary.exceptions.SensorExceptions import SensorInstantiationError
from commonLibrary.jobs.Job import Job
from commonLibrary.sensor.sample import Sample
from commonLibrary.utilities.stdpub import std_sensor_pub


class SensorJob():

   def __init__(self, name:str, sample_rate:float, sensorCls:str, fields:List[str], parent=None, **kwargs):
      self.logger = logging.getLogger(__name__)
      self.type = sensorCls
      self.name = f"{name}:{self.type}"
      self._name = name
      self.parent = parent
      self.sample_rate = sample_rate
      self.fields = fields

      self.logger.info(
          f"initalizing sensor {self.name} with sample rate of {sample_rate} Hz")
      try:
         lib = importlib.import_module(
            f'commonLibrary.sensor.{sensorCls}')
         sensorCls = getattr(lib, sensorCls)
         self.sensorCls = sensorCls(self.name, self.sample_rate, **kwargs)
      except SensorInstantiationError as err:
         raise err
      except Exception as err:
         raise SensorInstantiationError(self.name, err)

   def setup_job(self):
      self.parent.jobs.submit_job(
          self.name, self.sample, self.sample_rate, self.parent.threadError)

   def sample(self):
      value = self.sensorCls.sample()
      new_sample_time = datetime.datetime.now()
      parsed_value = self.sensorCls.parse(value)
      if not parsed_value:
         return
      sample_data = {}
      for field in self.fields:
         sample_data[field] = parsed_value[field]
      current_sample = Sample(data=sample_data, timestamp=new_sample_time)

      # self.parent and self.parent.sensorData[self.name].append(
      #     current_sample)
      # self.parent.sensorCallback(self.name)
      std_sensor_pub(self.name, current_sample)

   def cleanup(self):
      pass
