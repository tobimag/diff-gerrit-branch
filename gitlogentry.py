class GitLogEntry:

    def __init__(self, sha_id, short_name, change_id):

        self.sha_id = sha_id
        self.short_name = short_name
        self.change_id = change_id

    def __repr__(self):

        return self.short_name + " | Change-Id: " + self.change_id

    def __eq__(self, other):

        if isinstance(other, self.__class__):
            return self.change_id == other.change_id
        return False

    def __ne__(self, other):

        return not self == other
