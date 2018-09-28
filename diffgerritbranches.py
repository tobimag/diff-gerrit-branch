#!/usr/bin/env python

import subprocess, io

from gitlogparser import GitLogParser


def create_git_log_entries(raw_git_log):

    GitLogParser().run_all(raw_git_log)


def read_git_log(branch):

    raw_log = io.StringIO(subprocess.check_output(['git', 'log', branch]).decode('utf8'))
    log_as_list = []
    for line in raw_log:
        log_as_list.append(line.lstrip().rstrip())

    return log_as_list


def main():

    first_git_branch = 'first_test_branch'
    second_git_branch = 'second_test_branch'

    create_git_log_entries(read_git_log(first_git_branch))


if __name__ == '__main__':
    main()