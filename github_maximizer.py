#!/usr/bin/python3
from numpy import random
import argparse
import configparser
import datetime as dt
import github
import os
import subprocess
import sys

def check_git_installation():
    try:
        out = subprocess.check_output(['git', '--version'])
    except Exception as e:
        return False
    return out.startswith(b'git version')


def create_github_repository(user, repo_name):
    assert(isinstance(user, github.AuthenticatedUser.AuthenticatedUser))
    try:
        repository = user.create_repo(repo_name)
        return repository
    except github.BadCredentialsException:
        print('Invalid credentials')
        return None
    except Exception as e:
        print(e)
        return None


def initialize_local_repository(repo_path):
    if not os.path.lexists(repo_path):
        return False
    try:
        os.makedirs(repo_path)
    except Exception as e:
        print(e)
        return False
    readme_path = os.path.join(repo_path, 'README')
    with open(readme_path, 'w') as f:
        f.write('Initial Commit\n')

    try:
        subprocess.call(['git', 'init'], cwd=repo_path)
        subprocess.call(['git', 'add', 'README'], cwd=repo_path)
        subprocess.call(['git', 'commit', '-m', 'Initial Commit'], cwd=repo_path)
    except Exception as e:
        print(e)
        return False
    return True


def prepare_local_repository(work_path, repo_name, username, password):
    repo_path = os.path.join(work_path, repo_name)
    if os.path.lexists(repo_path):
        try:
            # Make sure the repository exists and is up to date
            subprocess.check_call(
                ['git', 'fetch'], cwd=repo_path, timeout=60)
            subprocess.check_call(
                ['git', 'checkout', 'master'], cwd=repo_path, timeout=60)
            subprocess.check_call(
                ['git', 'pull'], cwd=repo_path, timeout=60)
        except Exception as e:
            print(e)
            return False
    else:
        # Make the work directory
        if not os.path.lexists(work_path):
            try:
                os.makedirs(work_path)
            except Exception as e:
                print(e)
                return False
        # Clone the repository
        repo_uri = 'https://{0:s}:{1:s}@github.com/{0:s}/{2:s}.git/'.format(
            username, password, repo_name)
        try:
            subprocess.check_call(
                ['git', 'clone', repo_uri], cwd=work_path, timeout=60)
        except Exception as e:
            print(e)
            return False

    # Check that README file exists
    readme_path = os.path.join(repo_path, 'README')
    if os.path.lexists(readme_path):
        return True
    else:
        print('README does not exist in the repository')
        return False


def get_commit_schedule(start, end):
    out = []
    # Use a poisson distribution for an organic feeling
    days = (end - start).days
    for day_offset in range(0, days):
        commit_date = start + dt.timedelta(days=day_offset)
        # if the day is a weekday use a larger distribution
        # This has the effect of following a weekly work schedule
        if commit_date.weekday() <= 4:
            num_commits = random.poisson(4)
        else:
            num_commits = random.poisson(1)
        commit_times = random.randint(0, 60 * 60 * 24 - 1, num_commits)
        commit_times.sort()
        for seconds in commit_times:
            commit_time = dt.datetime.combine(commit_date, dt.time())
            commit_time += dt.timedelta(seconds=int(seconds))
            out += [commit_time]
    return out


def main():
    parser = argparse.ArgumentParser(
        description='This module automatically maximizes your Github'
        ' contribution graph.')
    parser.add_argument(
        '-n', '--repo-name', required=True, metavar='REPO_NAME',
        dest='repo_name',
        help='Specify the name of the repository to be created.')
    parser.add_argument(
        '-c', '--config', required=True, metavar='CONFIG', dest='config',
        help='Specify a configuration file. Mainly for credentials.')
    parser.add_argument(
        '-d', '--days', default=365, type=int, metavar='DAYS', dest='days',
        help='Specify the number of days (from today) to commit to.')
    parser.add_argument(
        '--author', default=None, metavar='AUTHOR', dest='author',
        help='Override the default author from git config. Use standard git '
        '"A U Thor <author@foo.com>" format')
    args = parser.parse_args()

    try:
        conf = configparser.ConfigParser()
        conf.read(args.config)
        username = conf.get('credentials', 'username')
        password = conf.get('credentials', 'password')
    except Exception as e:
        print('Error reading credentials')
        sys.exit(1)

    if not check_git_installation():
        print('Could not execute \'git --version\'')
        sys.exit(1)

    github_user = github.Github(username, password).get_user()

    try:
        repository = github_user.get_repo(args.repo_name)
    except github.UnknownObjectException as e:
        print('Repository {:s} does not exist. Need to initialize repository.'
            .format(args.repo_name))
        repository = None
    except github.BadCredentialsException as e:
        print('Credentials for {:s} are invalid.'.format(username))
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

    # This gets the directory of github_maximer.py
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    work_path = os.path.join(dir_path, 'work')
    repo_path = os.path.join(work_path, args.repo_name)
    if repository is None:
        repository = create_github_repository(
            github_user, args.repo_name)
        if repository is None:
            print('Could not create repository on Github')
            sys.exit(1)
        if not initialize_local_repository(repo_path):
            print('Could not create local repository {:s}'.format(repo_path))
            repository.delete()
            sys.exit(1)
    else:
        if not prepare_local_repository(work_path, args.repo_name, username, password):
            print('Could not prepare local repository')
            sys.exit(1)

    end_date = dt.date.today()
    start_date = end_date - dt.timedelta(days=args.days)

    commit_times = get_commit_schedule(start_date, end_date)
    os.chdir(repo_path)
    nouns = ['Airbus', 'Dollar', 'Flintlock', 'Focus', 'Love', 'Orchard', 'Rat',
             'Trolley', 'Zampone', 'Zoology']
    for commit in commit_times:
        with open('./README', 'a') as f:
            f.write(str(commit) + '\n')
        subprocess.call(['git', 'add', 'README'], cwd=repo_path)
        message = "Implements a {:s}".format(random.choice(nouns))
        date_arg = "--date=\"{:s}\"".format(str(commit))
        commit_args = ['git', 'commit', '-m', message, date_arg]
        if args.author is not None:
            commit_args.append('--author=' + args.author)
        subprocess.call(commit_args, cwd=repo_path)

    repo_uri = 'https://{0:s}:{1:s}@github.com/{0:s}/{2:s}.git/'.format(
        username, password, args.repo_name)
    subprocess.call(['git', 'push', repo_uri, 'master'], cwd=repo_path)
    sys.exit()

if __name__ == '__main__':
    main()
