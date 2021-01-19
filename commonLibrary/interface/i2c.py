import logging

import smbus2 as smbus
from commonLibrary.abstract.interface.InterfaceAbstract import Interface


class I2CInterface(Interface):

   def __init__(self, *args, **kwargs):
      super(I2CInterface, self).__init__(*args, **kwargs)
      self.logger = logging.getLogger(__name__)
      try:
         self.i2c = smbus.SMBus(self.channel)
      except FileNotFoundError as err:
         raise err

   def open(self):
      pass

   def close(self):
      self.i2c.close()

   def read(self, offset, num_bytes):
      return self.i2c.read_i2c_block_data(self.address, offset, num_bytes)

   def write(self, register, value):
      self.i2c.write_byte_data(self.address, register, value)

   def write_block(self, offset, lst):
      self.i2c.write_i2c_block_data(self.address, offset, lst)
   

