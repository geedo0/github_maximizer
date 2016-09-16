#!/usr/bin/python3
from subprocess import call
import argparse
import datetime as dt
import numpy as np
import os
import sys
import getopt

'''
TODO
-Refactor things for future features
-Some kind of cool code generation
-Some type of commit message generation
-It would be neat to use some machine learning to generate this stuff
-Make a cool README.md file
-Package it nicely, learn how to automatically fetch dependencies and stuff
-Add code to initialize and push git repositories
-Check assertion that git is setup correctly
-Profiles for selecting the distribution. Night owl vs office worker
-Improve distribution of commit times
-Automatically determine how to distribute commits
-Service that constantly pushes to Github
-Use Github API to create repositories
'''

RANGE = 365
widgets = ['foo', 'bar', 'baz']

def main():
  parser = argparse.ArgumentParser(description='This module automatically '
  'maximizes your Github contribution graph.')
  parser.add_argument('-n', '--repo-name', default='ocean', metavar='REPO_NAME',
    dest='repo_name', help='Specify the name of the repository to be created.')
  parser.add_argument('-d', '--days', default=365, type=int, metavar='DAYS',
    dest='days', help='Specify the number of days (from today) to commit to.')
  args = parser.parse_args()
  print(args)
  sys.exit()


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
  main()