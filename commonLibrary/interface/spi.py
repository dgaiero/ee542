import spidev
import logging
from commonLibrary.abstract.interface.InterfaceAbstract import Interface


class SPIInterface(Interface):

   def __init__(self, *args, **kwargs):
      super().__init__(self, *args, **kwargs)
      self.logger = logging.getLogger(__name__)
      self.max_speed = 500000

      self.spi = spidev.spiDev()
      self.spi.mode = 0

   def open(self):
      self.spi.open(self.bus, self.device)
      self.spi.max_speed_hz = self.max_speed

   def read(self, num_bytes):
      return self.spi.readbytes(num_bytes)

   def write(self, lst):
      self.spi.writebytes2(lst)

   def close(self):
      self.spi.close()
