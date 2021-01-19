from commonLibrary.communication.AWSServerProxy import AWSServerProxy
from commonLibrary.sensor.sample import Sample
from commonLibrary.utilities.decorators.threadedFunctionDecorator import \
    threaded
from commonLibrary.utilities.Singleton import singleton


@singleton
class AWSServerProxySub:
   def __init__(self, name:str, config_payload:dict=None):
      self.server_proxy = AWSServerProxy(config_payload)
      self.server_proxy.connect()

   @threaded
   def newSensorValue(self, sensor_name:str=None, sample_data:Sample=None):
      self.server_proxy.post(sample_data.to_dict())

   def onShutdown(self):
      self.server_proxy.disconnect()
