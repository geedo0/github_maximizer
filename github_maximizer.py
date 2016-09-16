#!/usr/bin/python3
import sys
import datetime as dt
import numpy as np
import os
from subprocess import call

RANGE = 365
widgets = ['foo', 'bar', 'baz']

def main(argv):
  '''
  Create a poisson distribution for how many commits to make each day
  Generate the dates
  for each commit on day generate a time
  for each day from today to RANG
    commit to a repository
  '''
  os.chdir('/home/geedo/foo')
  # Use a poisson distribution for an organic feeling
  commit_distribution = np.random.poisson(2, RANGE)
  for day_offset, num_commits in enumerate(commit_distribution):
    commit_date = dt.date.today() - dt.timedelta(days=day_offset)
    print('{:d} commits on {:s}'.format(num_commits, str(commit_date)))
    commit_times = np.random.randint(0, 60*60*24 - 1, num_commits)
    commit_times.sort()
    for seconds in commit_times:
      commit_time = dt.datetime.combine(commit_date, dt.time())
      commit_time += dt.timedelta(seconds=int(seconds))
      with open('./test.py', 'a') as f:
        f.write(str(commit_time) + '\n')
      call(['git', 'add', 'test.py'])
      message = "Implements a {:s}".format(np.random.choice(widgets))
      date_arg = "--date=\"{:s}\"".format(str(commit_time))
      call(['git', 'commit', '-m', message, date_arg])

if __name__ == '__main__':
  main(sys.argv)