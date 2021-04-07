
class InputError(Exception):
    def __init__(self, entry):
        self.entry = entry
        super().__init__("Wrong Input: "+self.entry)

class NoGameError(Exception):
    def __init__(self, entry):
        self.entry = entry
        super().__init__("Couldn't find Game with entry: "+self.entry)

class FindPriceError(Exception):
    def __init__(self, url, subId):
        self.url = url
        self.subId = subId
        super().__init__("Couldn't find Price with Url: "+self.url+", SubId: "+self.subId)

class AlreadyTrackedError(Exception):
    def __init__(self, userId, subId):
        self.userId = userId
        self.subId = subId
        super().__init__("Entry alread exists. userId: "+ userId + ", subid: "+subId)