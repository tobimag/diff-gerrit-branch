#!/usr/bin/env python

import subprocess
import io


class GitLogEntry:

    def __init__(self, sha_id, short_name, change_id):

        self.sha_id = sha_id
        self.short_name = short_name
        self.change_id = change_id

    def __eq__(self, other):

        if isinstance(other, self.__class__):
            return self.change_id == other.change_id
        return False

    def __ne__(self, other):

        return not self == other


def git_log_entries_creator(raw_git_log):

    string_buffer = io.StringIO(raw_git_log)
    for line in string_buffer:
        display(line)




def read_git_log(branch):

    return subprocess.check_output(['git', 'log', branch]).decode('utf8')


def main():

    first_git_branch = 'first_test_branch'
    second_git_branch = 'second_test_branch'

    git_log_entries_creator(read_git_log(first_git_branch))


if __name__ == '__main__':
    main()