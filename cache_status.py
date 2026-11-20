# Thống kê kết quả 
class CacheStatus:
    def __init__(self):
        self.reads: int = 0
        self.writes: int = 0
        self.hits: int = 0
        self.misses: int = 0

    def reset(self):
        self.reads = 0
        self.writes = 0
        self.hits = 0
        self.misses = 0

    def hit_ratio(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total
