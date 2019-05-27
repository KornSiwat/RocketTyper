class ComponentList():

    def __init__(self):
        self._components = []

    def draw(self):
        if len(self._components) > 0:
            for component in self._components:
                component.draw()

    def add_component(self, component):

        self._components.append(component)

    def update(self):
        if len(self._components) > 0:
            for component in self._components:
                component.update()
                component.update_animation()
