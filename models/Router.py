from models.Route import Route
import sys

sys.path.append('..')


class Router():
    def __init__(self):
        self.routes = []
        self.current_scene = None

    def change_route(self, route):
        self.current_scene = self.routes[route]
