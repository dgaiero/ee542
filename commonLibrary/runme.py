import argparse
import os
import pprint
import signal
import sys
import threading
import time
import uuid
from pubsub import pub

import commentjson as json

from commonLibrary.control.ControlUnit import ControlUnit
from commonLibrary.exceptions.SensorExceptions import SensorInstantiationError
from commonLibrary.logHandler.logger import setup_root_logger
from commonLibrary.sensor.SensorJob import SensorJob


class RunMe():

   def __init__(self):
      self.logger = setup_root_logger(__package__)
      self.parse_arguments()
      self.logger.info('Starting demo')
      self.run_id = uuid.uuid4()
      self.logger.info(f'RUN ID: {self.run_id}')
      signal.signal(signal.SIGINT, self.exit_signal_handler)
      signal.signal(signal.SIGTERM, self.exit_signal_handler)

   def start(self):
      try:
         self.setupCU()
         self.ControlUnit.initalizeSensors()
         self.ControlUnit.initalizeSubscribers()
         # Demo.ControlUnit.startUIControlProcess()
         self.ControlUnit.startSensorPool()
         signal.pause()
      except Exception:
         self.logger.exception("A fatal exception occured.")

   def parse_arguments(self):
      parser = argparse.ArgumentParser()
      parser.add_argument('config', help='experiment sensor config')
      parser.add_argument('-m', '--metadata', help='metadata for experiment')
      parser.add_argument('-l', '--log_level',
                          const='INFO', nargs='?',
                          choices=['INFO', 'DEBUG',
                                   'WARNING', 'ERROR', 'CRITICAL'],
                          help='Set logging level (default: INFO)')
      args = parser.parse_args()

      config_path = args.config
      if config_path:
         if os.path.isfile(config_path) == True:
            with open(config_path) as jsonfile:
               self.config_data = json.load(jsonfile)
         else:
            self.logger.critical("Config file could not be opened.")
            sys.exit(os.EX_OSFILE)
      else:
         self.logger.critical("Config file not found.")
         sys.exit(os.EX_OSFILE)

      if 'Logging' in self.config_data:
         self.logger = setup_root_logger(
             __package__, logging_dict=self.config_data['Logging'])

      if args.log_level:
         self.logger.setLevel(args.log_level)

      metadata_path = args.metadata
      if metadata_path:
         if os.path.isfile(metadata_path) == True:
            with open(metadata_path) as jsonfile:
               self.metadata = json.load(jsonfile)
            self.metadata['sensors'] = [i['type']
               for i in self.config_data['Sensors'] if 'type' in i]
      else:
         self.logger.warning("Metadata file not found.")


   def exit_signal_handler(self, signal, frame):
      sys.stdout.write('\b\b\r')
      sys.stdout.flush()
      self._exit_signal_handler()

   def _exit_signal_handler(self):
      self.logger.debug("Running onShutdown")
      pub.sendMessage('onShutdown')
      self.ControlUnit.cleanup()
      self.ControlUnit.dumpJSONToFS('./sensorData.json')
      self.logger.debug("exiting demo")
      sys.exit(0)

   def setupCU(self):
      
      self.ControlUnit = ControlUnit(
          self.setupSubscribers(), self.setupSensors())

   def setupSensors(self):
      if 'Sensors' not in self.config_data:
         return {}
      sensors = {}
      sensor_names = list()
      for sensor in self.config_data['Sensors']:
         sensor_id = str(uuid.uuid4())
         if 'name' in sensor:
            if sensor['name'] in sensor_names:
               self.logger.warning(f"Sensor Name {sensor['name']}"\
                  "already exists. Using UUID instead.")
            else:
               sensor_id = sensor['name']
         kwargs = {}
         if 'config_payload' in sensor:
            kwargs['config_payload'] = sensor['config_payload']
         try:
            tmp = SensorJob(
               sensor_id, sensor['sample_rate'], sensor['type'],
               sensor['fields'], **kwargs)
         except SensorInstantiationError as err:
            self.logger.error(f"{err}: {err.reason}")
            self.logger.error(f"Deleting sensor {sensor_id}")
            continue
         sensors[tmp.name] = tmp
         sensor_names.append(sensor_id)
      return sensors

   def setupSubscribers(self):
      if 'Subscribers' not in self.config_data:
         return {}
      return self.config_data['Subscribers']
