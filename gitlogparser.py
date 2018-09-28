import re

from statemachine import StateMachine, State


class LookForGitCommitId(State):

    def run(self):
        pass

    def next(self, input):

        pattern = re.compile("(commit )([a-f0-9]+)")
        match = re.fullmatch(pattern, input)
        if match:
            GitLogParser.entries.append({'CommitId': match.group(2)})
            return GitLogParser.lookForAuthor

        return GitLogParser.lookForGitCommitId


class LookForAuthor(State):

    def run(self):
        pass

    def next(self, input):

        pattern = re.compile("Author: [A-Za-z ]+ \<[a-zA-Z0-9.]+@[a-zA-Z0-9]+.[a-zA-Z]+\>")
        match = re.fullmatch(pattern, input)
        if match:
            return GitLogParser.lookForDate

        return GitLogParser.lookForAuthor


class LookForDate(State):

    def run(self):
        pass

    def next(self, input):

        pattern = \
            re.compile("Date:   [A-Z][a-z]{2} [A-Z][a-z]{2} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4} \+[0-9]{4}")
        match = re.fullmatch(pattern, input)
        if match:
            return GitLogParser.lookForShortName

        return GitLogParser.lookForDate


class LookForShortName(State):

    def run(self):
        pass

    def next(self, input):

        pattern = re.compile("[A-Za-z0-9 ._\-/]+")
        match = re.fullmatch(pattern, input)
        if match:
            GitLogParser.entries[-1].update({'ShortName': match.group(0)})
            return GitLogParser.lookForGerritChangeId

        return GitLogParser.lookForShortName


class LookForGerritChangeId(State):

    def run(self):
        pass

    def next(self, input):

        pattern = re.compile("(Change-Id: )(I[a-z0-9]+)")
        match = re.fullmatch(pattern, input)
        if match:
            GitLogParser.entries[-1].update({'ChangeId': match.group(2)})
            return GitLogParser.lookForGitCommitId

        pattern = re.compile("(commit )([a-f0-9]+)")
        match = re.fullmatch(pattern, input)
        if match:
            GitLogParser.entries.append({'CommitId': match.group(2)})
            return GitLogParser.lookForAuthor

        return GitLogParser.lookForGerritChangeId


class GitLogParser(StateMachine):

    def __init__(self):

        StateMachine.__init__(self, GitLogParser.lookForGitCommitId)
        GitLogParser.entries = []


GitLogParser.lookForGitCommitId = LookForGitCommitId()
GitLogParser.lookForAuthor = LookForAuthor()
GitLogParser.lookForDate = LookForDate()
GitLogParser.lookForGitCommitId = LookForGitCommitId()
GitLogParser.lookForShortName = LookForShortName()
GitLogParser.lookForGerritChangeId = LookForGerritChangeId()