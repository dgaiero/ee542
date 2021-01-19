import importlib
import json
import logging
import math
import signal
import sys
import threading
import uuid
from pprint import pprint

from commonLibrary.communication.AWSServerProxy import AWSServerProxy
from commonLibrary.exceptions.SensorExceptions import SensorInstantiationError
from commonLibrary.exceptions.ThreadExceptions import ThreadUnrecoverableError
from commonLibrary.jobs.JobHandler import JobScheduler
from commonLibrary.sensor.sample import Sample
from commonLibrary.sensor.SensorJob import SensorJob
from pubsub import pub


class ControlUnit:

   def __init__(self, subscribers: list, sensorPool: dict):
      self.logger = logging.getLogger(__name__)
      self.logger.info(f"initalizing {__name__}")
      # self.threadPool = threadPool
      self.subscribers = subscribers
      self.sensorPool = sensorPool
      self.subscriberPool = {}
      self.sensorData = {}
      self.jobs = JobScheduler()
      # self.pub.setTopicUnspecifiedFatal(true)

      if len(sensorPool) == 0:
         self.logger.error("No sensors added to pool. Shutting down.")
         sys.exit(0)

      if len(subscribers) == 0:
         self.logger.info("No subscribers added to pool.")
      pub.subscribe(self._addSensorData, 'newSensorValue')
      pub.subscribe(self._logSensorValue, 'newSensorValue')

   def _addSensorData(self, sensor_name=None, sample_data=None):
      self.sensorData[sensor_name].append(sample_data)

   def _logSensorValue(self, sensor_name=None, sample_data=None):
         self.logger.debug(
             f'Received new value from: {sensor_name} [{sample_data}]')

   def threadError(self, exception: ThreadUnrecoverableError):
      self.logger.exception(
         f'{exception.thread} ({exception.name}) encountered an error. Removing from pool.'
      )
      self.stopSensor(exception.name)

   def UIControlProcess(self):
      self.logger.info(
          f"Started UIControlProcess thread with id {threading.get_ident()}")

   def initalizeSubscribers(self):
      for sub_name, sub_data in self.subscribers.items():
         self.logger.info(f"Found new subscriber: {sub_name}")
         try:
            lib = importlib.import_module(sub_data['path'])
            subCls = getattr(lib, sub_data['name'])
         except AttributeError:
            self.logger.error(f"Failed to import subscriber {sub_name}")
            continue
         config_payload = None
         if 'config_payload' in sub_data:
            config_payload = sub_data['config_payload']
         try:
            tmp = subCls(str(uuid.uuid4()), config_payload)
            self.subscriberPool[sub_name] = tmp
            for topic in sub_data['listeners']:
               self.logger.info(f"Subscriber {sub_name} subscribed to {topic}")
               listner = getattr(self.subscriberPool[sub_name], topic)
               pub.subscribe(listner, topic)
         except Exception as err:
            self.logger.error(f"Failed to initalize subscriber {sub_name}")
            self.logger.error(err)

   def startSensorPool(self):
      self.logger.info('starting sensor pool')
      for _, sensor in self.sensorPool.items():
         self.sensorData[sensor.name] = list()
         sensor.parent = self
         sensor.setup_job()
      self.jobs.start()

   def stopSensor(self, sensor_name: str):
      self.sensorPool[sensor_name].cleanup()
      self.jobs.stop_job(sensor_name)
      del self.sensorPool[sensor_name]

   def dumpJSONToFS(self, loc):
      with open(loc, 'w') as fp:
         json.dump(self.sensorData, fp, default=serialize)

   def initalizeSensors(self):
      for sensor_name in list(self.sensorPool.keys()):
         sensor = self.sensorPool[sensor_name]
         try:
            sensor.sensorCls.open()
         except Exception as err:
            self.logger.error(f"Sensor {sensor_name} failed to open")
            self.logger.exception(f"{err}")
            self.logger.error(f"Deleting sensor {sensor_name}")
            self.sensorPool[sensor_name].cleanup()
            del self.sensorPool[sensor_name]

   def stopSensorPool(self):
      for _, sensor in self.sensorPool.items():
         sensor.cleanup()
      self.jobs.stop()

   def startUIControlProcess(self):
      self.logger.info("initalizing UIControlProcess")
      self.uiControlProcessThread = threading.Thread(
          target=self.UIControlProcess)
      self.uiControlProcessThread.start()
      self.uiControlProcessThread.join()

   def stopUIControlProcess(self):
      self.logger.info("stopping UIControlProcess")
      # self.uiControlProcessThread.

   def cleanup(self):
      # self.stopUIControlProcess()
      self.stopSensorPool()


def serialize(obj):
   if isinstance(obj, Sample):
      return obj.to_dict()

   return obj.__dict__
