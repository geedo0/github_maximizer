#!/usr/bin/python3
import argparse
import datetime as dt
import getopt
import github
import numpy as np
import os
import subprocess
import sys

debug = False

if debug:
  import configparser
  conf = configparser.ConfigParser()
  conf.read('config.ini')
  USER = conf.get('development', 'username')
  PASS = conf.get('development', 'password')
  AUTH = conf.get('development', 'author')

def check_git_installation():
  try:
    out = subprocess.check_output(['git', '--version'])
  except Exception as e:
    return False
  return out.startswith(b'git version')

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

def initialize_local_repository(repo_path):
  try:
    os.mkdir(repo_path)
  except Exception as e:
    print(e)
    return False
  readme_path = os.path.join(repo_path, 'README')
  with open(readme_path, 'w') as f:
    f.write('Initial Commit\n')

  os.chdir(repo_path)
  try:
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'add', 'README'])
    subprocess.call(['git', 'commit', '-m', 'Initial Commit'])
  except Exception as e:
    print(e)
    return False
  return True

def get_commit_schedule(start, end, average=1):
  out = []
  # Use a poisson distribution for an organic feeling
  days = (end - start).days
  commit_distribution = np.random.poisson(average, days)
  for day_offset, num_commits in enumerate(commit_distribution):
    commit_date = start + dt.timedelta(days=day_offset)
    commit_times = np.random.randint(0, 60*60*24 - 1, num_commits)
    commit_times.sort()
    for seconds in commit_times:
      commit_time = dt.datetime.combine(commit_date, dt.time())
      commit_time += dt.timedelta(seconds=int(seconds))
      out += [commit_time]
  return out

def main():
  parser = argparse.ArgumentParser(description='This module automatically '
  'maximizes your Github contribution graph.')
  parser.add_argument('-d', '--days', default=365, type=int, metavar='DAYS',
    dest='days', help='Specify the number of days (from today) to commit to.')
  parser.add_argument('-n', '--repo-name', default='ocean', metavar='REPO_NAME',
    dest='repo_name', help='Specify the name of the repository to be created.')
  parser.add_argument('--repo-path', default=os.getcwd(), metavar='REPO_PATH',
    dest='repo_path',
    help='Specify the path where the repository should be created.')
  parser.add_argument('--author', default=None, metavar='AUTHOR', dest='author',
    help='Override the default author from git config. Use standard git '
    '"A U Thor <author@foo.com>" format')
  parser.add_argument('-u', '--username', required=True, metavar='USERNAME',
    dest='username', help='Your Github username')
  parser.add_argument('-p', '--password', required=True, metavar='PASSWORD',
    dest='password', help='Your Github password')
  if debug:
    args = parser.parse_args(['-u', USER, '-p', PASS, '--author', AUTH])
  else:
    args = parser.parse_args()

  if not check_git_installation():
    print('Could not execute \'git --version\'')
    sys.exit(1)

  repository = create_github_repository(args.username, args.password,
    args.repo_name)
  if repository is None:
    print('Could not create repository on Github')
    sys.exit(1)

  repo_path = os.path.join(args.repo_path, args.repo_name)
  if not initialize_local_repository(repo_path):
    print('Could not create local repository {:s}'.format(repo_path))
    sys.exit(1)

  end_date = dt.date.today()
  start_date = end_date - dt.timedelta(days=args.days)

  commit_times = get_commit_schedule(start_date, end_date, 2)
  os.chdir(repo_path)
  nouns = ['Airbus', 'Dollar', 'Flintlock', 'Focus', 'Love', 'Orchard', 'Rat',
  'Trolley', 'Zampone', 'Zoology']
  for commit in commit_times:
    with open('./README', 'a') as f:
      f.write(str(commit) + '\n')
    subprocess.call(['git', 'add', 'README'])
    message = "Implements a {:s}".format(np.random.choice(nouns))
    date_arg = "--date=\"{:s}\"".format(str(commit))
    commit_args = ['git', 'commit', '-m', message, date_arg]
    if args.author is not None:
      commit_args.append('--author=' + args.author)
    subprocess.call(commit_args)

  repo_uri = 'https://{0:s}:{1:s}@github.com/{0:s}/{2:s}.git/'.format(
    args.username, args.password, args.repo_name)
  subprocess.call(['git', 'push', repo_uri, 'master'])
  sys.exit()

if __name__ == '__main__':
  main()