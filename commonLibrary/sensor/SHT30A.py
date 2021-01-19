import logging
import time
from enum import IntEnum

from commonLibrary.abstract.Sensor.Sensor import Sensor
from commonLibrary.exceptions.SensorExceptions import (
    ChecksumError, SensorInstantiationError)
from commonLibrary.interface.i2c import I2CInterface
from commonLibrary.utilities.crc import dow_crc
from construct import BitsInteger, BitStruct, BytesInteger


class SHT30X_REGISTERS(IntEnum):
   ADDR = 0x44
   SS = 0x2C
   HIGH = 0x06
   READ = 0x00

SHT30X_DATA = BitStruct(
   "temperature" / BitsInteger(16),
   "temperature_crc" / BitsInteger(8),
   "humidity" / BitsInteger(16),
   "humidity_crc" / BitsInteger(8)
)

class SHT30A(Sensor):

   def __init__(self, sensor_id: str, sample_rate: float, config_payload: dict = None):
      super().__init__(sensor_id, sample_rate, config_payload=config_payload)
      self.logger = logging.getLogger(__name__)
      self._temperature = 0
      self._relative_humidity = 0
      try:
         self.inf = I2CInterface(channel=self.config_payload['channel'],\
            address=config_payload['address'])
      except FileNotFoundError as err:
         raise SensorInstantiationError(sensor_id, err)

   def open(self):
      pass

   def close(self):
      self.inf.close()

   def sample(self):
      self.inf.write_block(SHT30X_REGISTERS.SS, [0x06])
      # time.sleep(0.1575)  # t_{pu} defined as max of 1.5 ms + 5% margin
      return bytearray(self.inf.read(SHT30X_REGISTERS.READ, 6))

   def parse(self, val):
      self.structure = SHT30X_DATA.parse(val)
      crc_check = ["temperature", "humidity"]
      parsed_data = {'temperature': 0, 'humidity': 0}
      parsed_data['temperature'] = -45 + \
          (175 * self.structure['temperature']/65535.0)
      parsed_data['humidity'] = 100 * (self.structure['humidity']/65535.0)
      for check_val in crc_check:
         try:
            self._chksum_check(
               self.structure[check_val], self.structure[f"{check_val}_crc"])
         except ChecksumError as err:
            self.logger.error(f"{self.name}: {err}")
            parsed_data[check_val.lower()] = None
      return parsed_data

   def _chksum_check(self, data, ref):
      crc = dow_crc(
         0xFF, 0x31, 0x02, (data).to_bytes(2, "big"), 0x00)
      if (crc != ref):
         raise ChecksumError(crc, f"0x{ref:02x}")

def main():

   # This won't actually work as written. You need to comment out the inf
   # stuff in __init__
   from construct import Container, Struct
   test = None
   test = SHT30A('test', 1, {'channel': 1, 'address': 0x44})
   data = bytearray()
   data.append(0xBE)
   data.append(0xEF)
   data.append(0x92)
   data.append(0xAC)
   data.append(0xEA)
   data.append(0x11)
   print(test.parse(data))

if __name__ == "__main__":
   main()
