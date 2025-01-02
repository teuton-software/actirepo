from pprint import pprint

class Stats:

    def __init__(self):
        self.total = 0
        self.types = {}

    def __add__(self, stats):
        if not isinstance(stats, Stats):
            return NotImplemented
        result = Stats()
        result.total = self.total + stats.total
        result.types = self.types.copy()
        for key, value in stats.types.items():
            if key in result.types:
                result.types[key] += value
            else:
                result.types[key] = value
        return result
    
    def __str__(self):
        return self.__dict__.__str__()
