class SensorInstantiationError(Exception):
   """Exception raised when sensor fails to instantiate for any reason
   """

   def __init__(self, sensor_id: str, reason: Exception):
      """
      :param sensor_id: ID of the sensor that failed to instantiate
      :param reason: Exception that was initially raised during failed instantiation
      """
      msg = f"{sensor_id} failed to instantiate"
      super(SensorInstantiationError, self).__init__(msg)
      self.reason = reason

class ChecksumError(Exception):
   """Exception raised when a checksum is incorrect
   """

   def __init__(self, actual: int, expected: str):
      """
      :param actual: actual checksum reported
      :param expected: expected checksum
      """
      msg = f"Expected checksum of 0x{expected:02x}, but got 0x{actual:02x}"
      super(ChecksumError, self).__init__(msg)
