# This file is modified from the timeloop library
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

import sys
import logging

import threading

from commonLibrary.jobs.Job import Job


class JobScheduler():
   def __init__(self):
      self.jobs = {}
      self.logger = logging.getLogger(__name__)

   def submit_job(self, name, func, sample_rate, exec_handle, *args, **kwargs):
      job = Job(name, sample_rate, func, exec_handle, *args, **kwargs)
      self.jobs[name] = job

   def _start_jobs(self, block):
      for _, j in self.jobs.items():
         j.daemon = not block
         j.start()
         self.logger.info(f'Registered new job {j.job_name}')

   def _stop_jobs(self):
      for _, j in self.jobs.items():
         self.logger.info(f'Terminating job {j.job_name}')
         j.stop()

   def stop_job(self, name: str):
      """This stops the requested job. This should only be called from inside
      a thread
      :param name: Name of the thread to remove
      """
      if threading.current_thread() is threading.main_thread():
         self.logger.error("stop_job was called from the MainThread")
         return
      j = self.jobs[name]
      self.logger.info(f'Terminating job {j.job_name}')
      del self.jobs[name]
      sys.exit()

   def start(self, block=False):
      self._start_jobs(block=block)

   def stop(self):
      self._stop_jobs()
