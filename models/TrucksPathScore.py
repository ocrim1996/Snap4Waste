import geopy.distance
from datetime import datetime

speed_ms = 4.1666 # 15km/h in m/s
#speed_ms = 2.7777  # 10km/h in m/s
#speed_ms = 1.3888  # 5km/h in m/s


class TruckPath:
    def __init__(self, index):
        self.index = index
        self.measures = []
        self.tot_weight = 0

    def add_measure(self, new_measure):
        self.measures.append(new_measure)
        self.tot_weight = self.tot_weight + new_measure.weight

    def check_measure_in_path(self, measure):
        # get distance between measures
        last_measure = self.measures[-1]
        position1 = (last_measure.lat, last_measure.long)
        position2 = (measure.lat, measure.long)
        dst = geopy.distance.distance(position1, position2).km * 1000

        # get time between measures
        date1 = datetime.strptime(last_measure.date, "%Y-%m-%dT%H:%M:%S.%fZ")
        date2 = datetime.strptime(measure.date, "%Y-%m-%dT%H:%M:%S.%fZ")
        diff = (date2 - date1).seconds

        max_distance_allowed = diff * speed_ms

        score = 2 * dst + diff

        if dst < 1000 and diff < 3600 and (self.tot_weight + measure.weight) < 14000:
            return True, score
        if dst <= max_distance_allowed and (self.tot_weight + measure.weight) < 14000 and dst < 3000:
            return True, score
        else:
            return False, score

