#!/usr/bin/env python

import subprocess, io, argparse

from gitlogparser import GitLogParser
from gerritchange import GerritChange


def print_results(results, first_branch_name, second_branch_name):

    print('Unique changes on ' + first_branch_name + ':')
    print('-'*60)
    for entry in sorted(results['first'], key=lambda log_post: log_post.date, reverse=True):
        print(entry)

    print('')
    print('-' * 60)
    print('Unique changes on ' + second_branch_name + ':')
    for entry in sorted(results['second'], key=lambda log_post: log_post.date, reverse=True):
        print(entry)


def diff_changes(changes_in_first_branch, changes_in_second_branch):

    changes_in_both_branches = set(changes_in_first_branch) & set(changes_in_second_branch)
    changes_only_in_first_branch = set(changes_in_first_branch) - set(changes_in_second_branch)
    changes_only_in_second_branch = set(changes_in_second_branch) - set(changes_in_first_branch)

    result = {'both': changes_in_both_branches,
              'first': changes_only_in_first_branch,
              'second': changes_only_in_second_branch}

    return result


def create_gerrit_changes(raw_git_log):

    GitLogParser().run_all(raw_git_log)
    gerrit_changes = []
    for log_post in GitLogParser.logposts:
        gerrit_changes.append(GerritChange(log_post['CommitId'], log_post['ShortName'],
                                           log_post.get('ChangeId', ""), log_post.get('Date')))
    return gerrit_changes


def read_git_log(branch):

    raw_log = io.StringIO(subprocess.check_output(['git', 'log', branch]).decode('utf8'))
    log_as_list = []
    for line in raw_log:
        log_as_list.append(line.lstrip().rstrip())

    return log_as_list


def main():

    parser = argparse.ArgumentParser(description="Get changes not shared between two branches.")
    parser.add_argument('first_branch', metavar='<first branch>')
    parser.add_argument('second_branch', metavar='<second branch>')
    args = parser.parse_args()

    first_branch_name = args.first_branch
    second_branch_name = args.second_branch

    changes_in_first_branch = create_gerrit_changes(read_git_log(first_branch_name))
    changes_in_second_branch = create_gerrit_changes(read_git_log(second_branch_name))

    result = diff_changes(changes_in_first_branch, changes_in_second_branch)

    print_results(result, first_branch_name, second_branch_name)


if __name__ == '__main__':
    main()