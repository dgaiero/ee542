class TempThresholdError(Exception):
   """Exception raised when system temperature is excedded
   """

   def __init__(self, temp: float, threshold: float):
      """
      :param sensor_id: ID of the sensor that failed to instantiate
      :param reason: Exception that was initially raised during failed instantiation
      """
      msg = f"Temperature Excedded Threshold {temp}C > {threshold}C"
      super(TempThresholdError, self).__init__(msg)
