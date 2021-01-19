import commentjson as json
import logging
import os
import time as t
from enum import Enum
from random import randint
from typing import Callable, Dict, List, Type

from awscrt import auth, http, io, mqtt
from awsiot import mqtt_connection_builder


class AWSServerProxyState(Enum):
    CONNECTION_INTERRUPTED = "CONNECTION_INTERRUPTED",
    CONNECTION_RESUMED = "CONNECTION_RESUMED",
    CONNECTED = "CONNECTED",
    CONNECTING = "CONNECTING",
    DISCONNECTING = "DISCONNECTING",
    DISCONNECTED = "DISCONNECTED",


class AWSServerData(Enum):
    ROTATION_X = "rotation_x"
    ROTATION_Y = "rotation_y"
    ROTATION_Z = "rotation_z"
    HUMIDITY = "humidity"
    TEMPERATURE = "temperature"
    TIMESTAMP = "timestamp"

    def __str__(self):
        return str(self.value)


class AWSServerProxy:
    def __init__(self, deviceConfig:dict, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.config = deviceConfig
        self.mqtt_connection = None
        self.connected = False
        self.state: AWSServerProxyState = AWSServerProxyState.DISCONNECTED
        self.event_subscriptions: Dict[str, List[Callable[[AWSServerProxy]: None]]] = ({
            AWSServerProxyState.CONNECTION_INTERRUPTED: [],
            AWSServerProxyState.CONNECTED: [],
            AWSServerProxyState.DISCONNECTED: [],
            AWSServerProxyState.CONNECTION_RESUMED: []})

    def connect(self):
        """
        Connects device to the AWS server.
        """
        if self.state == AWSServerProxyState.CONNECTING or self.state == AWSServerProxyState.CONNECTED:
            return
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.config["endpoint"],
            cert_filepath=self.config["certificate_path"],
            pri_key_filepath=self.config["key_path"],
            client_bootstrap=client_bootstrap,
            ca_filepath=self.config["root_path"],
            client_id=self.config["client_id"],
            clean_session=False,
            keep_alive_secs=6,
            on_connection_interrupted=self.on_connection_interrupted,
            on_connection_resumed=self.on_connection_resumed,
        )
        connect_future = self.mqtt_connection.connect()
        connect_future.result()
        self.set_state(AWSServerProxyState.CONNECTED)

    def post(self, payload: dict):
        """
        Publishes timeseries snapshot to the server.
        """
        if self.state != AWSServerProxyState.CONNECTED:
            return self.logger.warning("AWSServerProxy is not connected to the server, call connect() before post().")
        payload["device_id"] = self.config["device_id"]
        topic = self.config["topic"] + self.config["device_id"]
        self.mqtt_connection.publish(topic=topic, payload=json.dumps(
            payload), qos=mqtt.QoS.AT_LEAST_ONCE)

    def disconnect(self):
        """
        Severs connection to AWS.
        """
        if not self.connected:
            return
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()
        self.set_state(AWSServerProxyState.DISCONNECTED)
    
    def set_state(self, new_state: AWSServerProxyState):
        self.state = new_state
        for func in self.event_subscriptions.get(new_state, []):
            func(self)

    def on_connection_interrupted(self):
        self.set_state(AWSServerProxyState.CONNECTION_INTERRUPTED)
        self.set_state(AWSServerProxyState.DISCONNECTED)

    def on_connection_resumed(self):
        self.set_state(AWSServerProxyState.CONNECTION_RESUMED)
        self.set_state(AWSServerProxyState.CONNECTED)

    def subscribe(self, event: AWSServerProxyState, callback):
        if event not in self.event_subscriptions:
            return
        self.event_subscriptions[event].append(callback)

    def __del__(self):
        self.disconnect()

if __name__ == "__main__":
    config_data = {}
    config_path = "./config.json"
    if os.path.isfile(config_path) == True:
            with open(config_path) as jsonfile:
               config_data = json.load(jsonfile)
    proxy = AWSServerProxy(config_data["DeviceConfig"])
    proxy.connect()
    payload = {
        AWSServerData.ROTATION_X.value: randint(0, 90),
        AWSServerData.ROTATION_Y.value: randint(0, 90),
        AWSServerData.ROTATION_Z.value: randint(0, 90),
        AWSServerData.HUMIDITY.value: randint(0, 100),
        AWSServerData.TEMPERATURE.value: randint(60, 110),
        AWSServerData.TIMESTAMP.value: t.time()}
    proxy.post(payload)
    proxy.disconnect()
