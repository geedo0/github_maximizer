#!/usr/bin/python3
from subprocess import call
import argparse
import datetime as dt
import getopt
import github
import numpy as np
import os
import sys

debug = True

if debug:
  import configparser
  conf = configparser.ConfigParser()
  conf.read('config.ini')
  USER = conf.get('development', 'username')
  PASS = conf.get('development', 'password')

def create_github_repository(username, password, repo_name):
  try:
    g = github.Github(username, password)
    u = g.get_user()
    if debug:
      # Delete the repo if it exists
      try:
        u.get_repo(repo_name).delete()
      except Exception:
        pass
    repository = u.create_repo(repo_name)
  except github.GithubException as e:
    print(e)
    return None
  return repository

def main():
  parser = argparse.ArgumentParser(description='This module automatically '
  'maximizes your Github contribution graph.')
  parser.add_argument('-d', '--days', default=365, type=int, metavar='DAYS',
    dest='days', help='Specify the number of days (from today) to commit to.')
  parser.add_argument('-n', '--repo-name', default='ocean', metavar='REPO_NAME',
    dest='repo_name', help='Specify the name of the repository to be created.')
  parser.add_argument('-u', '--username', required=True, metavar='USERNAME',
    dest='username', help='Your Github username')
  parser.add_argument('-p', '--password', required=True, metavar='PASSWORD',
    dest='password', help='Your Github password')
  if debug:
    args = parser.parse_args(['-u', USER, '-p', PASS])
  else:
    args = parser.parse_args()

  repository = create_github_repository(args.username, args.password,
    args.repo_name)
  if repository is None:
    print('Could not create repository on Github')
    sys.exit(1)

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