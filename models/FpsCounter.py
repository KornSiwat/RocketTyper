class FpsCounter:
    def __init__(self):
        import time
        import collections
        self.time = time.perf_counter
        self.frametime = collections.deque(maxlen=60)
        self.t = self.time()

    def tick(self):
        t = self.time()
        dt = t-self.t
        self.frametime.append(dt)
        self.t = t

    def fps(self):
        try:
            return 60/sum(self.frametime)
        except ZeroDivisionError:
            return 0
