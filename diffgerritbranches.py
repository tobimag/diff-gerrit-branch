#!/usr/bin/env python

import subprocess, io

from gitlogparser import GitLogParser
from gitlogentry import GitLogEntry


def print_results(results, first_branch_name, second_branch_name):

    print('Unique changes on ' + first_branch_name + ':')
    for entry in results['first']:
        print(entry)

    print('')

    print('Unique changes on ' + second_branch_name + ':')
    for entry in results['second']:
        print(entry)


def diff_log_entries(first_log_entries, second_log_entries):

    changes_in_both_branches = set(first_log_entries) & set(second_log_entries)
    changes_only_in_first_branch = set(first_log_entries) - set(second_log_entries)
    changes_only_in_second_branch = set(second_log_entries) - set(first_log_entries)

    result = {'both': changes_in_both_branches,
              'first': changes_only_in_first_branch,
              'second': changes_only_in_second_branch}

    return result


def create_git_log_entries(raw_git_log):

    GitLogParser().run_all(raw_git_log)
    git_log_entries =  []
    for entry in GitLogParser.entries:
        git_log_entries.append(GitLogEntry(entry['CommitId'], entry['ShortName'], entry.get('ChangeId', "")))
    return git_log_entries


def read_git_log(branch):

    raw_log = io.StringIO(subprocess.check_output(['git', 'log', branch]).decode('utf8'))
    log_as_list = []
    for line in raw_log:
        log_as_list.append(line.lstrip().rstrip())

    return log_as_list


def main():

    first_git_branch = 'first_test_branch'
    second_git_branch = 'second_test_branch'

    first_branch_log_entries = create_git_log_entries(read_git_log(first_git_branch))
    second_branch_log_entries = create_git_log_entries(read_git_log(second_git_branch))

    result = diff_log_entries(first_branch_log_entries, second_branch_log_entries)

    print_results(result, first_git_branch, second_git_branch)


if __name__ == '__main__':
    main()