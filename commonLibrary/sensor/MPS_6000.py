
import logging
import time
from enum import IntEnum, Enum
from collections import namedtuple
from commonLibrary.abstract.Sensor.Sensor import Sensor
from commonLibrary.exceptions.SensorExceptions import (SensorInstantiationError)
from commonLibrary.interface.i2c import I2CInterface
from commonLibrary.utilities.crc import tsy01_crc
from construct import BitStruct, BitsInteger


class MPS_6000_REGISTERS(IntEnum):
    GYRO_CONFIG = 0x1B
    ACCEL_CONFIG = 0x1C
    PWR_MGMT_CONFIG = 0x6B


class MPS_6000_COMMANDS(IntEnum):
   GYRO_FSR = 0x18
   ACCEL_FSR = 0x18
   PLL_HYRO_REF = 0x01


MPS_6000_SENS_TUPLE = namedtuple('MPS_6000_SENS_TUPLE', 'GYRO_SENS ACCEL_SENS')
MPS_6000_SENS = MPS_6000_SENS_TUPLE(2000.0, 16.0)

MPS_6000_DATA = BitStruct(
   "accel_x" / BitsInteger(16),
   "accel_y" / BitsInteger(16),
   "accel_z" / BitsInteger(16),
   "gyro_x"  / BitsInteger(16),
   "gyro_y"  / BitsInteger(16),
   "gyro_z"  / BitsInteger(16),
)



class MPS_6000(Sensor):

   def __init__(self, sensor_id: str, sample_rate: float, config_payload: dict = None):
      super().__init__(sensor_id, sample_rate, config_payload=config_payload)
      self.logger = logging.getLogger(__name__)
      self._temperature = 0
      try:
         self.inf = I2CInterface(channel=self.config_payload['channel'],
                                 address=self.config_payload['address'])
      except FileNotFoundError as err:
         raise SensorInstantiationError(sensor_id, err)

   def open(self):
      self.inf.write(MPS_6000_REGISTERS.GYRO_CONFIG,
                     MPS_6000_COMMANDS.GYRO_FSR)
      self.inf.write(MPS_6000_REGISTERS.ACCEL_CONFIG,
                     MPS_6000_COMMANDS.ACCEL_FSR)
      self.inf.write(MPS_6000_REGISTERS.PWR_MGMT_CONFIG,
                     MPS_6000_COMMANDS.PLL_HYRO_REF)
      time.sleep(0.8)

   def close(self):
      self.inf.close()

   def sample(self):
      data_1 = self.inf.read(0x3B, 6)
      data_2 = self.inf.read(0x43, 6)
      return bytearray(data_1 + data_2)

   def parse(self, val):
      data = MPS_6000_DATA.parse(val)
      for key, value in data.items():
         # print(key)
         sensor_type = key.split("_")[0]
         try:
            if value > 32768:
               data[key] = value - 655360
            if sensor_type == "accel":
               data[key] = (value/(2.0**15))*MPS_6000_SENS.ACCEL_SENS
            else:
               data[key] = (value/(2.0**15))*MPS_6000_SENS.GYRO_SENS
         except TypeError:
            pass
      return data
