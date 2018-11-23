from datetime import datetime

class GerritChange:

    def __init__(self, commit_id, short_name, change_id, date):

        self.commit_id = commit_id
        self.short_name = short_name
        self.change_id = change_id
        self.date = datetime.strptime(date, '%b %d %H:%M:%S %Y')

    def __repr__(self):

        return "{} | {} | Change-Id: {} | Commit-Id: {}".format(
            self.date, self.short_name, self.change_id[0:6], self.commit_id[0:6])

    def __eq__(self, other):

        if isinstance(other, self.__class__):
            return self.change_id == other.change_id
        return False

    def __ne__(self, other):

        return not self == other

    def __hash__(self):

        return hash(self.change_id)
