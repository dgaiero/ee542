class ThreadUnrecoverableError(Exception):
   """Exception raised when a thread encounters an error that it cannot recover
   from
   """

   def __init__(self, thread: str, name: str, reason: Exception):
      """
      :param thread: thread that encountered error
      :param reason: exception that was raised
      """
      msg = f"{thread} encountered an unrecoverable error"
      super(ThreadUnrecoverableError, self).__init__(msg)
      self.thread = thread
      self.name = name
      self.reason = reason
