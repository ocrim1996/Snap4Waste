class Measure:
    def __init__(self, id, date, lat, long, weight):
        self.id = id
        self.lat = lat
        self.long = long
        self.date = date
        self.weight = float(weight)

    def __str__(self):
        return self.id + " - " + str(self.date) + " - " + str(self.lat) + " - " + str(self.long) + " - " + str(
            self.weight)