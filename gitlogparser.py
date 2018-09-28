import re

from statemachine import StateMachine, State


class LookForGitCommitId(State):

    def run(self):
        print("Looking for commit ID")

    def next(self, input):

        pattern = re.compile("commit [a-f0-9]+")
        if re.fullmatch(pattern, input) is not None:
            return GitLogParser.lookForAuthor

        return GitLogParser.lookForGitCommitId


class LookForAuthor(State):

    def run(self):
        print("Looking for Author")

    def next(self, input):

        pattern = re.compile("Author: [A-Za-z ]+ \<[a-zA-Z0-9.]+@[a-zA-Z0-9]+.[a-zA-Z]+\>")
        if re.fullmatch(pattern, input):
            return GitLogParser.lookForDate

        return GitLogParser.lookForAuthor


class LookForDate(State):

    def run(self):
        print("Looking for Date")

    def next(self, input):

        pattern = \
            re.compile("Date:   [A-Z][a-z]{2} [A-Z][a-z]{2} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4} \+[0-9]{4}")
        if re.fullmatch(pattern, input):
            return GitLogParser.lookForShortName

        return GitLogParser.lookForDate


class LookForShortName(State):

    def run(self):
        print("Looking for Short Name")

    def next(self, input):

        pattern = re.compile("[A-Za-z0-9 ._\-/]+")
        if re.fullmatch(pattern, input):
            return GitLogParser.lookForGerritChangeId

        return GitLogParser.lookForShortName


class LookForGerritChangeId(State):

    def run(self):
        print("Looking for Gerrit Change-Id")

    def next(self, input):

        pattern = re.compile("Change-Id: I[a-z0-9]+")
        if re.fullmatch(pattern, input):
            return GitLogParser.lookForGitCommitId

        pattern = re.compile("commit [a-f0-9]+")
        if re.fullmatch(pattern, input):
            return GitLogParser.lookForGitCommitId

        return GitLogParser.lookForGerritChangeId


class GitLogParser(StateMachine):

    def __init__(self):

        StateMachine.__init__(self, GitLogParser.lookForGitCommitId)


GitLogParser.lookForGitCommitId = LookForGitCommitId()
GitLogParser.lookForAuthor = LookForAuthor()
GitLogParser.lookForDate = LookForDate()
GitLogParser.lookForGitCommitId = LookForGitCommitId()
GitLogParser.lookForShortName = LookForShortName()
GitLogParser.lookForGerritChangeId = LookForGerritChangeId()