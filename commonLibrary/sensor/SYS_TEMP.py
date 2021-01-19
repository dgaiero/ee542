import logging
import os
import re

from commonLibrary.abstract.Sensor.Sensor import Sensor


class SYS_TEMP(Sensor):

   def __init__(self, sensor_id: str, sample_rate: float, config_payload: dict = None):
      super().__init__(sensor_id, sample_rate, config_payload=config_payload)
      self.logger = logging.getLogger(__name__)
      self.inf = None

   def open(self):
      pass

   def close(self):
      pass

   def sample(self):
      temp = os.popen("vcgencmd measure_temp").readline()
      return float(re.findall(r"\d+\.\d+", temp)[0])

   def parse(self, val):
      threshold = self.config_payload['threshold']
      if val > threshold:
         msg = f"System Temperature Excedded Threshold {val}C > {threshold}C"
         self.logger.critical(msg.upper())
      return {'temperature': val}
