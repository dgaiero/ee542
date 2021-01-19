class SingletonError(Exception):
   """Exception raised when a Singleton is instantiated more than once
   """

   def __init__(self, name:str):
      """
      Initalizer Function
      :param: name: Name of Singleton trying to me instantiated
      """
      msg = f"Singleton intialized more than once: {name}"
      super(SingletonError, self).__init__(msg)
