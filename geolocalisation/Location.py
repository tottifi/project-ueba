class Location:
    def __init__(self, location):
        if location == '':
            raise ValueError('no valid location')
        self.location = [location]

    def addLocation(self, location):
        self.location.append(location)
        if len(self.location) == 11:
            self.location = self.location[1:]

    def isLocationKnown(self, location):
        if location == '':
            return False
        if location in self.location:
            self.addLocation(location)
            return True
        self.addLocation(location)
        return False
