from pubsub import pub
from commonLibrary.sensor.sample import Sample

def std_sensor_pub(sensor_id: str, sample: Sample):
   pub.sendMessage('newSensorValue', sensor_name=sensor_id, sample_data=sample)
   pub.sendMessage(f'newSensorValue:{sensor_id}', sample_data=sample)
