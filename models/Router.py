import sys

sys.path.append('..')
from models.Route import Route

class Router():
    def __init__(self):
        self.routes = []
        self.current_scene = None

    def change_route(self, route):
        self.current_scene = self.routes[route]
