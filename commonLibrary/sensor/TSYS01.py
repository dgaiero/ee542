
import logging
import time
from enum import IntEnum

from commonLibrary.abstract.Sensor.Sensor import Sensor
from commonLibrary.exceptions.SensorExceptions import (
    ChecksumError, SensorInstantiationError)
from commonLibrary.interface.i2c import I2CInterface
from commonLibrary.utilities.crc import tsy01_crc
from construct import BitsInteger


class TSY01_REGISTERS(IntEnum):
    ADDR = 0x77
    PROM_READ = 0xA0
    RESET = 0x1E
    CONVERT = 0x48
    READ = 0x00
    CHK_SUM = 0xAE


class TSYS01(Sensor):

   def __init__(self, sensor_id:str, sample_rate:float, config_payload:dict=None):
      super().__init__(sensor_id, sample_rate, config_payload=config_payload)
      self.logger = logging.getLogger(__name__)
      self._temperature = 0
      try:
         self.inf = I2CInterface(channel=self.config_payload['channel'],\
            address=self.config_payload['address'])
      except FileNotFoundError as err:
         raise SensorInstantiationError(sensor_id, err)

   def open(self):
      self.inf.i2c.write_byte(self.inf.address, TSY01_REGISTERS.RESET)
      time.sleep(0.1)
      prom_lst = list()
      for ra in range(0xAE, 0xA0-2, -2):
         p = self.inf.i2c.read_word_data(self.inf.address, ra)
         p = ((p & 0xFF) << 8) | (p >> 8)
         prom_lst.append(p)
      self.k_coef = prom_lst[2:7]
      chksum = tsy01_crc(prom_lst)
      try:
         if chksum == 0x00:
            raise ChecksumError(chksum, "!0")
      except ChecksumError as err:
         self.logger.error(f"{self.name}: {err}")


   def close(self):
      self.inf.close()

   def sample(self):
      self.inf.i2c.write_byte(self.inf.address, TSY01_REGISTERS.CONVERT)
      time.sleep(0.01)
      adc_val = self.inf.read(TSY01_REGISTERS.READ, 3)
      return adc_val[0] << 16 | adc_val[1] << 8 | adc_val[2]

   def parse(self, val):
      val16 = val/256
      temp = -2 * self.k_coef[4] * 10**-21 * val16**4 + \
         4 * self.k_coef[3] * 10**-16 * val16**3 + \
         -2 * self.k_coef[2] * 10**-11 * val16**2 + \
         1 * self.k_coef[1] * 10**-6 * val16 + \
         -1.5 * self.k_coef[0] * 10**-2
      return {'temperature': temp}
