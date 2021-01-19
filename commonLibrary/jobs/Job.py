# This file is lightly modified from the timeloop library
# As such, this file follows the license of the timedelta library

# MIT License

# Copyright (c) 2018 sankalpjonn

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
from math import floor
from threading import Event, Thread

from commonLibrary.exceptions.ThreadExceptions import ThreadUnrecoverableError


class Job(Thread):
   def __init__(self, name, sample_rate, func, exec_handle, *args, **kwargs):
      Thread.__init__(self)
      self.logger = logging.getLogger(__name__)
      self.job_name = name
      self.stopped = Event()
      self.interval = 1/sample_rate
      self.func = func
      self.exec_handle = exec_handle
      self.args = args
      self.kwargs = kwargs

   def stop(self):
      self.stopped.set()
      self.join()

   def run(self):
      try:
         while not self.stopped.wait(self.interval):
            self.func(*self.args, **self.kwargs)
      except Exception as err:
         self.exec_handle(ThreadUnrecoverableError(self.getName(), self.job_name, err))
